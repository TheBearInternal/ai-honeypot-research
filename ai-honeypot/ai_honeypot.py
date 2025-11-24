#!/usr/bin/env python3
"""
AI-Enhanced SSH Honeypot using Paramiko
Fully featured with realistic environment simulation and attacker profiling
"""

import os
import socket
import logging
import threading
import json
import time
from datetime import datetime
from pathlib import Path

import paramiko

# ---------------- Configuration ----------------

HOST = "0.0.0.0"
PORT = 2222
LOG_DIR = "/home/claude/ai-honeypot/logs"
HOST_KEY_PATH = "/home/claude/ai-honeypot/configs/ssh_host_key_paramiko"

# ---------------- Logging setup ----------------

Path(LOG_DIR).mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'{LOG_DIR}/ai_honeypot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('AI-Honeypot-Paramiko')


# ---------------- Honeypot Session ----------------

class HoneypotSession:
    """Handles individual SSH session with realistic responses"""
    
    def __init__(self, username, peer_ip):
        self.username = username
        self.peer_ip = peer_ip
        self.session_id = f"{peer_ip}_{int(time.time())}"
        self.command_history = []
        self.session_start = datetime.now()
        self.fake_system_context = self._initialize_fake_system()
        
    def _initialize_fake_system(self):
        """Create a fake system context with 'vulnerabilities'"""
        return {
            "hostname": "prod-web-server-02",
            "current_dir": "/home/" + self.username,
            "fake_files": {
                "/home/" + self.username: ["documents", "scripts", ".bash_history", ".ssh"],
                "/home/" + self.username + "/documents": ["passwords.txt", "api_keys.txt", "notes.md", "todo.txt"],
                "/home/" + self.username + "/scripts": ["backup.sh", "deploy.py", "maintenance.sh", "cleanup.sh"],
                "/home/" + self.username + "/.ssh": ["id_rsa", "id_rsa.pub", "authorized_keys", "known_hosts"],
                "/etc": ["passwd", "shadow", "hosts", "ssh", "nginx"],
                "/var/www": ["html", "api", "admin"],
                "/var/log": ["nginx", "mysql", "syslog", "auth.log"],
            },
            "fake_users": ["root", "admin", self.username, "deploy", "backup"],
            "accessed_files": [],
            "attacker_profile": {
                "skill_level": "unknown",
                "primary_intent": "unknown",
                "sophistication_score": 0,
                "behavior_patterns": []
            }
        }
    
    def classify_attacker_behavior(self, command):
        """Classify attacker's skill level and intent"""
        profile = self.fake_system_context['attacker_profile']
        profile['behavior_patterns'].append(command)
        
        # Skill level indicators
        novice_indicators = ['help', 'ls', 'pwd', 'whoami', 'cat /etc/passwd']
        intermediate_indicators = ['find', 'grep', 'ps aux', 'netstat', 'which']
        advanced_indicators = ['wget', 'curl', 'python', 'perl', 'base64', 'nc ', 'nmap']
        
        # Intent indicators
        recon_commands = ['ls', 'pwd', 'whoami', 'uname', 'id', 'hostname']
        data_theft = ['cat', 'grep', 'find', 'scp', 'wget', 'curl']
        privilege_escalation = ['sudo', 'su', 'chmod', 'chown', 'passwd']
        
        # Score sophistication
        if any(indicator in command.lower() for indicator in advanced_indicators):
            profile['sophistication_score'] = min(profile['sophistication_score'] + 3, 10)
            profile['skill_level'] = 'advanced'
        elif any(indicator in command.lower() for indicator in intermediate_indicators):
            profile['sophistication_score'] = min(profile['sophistication_score'] + 2, 10)
            if profile['skill_level'] == 'unknown':
                profile['skill_level'] = 'intermediate'
        elif any(indicator in command.lower() for indicator in novice_indicators):
            profile['sophistication_score'] = min(profile['sophistication_score'] + 1, 10)
            if profile['skill_level'] == 'unknown':
                profile['skill_level'] = 'novice'
        
        # Determine intent
        if any(cmd in command.lower() for cmd in privilege_escalation):
            profile['primary_intent'] = 'privilege_escalation'
        elif any(cmd in command.lower() for cmd in data_theft):
            if profile['primary_intent'] == 'unknown':
                profile['primary_intent'] = 'data_theft'
        elif any(cmd in command.lower() for cmd in recon_commands):
            if profile['primary_intent'] == 'unknown':
                profile['primary_intent'] = 'reconnaissance'
        
        return profile
    
    def get_fallback_response(self, command):
        """Generate realistic response without AI"""
        cmd = command.strip().lower()
        
        # Handle cd commands
        if cmd.startswith('cd '):
            target = command.split('cd ', 1)[1].strip()
            if target == '..':
                parts = self.fake_system_context['current_dir'].split('/')
                if len(parts) > 2:
                    self.fake_system_context['current_dir'] = '/'.join(parts[:-1])
            elif target.startswith('/'):
                self.fake_system_context['current_dir'] = target
            elif target == '~':
                self.fake_system_context['current_dir'] = f"/home/{self.username}"
            else:
                current = self.fake_system_context['current_dir']
                new_path = f"{current}/{target}".replace('//', '/')
                if new_path in self.fake_system_context['fake_files']:
                    self.fake_system_context['current_dir'] = new_path
                else:
                    return f"bash: cd: {target}: No such file or directory"
            return ""
        
        # Handle cat commands
        if cmd.startswith('cat '):
            filename = command.split('cat ', 1)[1].strip()
            basename = filename.split('/')[-1]
            
            if basename not in self.fake_system_context['accessed_files']:
                self.fake_system_context['accessed_files'].append(basename)
            
            # Return fake sensitive content
            fake_docs = {
                "passwords.txt": """# Production Passwords - DO NOT SHARE
# Last updated: 2024-11-15

# Database
mysql_prod: MySQLr00t!2024
postgres_main: pg_S3cur3_Pass

# API Keys  
stripe_live: sk_live_fake123456789
aws_access: AKIA_FAKE_KEY_12345

# FTP
backup_ftp: ftpBackup2024!
deploy_ftp: D3ploy_secure_99""",
                "api_keys.txt": """# API Keys - Production
AWS_ACCESS_KEY_ID=AKIA_FAKE_ACCESS_123
AWS_SECRET_ACCESS_KEY=wJalrXUtn_FAKE_SECRET_KEY

STRIPE_SECRET_KEY=sk_live_fake_stripe_key
SENDGRID_API_KEY=SG.fake_sendgrid_key""",
                ".bash_history": """ls -la
cd /var/www
vim config.php
mysql -u root -p'MySQLr00t!2024'
ps aux | grep nginx
sudo systemctl restart nginx
cat /etc/passwd
whoami
cd ~/.ssh
cat id_rsa
history | grep password""",
                "notes.md": """# Production Server Notes

## Server IPs
- Web: 10.0.1.50
- DB: 10.0.1.51

## Deploy credentials
User: deploy
Pass: D3ploy_prod_2024

## Database
Host: 10.0.1.51:3306
User: admin
Pass: MySQLr00t!2024""",
                "backup.sh": """#!/bin/bash
# DB Password: MySQLr00t!2024
DATE=$(date +%Y%m%d)
mysqldump -u root -p'MySQLr00t!2024' --all-databases > backup_$DATE.sql""",
                "deploy.py": """#!/usr/bin/env python3
# AWS Key: AKIA_FAKE_KEY_12345
DB_HOST = "10.0.1.51"
DB_USER = "admin"
DB_PASS = "MySQLr00t!2024"
STRIPE_KEY = "sk_live_fake_stripe_key"
""",
                "id_rsa": """-----BEGIN OPENSSH PRIVATE KEY-----
[SSH private key - DO NOT SHARE]
-----END OPENSSH PRIVATE KEY-----"""
            }
            
            if basename in fake_docs:
                return fake_docs[basename]
            
            return f"cat: {filename}: No such file or directory"
        
        # Common commands
        responses = {
            'ls': '\n'.join(self.fake_system_context['fake_files'].get(self.fake_system_context['current_dir'], ['[empty directory]'])),
            'pwd': self.fake_system_context['current_dir'],
            'whoami': self.username,
            'hostname': self.fake_system_context['hostname'],
            'uname -a': f"Linux {self.fake_system_context['hostname']} 5.15.0-89-generic #99-Ubuntu SMP x86_64 GNU/Linux",
            'id': f"uid=1000({self.username}) gid=1000({self.username}) groups=1000({self.username}),27(sudo)",
            'ps aux': '\n'.join(['USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND',
                                'root      1000  0.0  0.1  10000  2000 ?        Ss   Nov22   0:05 nginx: master process',
                                'root      1001  0.0  0.2  15000  3000 ?        Ss   Nov22   0:10 mysqld --basedir=/usr',
                                'root      1002  0.0  0.1   8000  1500 ?        Ss   Nov22   0:02 python3 /opt/app/server.py']),
            'ifconfig': """eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.0.1.50  netmask 255.255.255.0  broadcast 10.0.1.255
        ether 08:00:27:4e:66:a1  txqueuelen 1000  (Ethernet)""",
            'ip addr': """1: lo: <LOOPBACK,UP,LOWER_UP>
    inet 127.0.0.1/8 scope host lo
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP>
    inet 10.0.1.50/24 brd 10.0.1.255 scope global eth0"""
        }
        
        if cmd in responses:
            return responses[cmd]
        
        # Default for unknown commands
        return f"bash: {command.split()[0] if command else 'command'}: command not found"
    
    def log_command(self, command, response, duration):
        """Log command for analysis"""
        log_entry = {
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "username": self.username,
            "ip": self.peer_ip,
            "command": command,
            "response_length": len(response),
            "duration_ms": duration * 1000,
            "command_number": len(self.command_history),
            "attacker_profile": {
                "skill_level": self.fake_system_context['attacker_profile']['skill_level'],
                "primary_intent": self.fake_system_context['attacker_profile']['primary_intent'],
                "sophistication_score": self.fake_system_context['attacker_profile']['sophistication_score']
            },
            "files_accessed": len(self.fake_system_context['accessed_files']),
            "honeypot_type": "ai_enhanced"
        }
        
        log_file = Path(f"{LOG_DIR}/commands.jsonl")
        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        
        logger.info(f"[{self.peer_ip}] {self.username}$ {command} [Skill: {self.fake_system_context['attacker_profile']['skill_level']}]")


# ---------------- Paramiko Server ----------------

def get_host_key():
    """Get or generate host key"""
    Path(HOST_KEY_PATH).parent.mkdir(parents=True, exist_ok=True)
    
    if os.path.exists(HOST_KEY_PATH):
        return paramiko.RSAKey(filename=HOST_KEY_PATH)
    
    key = paramiko.RSAKey.generate(2048)
    key.write_private_key_file(HOST_KEY_PATH)
    logger.info("Generated new SSH host key")
    return key


class HoneypotServer(paramiko.ServerInterface):
    """Paramiko server interface"""
    
    def __init__(self, client_addr):
        self.event = threading.Event()
        self.client_addr = client_addr

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        # Log authentication
        logger.info(f"Login attempt - Username: {username}, Password: {password}, IP: {self.client_addr}")
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "auth_attempt",
            "username": username,
            "password": password,
            "ip": self.client_addr,
            "success": True
        }
        
        log_file = Path(f"{LOG_DIR}/auth.jsonl")
        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        
        return paramiko.AUTH_SUCCESSFUL

    def get_allowed_auths(self, username):
        return "password"

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True


def handle_client(client_sock, addr, host_key):
    """Handle individual client connection"""
    client_ip, client_port = addr
    logger.info(f"Connection received from {client_ip}:{client_port}")

    transport = paramiko.Transport(client_sock)
    transport.add_server_key(host_key)

    server = HoneypotServer(client_ip)
    try:
        transport.start_server(server=server)
    except paramiko.SSHException as e:
        logger.error(f"SSH negotiation failed for {client_ip}: {e}")
        return

    chan = transport.accept(20)
    if chan is None:
        logger.warning(f"No channel for {client_ip}")
        return

    server.event.wait(10)
    if not server.event.is_set():
        logger.warning(f"No shell request from {client_ip}")
        chan.close()
        return

    # Get username from transport
    username = transport.get_username() or "user"
    
    # Create session
    session = HoneypotSession(username, client_ip)
    logger.info(f"Session started for {username}@{client_ip}")

    # Send banner
    banner = (
        "Welcome to Ubuntu 22.04.4 LTS (GNU/Linux 5.15.0-89-generic x86_64)\r\n"
        "\r\n"
        "* Documentation:  https://help.ubuntu.com\r\n"
        "* Management:     https://landscape.canonical.com\r\n"
        "\r\n"
    )
    
    try:
        chan.send(banner.encode("utf-8"))
        
        # Main command loop
        while True:
            prompt = f"{session.username}@{session.fake_system_context['hostname']}:{session.fake_system_context['current_dir']}$ "
            chan.send(prompt.encode("utf-8"))
            
            # Read command using simple recv
            cmd_bytes = b""
            while not cmd_bytes.endswith(b"\n"):
                chunk = chan.recv(1024)
                if not chunk:
                    raise EOFError
                # Echo what user typed
                chan.send(chunk)
                cmd_bytes += chunk
            
            command = cmd_bytes.decode("utf-8", "ignore").strip()
            
            if not command:
                continue
                
            if command.lower() in ("exit", "logout", "quit"):
                chan.send(b"\r\nlogout\r\n")
                logger.info(f"Session ended for {session.session_id}")
                break

            # Process command
            session.command_history.append(command)
            session.classify_attacker_behavior(command)
            
            start_time = time.time()
            response = session.get_fallback_response(command)
            duration = time.time() - start_time
            
            session.log_command(command, response, duration)
            
            # Send response
            if response:
                chan.send(f"\r\n{response}\r\n".encode("utf-8"))

    except EOFError:
        logger.info(f"Connection closed by {client_ip}")
    except Exception as e:
        logger.exception(f"Error in session with {client_ip}: {e}")
    finally:
        chan.close()
        transport.close()
        client_sock.close()
        logger.info(f"Session ended for {client_ip}")


def main():
    """Main server loop"""
    host_key = get_host_key()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(100)

    logger.info(f"AI Honeypot listening on {HOST}:{PORT}")
    logger.info(f"Logs: {LOG_DIR}")

    try:
        while True:
            client, addr = sock.accept()
            t = threading.Thread(
                target=handle_client, 
                args=(client, addr, host_key), 
                daemon=True
            )
            t.start()
    except KeyboardInterrupt:
        logger.info("Shutting down honeypot...")
    finally:
        sock.close()


if __name__ == "__main__":
    main()
