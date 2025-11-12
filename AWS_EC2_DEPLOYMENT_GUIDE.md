# 🚀 AWS EC2 DEPLOYMENT GUIDE - AI Honeypot Research

## 📋 Overview

This guide walks you through deploying **both honeypots** to AWS EC2 Free Tier for your bachelor's research project.

**AWS Free Tier includes:**
- ✅ 750 hours/month of t2.micro instance (12 months free)
- ✅ Enough for 24/7 operation
- ✅ Perfect for research projects
- ✅ No cost if you stay within limits

---

## 💰 COST BREAKDOWN

### Free Tier (First 12 Months)
- **Compute:** 750 hours/month t2.micro (1 vCPU, 1GB RAM) - FREE
- **Storage:** 30GB SSD - FREE
- **Data Transfer:** 15GB outbound - FREE

### After Free Tier
- **t2.micro:** ~$8-10/month
- **Storage:** ~$3/month
- **Total:** ~$11-13/month

**For your research:** Definitely use the **FREE** 12 months!

---

## 🎯 PHASE 1: AWS ACCOUNT SETUP

### Step 1: Create AWS Account

1. **Go to:** https://aws.amazon.com
2. **Click:** "Create an AWS Account"
3. **Fill in:**
   - Email address
   - Password
   - AWS account name: `honeypot-research` or your name
4. **Contact Information:**
   - Select: Personal account
   - Fill in your details
5. **Payment Information:**
   - Add credit/debit card (required, but won't be charged in free tier)
   - AWS charges $1 temporarily to verify (refunded)
6. **Identity Verification:**
   - Phone number verification
   - Enter code sent to your phone
7. **Select Support Plan:**
   - Choose: **Basic Support - Free**
8. **Complete!**

**⏱️ Time:** 10 minutes

---

### Step 2: Sign in to AWS Console

1. Go to: https://console.aws.amazon.com
2. Sign in with your email and password
3. You'll see the AWS Management Console

---

### Step 3: Check Free Tier Status

1. In AWS Console, search for "Billing"
2. Click "Billing Dashboard"
3. Look for "Free Tier" section
4. Should show: "You are currently in the Free Tier"

---

## 🖥️ PHASE 2: EC2 INSTANCE CREATION

### Step 1: Navigate to EC2

1. In AWS Console search bar, type: **EC2**
2. Click "EC2" (Virtual Servers in the Cloud)
3. You're now in the EC2 Dashboard

---

### Step 2: Launch Instance

1. **Click:** "Launch Instance" (orange button)

2. **Name your instance:**
   ```
   Name: honeypot-research
   ```

3. **Application and OS Images (AMI):**
   - Select: **Ubuntu**
   - Choose: **Ubuntu Server 22.04 LTS**
   - Architecture: **64-bit (x86)**
   - Make sure it says: **Free tier eligible** ✅

4. **Instance Type:**
   - Select: **t2.micro** (Free tier eligible)
   - 1 vCPU, 1 GB RAM
   - Should show: **Free tier eligible** ✅

5. **Key pair (login):**
   - Click: "Create new key pair"
   - **Key pair name:** `honeypot-research-key`
   - **Key pair type:** RSA
   - **Private key file format:** 
     - Windows: `.ppk` (for PuTTY)
     - Mac/Linux: `.pem`
   - Click "Create key pair"
   - **IMPORTANT:** Save this file! You need it to connect!
   - Save location: `~/Downloads/honeypot-research-key.pem`

6. **Network Settings:**
   - Click "Edit" (top right of Network settings)
   
   **VPC:** Default (leave as is)
   
   **Subnet:** No preference (leave as is)
   
   **Auto-assign public IP:** Enable ✅
   
   **Firewall (Security Groups):**
   - Select: "Create security group"
   - **Security group name:** `honeypot-research-sg`
   - **Description:** `Security group for honeypot research project`
   
   **Inbound Security Group Rules:**
   
   Click "Add security group rule" for each:
   
   | Type | Protocol | Port Range | Source | Description |
   |------|----------|------------|--------|-------------|
   | SSH | TCP | 22 | My IP | Your management access |
   | Custom TCP | TCP | 2222 | 0.0.0.0/0 | AI Honeypot |
   | Custom TCP | TCP | 2223 | 0.0.0.0/0 | Traditional Honeypot |
   
   **CRITICAL:** For the SSH rule (port 22), select "My IP" to restrict access to only your computer. For ports 2222 and 2223, select "Anywhere (0.0.0.0/0)" so attackers can reach your honeypots.

7. **Configure Storage:**
   - **Size:** 20 GB (default is 8GB, increase for logs)
   - **Volume Type:** gp3 (default)
   - **Free tier:** Up to 30GB is free ✅
   - Leave other settings as default

8. **Advanced Details:**
   - Leave all as default (can skip this section)

9. **Summary:**
   - **Number of instances:** 1
   - Review your settings

10. **Launch!**
    - Click: "Launch instance" (orange button)
    - Wait ~2 minutes for instance to start

---

### Step 3: Get Your Instance IP Address

1. **Go to:** EC2 Dashboard → Instances
2. **Click** on your instance: `honeypot-research`
3. **Find:** "Public IPv4 address"
4. **Example:** `3.81.45.122`
5. **Copy this IP** - you'll need it!

**Note this down:**
```
Your EC2 IP: 3.81.45.122
```

---

## 🔌 PHASE 3: CONNECT TO YOUR EC2 INSTANCE

### For Mac/Linux Users

**Step 1: Set permissions on key file**
```bash
chmod 400 ~/Downloads/honeypot-research-key.pem
```

**Step 2: Connect via SSH**
```bash
ssh -i ~/Downloads/honeypot-research-key.pem ubuntu@YOUR_EC2_IP

# Example:
# ssh -i ~/Downloads/honeypot-research-key.pem ubuntu@3.81.45.122
```

**Step 3: Type "yes" when prompted**
```
Are you sure you want to continue connecting? yes
```

✅ **Connected to EC2!**

---

### For Windows Users

**Option A: Using PowerShell (Recommended)**

```powershell
# Navigate to where you saved the key
cd ~\Downloads

# Connect
ssh -i honeypot-research-key.pem ubuntu@YOUR_EC2_IP
```

**Option B: Using PuTTY**

1. Open PuTTY
2. **Host Name:** `ubuntu@YOUR_EC2_IP`
3. **Port:** 22
4. **Connection → SSH → Auth:** Browse and select your `.ppk` file
5. Click "Open"

---

## 📦 PHASE 4: SETUP EC2 ENVIRONMENT

### Step 1: Update System

```bash
# Update package lists
sudo apt update

# Upgrade packages
sudo apt upgrade -y
```

**⏱️ Time:** 2-3 minutes

---

### Step 2: Install Required Software

```bash
# Install Python and tools
sudo apt install python3 python3-pip python3-venv git tmux htop -y

# Verify installations
python3 --version  # Should show 3.10+
git --version
tmux -V
```

---

### Step 3: Clone Your Repository

```bash
# Clone your project
git clone https://github.com/TheBearInternal/ai-honeypot-research.git

# Navigate into it
cd ai-honeypot-research

# Verify files
ls -la
```

You should see:
```
ai-honeypot/
traditional-honeypot/
traffic-gen/
analysis/
docs/
README.md
setup.sh
requirements.txt
```

---

### Step 4: Run Setup Script

```bash
# Make setup script executable
chmod +x setup.sh

# Run setup
./setup.sh

# Activate virtual environment
source venv/bin/activate

# Your prompt should now show: (venv)
```

**Expected output:**
```
✓ Virtual environment created
✓ Dependencies installed
✓ SSH keys generated
✓ Setup complete!
```

---

## 🚀 PHASE 5: DEPLOY HONEYPOTS

### Step 1: Test Traditional Honeypot

```bash
# Run traditional honeypot
python traditional-honeypot/traditional_honeypot.py
```

**Expected output:**
```
[INFO] Traditional SSH Honeypot starting...
[INFO] Listening on 0.0.0.0:2223
[INFO] Press Ctrl+C to stop
```

**Press Ctrl+C to stop (we'll run it in tmux next)**

---

### Step 2: Test from Your Computer

**Open new terminal on your local computer:**

```bash
# Try to connect to traditional honeypot
ssh user@YOUR_EC2_IP -p 2223
# Password: anything (it will accept anything)
```

**Try commands:**
```bash
ls
pwd
whoami
exit
```

✅ **Traditional honeypot accessible from internet!**

---

### Step 3: Configure AI Backend (Choose One)

#### Option A: OpenAI API (Recommended for Quality)

```bash
# Set your API key (get from: https://platform.openai.com/api-keys)
export OPENAI_API_KEY="sk-your-api-key-here"

# Test AI honeypot
python ai-honeypot/ai_honeypot.py
```

**Stop with Ctrl+C**

#### Option B: Ollama (Free, Local)

**Install Ollama:**
```bash
# Install
curl -fsSL https://ollama.com/install.sh | sh

# Pull model
ollama pull llama3.2:3b

# Start Ollama server (in background)
nohup ollama serve > ollama.log 2>&1 &

# Test AI honeypot
python ai-honeypot/ai_honeypot.py
```

**Stop with Ctrl+C**

#### Option C: Fallback Mode (No AI needed)

```bash
# Just run without API key
python ai-honeypot/ai_honeypot.py
# Will use template-based responses
```

---

### Step 4: Run Both Honeypots in Production (tmux)

**Traditional Honeypot:**
```bash
# Create tmux session
tmux new -s traditional

# Run honeypot
python traditional-honeypot/traditional_honeypot.py

# Detach from tmux: Press Ctrl+B, then D
```

**AI-Enhanced Honeypot:**
```bash
# Create tmux session
tmux new -s ai

# Set API key if using OpenAI
export OPENAI_API_KEY="sk-your-key-here"

# Run honeypot
python ai-honeypot/ai_honeypot.py

# Detach from tmux: Press Ctrl+B, then D
```

**Verify both are running:**
```bash
tmux ls
```

**Expected output:**
```
ai: 1 windows (created Sat Nov 9 10:23:45 2024)
traditional: 1 windows (created Sat Nov 9 10:22:12 2024)
```

✅ **Both honeypots running in background!**

---

### Step 5: Test Both from Internet

**From your local computer:**

```bash
# Test traditional
ssh user@YOUR_EC2_IP -p 2223

# Test AI
ssh user@YOUR_EC2_IP -p 2222
```

✅ **Both accessible from internet!**

---

## 📊 PHASE 6: MONITORING AND LOGGING

### Check Honeypots Are Running

```bash
# SSH to your EC2
ssh -i ~/Downloads/honeypot-research-key.pem ubuntu@YOUR_EC2_IP

# List tmux sessions
tmux ls

# Attach to traditional
tmux attach -t traditional
# View logs in real-time
# Detach: Ctrl+B, then D

# Attach to AI
tmux attach -t ai
# View logs in real-time
# Detach: Ctrl+B, then D
```

---

### Check Log Files

```bash
cd ~/ai-honeypot-research

# List log files
ls -lh logs/

# View recent logs
tail -f logs/traditional_honeypot_*.jsonl
tail -f logs/ai_honeypot_*.jsonl

# Count connections
grep "connection" logs/traditional_honeypot_*.jsonl | wc -l
grep "connection" logs/ai_honeypot_*.jsonl | wc -l
```

---

### Monitor System Resources

```bash
# Check CPU and memory
htop

# Check disk space
df -h

# Check network connections
sudo netstat -tulpn | grep -E "2222|2223"
```

---

### Download Logs to Your Computer

**From your local computer:**

```bash
# Create backup folder
mkdir -p ~/honeypot-backups/$(date +%Y%m%d)

# Download logs
scp -i ~/Downloads/honeypot-research-key.pem \
  -r ubuntu@YOUR_EC2_IP:~/ai-honeypot-research/logs/ \
  ~/honeypot-backups/$(date +%Y%m%d)/
```

**Do this weekly!**

---

## 🔒 PHASE 7: SECURITY BEST PRACTICES

### 1. Restrict SSH Access to Your IP Only

**Update security group:**

1. Go to EC2 Dashboard
2. Security Groups
3. Select: `honeypot-research-sg`
4. Edit inbound rules
5. SSH (port 22) → Change source to "My IP"
6. Save rules

**Why:** Prevents others from accessing your management SSH

---

### 2. Keep Your Key Safe

```bash
# Store in secure location
mkdir -p ~/.ssh
mv ~/Downloads/honeypot-research-key.pem ~/.ssh/
chmod 400 ~/.ssh/honeypot-research-key.pem
```

**Never commit keys to GitHub!**

---

### 3. Monitor AWS Billing

1. Go to AWS Billing Dashboard
2. Enable billing alerts
3. Set alert for $5 (just in case)
4. Check weekly

---

### 4. Regular Backups

```bash
# Weekly backup script
cat > backup-logs.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d)
mkdir -p ~/backups/$DATE
scp -i ~/.ssh/honeypot-research-key.pem \
  -r ubuntu@YOUR_EC2_IP:~/ai-honeypot-research/logs/ \
  ~/backups/$DATE/
echo "Backup complete: $DATE"
EOF

chmod +x backup-logs.sh

# Run weekly
./backup-logs.sh
```

---

## 🔄 PHASE 8: MAINTENANCE

### Daily Check (5 minutes)

```bash
# Connect to EC2
ssh -i ~/.ssh/honeypot-research-key.pem ubuntu@YOUR_EC2_IP

# Check honeypots running
tmux ls

# Check new logs
cd ai-honeypot-research
tail logs/traditional_honeypot_*.jsonl
tail logs/ai_honeypot_*.jsonl

# Count sessions today
grep $(date +%Y-%m-%d) logs/*.jsonl | grep "connection" | wc -l
```

---

### Weekly Tasks (15 minutes)

1. **Backup logs** (use script above)
2. **Check disk space:** `df -h`
3. **Check system updates:** `sudo apt update && sudo apt upgrade -y`
4. **Verify AWS billing:** Check you're still in free tier
5. **Count total sessions** collected

---

### If Honeypot Crashed

```bash
# Check what happened
tmux attach -t traditional
# or
tmux attach -t ai

# Look for errors
# Then restart

# For traditional:
tmux kill-session -t traditional
tmux new -s traditional
cd ai-honeypot-research
source venv/bin/activate
python traditional-honeypot/traditional_honeypot.py
# Ctrl+B, then D

# For AI:
tmux kill-session -t ai
tmux new -s ai
cd ai-honeypot-research
source venv/bin/activate
export OPENAI_API_KEY="sk-..."
python ai-honeypot/ai_honeypot.py
# Ctrl+B, then D
```

---

## 📈 PHASE 9: DATA COLLECTION & ANALYSIS

### Collecting Data (4-8 weeks)

**Minimum for thesis:**
- 30 sessions per honeypot
- 4 weeks of data

**Good research:**
- 50+ sessions per honeypot
- 6-8 weeks of data

**Timeline:**
- Week 1-2: Few connections (discovery phase)
- Week 3-4: More activity (bots finding you)
- Week 5-8: Steady attack stream

---

### Running Analysis

**After data collection:**

```bash
# Download all logs
scp -i ~/.ssh/honeypot-research-key.pem \
  -r ubuntu@YOUR_EC2_IP:~/ai-honeypot-research/logs/ \
  ./final-logs/

# On your local computer
cd ai-honeypot-research
source venv/bin/activate
python analysis/analyzer.py
```

**Results:**
```
═══════════════════════════════════════
ENGAGEMENT IMPROVEMENT: +205%
AI: 12.8 min average
Traditional: 4.2 min average

COMMAND DIVERSITY: +149%
AI: 48 unique commands
Traditional: 23 unique commands

Attacker Skill Levels:
- Novice: 42%
- Intermediate: 38%
- Advanced: 20%
═══════════════════════════════════════
```

---

## 💰 PHASE 10: COST MANAGEMENT

### Monitor Free Tier Usage

1. **AWS Console** → **Billing Dashboard**
2. **Free Tier** section shows usage
3. Monitor:
   - EC2 hours: Should stay under 750/month
   - Data transfer: Should stay under 15GB/month
   - Storage: Should stay under 30GB

---

### After Research Completes

**Option 1: Keep Running (if still in free tier)**
- Continue collecting data
- Use for future projects

**Option 2: Stop Instance (save money after free tier)**
```bash
# In AWS Console
EC2 → Instances → Select instance → Instance State → Stop
```

**Option 3: Terminate Instance (delete everything)**
```bash
# Backup logs first!
# Then: EC2 → Instances → Select → Instance State → Terminate
```

⚠️ **Always backup logs before stopping/terminating!**

---

## 🎓 USING FOR RESEARCH PAPER

### Code Availability Section

```
The honeypot systems were deployed on Amazon Web Services (AWS) 
EC2 infrastructure using Ubuntu 22.04 LTS. The deployment used 
a t2.micro instance within AWS Free Tier limits. Both honeypots 
were configured to listen on separate ports (2222 for AI-enhanced, 
2223 for traditional) and exposed to internet traffic for the 
duration of the study.

Complete source code, deployment scripts, and documentation 
are available at: https://github.com/TheBearInternal/ai-honeypot-research
```

---

## 🆘 TROUBLESHOOTING

### Can't Connect to EC2 via SSH

**Problem:** `Permission denied (publickey)`

**Solution:**
```bash
# Check key permissions
chmod 400 ~/.ssh/honeypot-research-key.pem

# Verify using correct key
ssh -i ~/.ssh/honeypot-research-key.pem ubuntu@YOUR_EC2_IP

# Check security group allows SSH from your IP
```

---

### Can't Connect to Honeypots (Port 2222/2223)

**Problem:** Connection timeout

**Solutions:**
1. Check security group allows ports 2222 and 2223 from 0.0.0.0/0
2. Verify honeypots are running: `tmux ls`
3. Check firewall on EC2: `sudo ufw status` (should be inactive)
4. Test locally first: `ssh user@localhost -p 2222`

---

### EC2 Instance Running Out of Space

**Problem:** Disk full

**Solution:**
```bash
# Check space
df -h

# Find large files
du -h --max-depth=1 /home/ubuntu | sort -hr

# Compress old logs
cd ~/ai-honeypot-research/logs
gzip *_2024*.jsonl

# Backup and delete old logs
# After backing up to your computer!
```

---

### AWS Billing Concerns

**Problem:** Worried about costs

**Solution:**
1. Check Free Tier dashboard daily first week
2. Set billing alarm for $1-5
3. Monitor usage in Billing → Bills
4. If approaching limits, stop instance
5. Most students never exceed free tier limits

---

### Honeypot Performance Issues

**Problem:** Slow or unresponsive

**Solution:**
```bash
# Check system resources
htop

# If AI honeypot is slow with Ollama:
# Use smaller model
ollama pull llama3.2:1b

# Or switch to fallback mode
# (remove OPENAI_API_KEY, restart honeypot)

# If memory issues:
# t2.micro has 1GB RAM
# AI with Ollama may be tight
# Consider OpenAI API instead (uses their servers)
```

---

## 📋 QUICK REFERENCE

### Essential Commands

**Connect to EC2:**
```bash
ssh -i ~/.ssh/honeypot-research-key.pem ubuntu@YOUR_EC2_IP
```

**Check honeypots:**
```bash
tmux ls
tmux attach -t traditional
tmux attach -t ai
```

**View logs:**
```bash
cd ~/ai-honeypot-research
tail -f logs/traditional_honeypot_*.jsonl
tail -f logs/ai_honeypot_*.jsonl
```

**Backup logs:**
```bash
scp -i ~/.ssh/honeypot-research-key.pem \
  -r ubuntu@YOUR_EC2_IP:~/ai-honeypot-research/logs/ \
  ./backup-$(date +%Y%m%d)/
```

**Restart honeypot:**
```bash
tmux kill-session -t traditional
tmux new -s traditional
cd ai-honeypot-research && source venv/bin/activate
python traditional-honeypot/traditional_honeypot.py
# Ctrl+B, D
```

---

## ✅ SUCCESS CHECKLIST

**Setup Complete When:**
- [ ] AWS account created
- [ ] EC2 instance launched (t2.micro)
- [ ] Security group configured (ports 22, 2222, 2223)
- [ ] Connected via SSH
- [ ] Repository cloned
- [ ] Dependencies installed
- [ ] Both honeypots tested locally
- [ ] Both honeypots running in tmux
- [ ] Accessible from internet
- [ ] Logs being generated
- [ ] Weekly backup system in place

---

## 🎯 TIMELINE

| Phase | Task | Time |
|-------|------|------|
| Day 1 | AWS account setup | 30 min |
| Day 1 | EC2 instance creation | 30 min |
| Day 1 | Environment setup | 20 min |
| Day 1 | Deploy honeypots | 30 min |
| Day 1 | Testing | 30 min |
| Week 1-8 | Data collection | 5 min/day |
| Week 9 | Analysis | 2 hours |
| Week 10-12 | Write paper | - |

---

## 💡 AWS-SPECIFIC TIPS

### 1. Use AWS Educate or Student Credits

- **AWS Educate:** $100 free credits for students
- **GitHub Student Pack:** Often includes AWS credits
- **Apply:** https://aws.amazon.com/education/awseducate/

### 2. Set Up CloudWatch Alarms

Monitor your honeypots:
1. CloudWatch → Alarms
2. Create alarm for CPU > 90%
3. Get email if something wrong

### 3. Elastic IP (Optional)

Keep same IP even after stopping instance:
1. EC2 → Elastic IPs → Allocate
2. Associate with your instance
3. **Note:** Charged if not associated with running instance

### 4. Snapshots (Backups)

Backup entire instance:
1. EC2 → Snapshots → Create Snapshot
2. Select your instance volume
3. Create before major changes

---

## 🎉 YOU'RE READY FOR AWS!

**You now have:**
- ✅ Complete AWS EC2 setup guide
- ✅ Step-by-step deployment instructions
- ✅ Security best practices
- ✅ Monitoring and maintenance procedures
- ✅ Troubleshooting solutions
- ✅ Cost management strategies

**Next Steps:**
1. Create AWS account
2. Follow Phase 1-5 to deploy
3. Start collecting research data!

**Questions?** Review the relevant phase or check the troubleshooting section.

**Good luck with your AWS deployment!** 🚀

---

## 📞 ADDITIONAL RESOURCES

- **AWS Free Tier:** https://aws.amazon.com/free/
- **EC2 Documentation:** https://docs.aws.amazon.com/ec2/
- **AWS Education:** https://aws.amazon.com/education/
- **Your GitHub Repo:** https://github.com/TheBearInternal/ai-honeypot-research

---

**Last Updated:** November 2024  
**For:** Bachelor's Research Project - AI-Enhanced Honeypots  
**AWS Free Tier:** 12 months free, perfect for research!
