#!/usr/bin/env python3
"""
AI-Powered Traffic Generator - Dynamic "Dead Internet" Simulation
Uses LLMs to generate realistic, context-aware user activity patterns
"""

import asyncio
import random
import time
from datetime import datetime
import json
from pathlib import Path
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('AI-TrafficGen')


class AIUserPersona:
    """AI-driven user persona that generates contextual activity"""
    
    def __init__(self, role, llm_backend='fallback'):
        self.role = role
        self.llm_backend = llm_backend
        self.activity_history = []
        self.context = self._initialize_context()
        
    def _initialize_context(self):
        """Initialize persona-specific context"""
        contexts = {
            "developer": {
                "current_project": "e-commerce API",
                "tech_stack": "Python, Django, PostgreSQL, Redis",
                "recent_tasks": ["fixing bug in payment processing", "deploying to staging", "code review"],
                "work_hours": (9, 18)
            },
            "sysadmin": {
                "infrastructure": "30 Ubuntu servers, MySQL cluster, Nginx load balancers",
                "monitoring": "Prometheus, Grafana",
                "recent_tasks": ["investigating disk space issue", "patching security vulnerabilities", "backup verification"],
                "work_hours": (8, 20)
            },
            "data_analyst": {
                "tools": "Python, pandas, Jupyter, SQL",
                "current_analysis": "Q4 sales metrics",
                "recent_tasks": ["cleaning customer data", "building dashboard", "statistical analysis"],
                "work_hours": (9, 17)
            },
            "security_engineer": {
                "tools": "Nmap, Metasploit, Burp Suite, Wireshark",
                "focus": "penetration testing, vulnerability scanning",
                "recent_tasks": ["security audit", "analyzing logs", "updating firewall rules"],
                "work_hours": (10, 19)
            }
        }
        return contexts.get(self.role, contexts["developer"])
    
    async def generate_activity_sequence(self):
        """Use AI to generate realistic sequence of commands"""
        
        prompt = f"""Generate a realistic sequence of 5-7 Linux commands that a {self.role} would run.

Context:
- Role: {self.role}
- Current project/task: {self.context.get('current_project', self.context.get('infrastructure', 'system maintenance'))}
- Tech stack: {self.context.get('tech_stack', self.context.get('tools', 'Linux tools'))}
- Recent activity: {', '.join(self.activity_history[-3:]) if self.activity_history else 'starting work session'}

Requirements:
1. Commands should be realistic and contextual
2. Show natural workflow (e.g., cd to directory, then ls, then edit file)
3. Include some monitoring/checking commands
4. Make it look like actual work being done
5. Return ONLY the commands, one per line, no explanations

Example output format:
cd /var/www/api
git status
ls -la
cat config.py
tail -f logs/app.log"""

        try:
            if os.getenv("OPENAI_API_KEY"):
                commands = await self._generate_openai(prompt)
            elif await self._check_ollama():
                commands = await self._generate_ollama(prompt)
            else:
                commands = self._generate_fallback()
            
            # Parse commands into list
            command_list = [cmd.strip() for cmd in commands.split('\n') if cmd.strip() and not cmd.startswith('#')]
            
            # Update history
            self.activity_history.extend(command_list[-3:])  # Keep last 3 for context
            
            return command_list
            
        except Exception as e:
            logger.error(f"Error generating AI activity: {e}")
            return self._generate_fallback().split('\n')
    
    async def _generate_openai(self, prompt):
        """Generate using OpenAI"""
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
                    {"role": "system", "content": "You generate realistic Linux command sequences for different user roles."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.8,
                "max_tokens": 200
            }
            
            async with session.post("https://api.openai.com/v1/chat/completions", 
                                   headers=headers, json=payload, timeout=10) as resp:
                result = await resp.json()
                return result["choices"][0]["message"]["content"].strip()
    
    async def _generate_ollama(self, prompt):
        """Generate using Ollama"""
        import aiohttp
        
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": "llama3.2:3b",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.8,
                    "num_predict": 200
                }
            }
            
            async with session.post("http://localhost:11434/api/generate", 
                                   json=payload, timeout=15) as resp:
                result = await resp.json()
                return result.get("response", "").strip()
    
    async def _check_ollama(self):
        """Check if Ollama is available"""
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get("http://localhost:11434/api/tags", timeout=2) as resp:
                    return resp.status == 200
        except:
            return False
    
    def _generate_fallback(self):
        """Fallback to scripted commands"""
        fallback_sequences = {
            "developer": """cd /var/www/api
git pull origin master
python manage.py migrate
pytest tests/
tail -f logs/app.log""",
            "sysadmin": """top -n 1
df -h
systemctl status nginx
tail /var/log/syslog
netstat -tulpn""",
            "data_analyst": """cd ~/analysis
jupyter notebook list
python process_data.py
head -n 100 data/sales.csv
cat results/summary.txt""",
            "security_engineer": """nmap -sV localhost
cat /var/log/auth.log | grep Failed
sudo iptables -L
ps aux | grep suspicious
netstat -an | grep LISTEN"""
        }
        return fallback_sequences.get(self.role, "ls\npwd\nwhoami")


class AITrafficGenerator:
    """Manages AI-driven traffic generation"""
    
    def __init__(self, log_file="/home/claude/ai-honeypot/logs/ai_traffic.jsonl"):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Create diverse AI personas
        self.personas = [
            AIUserPersona("developer"),
            AIUserPersona("sysadmin"),
            AIUserPersona("data_analyst"),
            AIUserPersona("security_engineer"),
        ]
        
    def log_activity(self, persona_role, commands, generation_method):
        """Log AI-generated activity"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "ai_generated_traffic",
            "persona": persona_role,
            "commands": commands,
            "generation_method": generation_method,
            "command_count": len(commands)
        }
        
        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        
        logger.info(f"[AI-{persona_role}] Generated {len(commands)} commands")
    
    async def simulate_persona(self, persona):
        """Simulate single AI persona's activity"""
        logger.info(f"Starting AI simulation for: {persona.role}")
        
        while True:
            # Check if within work hours
            current_hour = datetime.now().hour
            work_start, work_end = persona.context['work_hours']
            
            if work_start <= current_hour < work_end:
                # Generate activity sequence using AI
                commands = await persona.generate_activity_sequence()
                
                # Determine generation method for logging
                if os.getenv("OPENAI_API_KEY"):
                    method = "openai"
                elif await persona._check_ollama():
                    method = "ollama"
                else:
                    method = "fallback"
                
                self.log_activity(persona.role, commands, method)
                
                # Execute commands with realistic timing
                for cmd in commands:
                    await asyncio.sleep(random.uniform(2, 8))  # Human-like pauses
                
                # Random burst activity (10% chance)
                if random.random() < 0.1:
                    logger.info(f"[{persona.role}] Burst activity detected")
                    extra_commands = await persona.generate_activity_sequence()
                    self.log_activity(persona.role, extra_commands, method + "_burst")
                    await asyncio.sleep(random.uniform(30, 60))
            
            # Sleep until next activity period
            sleep_duration = random.uniform(5 * 60, 20 * 60)  # 5-20 minutes
            await asyncio.sleep(sleep_duration)
    
    async def run(self):
        """Start all AI persona simulations"""
        logger.info("="*60)
        logger.info("AI-POWERED TRAFFIC GENERATOR STARTED")
        logger.info("="*60)
        logger.info(f"Active personas: {len(self.personas)}")
        logger.info(f"Using: {'OpenAI' if os.getenv('OPENAI_API_KEY') else 'Ollama/Fallback'}")
        logger.info("="*60)
        
        tasks = [self.simulate_persona(persona) for persona in self.personas]
        await asyncio.gather(*tasks)


async def main():
    generator = AITrafficGenerator()
    await generator.run()


if __name__ == "__main__":
    logger.info("🤖 AI-Powered Traffic Generator")
    logger.info("Generating realistic, context-aware user activity")
    logger.info("This is the 'Dead Internet' deception layer - AI edition")
    logger.info("")
    
    asyncio.run(main())
