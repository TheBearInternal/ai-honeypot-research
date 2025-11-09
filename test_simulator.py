#!/usr/bin/env python3
"""
Attack Simulator - Test both honeypots with realistic attack patterns
Used for controlled experiments and baseline testing
"""

import asyncio
import asyncssh
import random
import time
from datetime import datetime

class AttackSimulator:
    """Simulates various attack patterns for testing"""
    
    ATTACK_SCENARIOS = {
        "reconnaissance": [
            "whoami",
            "id",
            "uname -a",
            "hostname",
            "pwd",
            "ls -la",
            "cat /etc/passwd",
            "ps aux",
            "netstat -tulpn",
            "ifconfig",
            "w",
            "last"
        ],
        "data_hunting": [
            "ls -la",
            "cd documents",
            "ls",
            "cat passwords.txt",
            "cat .bash_history",
            "find / -name '*.conf' 2>/dev/null",
            "grep -r 'password' /home/",
            "cat /etc/shadow"
        ],
        "privilege_escalation": [
            "sudo -l",
            "cat /etc/sudoers",
            "find / -perm -4000 2>/dev/null",
            "sudo su",
            "su root"
        ],
        "persistence": [
            "crontab -l",
            "cat /etc/crontab",
            "ls -la /etc/cron.d",
            "systemctl list-units --type=service"
        ],
        "lateral_movement": [
            "cat .ssh/known_hosts",
            "cat .ssh/id_rsa",
            "cat .ssh/authorized_keys",
            "netstat -an"
        ],
        "automated_scanner": [
            "ls",
            "pwd",
            "uname -a",
            "cat /etc/issue",
            "exit"
        ],
        "curious_human": [
            "ls",
            "whoami",
            "ls -la",
            "cat .bash_history",
            "ps aux",
            "cat documents/passwords.txt",
            "cd /var/www",
            "ls",
            "cat /etc/passwd"
        ]
    }
    
    def __init__(self, host='localhost', ai_port=2222, trad_port=2223):
        self.host = host
        self.ai_port = ai_port
        self.trad_port = trad_port
        
    async def run_attack_scenario(self, port, scenario_name, delay_range=(1, 3)):
        """Execute an attack scenario against a honeypot"""
        
        commands = self.ATTACK_SCENARIOS.get(scenario_name, [])
        
        print(f"\n{'='*60}")
        print(f"Running '{scenario_name}' against port {port}")
        print(f"Commands: {len(commands)}")
        print(f"{'='*60}\n")
        
        try:
            async with asyncssh.connect(
                self.host,
                port=port,
                username='attacker',
                password='password123',
                known_hosts=None
            ) as conn:
                
                for i, command in enumerate(commands, 1):
                    print(f"[{i}/{len(commands)}] Executing: {command}")
                    
                    try:
                        result = await conn.run(command, check=False, timeout=10)
                        
                        if result.stdout:
                            output = result.stdout.strip()
                            # Only show first 200 chars
                            if len(output) > 200:
                                print(f"Response: {output[:200]}...")
                            else:
                                print(f"Response: {output}")
                        
                    except Exception as e:
                        print(f"Error running command: {e}")
                    
                    # Random delay between commands (human-like behavior)
                    delay = random.uniform(*delay_range)
                    await asyncio.sleep(delay)
                
                print(f"\n✅ Scenario complete: {scenario_name}")
                
        except Exception as e:
            print(f"\n❌ Connection error: {e}")
    
    async def run_comparison_test(self, scenario_name):
        """Run same attack against both honeypots for comparison"""
        
        print(f"\n{'#'*60}")
        print(f"COMPARATIVE TEST: {scenario_name}")
        print(f"{'#'*60}")
        
        start_time = time.time()
        
        # Test AI honeypot
        print("\n[1/2] Testing AI Honeypot...")
        await self.run_attack_scenario(self.ai_port, scenario_name)
        
        await asyncio.sleep(2)
        
        # Test traditional honeypot
        print("\n[2/2] Testing Traditional Honeypot...")
        await self.run_attack_scenario(self.trad_port, scenario_name)
        
        total_time = time.time() - start_time
        
        print(f"\n{'='*60}")
        print(f"Total test duration: {total_time:.2f} seconds")
        print(f"{'='*60}\n")
    
    async def run_all_scenarios(self, test_both=True):
        """Run all attack scenarios"""
        
        print("\n" + "="*60)
        print("ATTACK SIMULATOR - Running All Scenarios")
        print("="*60)
        
        for scenario in self.ATTACK_SCENARIOS.keys():
            if test_both:
                await self.run_comparison_test(scenario)
            else:
                await self.run_attack_scenario(self.ai_port, scenario)
            
            # Wait between scenarios
            await asyncio.sleep(5)
        
        print("\n" + "="*60)
        print("ALL SCENARIOS COMPLETE")
        print("Run 'python analysis/analyzer.py' to see results")
        print("="*60)
    
    async def continuous_simulation(self, sessions=10, delay_between=30):
        """Run continuous attack simulation for data collection"""
        
        print(f"\nRunning {sessions} attack sessions...")
        print(f"Delay between sessions: {delay_between}s\n")
        
        scenarios = list(self.ATTACK_SCENARIOS.keys())
        
        for i in range(sessions):
            # Randomly choose scenario and port
            scenario = random.choice(scenarios)
            port = random.choice([self.ai_port, self.trad_port])
            
            print(f"\n[Session {i+1}/{sessions}] {scenario} -> Port {port}")
            
            await self.run_attack_scenario(
                port,
                scenario,
                delay_range=(0.5, 2)  # Faster for simulation
            )
            
            if i < sessions - 1:
                await asyncio.sleep(delay_between)
        
        print("\n✅ Continuous simulation complete!")


async def main():
    simulator = AttackSimulator()
    
    print("\n" + "="*60)
    print("AI HONEYPOT ATTACK SIMULATOR")
    print("="*60)
    print("\nWhat would you like to do?\n")
    print("1. Run single scenario comparison (AI vs Traditional)")
    print("2. Run all scenarios")
    print("3. Continuous simulation (10 sessions)")
    print("4. Quick test (reconnaissance only)")
    print()
    
    choice = input("Enter choice (1-4) or press Enter for quick test: ").strip()
    
    if choice == '1':
        print("\nAvailable scenarios:")
        for i, scenario in enumerate(simulator.ATTACK_SCENARIOS.keys(), 1):
            print(f"{i}. {scenario}")
        
        scenario_idx = int(input("\nSelect scenario number: ")) - 1
        scenario_name = list(simulator.ATTACK_SCENARIOS.keys())[scenario_idx]
        
        await simulator.run_comparison_test(scenario_name)
        
    elif choice == '2':
        confirm = input("\nThis will run 7 scenarios against both honeypots. Continue? (y/n): ")
        if confirm.lower() == 'y':
            await simulator.run_all_scenarios()
    
    elif choice == '3':
        sessions = input("\nNumber of sessions (default 10): ").strip()
        sessions = int(sessions) if sessions else 10
        
        await simulator.continuous_simulation(sessions=sessions)
    
    else:
        # Quick test (default)
        print("\nRunning quick reconnaissance test...\n")
        await simulator.run_comparison_test("reconnaissance")
    
    print("\n✅ Done! Check logs/ directory for captured data")
    print("📊 Run: python analysis/analyzer.py")


if __name__ == "__main__":
    print("\n⚠️  Make sure both honeypots are running!")
    print("Terminal 1: python ai-honeypot/ai_honeypot.py")
    print("Terminal 2: python traditional-honeypot/traditional_honeypot.py\n")
    
    time.sleep(2)
    
    asyncio.run(main())
