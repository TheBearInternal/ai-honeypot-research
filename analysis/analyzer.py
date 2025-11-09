#!/usr/bin/env python3
"""
Honeypot Analysis Tool
Compares AI-enhanced vs Traditional honeypot effectiveness
"""

import json
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict, Counter

class HoneypotAnalyzer:
    """Analyzes honeypot data for research paper metrics"""
    
    def __init__(self, log_dir="/home/claude/ai-honeypot/logs"):
        self.log_dir = Path(log_dir)
        self.commands_file = self.log_dir / "commands.jsonl"
        self.auth_file = self.log_dir / "auth.jsonl"
        
    def load_commands(self):
        """Load all command logs"""
        if not self.commands_file.exists():
            print(f"Warning: {self.commands_file} not found")
            return []
        
        commands = []
        with open(self.commands_file, 'r') as f:
            for line in f:
                try:
                    commands.append(json.loads(line))
                except:
                    pass
        return commands
    
    def load_auth_attempts(self):
        """Load authentication attempts"""
        if not self.auth_file.exists():
            print(f"Warning: {self.auth_file} not found")
            return []
        
        attempts = []
        with open(self.auth_file, 'r') as f:
            for line in f:
                try:
                    attempts.append(json.loads(line))
                except:
                    pass
        return attempts
    
    def analyze_session_duration(self, commands):
        """Analyze session durations - KEY METRIC"""
        sessions = defaultdict(list)
        
        for cmd in commands:
            session_id = cmd.get('session_id')
            if session_id:
                sessions[session_id].append(cmd)
        
        ai_durations = []
        traditional_durations = []
        
        for session_id, cmds in sessions.items():
            if not cmds:
                continue
            
            timestamps = [datetime.fromisoformat(c['timestamp']) for c in cmds]
            duration_minutes = (max(timestamps) - min(timestamps)).total_seconds() / 60
            command_count = len(cmds)
            
            # Determine honeypot type from any command in session
            honeypot_type = cmds[0].get('honeypot_type', 'unknown')
            
            session_data = {
                'duration_minutes': duration_minutes,
                'command_count': command_count,
                'session_id': session_id,
                'ip': cmds[0].get('ip', 'unknown')
            }
            
            if 'traditional' in str(honeypot_type).lower():
                traditional_durations.append(session_data)
            else:
                ai_durations.append(session_data)
        
        return ai_durations, traditional_durations
    
    def analyze_command_diversity(self, commands):
        """Analyze variety of commands attempted"""
        ai_commands = defaultdict(list)
        traditional_commands = defaultdict(list)
        
        for cmd in commands:
            command = cmd.get('command', '')
            honeypot_type = cmd.get('honeypot_type', 'ai')
            
            if 'traditional' in str(honeypot_type).lower():
                traditional_commands[cmd.get('session_id')].append(command)
            else:
                ai_commands[cmd.get('session_id')].append(command)
        
        ai_diversity = [len(set(cmds)) for cmds in ai_commands.values()]
        trad_diversity = [len(set(cmds)) for cmds in traditional_commands.values()]
        
        return ai_diversity, trad_diversity
    
    def analyze_attack_patterns(self, commands):
        """Identify common attack patterns"""
        patterns = {
            'reconnaissance': ['ls', 'pwd', 'whoami', 'id', 'uname', 'hostname', 'ifconfig', 'netstat'],
            'privilege_escalation': ['sudo', 'su', 'passwd'],
            'data_exfiltration': ['cat', 'grep', 'find', 'scp', 'wget', 'curl'],
            'persistence': ['crontab', 'systemctl', 'service', 'vim', 'nano'],
            'lateral_movement': ['ssh', 'nc', 'telnet', 'ping']
        }
        
        ai_patterns = Counter()
        trad_patterns = Counter()
        
        # Track attacker skill levels (AI honeypot only)
        ai_skill_levels = Counter()
        ai_intents = Counter()
        
        for cmd in commands:
            command = cmd.get('command', '').lower()
            honeypot_type = cmd.get('honeypot_type', 'ai')
            
            # Collect attacker profiling data from AI honeypot
            if 'ai' in str(honeypot_type).lower() or honeypot_type == 'ai_enhanced':
                attacker_profile = cmd.get('attacker_profile', {})
                if attacker_profile:
                    skill = attacker_profile.get('skill_level', 'unknown')
                    intent = attacker_profile.get('primary_intent', 'unknown')
                    ai_skill_levels[skill] += 1
                    ai_intents[intent] += 1
            
            for pattern_type, keywords in patterns.items():
                if any(keyword in command for keyword in keywords):
                    if 'traditional' in str(honeypot_type).lower():
                        trad_patterns[pattern_type] += 1
                    else:
                        ai_patterns[pattern_type] += 1
        
        return ai_patterns, trad_patterns, ai_skill_levels, ai_intents
    
    def generate_report(self):
        """Generate comprehensive analysis report"""
        print("=" * 60)
        print("HONEYPOT EFFECTIVENESS ANALYSIS")
        print("AI-Enhanced vs Traditional Comparison")
        print("=" * 60)
        print()
        
        commands = self.load_commands()
        auth_attempts = self.load_auth_attempts()
        
        if not commands:
            print("No command data found. Run honeypots first.")
            return
        
        print(f"Total Commands Logged: {len(commands)}")
        print(f"Total Auth Attempts: {len(auth_attempts)}")
        print()
        
        # Session Duration Analysis
        print("-" * 60)
        print("1. SESSION DURATION ANALYSIS (Key Metric)")
        print("-" * 60)
        
        ai_sessions, trad_sessions = self.analyze_session_duration(commands)
        
        if ai_sessions:
            ai_avg = sum(s['duration_minutes'] for s in ai_sessions) / len(ai_sessions)
            ai_cmd_avg = sum(s['command_count'] for s in ai_sessions) / len(ai_sessions)
            print(f"AI Honeypot:")
            print(f"  - Average session duration: {ai_avg:.2f} minutes")
            print(f"  - Average commands per session: {ai_cmd_avg:.1f}")
            print(f"  - Total sessions: {len(ai_sessions)}")
        else:
            print("AI Honeypot: No sessions recorded yet")
        
        print()
        
        if trad_sessions:
            trad_avg = sum(s['duration_minutes'] for s in trad_sessions) / len(trad_sessions)
            trad_cmd_avg = sum(s['command_count'] for s in trad_sessions) / len(trad_sessions)
            print(f"Traditional Honeypot:")
            print(f"  - Average session duration: {trad_avg:.2f} minutes")
            print(f"  - Average commands per session: {trad_cmd_avg:.1f}")
            print(f"  - Total sessions: {len(trad_sessions)}")
        else:
            print("Traditional Honeypot: No sessions recorded yet")
        
        print()
        
        if ai_sessions and trad_sessions:
            improvement = ((ai_avg - trad_avg) / trad_avg) * 100
            print(f"⭐ ENGAGEMENT IMPROVEMENT: {improvement:+.1f}%")
        
        print()
        
        # Command Diversity Analysis
        print("-" * 60)
        print("2. COMMAND DIVERSITY ANALYSIS")
        print("-" * 60)
        
        ai_diversity, trad_diversity = self.analyze_command_diversity(commands)
        
        if ai_diversity:
            print(f"AI Honeypot - Avg unique commands/session: {sum(ai_diversity)/len(ai_diversity):.1f}")
        if trad_diversity:
            print(f"Traditional - Avg unique commands/session: {sum(trad_diversity)/len(trad_diversity):.1f}")
        
        print()
        
        # Attack Pattern Analysis
        print("-" * 60)
        print("3. ATTACK PATTERN ANALYSIS")
        print("-" * 60)
        
        ai_patterns, trad_patterns, ai_skill_levels, ai_intents = self.analyze_attack_patterns(commands)
        
        print("AI Honeypot patterns:")
        for pattern, count in ai_patterns.most_common():
            print(f"  - {pattern}: {count}")
        
        print()
        print("Traditional Honeypot patterns:")
        for pattern, count in trad_patterns.most_common():
            print(f"  - {pattern}: {count}")
        
        # NEW: Attacker Profiling (AI Honeypot only)
        if ai_skill_levels:
            print()
            print("-" * 60)
            print("4. ATTACKER PROFILING (AI Honeypot Intelligence)")
            print("-" * 60)
            
            print("Attacker Skill Levels Detected:")
            for skill, count in ai_skill_levels.most_common():
                percentage = (count / sum(ai_skill_levels.values())) * 100
                print(f"  - {skill}: {count} ({percentage:.1f}%)")
            
            print()
            print("Primary Attack Intents:")
            for intent, count in ai_intents.most_common():
                percentage = (count / sum(ai_intents.values())) * 100
                print(f"  - {intent}: {count} ({percentage:.1f}%)")
            
            print()
            print("⭐ AI Advantage: Automatic attacker classification!")
        
        print()
        
        # Authentication Analysis (now section 5)
        print("-" * 60)
        print("5. AUTHENTICATION ATTEMPTS")
        print("-" * 60)
        
        usernames = Counter([a.get('username') for a in auth_attempts])
        passwords = Counter([a.get('password') for a in auth_attempts])
        
        print("Top usernames attempted:")
        for user, count in usernames.most_common(5):
            print(f"  - {user}: {count}")
        
        print()
        print("Top passwords attempted:")
        for pwd, count in passwords.most_common(5):
            print(f"  - {pwd}: {count}")
        
        print()
        print("=" * 60)
        print("RESEARCH PAPER METRICS SUMMARY")
        print("=" * 60)
        
        metrics = {
            "Total Sessions": len(ai_sessions) + len(trad_sessions),
            "AI Sessions": len(ai_sessions),
            "Traditional Sessions": len(trad_sessions),
        }
        
        if ai_sessions and trad_sessions:
            metrics["Avg Engagement Time Increase"] = f"{improvement:.1f}%"
            metrics["AI Avg Duration"] = f"{ai_avg:.2f} min"
            metrics["Traditional Avg Duration"] = f"{trad_avg:.2f} min"
        
        for key, value in metrics.items():
            print(f"{key}: {value}")
        
        print()
        print("Analysis complete. Use this data for your research paper.")
        
        return {
            'ai_sessions': ai_sessions,
            'trad_sessions': trad_sessions,
            'ai_patterns': ai_patterns,
            'trad_patterns': trad_patterns,
            'auth_attempts': auth_attempts
        }
    
    def export_csv(self, output_dir="/home/claude/ai-honeypot/analysis"):
        """Export data to CSV for further analysis"""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        commands = self.load_commands()
        
        if commands:
            df = pd.DataFrame(commands)
            df.to_csv(output_dir / "commands.csv", index=False)
            print(f"Exported commands to {output_dir / 'commands.csv'}")
        
        auth_attempts = self.load_auth_attempts()
        if auth_attempts:
            df_auth = pd.DataFrame(auth_attempts)
            df_auth.to_csv(output_dir / "auth_attempts.csv", index=False)
            print(f"Exported auth attempts to {output_dir / 'auth_attempts.csv'}")


def main():
    analyzer = HoneypotAnalyzer()
    
    print("Starting analysis...")
    print()
    
    results = analyzer.generate_report()
    
    print()
    print("Exporting data to CSV...")
    analyzer.export_csv()
    
    print()
    print("Done! Check the analysis directory for CSV exports.")


if __name__ == "__main__":
    main()
