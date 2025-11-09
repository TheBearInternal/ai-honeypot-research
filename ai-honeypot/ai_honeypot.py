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

class AIHoneypotSession:
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
            
            async with session.post("http://localhost:11434/api/generate", 
                                   json=payload, timeout=15) as resp:
                result = await resp.json()
                return result.get("response", "").strip()
    
    def _generate_doc_fallback(self, filename):
        """Fallback document generation without AI"""
        fallback_docs = {
            "passwords.txt": """# Production Passwords - KEEP SECURE!
# Last updated: 2024-10-15

MySQL Root: MyS3cr3tP@ss2024!
FTP Server: ftp_upload_pass123
API Gateway: api_key_dev_abc123xyz
Backup Account: backup_user_2024!

# TODO: Rotate these next month
# Remember to update deployment scripts""",
            "api_keys.txt": """# API Keys - Production Environment
AWS_ACCESS_KEY=AKIA3X7MPLEKEY123456
AWS_SECRET=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
STRIPE_KEY=sk_live_51HexamplekeyGFHxyz
SENDGRID_API=SG.ExampleKey123.AbCdEfGhIjKlMnOp""",
            ".bash_history": """ls -la
cd /var/www/api
git pull origin master
mysql -u root -pMyS3cr3tP@ss2024!
sudo systemctl restart nginx
vim /etc/nginx/sites-available/default
cat /var/log/nginx/error.log
sudo apt update
df -h
ps aux | grep python
tail -f /var/log/syslog""",
            "backup.sh": """#!/bin/bash
# Daily backup script
# DB Password: MyS3cr3tP@ss2024!

mysqldump -u root -pMyS3cr3tP@ss2024! production_db > /backup/db.sql
rsync -av /var/www/html backup@192.168.1.50:/backups/
tar -czf /backup/files_$(date +%Y%m%d).tar.gz /var/www""",
            "deploy.py": """#!/usr/bin/env python3
# Deployment script - Production
# DB: mysql://root:MyS3cr3tP@ss2024!@localhost/prod

import os
import pymysql

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASS = 'MyS3cr3tP@ss2024!'  # TODO: Move to env vars
API_KEY = 'sk_live_abc123xyz789'

def deploy():
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS)
    # ... deployment logic ...""",
        }
        return fallback_docs.get(filename, f"# Content of {filename}\n# This file contains sensitive information")
    
    def classify_attacker_behavior(self, command):
        """Classify attacker based on command patterns"""
        profile = self.fake_system_context['attacker_profile']
        
        # Analyze command for sophistication
        advanced_indicators = ['find', 'grep -r', 'netstat', 'sudo -l', 'crontab', 'awk', 'sed', 'base64', 'curl', 'wget']
        recon_indicators = ['whoami', 'id', 'uname', 'hostname', 'ls', 'pwd', 'cat /etc/passwd', 'ps']
        data_theft_indicators = ['cat', 'grep', 'find', 'scp', 'rsync', 'tar', 'zip']
        privesc_indicators = ['sudo', 'su', 'passwd', 'chmod', 'chown']
        
        # Update sophistication score
        if any(ind in command for ind in advanced_indicators):
            profile['sophistication_score'] += 2
        elif any(ind in command for ind in recon_indicators):
            profile['sophistication_score'] += 1
        
        # Classify skill level
        if profile['sophistication_score'] > 10:
            profile['skill_level'] = 'advanced'
        elif profile['sophistication_score'] > 5:
            profile['skill_level'] = 'intermediate'
        else:
            profile['skill_level'] = 'novice'
        
        # Determine intent
        if any(ind in command for ind in privesc_indicators):
            profile['primary_intent'] = 'privilege_escalation'
        elif any(ind in command for ind in data_theft_indicators):
            profile['primary_intent'] = 'data_theft'
        else:
            profile['primary_intent'] = 'reconnaissance'
        
        # Log behavior pattern
        profile['behavior_patterns'].append({
            'command': command,
            'timestamp': datetime.now().isoformat(),
            'classification': profile['primary_intent']
        })
        
        return profile
    
    def get_fallback_response(self, command):
        """Fallback responses when LLM unavailable"""
        cmd = command.strip().lower().split()[0] if command.strip() else ""
        
        responses = {
            "ls": "\n".join(self.fake_system_context['fake_files'].get(
                self.fake_system_context['current_dir'], 
                ["file1.txt", "file2.txt"]
            )),
            "pwd": self.fake_system_context['current_dir'],
            "whoami": self.username,
            "id": f"uid=1001({self.username}) gid=1001({self.username}) groups=1001({self.username}),27(sudo)",
            "uname": "Linux prod-web-server-02 5.15.0-58-generic #64-Ubuntu SMP x86_64 GNU/Linux",
            "cat /etc/passwd": "root:x:0:0:root:/root:/bin/bash\nadmin:x:1000:1000::/home/admin:/bin/bash\n" + 
                               f"{self.username}:x:1001:1001::/home/{self.username}:/bin/bash",
            "ps aux": "\n".join(self.fake_system_context['fake_processes']),
            "hostname": self.fake_system_context['hostname'],
        }
        
        # Check for cd command
        if command.startswith("cd "):
            new_dir = command.split("cd ", 1)[1].strip()
            if new_dir in self.fake_system_context['fake_files']:
                self.fake_system_context['current_dir'] = new_dir
                return ""
            else:
                return f"bash: cd: {new_dir}: No such file or directory"
        
        return responses.get(cmd, f"bash: {cmd}: command not found")
    
    async def get_ai_response(self, command):
        """Get AI-powered response to command"""
        try:
            # Check if command is reading a file - generate AI content
            if command.strip().startswith("cat ") or command.strip().startswith("less ") or command.strip().startswith("more "):
                filename = command.split(maxsplit=1)[1].strip() if len(command.split()) > 1 else ""
                
                # Extract just the filename
                if '/' in filename:
                    filename = filename.split('/')[-1]
                
                # Check if this is a document we should AI-generate
                ai_gen_files = ["passwords.txt", "api_keys.txt", ".bash_history", "notes.md", 
                               "todo.txt", "backup.sh", "deploy.py", "id_rsa", "maintenance.sh"]
                
                if filename in ai_gen_files:
                    logger.info(f"Generating AI content for: {filename}")
                    content = await self.generate_ai_document(filename)
                    
                    # Track file access
                    self.fake_system_context['accessed_files'].append({
                        'file': filename,
                        'timestamp': datetime.now().isoformat()
                    })
                    
                    return content
            
            # Check if we can use OpenAI API (set via environment variable)
            if os.getenv("OPENAI_API_KEY"):
                response = await self._get_openai_response(command)
            # Check if we can use Ollama (local LLM)
            elif await self._check_ollama_available():
                response = await self._get_ollama_response(command)
            else:
                # Fallback to static responses
                logger.warning("No AI backend available, using fallback responses")
                response = self.get_fallback_response(command)
            
            return response
        except Exception as e:
            logger.error(f"Error getting AI response: {e}")
            return self.get_fallback_response(command)
    
    async def _check_ollama_available(self):
        """Check if Ollama is running locally"""
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get("http://localhost:11434/api/tags", timeout=2) as resp:
                    return resp.status == 200
        except:
            return False
    
    async def _get_ollama_response(self, command):
        """Get response from local Ollama LLM"""
        import aiohttp
        
        prompt = self.get_ai_prompt(command)
        
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": "llama3.2:3b",  # Use smaller model for speed
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


class AIHoneypotSession(asyncssh.SSHServerSession):
    """Interactive session handler"""
    
    def __init__(self):
        self._session = None
        
    def connection_made(self, chan):
        self._chan = chan
        peer = chan.get_extra_info('peername')[0]
        username = chan.get_extra_info('username', 'unknown')
        
        self._session = AIHoneypotSession(username, peer)
        logger.info(f"Session started for {username}@{peer}")
        
    def shell_requested(self):
        return True
    
    def session_started(self):
        self._chan.write(f"{self._session.username}@{self._session.fake_system_context['hostname']}:~$ ")
    
    def data_received(self, data, datatype):
        command = data.strip()
        
        if command.lower() in ['exit', 'logout', 'quit']:
            self._chan.write("\r\nlogout\r\n")
            self._chan.close()
            logger.info(f"Session ended for {self._session.session_id}")
            return
        
        if command:
            self._session.command_history.append(command)
            
            # Get AI response
            start_time = time.time()
            response = asyncio.create_task(self._session.get_ai_response(command))
            
            # This is a simplified sync wrapper - in production use proper async
            try:
                loop = asyncio.get_event_loop()
                result = loop.run_until_complete(response)
            except:
                result = self._session.get_fallback_response(command)
            
            duration = time.time() - start_time
            
            self._session.log_command(command, result, duration)
            
            self._chan.write(f"\r\n{result}\r\n")
        
        self._chan.write(f"{self._session.username}@{self._session.fake_system_context['hostname']}:{self._session.fake_system_context['current_dir']}$ ")


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
    
    await asyncssh.create_server(
        AIHoneypotServer,
        host,
        port,
        server_host_keys=[str(key_file)],
        session_factory=AIHoneypotSession
    )
    
    logger.info(f"AI Honeypot running on port {port}")


if __name__ == "__main__":
    # Create logs directory
    Path("/home/claude/ai-honeypot/logs").mkdir(parents=True, exist_ok=True)
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_honeypot())
    loop.run_forever()
