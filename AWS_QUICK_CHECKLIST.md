# ⚡ AWS EC2 QUICK DEPLOYMENT CHECKLIST

##  Goal
Deploy both honeypots to AWS EC2 Free Tier (12 months free!)

---

##  PHASE 1: AWS ACCOUNT (10 minutes)

- [ ] Go to https://aws.amazon.com
- [ ] Create account (requires credit card, but won't charge in free tier)
- [ ] Verify phone number
- [ ] Choose Basic Support (Free)
- [ ] Sign in to console: https://console.aws.amazon.com

---

##  PHASE 2: LAUNCH EC2 (15 minutes)

### In AWS Console:
- [ ] Search for "EC2" → Click EC2
- [ ] Click "Launch Instance"
- [ ] Name: `honeypot-research`
- [ ] OS: **Ubuntu Server 22.04 LTS** (Free tier eligible)
- [ ] Instance type: **t2.micro** (Free tier eligible)
- [ ] Key pair: Create new → Name: `honeypot-research-key` → Download and save!
- [ ] Security group: Create new
  - [ ] SSH (22) - My IP only
  - [ ] Custom TCP (2222) - 0.0.0.0/0 (AI honeypot)
  - [ ] Custom TCP (2223) - 0.0.0.0/0 (Traditional honeypot)
- [ ] Storage: 20 GB
- [ ] Click "Launch instance"
- [ ] Wait 2 minutes
- [ ] Copy Public IPv4 address: `___.___.___.___`

---

## ✅ PHASE 3: CONNECT (5 minutes)

### Mac/Linux:
```bash
chmod 400 ~/Downloads/honeypot-research-key.pem
ssh -i ~/Downloads/honeypot-research-key.pem ubuntu@YOUR_EC2_IP
```

### Windows:
```powershell
ssh -i ~/Downloads/honeypot-research-key.pem ubuntu@YOUR_EC2_IP
```

- [ ] Type "yes" when prompted
- [ ] Connected! ✅

---

##  PHASE 4: SETUP (10 minutes)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install tools
sudo apt install python3 python3-pip python3-venv git tmux -y

# Clone your repo
git clone https://github.com/TheBearInternal/ai-honeypot-research.git
cd ai-honeypot-research

# Setup
chmod +x setup.sh
./setup.sh
source venv/bin/activate
```

- [ ] System updated
- [ ] Tools installed
- [ ] Repo cloned
- [ ] Setup complete ✅

---

##  PHASE 5: DEPLOY HONEYPOTS (10 minutes)

### Test Traditional:
```bash
python traditional-honeypot/traditional_honeypot.py
# Press Ctrl+C to stop
```

### Test AI:
```bash
# Optional: Set OpenAI key
export OPENAI_API_KEY="sk-..."

python ai-honeypot/ai_honeypot.py
# Press Ctrl+C to stop
```

### Run in Production:
```bash
# Traditional
tmux new -s traditional
python traditional-honeypot/traditional_honeypot.py
# Press Ctrl+B, then D

# AI
tmux new -s ai
export OPENAI_API_KEY="sk-..."  # if using OpenAI
python ai-honeypot/ai_honeypot.py
# Press Ctrl+B, then D

# Verify both running
tmux ls
```

- [ ] Traditional tested
- [ ] AI tested
- [ ] Both running in tmux ✅

---

##  PHASE 6: VERIFY FROM INTERNET (2 minutes)

### From your local computer:
```bash
# Test traditional
ssh user@YOUR_EC2_IP -p 2223
# Try: ls, pwd, exit

# Test AI
ssh user@YOUR_EC2_IP -p 2222
# Try: ls, cat passwords.txt, exit
```

- [ ] Traditional accessible ✅
- [ ] AI accessible ✅
- [ ] **Both honeypots live on internet!** 🎉

---

## 📊 ONGOING: MONITORING

### Daily (5 minutes):
```bash
ssh -i ~/.ssh/honeypot-research-key.pem ubuntu@YOUR_EC2_IP
tmux ls  # Check still running
cd ai-honeypot-research
tail logs/*.jsonl  # View recent activity
```

### Weekly (15 minutes):
```bash
# Backup logs (from your computer)
scp -i ~/.ssh/honeypot-research-key.pem \
  -r ubuntu@YOUR_EC2_IP:~/ai-honeypot-research/logs/ \
  ./backup-$(date +%Y%m%d)/

# Check AWS billing
# AWS Console → Billing → Free Tier usage
```

---

##  COST MONITORING

### Free Tier Limits:
- ✅ 750 hours/month t2.micro (24/7 for one instance)
- ✅ 30 GB storage
- ✅ 15 GB data transfer out

### Stay Safe:
- [ ] Set billing alarm: AWS → Billing → Billing Preferences → Alert ($5)
- [ ] Check free tier usage weekly
- [ ] Monitor in Billing Dashboard

---

## 🆘 TROUBLESHOOTING

### Can't connect via SSH?
```bash
chmod 400 ~/.ssh/honeypot-research-key.pem
# Check security group allows SSH from your IP
```

### Can't connect to honeypots?
```bash
# Check they're running
ssh -i ~/.ssh/honeypot-research-key.pem ubuntu@YOUR_EC2_IP
tmux ls

# Attach and check for errors
tmux attach -t traditional
```

### Honeypot crashed?
```bash
tmux kill-session -t traditional
tmux new -s traditional
cd ai-honeypot-research
source venv/bin/activate
python traditional-honeypot/traditional_honeypot.py
# Ctrl+B, D
```

---

## 📈 DATA COLLECTION TIMELINE

| Week | Expected Activity |
|------|-------------------|
| 1-2 | Few connections (discovery) |
| 3-4 | More activity (bots find you) |
| 5-8 | Steady attack stream |

**Goal:** 30-50+ sessions per honeypot

---

##  COMPLETE DEPLOYMENT CHECKLIST

- [ ] AWS account created
- [ ] EC2 instance running
- [ ] Security group configured
- [ ] Connected via SSH
- [ ] Repository deployed
- [ ] Traditional honeypot running
- [ ] AI honeypot running
- [ ] Accessible from internet
- [ ] Logs being generated
- [ ] Backup system setup
- [ ] Billing alerts configured

---

##  SUCCESS = ALL CHECKED! 

**Your honeypots are:**
- ✅ Running on AWS EC2 Free Tier
- ✅ Exposed to internet
- ✅ Collecting research data
- ✅ Cost: $0/month (free tier)

**Next:** Wait 4-8 weeks for data collection!

---

##  FULL DOCUMENTATION

For complete details, see:
- **AWS_EC2_DEPLOYMENT_GUIDE.md** - Full step-by-step
- **COMPLETE_DEPLOYMENT_TUTORIAL.md** - General deployment
- **Your GitHub:** https://github.com/TheBearInternal/ai-honeypot-research

---

##  START NOW!

1. Create AWS account
2. Follow checklist above
3. Deploy in ~50 minutes
4. Start collecting data!

**You've got this!** 🎉
