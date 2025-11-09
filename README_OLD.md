# AI-Enhanced Honeypot Research Project

**Dead Internet Theory Meets Deception Technology**

A bachelor's research project comparing traditional static honeypots with AI-enhanced adaptive honeypots that leverage "dead internet" concepts to create more engaging deception environments.

## 🎯 Research Objective

Determine if AI-powered honeypots can:
1. **Increase attacker engagement time** (primary hypothesis)
2. **Gather more diverse intelligence** about attack patterns
3. **Better simulate realistic production environments**
4. **Justify the computational overhead** compared to traditional honeypots

## 📊 System Architecture

```
┌─────────────────────────────────────────────────┐
│                                                 │
│  ┌──────────────────┐    ┌──────────────────┐ │
│  │   AI Honeypot    │    │    Traditional    │ │
│  │   (Port 2222)    │    │    (Port 2223)    │ │
│  │                  │    │                    │ │
│  │  • LLM-powered   │    │  • Static responses│ │
│  │  • Adaptive      │    │  • Predefined      │ │
│  │  • Context-aware │    │  • Fast            │ │
│  └──────────────────┘    └──────────────────┘ │
│           │                       │             │
│           └───────┬───────────────┘             │
│                   │                             │
│         ┌─────────▼─────────┐                  │
│         │  Traffic Generator │                  │
│         │  (Dead Internet)   │                  │
│         └────────────────────┘                  │
│                   │                             │
│         ┌─────────▼─────────┐                  │
│         │   Analysis Tool    │                  │
│         │  (Research Data)   │                  │
│         └────────────────────┘                  │
└─────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone/navigate to project
cd ai-honeypot

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Option 2: Local Python (For Development)

```bash
# Install dependencies
pip install -r requirements.txt

# Terminal 1: Start AI honeypot
python ai-honeypot/ai_honeypot.py

# Terminal 2: Start traditional honeypot
python traditional-honeypot/traditional_honeypot.py

# Terminal 3: Start traffic generator
python traffic-gen/traffic_generator.py

# Terminal 4: Run analysis (after collecting data)
python analysis/analyzer.py
```

## 🧪 Experiment Setup

### Phase 1: Controlled Testing (Week 1-2)

Test with known attack tools to establish baseline:

```bash
# Test AI honeypot
ssh user@localhost -p 2222
# Password: anything (all passwords accepted)

# Test traditional honeypot
ssh user@localhost -p 2223
# Password: anything

# Run common recon commands:
whoami
ls -la
cat /etc/passwd
ps aux
netstat -tulpn
```

### Phase 2: Internet Exposure (Week 3-8)

**⚠️ SECURITY WARNING**: Only expose honeypots on isolated network/VM!

```bash
# Open ports to internet (on router/firewall)
# Forward external:22 → internal:2222 (AI)
# Forward external:2222 → internal:2223 (Traditional)

# Monitor in real-time
tail -f logs/*.log

# Analyze weekly
python analysis/analyzer.py
```

### Phase 3: Data Collection Strategy

**Minimum viable dataset for research paper:**
- 30-50 real attack sessions per honeypot
- 4-6 weeks of exposure
- Or 100+ synthetic attack simulations

**Key metrics to track:**
1. Average session duration (minutes)
2. Commands per session
3. Unique commands attempted
4. Attack pattern distribution
5. Response time overhead

## 📈 Running Analysis

```bash
# Generate comprehensive report
python analysis/analyzer.py

# Export to CSV for Excel/R/Python analysis
# Check the analysis/ directory for:
# - commands.csv
# - auth_attempts.csv
```

### Expected Output

```
HONEYPOT EFFECTIVENESS ANALYSIS
================================

1. SESSION DURATION ANALYSIS
   AI Honeypot:
   - Average session duration: 12.5 minutes
   - Average commands per session: 23.4
   
   Traditional Honeypot:
   - Average session duration: 4.2 minutes
   - Average commands per session: 8.7
   
   ⭐ ENGAGEMENT IMPROVEMENT: +197.6%

2. COMMAND DIVERSITY ANALYSIS
   AI: 15.2 unique commands/session
   Traditional: 6.1 unique commands/session
```

## 🤖 AI Backend Options

### Option A: OpenAI API (Easiest)

```bash
# Set API key
export OPENAI_API_KEY="sk-..."

# AI honeypot will automatically use it
docker-compose up
```

**Pros**: Best quality, no local resources
**Cons**: Costs ~$0.002 per command (estimate $20-50 for full project)

### Option B: Ollama (Local, Free)

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull model
ollama pull llama3.2:3b

# Start Ollama server
ollama serve

# AI honeypot will detect and use it
docker-compose up
```

**Pros**: Free, private, unlimited
**Cons**: Requires 8GB+ RAM, slower

### Option C: Fallback Mode (No AI)

AI honeypot will automatically use static responses if no LLM is available. Still logs all interactions for comparison.

## 📝 Research Paper Structure

### Suggested Sections

1. **Introduction**
   - Problem: Static honeypots are easily detected
   - Solution: AI-powered adaptive responses
   - Hypothesis: AI increases engagement time

2. **Methodology**
   - System architecture
   - Controlled vs real-world testing
   - Metrics definition
   - Ethical considerations

3. **Results**
   - Quantitative comparison (use analyzer.py output)
   - Attack pattern analysis
   - Cost-benefit analysis
   - Statistical significance tests

4. **Discussion**
   - Why AI honeypots perform better/worse
   - Attacker behavior differences
   - Limitations of study
   - Future improvements

5. **Conclusion**
   - Key findings
   - Practical applications
   - Research contributions

### Key Statistics to Report

```python
# Use these from analyzer.py output:
- Average engagement time increase: X%
- Command diversity increase: X%
- Total sessions analyzed: N
- Attack pattern distribution
- False positive rate
- Computational overhead (CPU/memory)
```

## 🔐 Security Considerations

**NEVER run these honeypots on production systems!**

✅ **Safe deployment:**
- Isolated VM/VPS
- Separate network segment
- No connection to real infrastructure
- Monitor for malware uploads
- Regularly backup and wipe

❌ **Never:**
- Run on systems with real data
- Use real passwords/credentials
- Connect to internal networks
- Allow file uploads without sandboxing

## 📊 Data Collection Timeline

| Week | Activity | Target |
|------|----------|--------|
| 1-2 | Setup + controlled testing | Baseline data |
| 3-4 | Internet exposure begins | 10-15 sessions |
| 5-6 | Continue data collection | 20-30 sessions |
| 7-8 | Final data collection | 30-50 sessions |
| 9-10 | Analysis + paper writing | Results |

## 🎓 Research Ethics

This project follows responsible disclosure:
- Only defensive security research
- No exploitation of real systems
- Logged attacks reported to ISPs/authorities if severe
- Privacy: IP addresses anonymized in published results

## 🛠️ Troubleshooting

### Honeypots not receiving connections

```bash
# Check if ports are open
netstat -tulpn | grep -E '2222|2223'

# Test locally first
ssh user@localhost -p 2222

# Check firewall
sudo ufw allow 2222
sudo ufw allow 2223
```

### AI responses not working

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Check OpenAI key
echo $OPENAI_API_KEY

# View AI honeypot logs
docker logs ai-honeypot
```

### No attack traffic

Patience! Real attacks can take days/weeks. Meanwhile:
- Use attack simulators (Metasploit, Nmap)
- Post on cybersecurity forums (ask permission first)
- Ensure ports are actually exposed to internet

## 📦 Project Structure

```
ai-honeypot/
├── ai-honeypot/
│   └── ai_honeypot.py          # AI-enhanced honeypot
├── traditional-honeypot/
│   └── traditional_honeypot.py  # Baseline honeypot
├── traffic-gen/
│   └── traffic_generator.py     # Dead internet simulation
├── analysis/
│   └── analyzer.py              # Research data analysis
├── logs/
│   ├── commands.jsonl           # All commands logged
│   ├── auth.jsonl               # Auth attempts
│   └── *.log                    # System logs
├── configs/
│   └── ssh_host_key*            # Generated SSH keys
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## 🎯 Success Criteria

Your research is successful if you can demonstrate:

1. ✅ Both honeypots operational and logging data
2. ✅ Minimum 30 sessions per honeypot
3. ✅ Clear statistical comparison of engagement metrics
4. ✅ Analysis of attack patterns and behaviors
5. ✅ Discussion of AI advantages/disadvantages
6. ✅ Reproducible methodology

## 🚀 Next Steps

1. **Today**: Deploy and test locally
2. **This week**: Expose to internet, start collecting data
3. **Week 2-8**: Monitor and analyze weekly
4. **Week 9-10**: Final analysis and paper writing
5. **Submit**: Research paper with data and code

## 📚 Additional Resources

- [SANS Honeypot Guide](https://www.sans.org)
- [Modern Honey Network](https://github.com/pwnlandia/mhn)
- [Awesome Honeypots](https://github.com/paralax/awesome-honeypots)
- [AI in Cybersecurity Papers](https://scholar.google.com)

## 🤝 Contributing

This is a research project - feel free to:
- Extend the AI prompt engineering
- Add more traffic patterns
- Improve analysis metrics
- Add visualization tools

## 📄 License

MIT License - Use for research and education

---

**Built for:** Bachelor's Cybersecurity Research Project
**Purpose:** Exploring AI-enhanced deception technology
**Status:** Ready for deployment and data collection

Good luck with your research! 🎓🔬
