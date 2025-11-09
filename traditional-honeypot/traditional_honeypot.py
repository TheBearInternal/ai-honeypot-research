#!/usr/bin/env python3
"""
Traditional Static Honeypot - Baseline for comparison
Uses predefined responses only, no AI
"""

import asyncio
import asyncssh
import json
import logging
import time
from datetime import datetime
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/claude/ai-honeypot/logs/traditional_honeypot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('Traditional-Honeypot')


class StaticResponses:
    """Static command responses"""
    
    RESPONSES = {
        "ls": "documents  scripts  Downloads  .bash_history  .ssh",
        "ls -la": """total 48
drwxr-xr-x 5 user user 4096 Nov  6 10:30 .
drwxr-xr-x 3 root root 4096 Oct 15 09:20 ..
-rw------- 1 user user  256 Nov  6 10:30 .bash_history
-rw-r--r-- 1 user user  220 Oct 15 09:20 .bash_logout
-rw-r--r-- 1 user user 3526 Oct 15 09:20 .bashrc
drwx------ 2 user user 4096 Oct 20 14:15 .ssh
drwxr-xr-x 2 user user 4096 Nov  1 11:45 documents
drwxr-xr-x 2 user user 4096 Oct 28 16:20 scripts""",
        "pwd": "/home/user",
        "whoami": "user",
        "id": "uid=1001(user) gid=1001(user) groups=1001(user),27(sudo)",
        "hostname": "prod-web-server-01",
        "uname -a": "Linux prod-web-server-01 5.15.0-58-generic #64-Ubuntu SMP Thu Oct 5 11:03:17 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux",
        "cat /etc/passwd": """root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
user:x:1001:1001::/home/user:/bin/bash
admin:x:1000:1000:Admin User:/home/admin:/bin/bash""",
        "ps aux": """USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.1  16940  9352 ?        Ss   10:20   0:01 /sbin/init
root       256  0.0  0.2  70828 17264 ?        Ss   10:20   0:00 /usr/sbin/sshd -D
www-data   512  0.5  1.2 125648 98256 ?        S    10:21   0:15 nginx: worker process
mysql      728  2.1  4.8 1876512 391824 ?      Sl   10:21   1:25 /usr/sbin/mysqld
root      1024  0.0  0.1  12344  8192 pts/0    Ss   10:30   0:00 -bash""",
        "cat .bash_history": """ls
cd documents
cat passwords.txt
mysql -u root -p
sudo systemctl restart nginx
vim /etc/nginx/sites-available/default
tail -f /var/log/nginx/access.log""",
        "cat /etc/shadow": "cat: /etc/shadow: Permission denied",
        "sudo -l": "[sudo] password for user:",
        "ifconfig": """eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.100  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::a00:27ff:fe4e:66a1  prefixlen 64  scopeid 0x20<link>
        ether 08:00:27:4e:66:a1  txqueuelen 1000  (Ethernet)""",
        "netstat -tulpn": """Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      256/sshd
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      512/nginx
tcp        0      0 0.0.0.0:3306            0.0.0.0:*               LISTEN      728/mysqld""",
        "ls documents": "passwords.txt  api_keys.txt  notes.md  budget.xlsx",
        "cat documents/passwords.txt": """# Development Passwords
MySQL: root / Test123!
FTP: admin / ftpPass2023
API Key: sk-dev-abc123xyz789""",
        "ls scripts": "backup.sh  deploy.py  maintenance.sh",
        "cat scripts/backup.sh": """#!/bin/bash
# Daily backup script
mysqldump -u root -pTest123! production_db > /backup/db_$(date +%Y%m%d).sql
rsync -av /var/www/html backup@192.168.1.50:/backups/""",
        "w": """USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
user     pts/0    192.168.1.50     10:30    0.00s  0.01s  0.00s w""",
        "last": """user     pts/0        192.168.1.50     Wed Nov  6 10:30   still logged in
admin    pts/0        10.0.0.25        Tue Nov  5 15:22 - 17:45  (02:23)
user     pts/1        192.168.1.50     Mon Nov  4 09:15 - 18:30  (09:15)""",
    }
    
    @classmethod
    def get_response(cls, command):
        """Get static response for command"""
        cmd = command.strip()
        
        # Exact matches
        if cmd in cls.RESPONSES:
            return cls.RESPONSES[cmd]
        
        # Pattern matching
        if cmd.startswith("cd "):
            return ""  # No output for successful cd
        elif cmd.startswith("cat ") and "documents" in cmd:
            return "Lorem ipsum sensitive data here..."
        elif cmd.startswith("sudo "):
            return "[sudo] password for user:\nSorry, try again."
        elif cmd.startswith("ssh "):
            return "ssh: connect to host " + cmd.split()[1] + " port 22: Connection refused"
        elif cmd == "":
            return ""
        else:
            return f"bash: {cmd.split()[0]}: command not found"


class TraditionalSession:
    """Session handler for traditional honeypot"""
    
    def __init__(self, username, peer_ip):
        self.username = username
        self.peer_ip = peer_ip
        self.session_id = f"{peer_ip}_{int(time.time())}"
        self.command_history = []
        self.session_start = datetime.now()
        
    def log_command(self, command, response, duration):
        """Log command and response"""
        log_entry = {
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "username": self.username,
            "ip": self.peer_ip,
            "command": command,
            "response_length": len(response),
            "duration_ms": duration * 1000,
            "command_number": len(self.command_history),
            "honeypot_type": "traditional"
        }
        
        log_file = Path("/home/claude/ai-honeypot/logs/commands.jsonl")
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        
        logger.info(f"[{self.peer_ip}] {self.username}$ {command}")


class TraditionalHoneypotServer(asyncssh.SSHServer):
    """SSH server for traditional honeypot"""
    
    def connection_made(self, conn):
        peer = conn.get_extra_info('peername')[0]
        logger.info(f"Connection received from {peer}")
        
    def password_auth_supported(self):
        return True
    
    def validate_password(self, username, password):
        """Accept any password"""
        peer = "unknown"
        logger.info(f"Login attempt - Username: {username}, Password: {password}")
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "auth_attempt",
            "username": username,
            "password": password,
            "ip": peer,
            "success": True,
            "honeypot_type": "traditional"
        }
        
        log_file = Path("/home/claude/ai-honeypot/logs/auth.jsonl")
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        
        return True


class TraditionalSSHSession(asyncssh.SSHServerSession):
    """Session handler"""
    
    def __init__(self):
        self._session = None
        
    def connection_made(self, chan):
        self._chan = chan
        peer = chan.get_extra_info('peername')[0]
        username = chan.get_extra_info('username', 'user')
        
        self._session = TraditionalSession(username, peer)
        logger.info(f"Session started for {username}@{peer}")
        
    def shell_requested(self):
        return True
    
    def session_started(self):
        self._chan.write(f"{self._session.username}@prod-web-server-01:~$ ")
    
    def data_received(self, data, datatype):
        command = data.strip()
        
        if command.lower() in ['exit', 'logout', 'quit']:
            self._chan.write("\r\nlogout\r\n")
            self._chan.close()
            logger.info(f"Session ended for {self._session.session_id}")
            return
        
        if command:
            self._session.command_history.append(command)
            
            start_time = time.time()
            response = StaticResponses.get_response(command)
            duration = time.time() - start_time
            
            self._session.log_command(command, response, duration)
            
            self._chan.write(f"\r\n{response}\r\n")
        
        self._chan.write(f"{self._session.username}@prod-web-server-01:~$ ")


async def start_traditional_honeypot(host='0.0.0.0', port=2223):
    """Start traditional honeypot"""
    
    key_file = Path("/home/claude/ai-honeypot/configs/ssh_host_key_traditional")
    if not key_file.exists():
        key_file.parent.mkdir(parents=True, exist_ok=True)
        key = asyncssh.generate_private_key('ssh-rsa')
        key_file.write_bytes(key.export_private_key())
        logger.info("Generated SSH host key")
    
    logger.info(f"Starting Traditional Honeypot on {host}:{port}")
    
    await asyncssh.create_server(
        TraditionalHoneypotServer,
        host,
        port,
        server_host_keys=[str(key_file)],
        session_factory=TraditionalSSHSession
    )
    
    logger.info(f"Traditional Honeypot running on port {port}")


if __name__ == "__main__":
    Path("/home/claude/ai-honeypot/logs").mkdir(parents=True, exist_ok=True)
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_traditional_honeypot())
    loop.run_forever()
