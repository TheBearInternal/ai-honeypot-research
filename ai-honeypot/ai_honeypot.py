#!/usr/bin/env python3
"""
AI-Enhanced Honeypot - Dynamic response system
Simulates realistic Linux environment with LLM-powered responses
"""

import asyncio
import asyncssh
import json
import logging
import time
from datetime import datetime
from pathlib import Path
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/claude/ai-honeypot/logs/ai_honeypot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('AI-Honeypot')

class HoneypotSession:
    """Handles individual SSH session with AI-powered responses"""
    
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
            "fake_processes": [
                "nginx: master process /usr/sbin/nginx",
                "mysqld --basedir=/usr",
                "python3 /opt/app/server.py",
                "/usr/sbin/sshd -D"
            ],
            "environment": {
                "USER": self.username,
                "HOME": f"/home/{self.username}",
                "SHELL": "/bin/bash",
                "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
            },
            "ai_generated_docs": {},  # Cache for AI-generated document contents
            "accessed_files": [],  # Track which files attacker has accessed
            "attacker_profile": {
                "skill_level": "unknown",  # Will be classified: novice, intermediate, advanced
                "primary_intent": "unknown",  # reconnaissance, data_theft, privilege_escalation
                "sophistication_score": 0,
                "behavior_patterns": []
            }
        }
    
    def get_ai_prompt(self, command):
        """Generate prompt for LLM based on command and context"""
        recent_history = "\n".join([f"$ {cmd}" for cmd in self.command_history[-5:]])
        
        # Classify attacker behavior
        attacker_profile = self.classify_attacker_behavior(command)
        
        prompt = f"""You are simulating a Linux system terminal. Respond ONLY with the terminal output, no explanations.

System Context:
- Hostname: {self.fake_system_context['hostname']}
- Current directory: {self.fake_system_context['current_dir']}
- User: {self.username}
- Attacker appears to be: {attacker_profile['skill_level']} (intent: {attacker_profile['primary_intent']})

Recent commands:
{recent_history if recent_history else "(no previous commands)"}

User just ran: {command}

Rules:
1. Give realistic Linux terminal output
2. Include subtle hints of vulnerabilities (weak passwords in comments, accessible config files)
3. Make it look like a real production system with sensitive data
4. Never break character - you ARE the terminal
5. Keep responses concise but realistic
6. If command is invalid, show bash-style error
7. For 'ls', show files from this fake structure: {json.dumps(self.fake_system_context['fake_files'].get(self.fake_system_context['current_dir'], []))}
8. For 'pwd', show: {self.fake_system_context['current_dir']}
9. For 'whoami', show: {self.username}
10. Adjust difficulty based on attacker skill level - more convincing for advanced attackers

Respond with ONLY the terminal output:"""
        
        return prompt
    
    async def generate_ai_document(self, filename):
        """Generate realistic document content using AI"""
        
        # Check cache first
        if filename in self.fake_system_context['ai_generated_docs']:
            return self.fake_system_context['ai_generated_docs'][filename]
        
        # Determine document type and generate appropriate content
        doc_prompts = {
            "passwords.txt": "Generate a realistic passwords.txt file that a developer might keep. Include 5-7 passwords with comments explaining what they're for (database, API, FTP, etc). Make it look authentic with dates and notes. Keep it under 150 words.",
            "api_keys.txt": "Generate realistic API keys file with keys for services like AWS, Stripe, SendGrid, etc. Include comments and dates. Make keys look real (but fake). Under 150 words.",
            ".bash_history": f"Generate realistic bash command history for a {self.username} user who is a system administrator. Include 15-20 commands showing database work, server management, and security mistakes. Under 200 words.",
            "notes.md": "Generate realistic work notes for a sysadmin. Include TODO items, server IP addresses, and deployment notes. Make it look like real production environment documentation. Under 200 words.",
            "backup.sh": "Generate a realistic bash backup script with database credentials in comments. Include rsync commands and mysql dump. Show realistic production server paths. Under 200 words.",
            "deploy.py": "Generate a realistic Python deployment script with hardcoded credentials and API keys in comments. Include database connections and server configurations. Under 200 words.",
            "id_rsa": "Generate text saying this is an SSH private key file (don't generate actual key, just explanatory text and header like -----BEGIN OPENSSH PRIVATE KEY-----). Under 50 words.",
            "todo.txt": "Generate a realistic TODO list for a sysadmin with tasks about security patches, user management, and server maintenance. Under 100 words."
        }
        
        prompt = doc_prompts.get(filename, f"Generate realistic content for a file named {filename} that might exist on a Linux server. Under 150 words.")
        
        try:
            # Try to generate using available AI
            if os.getenv("OPENAI_API_KEY"):
                content = await self._generate_doc_openai(prompt)
            elif await self._check_ollama_available():
                content = await self._generate_doc_ollama(prompt)
            else:
                # Fallback to template-based generation
                content = self._generate_doc_fallback(filename)
            
            # Cache the generated content
            self.fake_system_context['ai_generated_docs'][filename] = content
            return content
            
        except Exception as e:
            logger.error(f"Error generating document: {e}")
            return self._generate_doc_fallback(filename)
    
    async def _generate_doc_openai(self, prompt):
        """Generate document using OpenAI"""
        import aiohttp
        
        api_key = os.getenv("OPENAI_API_KEY")
        
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You generate realistic fake documents for honeypot systems. Make them look authentic."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.8,
                "max_tokens": 300
            }
            
            async with session.post("https://api.openai.com/v1/chat/completions", 
                                   headers=headers, json=payload, timeout=10) as resp:
                result = await resp.json()
                return result["choices"][0]["message"]["content"].strip()
    
    async def _generate_doc_ollama(self, prompt):
        """Generate document using Ollama"""
        import aiohttp
        
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": "llama3.2:3b",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.8,
                    "num_predict": 300
                }
            }
            
            async with session.post("http://localhost:11434/api/generate", json=payload, timeout=15) as resp:
                result = await resp.json()
                return result.get("response", "").strip()
    
    async def _check_ollama_available(self):
        """Check if Ollama is running"""
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get("http://localhost:11434/api/tags", timeout=2) as resp:
                    return resp.status == 200
        except:
            return False
    
    def _generate_doc_fallback(self, filename):
        """Generate document using templates when AI is unavailable"""
        templates = {
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
deploy_ftp: D3ploy_secure_99
""",
            "api_keys.txt": """# API Keys - Production
# Generated: 2024-11-10

AWS_ACCESS_KEY_ID=AKIA_FAKE_ACCESS_123
AWS_SECRET_ACCESS_KEY=wJalrXUtn_FAKE_SECRET_KEY_123456

STRIPE_SECRET_KEY=sk_live_fake_stripe_key_12345
SENDGRID_API_KEY=SG.fake_sendgrid_key.12345

# Slack webhook
SLACK_WEBHOOK=https://hooks.slack.com/services/FAKE/WEBHOOK/URL
""",
            ".bash_history": """ls -la
cd /var/www
vim config.php
mysql -u root -p'MySQLr00t!2024' 
ps aux | grep nginx
sudo systemctl restart nginx
cat /etc/passwd
whoami
cd ~/.ssh
ls -la
cat id_rsa
chmod 600 id_rsa
ssh deploy@prod-server
cd /home/admin/scripts
./backup.sh
history | grep password
export AWS_ACCESS_KEY=AKIA_FAKE_KEY
python3 deploy.py
""",
            "notes.md": """# Production Server Notes

## Server IPs
- Web: 10.0.1.50
- DB: 10.0.1.51
- Backup: 10.0.1.52

## TODO
- [ ] Update SSL certs (expires Dec 2024)
- [ ] Patch security vulnerability CVE-2024-1234
- [ ] Review firewall rules
- [ ] Backup user passwords file

## Deploy credentials
User: deploy
Pass: D3ploy_prod_2024

## Database
Host: 10.0.1.51:3306
User: admin
Pass: MySQLr00t!2024
""",
            "backup.sh": """#!/bin/bash
# Backup script - runs daily at 2am
# DB Password: MySQLr00t!2024

DATE=$(date +%Y%m%d)
BACKUP_DIR="/backups/$DATE"

# Create backup directory
mkdir -p $BACKUP_DIR

# MySQL dump
mysqldump -u root -p'MySQLr00t!2024' --all-databases > $BACKUP_DIR/mysql_backup.sql

# Rsync to backup server
rsync -avz $BACKUP_DIR/ backup@10.0.1.52:/backups/

echo "Backup completed: $DATE"
""",
            "deploy.py": """#!/usr/bin/env python3
# Deployment script
# AWS Key: AKIA_FAKE_KEY_12345

import os
import subprocess

# Database connection
DB_HOST = "10.0.1.51"
DB_USER = "admin"
DB_PASS = "MySQLr00t!2024"
DB_NAME = "production"

# API Keys
STRIPE_KEY = "sk_live_fake_stripe_key_12345"
AWS_KEY = "AKIA_FAKE_ACCESS_123"

def deploy():
    print("Starting deployment...")
    # Deploy code here
    pass

if __name__ == "__main__":
    deploy()
""",
            "id_rsa": """-----BEGIN OPENSSH PRIVATE KEY-----
[This would be an SSH private key]
[DO NOT distribute this key]
[Used for production server access]
-----END OPENSSH PRIVATE KEY-----
""",
            "todo.txt": """TODO List - System Administration

HIGH PRIORITY:
- Apply security patch for CVE-2024-1234
- Update root password (current: R00t_temp_2024)
- Review user access permissions
- Backup /etc/shadow file

MEDIUM:
- Clean up old log files
- Update SSL certificates
- Audit firewall rules
- Document deployment process

LOW:
- Organize scripts folder
- Update documentation
"""
        }
        
        return templates.get(filename, f"# Content for {filename}\n[File contents would appear here]\n")
    
    def classify_attacker_behavior(self, command):
        """Classify attacker's skill level and intent based on commands"""
        profile = self.fake_system_context['attacker_profile']
        
        # Track behavior patterns
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
    
    async def get_ai_response(self, command):
        """Get AI-powered response to command"""
        try:
            # Try AI services in priority order
            if os.getenv("OPENAI_API_KEY"):
                return await self._get_openai_response(command)
            elif await self._check_ollama_available():
                return await self._get_ollama_response(command)
            else:
                return self.get_fallback_response(command)
        except Exception as e:
            logger.error(f"AI response error: {e}")
            return self.get_fallback_response(command)
    
    async def _get_ollama_response(self, command):
        """Get response from Ollama"""
        import aiohttp
        
        prompt = self.get_ai_prompt(command)
        
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": "llama3.2:3b",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 200
                }
            }
            
            async with session.post("http://localhost:11434/api/generate", json=payload) as resp:
                result = await resp.json()
                return result.get("response", "").strip()
    
    async def _get_openai_response(self, command):
        """Get response from OpenAI API"""
        import aiohttp
        
        api_key = os.getenv("OPENAI_API_KEY")
        prompt = self.get_ai_prompt(command)
        
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are a Linux terminal simulator. Respond ONLY with terminal output."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 200
            }
            
            async with session.post("https://api.openai.com/v1/chat/completions", 
                                   headers=headers, json=payload) as resp:
                result = await resp.json()
                return result["choices"][0]["message"]["content"].strip()
    
    def get_fallback_response(self, command):
        """Generate response without AI"""
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
                # Relative path
                current = self.fake_system_context['current_dir']
                new_path = f"{current}/{target}".replace('//', '/')
                if new_path in self.fake_system_context['fake_files']:
                    self.fake_system_context['current_dir'] = new_path
                else:
                    return f"bash: cd: {target}: No such file or directory"
            return ""
        
        # Handle cat commands for sensitive files
        if cmd.startswith('cat '):
            filename = command.split('cat ', 1)[1].strip()
            basename = filename.split('/')[-1]
            
            # Track file access
            if basename not in self.fake_system_context['accessed_files']:
                self.fake_system_context['accessed_files'].append(basename)
            
            # Return fake sensitive content
            if basename in ['passwords.txt', 'api_keys.txt', '.bash_history', 'notes.md', 
                          'backup.sh', 'deploy.py', 'id_rsa', 'todo.txt']:
                return self._generate_doc_fallback(basename)
            
            return f"cat: {filename}: No such file or directory"
        
        # Common commands
        responses = {
            'ls': '\n'.join(self.fake_system_context['fake_files'].get(self.fake_system_context['current_dir'], ['[empty directory]'])),
            'pwd': self.fake_system_context['current_dir'],
            'whoami': self.username,
            'hostname': self.fake_system_context['hostname'],
            'uname -a': f"Linux {self.fake_system_context['hostname']} 5.15.0-89-generic #99-Ubuntu SMP x86_64 GNU/Linux",
            'id': f"uid=1000({self.username}) gid=1000({self.username}) groups=1000({self.username}),27(sudo)",
            'ps aux': '\n'.join(['USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND'] + 
                               [f"root      {i+1000}  0.0  0.1 {10000+i*1000}  {2000+i*100} ?        Ss   Nov22   0:05 {proc}" 
                                for i, proc in enumerate(self.fake_system_context['fake_processes'])]),
            'ifconfig': """eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.0.1.50  netmask 255.255.255.0  broadcast 10.0.1.255
        inet6 fe80::a00:27ff:fe4e:66a1  prefixlen 64  scopeid 0x20<link>
        ether 08:00:27:4e:66:a1  txqueuelen 1000  (Ethernet)""",
            'ip addr': """1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN
    inet 127.0.0.1/8 scope host lo
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP
    inet 10.0.1.50/24 brd 10.0.1.255 scope global eth0"""
        }
        
        if cmd in responses:
            return responses[cmd]
        
        # Default for unknown commands
        return f"bash: {command.split()[0]}: command not found"
    
    def log_command(self, command, response, duration):
        """Log command and response for analysis"""
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
        
        log_file = Path("/home/claude/ai-honeypot/logs/commands.jsonl")
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        
        logger.info(f"[{self.peer_ip}] {self.username}$ {command} [Skill: {self.fake_system_context['attacker_profile']['skill_level']}]")


class AIHoneypotServer(asyncssh.SSHServer):
    """SSH server that accepts all connections and uses AI responses"""
    
    def connection_made(self, conn):
        peer = conn.get_extra_info('peername')[0]
        logger.info(f"Connection received from {peer}")
        
    def connection_lost(self, exc):
        if exc:
            logger.error(f"Connection error: {exc}")
    
    def password_auth_supported(self):
        return True
    
    def validate_password(self, username, password):
        """Accept any password (this is a honeypot!)"""
        peer = "unknown"
        logger.info(f"Login attempt - Username: {username}, Password: {password}, IP: {peer}")
        
        # Log authentication attempt
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "auth_attempt",
            "username": username,
            "password": password,
            "ip": peer,
            "success": True
        }
        
        log_file = Path("/home/claude/ai-honeypot/logs/auth.jsonl")
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        
        return True


class SSHSessionHandler(asyncssh.SSHServerSession):
    """Interactive SSH session handler - FIXED VERSION"""
    
    def __init__(self, *args, **kwargs):
        """Accept asyncssh parameters properly"""
        super().__init__()
        self._session = None
        self._chan = None
        
    def connection_made(self, chan):
        self._chan = chan
        peer = chan.get_extra_info('peername')[0]
        username = chan.get_extra_info('username', 'unknown')
        
        # Create the session logic handler
        self._session = HoneypotSession(username, peer)
        logger.info(f"Session started for {username}@{peer}")
        
    def shell_requested(self):
        logger.info(f"Shell requested for {self._session.username if self._session else 'unknown'}")
        return True
    
    def session_started(self):
        logger.info(f"Session started, sending initial prompt")
        try:
            prompt = f"{self._session.username}@{self._session.fake_system_context['hostname']}:~$ "
            self._chan.write(prompt)
            logger.info(f"Initial prompt sent: {prompt}")
        except Exception as e:
            logger.error(f"Error in session_started: {e}")
    
    def data_received(self, data, datatype):
        # Decode bytes to string if needed
        if isinstance(data, bytes):
            try:
                command = data.decode('utf-8').strip()
            except:
                command = data.decode('latin-1').strip()
        else:
            command = data.strip()
        
        # Handle exit commands
        if command.lower() in ['exit', 'logout', 'quit']:
            self._chan.write("\r\nlogout\r\n")
            self._chan.close()
            logger.info(f"Session ended for {self._session.session_id}")
            return
        
        # Process command if not empty
        if command:
            self._session.command_history.append(command)
            
            # Get response
            start_time = time.time()
            
            # Use fallback responses for stability
            result = self._session.get_fallback_response(command)
            
            duration = time.time() - start_time
            
            self._session.log_command(command, result, duration)
            
            self._chan.write(f"\r\n{result}\r\n")
        
        # Always show prompt
        prompt = f"{self._session.username}@{self._session.fake_system_context['hostname']}:{self._session.fake_system_context['current_dir']}$ "
        self._chan.write(prompt)


async def start_honeypot(host='0.0.0.0', port=2222):
    """Start the AI honeypot SSH server"""
    
    # Generate host key if not exists
    key_file = Path("/home/claude/ai-honeypot/configs/ssh_host_key")
    if not key_file.exists():
        key_file.parent.mkdir(parents=True, exist_ok=True)
        key = asyncssh.generate_private_key('ssh-rsa')
        key_file.write_bytes(key.export_private_key())
        logger.info("Generated new SSH host key")
    
    logger.info(f"Starting AI Honeypot on {host}:{port}")
    
    # Create server with reuse_address to avoid "address already in use" errors
    server = await asyncssh.create_server(
        AIHoneypotServer,
        host,
        port,
        server_host_keys=[str(key_file)],
        session_factory=SSHSessionHandler,
        reuse_address=True
    )
    
    logger.info(f"AI Honeypot running on port {port}")
    
    # Keep server running
    async with server:
        await server.wait_closed()


async def main():
    """Main entry point"""
    try:
        await start_honeypot()
    except KeyboardInterrupt:
        logger.info("Shutting down honeypot...")
    except Exception as e:
        logger.error(f"Honeypot error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    # Create logs directory
    Path("/home/claude/ai-honeypot/logs").mkdir(parents=True, exist_ok=True)
    
    # Run the honeypot
    asyncio.run(main())