# 🚀 COMPLETE DEPLOYMENT TUTORIAL - AI Honeypot Research

## 📋 Overview

This tutorial will guide you through deploying **both honeypots** for your research:
1. **Traditional Honeypot** (baseline for comparison)
2. **AI-Enhanced Honeypot** (your novel contribution)

You'll run them simultaneously to collect comparative data for your bachelor's thesis.

---

## 🎯 DEPLOYMENT STRATEGY

### Phase 1: Local Testing (1-2 days)
✅ Test on your computer  
✅ Verify everything works  
✅ Get familiar with the system  

### Phase 2: VPS Deployment (Week 1)
✅ Deploy to cloud server  
✅ Expose to internet  
✅ Start data collection  

### Phase 3: Data Collection (4-8 weeks)
✅ Monitor daily  
✅ Collect 30+ sessions per honeypot  
✅ Ensure system stability  

### Phase 4: Analysis (Week 9+)
✅ Run analysis scripts  
✅ Generate graphs  
✅ Write research paper  

---

## 📦 PHASE 1: LOCAL TESTING (START HERE!)

### Prerequisites

**What you need:**
- ✅ Your GitHub repository cloned
- ✅ Python 3.8+ installed
- ✅ Terminal/PowerShell access
- ✅ 8GB RAM (recommended)

**Check Python version:**
```bash
python --version
# Should show: Python 3.8 or higher
```

If not installed:
- **Windows:** Download from python.org
- **Mac:** `brew install python3`
- **Linux:** `sudo apt-get install python3`

---

### Step 1: Clone Your Repository

```bash
# Clone your repo
git clone https://github.com/TheBearInternal/ai-honeypot-research.git

# Navigate into it
cd ai-honeypot-research

# Verify files are there
ls
# You should see: ai-honeypot/, traditional-honeypot/, etc.
```

---

### Step 2: Run Setup Script

**On Mac/Linux:**
```bash
# Make setup script executable
chmod +x setup.sh

# Run setup
./setup.sh
```

**On Windows (PowerShell):**
```powershell
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

**Expected output:**
```
✓ Virtual environment created
✓ Dependencies installed
✓ SSH keys generated
✓ Ready to run!
```

---

### Step 3: Test Traditional Honeypot First

**Open Terminal 1:**
```bash
# Activate virtual environment (if not already)
source venv/bin/activate  # Mac/Linux
# or
.\venv\Scripts\Activate.ps1  # Windows

# Run traditional honeypot
python traditional-honeypot/traditional_honeypot.py
```

**Expected output:**
```
[INFO] Traditional SSH Honeypot starting...
[INFO] Listening on 0.0.0.0:2223
[INFO] Press Ctrl+C to stop
```

✅ **If you see this, it's working!**

---

### Step 4: Test Connection to Traditional Honeypot

**Open Terminal 2 (keep Terminal 1 running):**
```bash
# Try to connect to it
ssh user@localhost -p 2223
# Password: anything (it will accept any password)
```

**What you should see:**
```
Welcome to Ubuntu 20.04.3 LTS
user@honeypot:~$ 
```

**Try commands:**
```bash
ls
pwd
whoami
cat /etc/passwd
exit
```

**Back in Terminal 1, you should see logs:**
```
[INFO] New connection from 127.0.0.1:xxxxx
[AUTH] Login attempt: user / password
[CMD] ls
[CMD] pwd
[CMD] whoami
[INFO] Connection closed
```

✅ **Traditional honeypot works!**

---

### Step 5: Test AI-Enhanced Honeypot

**Stop Terminal 1 (Ctrl+C)**

**Configure AI Backend (Choose One):**

#### Option A: OpenAI API (Best Quality)
```bash
# Set API key
export OPENAI_API_KEY="sk-your-key-here"

# Run AI honeypot
python ai-honeypot/ai_honeypot.py
```

#### Option B: Ollama (Free, Local)
```bash
# Install Ollama first
# Mac: brew install ollama
# Linux: curl -fsSL https://ollama.com/install.sh | sh
# Windows: Download from ollama.com

# Pull model
ollama pull llama3.2:3b

# Start Ollama server (Terminal 3)
ollama serve

# Run AI honeypot (Terminal 1)
python ai-honeypot/ai_honeypot.py
```

#### Option C: Fallback Mode (No AI needed)
```bash
# Just run without API key
python ai-honeypot/ai_honeypot.py
# Will use template-based responses
```

**Expected output:**
```
[INFO] AI-Enhanced SSH Honeypot starting...
[INFO] AI Backend: OpenAI GPT-4 (or Ollama/Fallback)
[INFO] Listening on 0.0.0.0:2222
[INFO] Press Ctrl+C to stop
```

---

### Step 6: Test Connection to AI Honeypot

**Open Terminal 2:**
```bash
# Connect to AI honeypot
ssh user@localhost -p 2222
# Password: anything
```

**Try commands:**
```bash
ls
cat passwords.txt
cat financial_data.xlsx
whoami
pwd
uname -a
exit
```

**Observe in Terminal 1:**
```
[INFO] New connection from 127.0.0.1
[PROFILE] Analyzing attacker behavior...
[PROFILE] Skill Level: intermediate
[PROFILE] Intent: data_theft
[AI] Generating realistic file content...
[CMD] ls
[CMD] cat passwords.txt
[AI] File accessed: passwords.txt (generated)
```

✅ **AI honeypot works!**

---

### Step 7: Run Both Simultaneously (For Testing)

**Terminal 1 - Traditional:**
```bash
python traditional-honeypot/traditional_honeypot.py
```

**Terminal 2 - AI:**
```bash
python ai-honeypot/ai_honeypot.py
```

**Terminal 3 - Test Traditional:**
```bash
ssh user@localhost -p 2223
```

**Terminal 4 - Test AI:**
```bash
ssh user@localhost -p 2222
```

✅ **Both running at the same time!**

---

### Step 8: Verify Logging

**Check logs folder:**
```bash
ls logs/

# You should see:
# traditional_honeypot_YYYYMMDD.jsonl
# ai_honeypot_YYYYMMDD.jsonl
```

**View logs:**
```bash
# Traditional logs
cat logs/traditional_honeypot_*.jsonl

# AI logs
cat logs/ai_honeypot_*.jsonl
```

**Each log entry looks like:**
```json
{"timestamp": "2024-11-10T12:34:56", "event": "connection", "ip": "127.0.0.1", ...}
{"timestamp": "2024-11-10T12:34:58", "event": "command", "command": "ls", ...}
```

✅ **Logging works!**

---

## ✅ PHASE 1 COMPLETE!

You've successfully:
- ✅ Set up both honeypots
- ✅ Tested them locally
- ✅ Verified logging
- ✅ Confirmed they run simultaneously

**You're ready for Phase 2: Real Deployment!**

---

## 🌐 PHASE 2: VPS DEPLOYMENT (Real Research Data)

### Why Deploy to VPS?

**Local testing:** Only you can connect (no real attackers)  
**VPS deployment:** Exposed to internet (real attack data!)

### VPS Provider Options

**Recommended for students:**

1. **DigitalOcean** ($6/month, $200 free credit for students)
   - Student: https://www.digitalocean.com/github-students
   - Easy setup
   - Good for honeypots

2. **Linode/Akamai** ($5/month, $100 free credit)
   - Reliable
   - Good support

3. **Vultr** ($5/month, frequent promotions)
   - Fast deployment
   - Good locations

4. **AWS/Google Cloud** (Free tier available)
   - More complex
   - Good if you're already familiar

**Recommended specs:**
- **RAM:** 2GB minimum (4GB better)
- **CPU:** 1-2 cores
- **Storage:** 25GB
- **OS:** Ubuntu 22.04 LTS
- **Location:** Your choice (affects which attackers you attract)

---

### Step 1: Create VPS

**Example: DigitalOcean**

1. Sign up at digitalocean.com
2. Apply student credit if available
3. Create new Droplet:
   ```
   Image: Ubuntu 22.04 LTS
   Plan: Basic ($6/month - 2GB RAM)
   Datacenter: Choose closest to you
   Authentication: SSH key (recommended) or Password
   ```
4. Click "Create Droplet"
5. Note your IP address: `123.45.67.89`

---

### Step 2: Connect to VPS

```bash
# Connect via SSH
ssh root@123.45.67.89

# You're now on your VPS!
```

---

### Step 3: Setup VPS Environment

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv git -y

# Install additional tools
sudo apt install htop tmux -y

# Create user for honeypots (security best practice)
sudo adduser honeypot
sudo usermod -aG sudo honeypot

# Switch to honeypot user
su - honeypot
```

---

### Step 4: Deploy Your Code

```bash
# Clone your repository
git clone https://github.com/TheBearInternal/ai-honeypot-research.git
cd ai-honeypot-research

# Run setup
chmod +x setup.sh
./setup.sh

# Activate virtual environment
source venv/bin/activate
```

---

### Step 5: Configure Firewall

```bash
# Allow SSH (your management access)
sudo ufw allow 22/tcp

# Allow honeypot ports
sudo ufw allow 2222/tcp  # AI honeypot
sudo ufw allow 2223/tcp  # Traditional honeypot

# Enable firewall
sudo ufw enable
sudo ufw status
```

**Output:**
```
Status: active
To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere
2222/tcp                   ALLOW       Anywhere
2223/tcp                   ALLOW       Anywhere
```

---

### Step 6: Run Honeypots on VPS (Production)

**Use tmux to keep them running after you disconnect:**

```bash
# Create tmux session for traditional
tmux new -s traditional

# Run traditional honeypot
python traditional-honeypot/traditional_honeypot.py

# Detach: Press Ctrl+B, then D
```

```bash
# Create tmux session for AI
tmux new -s ai

# Set API key (if using OpenAI)
export OPENAI_API_KEY="sk-your-key-here"

# Run AI honeypot
python ai-honeypot/ai_honeypot.py

# Detach: Press Ctrl+B, then D
```

**Verify both are running:**
```bash
tmux ls
# Should show: traditional and ai sessions
```

**To check on them:**
```bash
# Attach to traditional
tmux attach -t traditional

# Detach again: Ctrl+B, then D

# Attach to AI
tmux attach -t ai
```

---

### Step 7: Verify Internet Access

**From your local computer:**
```bash
# Test traditional honeypot
ssh user@123.45.67.89 -p 2223

# Test AI honeypot
ssh user@123.45.67.89 -p 2222
```

✅ **If you can connect, your honeypots are live on the internet!**

---

### Step 8: Monitoring

**Check logs:**
```bash
# SSH to VPS
ssh honeypot@123.45.67.89

cd ai-honeypot-research

# View recent logs
tail -f logs/traditional_honeypot_*.jsonl
tail -f logs/ai_honeypot_*.jsonl

# Count connections
grep "connection" logs/traditional_honeypot_*.jsonl | wc -l
grep "connection" logs/ai_honeypot_*.jsonl | wc -l
```

**Daily monitoring (recommended):**
```bash
# Check honeypots are still running
tmux ls

# Check logs for new activity
cd ai-honeypot-research
ls -lh logs/
```

---

### Step 9: Backup Logs Regularly

**Download logs to your computer (weekly):**
```bash
# From your local computer
scp -r honeypot@123.45.67.89:~/ai-honeypot-research/logs ./backup-YYYYMMDD/
```

---

## ✅ PHASE 2 COMPLETE!

Your honeypots are:
- ✅ Running on internet-accessible VPS
- ✅ Logging all activity
- ✅ Ready to collect research data
- ✅ Monitored daily

**Now wait 4-8 weeks for data collection!**

---

## 📊 PHASE 3: DATA COLLECTION (4-8 weeks)

### Weekly Checklist

**Every week:**
- [ ] SSH to VPS
- [ ] Check honeypots are running (`tmux ls`)
- [ ] Check log file sizes (`ls -lh logs/`)
- [ ] Download logs to backup
- [ ] Verify disk space (`df -h`)

**If honeypot crashed:**
```bash
# Check what happened
tmux attach -t traditional
# or
tmux attach -t ai

# Restart if needed
python traditional-honeypot/traditional_honeypot.py
# or
python ai-honeypot/ai_honeypot.py
```

### What You're Waiting For

**Minimum for thesis:**
- 30 sessions on traditional honeypot
- 30 sessions on AI honeypot

**Good research:**
- 50+ sessions each

**Excellent research:**
- 100+ sessions each

**Timeline:**
- Week 1-2: Few connections (honeypot discovery)
- Week 3-4: More activity (bots find you)
- Week 5-8: Steady stream of attacks

---

## 📈 PHASE 4: ANALYSIS

### Step 1: Download All Logs

```bash
# From your local computer
scp -r honeypot@123.45.67.89:~/ai-honeypot-research/logs ./final-logs/
```

---

### Step 2: Run Analysis

```bash
cd ai-honeypot-research

# Activate virtual environment
source venv/bin/activate

# Run analyzer
python analysis/analyzer.py
```

**Output:**
```
═══════════════════════════════════════
HONEYPOT COMPARISON ANALYSIS
═══════════════════════════════════════

Traditional Honeypot Statistics:
- Total Sessions: 45
- Average Duration: 4.2 minutes
- Commands Per Session: 6.3
- Unique Commands: 23

AI-Enhanced Honeypot Statistics:
- Total Sessions: 47
- Average Duration: 12.8 minutes
- Commands Per Session: 15.7
- Unique Commands: 48

═══════════════════════════════════════
KEY FINDINGS
═══════════════════════════════════════

ENGAGEMENT IMPROVEMENT: +205%
AI honeypot sessions lasted 205% longer on average

COMMAND DIVERSITY: +149%
AI honeypot attracted 149% more unique commands

Attacker Skill Levels (AI Honeypot):
- Novice: 42%
- Intermediate: 38%
- Advanced: 20%
```

---

### Step 3: Export for Paper

```bash
# CSV exports
ls analysis/*.csv

# Import into Excel/Google Sheets for graphs
```

---

### Step 4: Generate Graphs

Use the CSV data to create:
- Session duration comparison (bar chart)
- Commands per session (bar chart)
- Attack pattern distribution (pie chart)
- Timeline of attacks (line graph)

---

## 🎓 RESEARCH PAPER STRUCTURE

### Abstract
"This research compares traditional static SSH honeypots with AI-enhanced adaptive honeypots..."

### Introduction
- Honeypot background
- Dead Internet Theory connection
- Research question

### Methodology
- Experimental setup (2 honeypots, VPS deployment)
- Data collection period
- Metrics measured

### Results
- Session duration comparison
- Command diversity analysis
- Attacker profiling (AI-only)
- Statistical significance tests

### Discussion
- Why AI performed better
- Implications for cybersecurity
- Limitations

### Conclusion
- AI honeypots significantly outperform traditional
- Novel contribution: automated attacker profiling
- Future work

---

## 🔧 TROUBLESHOOTING

### Honeypot Not Receiving Connections

**Possible causes:**
1. Firewall blocking ports
   ```bash
   sudo ufw status
   sudo ufw allow 2222/tcp
   sudo ufw allow 2223/tcp
   ```

2. Honeypot not running
   ```bash
   tmux ls
   tmux attach -t traditional
   ```

3. Port already in use
   ```bash
   sudo netstat -tulpn | grep 2222
   sudo netstat -tulpn | grep 2223
   ```

4. Takes time for attackers to find you (normal - wait 1-2 weeks)

---

### AI Honeypot Errors

**"OpenAI API error"**
- Check API key is set: `echo $OPENAI_API_KEY`
- Check API credits: https://platform.openai.com/usage
- Fallback mode will activate automatically

**"Ollama connection failed"**
- Check Ollama is running: `ps aux | grep ollama`
- Start Ollama: `ollama serve`

---

### VPS Running Out of Space

```bash
# Check space
df -h

# Clean up old logs (after backing up!)
cd ai-honeypot-research/logs
# Compress old logs
gzip *_202411*.jsonl

# Download to your computer
# Then delete from VPS
```

---

### Honeypot Crashed

**Check logs:**
```bash
cd ai-honeypot-research
tmux attach -t traditional
# Look for error messages

# Restart
python traditional-honeypot/traditional_honeypot.py
```

---

## 📋 QUICK REFERENCE COMMANDS

### Daily Monitoring
```bash
# SSH to VPS
ssh honeypot@YOUR_VPS_IP

# Check honeypots running
tmux ls

# View logs
cd ai-honeypot-research
tail logs/traditional_honeypot_*.jsonl
tail logs/ai_honeypot_*.jsonl

# Count sessions
grep "connection" logs/*.jsonl | wc -l
```

### Weekly Backup
```bash
# From local computer
scp -r honeypot@YOUR_VPS_IP:~/ai-honeypot-research/logs ./backup-$(date +%Y%m%d)/
```

### Restart Honeypots
```bash
# Kill all
tmux kill-server

# Start traditional
tmux new -s traditional
python traditional-honeypot/traditional_honeypot.py
# Ctrl+B, D to detach

# Start AI
tmux new -s ai
export OPENAI_API_KEY="sk-..."
python ai-honeypot/ai_honeypot.py
# Ctrl+B, D to detach
```

---

## 🎯 TIMELINE SUMMARY

**Week 1:** Local testing, VPS setup, deployment  
**Weeks 2-9:** Data collection (monitor weekly)  
**Week 10:** Analysis and graph generation  
**Weeks 11-12:** Write research paper  
**Week 13:** Final revisions and submission  

---

## ✅ SUCCESS CRITERIA

**Minimum viable thesis:**
- ✅ 30 sessions per honeypot
- ✅ 4 weeks of data
- ✅ Statistical comparison showing difference
- ✅ Basic analysis

**Strong thesis:**
- ✅ 50+ sessions per honeypot
- ✅ 6-8 weeks of data
- ✅ Multiple statistical tests
- ✅ Novel attacker profiling metrics

**Excellent thesis:**
- ✅ 100+ sessions per honeypot
- ✅ 8+ weeks of data
- ✅ Publication-quality analysis
- ✅ Comprehensive attacker taxonomy

---

## 🆘 GETTING HELP

**If stuck:**
1. Check GitHub documentation
2. Review logs for errors
3. Check tmux sessions are running
4. Verify firewall rules
5. Test connection from outside VPS

**Documentation locations:**
- Full deployment: `docs/DEPLOYMENT.md`
- Feature comparison: `docs/COMPARISON.md`
- Research methodology: `docs/RESEARCH.md`

---

## 🎉 YOU'RE READY!

Follow this tutorial step-by-step and you'll have a complete research project!

**Next step:** Start with Phase 1 (Local Testing)

**Questions?** Check the docs in your GitHub repo or review this tutorial again.

**Good luck with your research!** 🚀
