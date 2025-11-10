# ⚡ QUICK DEPLOYMENT CHECKLIST

## 🎯 GOAL
Run both honeypots simultaneously to collect comparative research data.

---

## ✅ PHASE 1: LOCAL TESTING (Do This First!)

### 1. Clone Your Repository
```bash
git clone https://github.com/TheBearInternal/ai-honeypot-research.git
cd ai-honeypot-research
```

### 2. Setup Environment
```bash
# Mac/Linux
./setup.sh

# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Test Traditional Honeypot
**Terminal 1:**
```bash
python traditional-honeypot/traditional_honeypot.py
```

**Terminal 2:**
```bash
ssh user@localhost -p 2223
# Try: ls, pwd, whoami
```

✅ Traditional works!

### 4. Test AI Honeypot
**Terminal 1:**
```bash
export OPENAI_API_KEY="sk-..."  # If using OpenAI
python ai-honeypot/ai_honeypot.py
```

**Terminal 2:**
```bash
ssh user@localhost -p 2222
# Try: ls, cat passwords.txt
```

✅ AI works!

### 5. Run Both Simultaneously
**Terminal 1:** `python traditional-honeypot/traditional_honeypot.py`  
**Terminal 2:** `python ai-honeypot/ai_honeypot.py`  
**Terminal 3:** Test traditional (port 2223)  
**Terminal 4:** Test AI (port 2222)  

✅ Both running!

---

## 🌐 PHASE 2: VPS DEPLOYMENT (Real Research)

### 1. Get VPS
- DigitalOcean ($6/month, student credit available)
- Ubuntu 22.04, 2GB RAM
- Note IP: `123.45.67.89`

### 2. Connect & Setup
```bash
ssh root@123.45.67.89
apt update && apt upgrade -y
apt install python3 python3-pip python3-venv git tmux -y
```

### 3. Deploy Code
```bash
git clone https://github.com/TheBearInternal/ai-honeypot-research.git
cd ai-honeypot-research
./setup.sh
source venv/bin/activate
```

### 4. Configure Firewall
```bash
sudo ufw allow 22/tcp
sudo ufw allow 2222/tcp
sudo ufw allow 2223/tcp
sudo ufw enable
```

### 5. Run Honeypots (Production)
```bash
# Traditional
tmux new -s traditional
python traditional-honeypot/traditional_honeypot.py
# Press: Ctrl+B, then D

# AI
tmux new -s ai
export OPENAI_API_KEY="sk-..."
python ai-honeypot/ai_honeypot.py
# Press: Ctrl+B, then D
```

### 6. Verify From Internet
```bash
# From your computer
ssh user@123.45.67.89 -p 2223  # Traditional
ssh user@123.45.67.89 -p 2222  # AI
```

✅ Live on internet!

---

## 📊 PHASE 3: DATA COLLECTION (4-8 weeks)

### Weekly Tasks
```bash
# Check still running
ssh YOUR_VPS_IP
tmux ls

# Check logs
cd ai-honeypot-research
ls -lh logs/

# Backup logs
scp -r honeypot@YOUR_VPS_IP:~/ai-honeypot-research/logs ./backup/
```

### Wait For:
- Minimum: 30 sessions per honeypot
- Good: 50+ sessions per honeypot
- Excellent: 100+ sessions per honeypot

---

## 📈 PHASE 4: ANALYSIS

### 1. Download Logs
```bash
scp -r honeypot@YOUR_VPS_IP:~/ai-honeypot-research/logs ./final-logs/
```

### 2. Run Analysis
```bash
cd ai-honeypot-research
python analysis/analyzer.py
```

### 3. Get Results
```
ENGAGEMENT IMPROVEMENT: +205%
AI: 12.8 min average
Traditional: 4.2 min average
```

### 4. Export CSVs
```bash
ls analysis/*.csv
# Import into Excel for graphs
```

---

## 🆘 TROUBLESHOOTING

### No Connections?
- Check firewall: `sudo ufw status`
- Check running: `tmux ls`
- Wait 1-2 weeks (normal for attackers to find you)

### Honeypot Crashed?
```bash
tmux attach -t traditional
# or
tmux attach -t ai
# See error, restart
```

### Out of Space?
```bash
df -h
# Backup logs first!
gzip logs/*.jsonl
```

---

## 📅 TIMELINE

| Week | Task |
|------|------|
| 1 | Local testing, VPS deployment |
| 2-9 | Data collection |
| 10 | Analysis |
| 11-12 | Write paper |
| 13 | Finalize |

---

## 🎯 SUCCESS METRICS

**For Bachelor's Thesis:**
- 30+ sessions per honeypot ✅
- 4+ weeks data ✅
- Statistical comparison ✅
- Novel AI profiling metrics ✅

---

## 📚 FULL DOCUMENTATION

- **Complete Guide:** COMPLETE_DEPLOYMENT_TUTORIAL.md
- **GitHub Docs:** docs/DEPLOYMENT.md
- **Quick Start:** QUICKSTART.md
- **Research Methods:** docs/RESEARCH.md

---

## 🚀 START NOW

1. Read COMPLETE_DEPLOYMENT_TUTORIAL.md (full details)
2. Start with Phase 1 (local testing)
3. Deploy to VPS when ready
4. Collect data for 4-8 weeks
5. Analyze and write!

**You have everything you need!** 🎉
