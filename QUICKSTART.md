# 🚀 QUICK START - Get Running in 5 Minutes

## Prerequisites
- Python 3.8+
- 8GB RAM recommended
- Linux/Mac (Windows WSL works too)

## Installation

```bash
# 1. Navigate to project
cd /home/claude/ai-honeypot

# 2. Run setup
./setup.sh

# If permission denied:
chmod +x setup.sh
./setup.sh
```

## Running the System

### Option A: Manual (Recommended for learning)

Open **3 separate terminals**:

```bash
# Terminal 1: AI Honeypot
python ai-honeypot/ai_honeypot.py

# Terminal 2: Traditional Honeypot  
python traditional-honeypot/traditional_honeypot.py

# Terminal 3: Traffic Generator (optional)
python traffic-gen/traffic_generator.py
```

### Option B: Docker (Set it and forget it)

```bash
docker-compose up -d
```

## Testing

```bash
# Open a 4th terminal and test the honeypots:
ssh user@localhost -p 2222   # AI honeypot (password: anything)
ssh user@localhost -p 2223   # Traditional honeypot (password: anything)

# Try commands:
ls
whoami
cat /etc/passwd
ps aux
```

## Run Attack Simulation

```bash
# This will test both honeypots with realistic attacks
python test_simulator.py
```

## Analyze Results

```bash
# After collecting some data, run:
python analysis/analyzer.py
```

You'll see output like:
```
ENGAGEMENT IMPROVEMENT: +197%
AI Honeypot: 12.5 minutes average
Traditional: 4.2 minutes average
```

## For Research Paper

1. **Collect data for 4-6 weeks**
2. **Run analyzer.py weekly**
3. **Export CSVs** from analysis/ directory
4. **Use the metrics** in your paper

## Need AI Responses?

### Option 1: Use Ollama (Free, Local)
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull model
ollama pull llama3.2:3b

# Run Ollama
ollama serve
```

### Option 2: Use OpenAI (Paid, Better Quality)
```bash
# Set your API key
export OPENAI_API_KEY="sk-your-key-here"
```

### Option 3: Fallback Mode (No AI)
- Just run without either - honeypot uses static responses
- Still collects all data for comparison

## Troubleshooting

**"Address already in use"**
```bash
# Find and kill the process
sudo lsof -ti:2222 | xargs kill -9
sudo lsof -ti:2223 | xargs kill -9
```

**"Can't connect to honeypot"**
```bash
# Check if running
ps aux | grep honeypot

# Test locally first before exposing to internet
```

**"No AI responses"**
- Check Ollama: `curl http://localhost:11434/api/tags`
- Check OpenAI: `echo $OPENAI_API_KEY`
- Fallback mode still works - just logs differently

## Project Timeline

| Week | Task |
|------|------|
| 1 | Setup + local testing |
| 2-8 | Internet exposure + data collection |
| 9-10 | Analysis + paper writing |

## Essential Commands

```bash
# View real-time logs
tail -f logs/*.log

# Stop everything
pkill -f honeypot
# or with Docker:
docker-compose down

# Analyze data
python analysis/analyzer.py

# Run tests
python test_simulator.py
```

## Next Steps

1. ✅ Get it running locally
2. ✅ Test with simulator
3. ✅ Verify data collection
4. ⏳ Expose to internet (carefully!)
5. ⏳ Collect data for 4-6 weeks
6. ⏳ Write research paper

## Full Documentation

See [README.md](README.md) for complete details.

---

**Ready?** Run `./setup.sh` now! 🚀
