#!/usr/bin/env python3
"""
Traffic Generator - Simulates realistic user activity
Part of the "dead internet" deception layer
"""

import asyncio
import random
import time
from datetime import datetime
import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('TrafficGen')


class FakeUser:
    """Simulates a single user's behavior patterns"""
    
    USER_PROFILES = [
        {
            "name": "developer",
            "commands": [
                "git status", "git pull", "git log", "ls -la", "vim app.py",
                "python manage.py runserver", "docker ps", "docker logs api",
                "cat requirements.txt", "pip install -r requirements.txt",
                "pytest", "tail -f /var/log/app.log"
            ],
            "active_hours": (9, 18),
            "frequency_minutes": (5, 20)
        },
        {
            "name": "sysadmin",
            "commands": [
                "top", "htop", "free -m", "df -h", "systemctl status nginx",
                "tail -f /var/log/syslog", "netstat -tulpn", "ps aux",
                "uptime", "who", "last", "sudo systemctl restart nginx"
            ],
            "active_hours": (8, 20),
            "frequency_minutes": (10, 30)
        },
        {
            "name": "data_analyst",
            "commands": [
                "ls data/", "cat data/report.csv", "python analyze.py",
                "head -n 100 data/logs.csv", "wc -l data/*.csv",
                "grep ERROR logs/*.log", "jupyter notebook list"
            ],
            "active_hours": (9, 17),
            "frequency_minutes": (15, 45)
        },
        {
            "name": "backup_bot",
            "commands": [
                "rsync -av /var/www /backup/", "tar -czf backup.tar.gz data/",
                "ls -lh /backup/", "df -h /backup", "find /var/log -mtime +7"
            ],
            "active_hours": (2, 4),
            "frequency_minutes": (60, 120)
        }
    ]
    
    def __init__(self, profile):
        self.profile = profile
        self.name = profile["name"]
        self.commands = profile["commands"]
        self.active_hours = profile["active_hours"]
        self.frequency_minutes = profile["frequency_minutes"]
        
    def is_active_hour(self):
        """Check if current hour is within active hours"""
        current_hour = datetime.now().hour
        start, end = self.active_hours
        return start <= current_hour < end
    
    def get_next_command(self):
        """Get random command from profile"""
        return random.choice(self.commands)
    
    def get_sleep_duration(self):
        """Get random sleep duration in seconds"""
        minutes = random.uniform(*self.frequency_minutes)
        return minutes * 60


class TrafficGenerator:
    """Manages multiple fake users generating traffic"""
    
    def __init__(self, log_file="/home/claude/ai-honeypot/logs/fake_traffic.jsonl"):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self.users = [FakeUser(profile) for profile in FakeUser.USER_PROFILES]
        
    def log_activity(self, user_name, command):
        """Log fake user activity"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "fake_traffic",
            "user": user_name,
            "command": command,
            "source": "traffic_generator"
        }
        
        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        
        logger.info(f"[{user_name}] {command}")
    
    async def simulate_user(self, user):
        """Simulate single user's activity"""
        logger.info(f"Starting simulation for user: {user.name}")
        
        while True:
            if user.is_active_hour():
                command = user.get_next_command()
                self.log_activity(user.name, command)
                
                # Add random micro-variations to make it look more realistic
                if random.random() < 0.1:  # 10% chance of burst activity
                    await asyncio.sleep(random.uniform(1, 5))
                    command2 = user.get_next_command()
                    self.log_activity(user.name, command2)
            
            sleep_duration = user.get_sleep_duration()
            await asyncio.sleep(sleep_duration)
    
    async def run(self):
        """Start all user simulations"""
        logger.info(f"Starting traffic generation with {len(self.users)} users")
        
        tasks = [self.simulate_user(user) for user in self.users]
        await asyncio.gather(*tasks)


class AdvancedTrafficPattern:
    """More sophisticated traffic patterns for AI enhancement"""
    
    @staticmethod
    def web_browsing_pattern():
        """Simulate web server access patterns"""
        endpoints = [
            "/api/users", "/api/products", "/api/orders", "/admin/dashboard",
            "/health", "/metrics", "/login", "/logout", "/api/search"
        ]
        methods = ["GET", "POST", "PUT", "DELETE"]
        
        pattern = []
        for _ in range(random.randint(5, 15)):
            endpoint = random.choice(endpoints)
            method = random.choice(methods)
            status = random.choices([200, 201, 400, 404, 500], weights=[70, 10, 10, 5, 5])[0]
            
            pattern.append({
                "type": "http_request",
                "method": method,
                "endpoint": endpoint,
                "status": status,
                "timestamp": datetime.now().isoformat()
            })
            
        return pattern
    
    @staticmethod
    def database_activity_pattern():
        """Simulate database query patterns"""
        queries = [
            "SELECT * FROM users WHERE active=1",
            "INSERT INTO logs (event, timestamp) VALUES",
            "UPDATE sessions SET last_active=NOW()",
            "SELECT COUNT(*) FROM orders WHERE date > NOW() - INTERVAL 1 DAY",
            "DELETE FROM temp_cache WHERE created < NOW() - INTERVAL 1 HOUR"
        ]
        
        pattern = []
        for _ in range(random.randint(3, 10)):
            pattern.append({
                "type": "database_query",
                "query": random.choice(queries),
                "duration_ms": random.uniform(10, 500),
                "timestamp": datetime.now().isoformat()
            })
            
        return pattern
    
    @staticmethod
    def network_activity_pattern():
        """Simulate network traffic patterns"""
        destinations = [
            "api.stripe.com", "api.github.com", "registry.npmjs.org",
            "pypi.org", "cdn.example.com", "analytics.example.com"
        ]
        
        pattern = []
        for _ in range(random.randint(5, 20)):
            pattern.append({
                "type": "network_request",
                "destination": random.choice(destinations),
                "bytes": random.randint(1000, 100000),
                "protocol": random.choice(["HTTPS", "HTTP"]),
                "timestamp": datetime.now().isoformat()
            })
            
        return pattern


class EnhancedTrafficGenerator:
    """Enhanced generator with multiple traffic types"""
    
    def __init__(self, log_file="/home/claude/ai-honeypot/logs/enhanced_traffic.jsonl"):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self.pattern_generator = AdvancedTrafficPattern()
        
    def log_pattern(self, pattern_type, data):
        """Log traffic pattern"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "pattern_type": pattern_type,
            "data": data,
            "source": "enhanced_traffic_generator"
        }
        
        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    
    async def generate_patterns(self):
        """Continuously generate various traffic patterns"""
        logger.info("Starting enhanced traffic generation")
        
        while True:
            # Generate different types of patterns
            pattern_type = random.choice(["web", "database", "network"])
            
            if pattern_type == "web":
                data = self.pattern_generator.web_browsing_pattern()
                self.log_pattern("web_traffic", data)
            elif pattern_type == "database":
                data = self.pattern_generator.database_activity_pattern()
                self.log_pattern("database_activity", data)
            else:
                data = self.pattern_generator.network_activity_pattern()
                self.log_pattern("network_activity", data)
            
            # Random sleep between bursts
            await asyncio.sleep(random.uniform(30, 120))


async def main():
    """Run both basic and enhanced traffic generators"""
    basic_gen = TrafficGenerator()
    enhanced_gen = EnhancedTrafficGenerator()
    
    await asyncio.gather(
        basic_gen.run(),
        enhanced_gen.generate_patterns()
    )


if __name__ == "__main__":
    logger.info("=== Traffic Generator Started ===")
    logger.info("Simulating realistic user and system activity")
    logger.info("This creates the 'dead internet' deception layer")
    
    asyncio.run(main())
