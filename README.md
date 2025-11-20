# BugCon 2025 - Security Demonstrations

> **Professional security demonstrations for conference presentations and training**

## 🎯 Overview

This repository contains security demonstrations and presentation materials for BugCon 2025. Each demo is self-contained with both offensive (red team) and defensive (blue team) perspectives.

**Target Audience:** Security researchers, penetration testers, SOC analysts, IT defenders, and conference attendees

---

## 📁 Repository Structure

```
bugcon2025/
├── slides/                              # Presentation materials
│   ├── index.html                       # Main presentation with speaker notes
│   ├── serve_slides.py                  # Local presentation server
│   └── README.md                        # Slides documentation
│
└── demos/                               # Security demonstrations
    └── chrome-debugging-exploit/        # Chrome remote debugging attack & detection
        ├── README.md                    # Demo-specific documentation
        ├── requirements.txt             # Python dependencies
        ├── red-team/                    # Offensive tools
        ├── blue-team/                   # Defensive tools
        ├── docs/                        # Detailed documentation
        └── output/                      # Generated artifacts
```

---

## 🎬 Available Demos

### 1. Chrome Remote Debugging Exploitation

**Path:** `demos/chrome-debugging-exploit/`

**Description:** Demonstrates session hijacking via Chrome's debugging protocol, including cookie theft, screenshot capture, and JavaScript injection - plus comprehensive detection methods.

**Key Features:**
- 🔴 **Red Team:** Exploit Chrome debugging to steal sessions
- 🔵 **Blue Team:** Detect and respond to the attack
- ⏱️ **Demo Time:** 3-4 minutes
- 🎯 **Impact:** Critical

**Quick Start:**
```bash
cd demos/chrome-debugging-exploit
pip install -r requirements.txt

# Red Team (Attack)
cd red-team
start_chrome_debug.bat
python chrome_hijack_basic.py

# Blue Team (Detection)
cd ../blue-team
python chrome_debug_detector.py
```

**Full Documentation:** See `demos/chrome-debugging-exploit/README.md`

---

## 🎤 Presentation Materials

### Slides
**Path:** `slides/`

Main presentation built with [reveal.js](https://revealjs.com/) including:
- Technical deep dives
- Live demo integration points
- Speaker notes
- Q&A preparation

**View Slides:**
```bash
cd slides
python serve_slides.py
# Navigate to http://localhost:8000
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- Google Chrome
- Git (for cloning)

### Installation

```bash
# Clone the repository
git clone https://github.com/benibits/bugcon2025.git
cd bugcon2025

# Install demo dependencies
cd demos/chrome-debugging-exploit
pip install -r requirements.txt
```

### Running a Demo

1. Navigate to the specific demo directory
2. Follow the demo's README.md
3. Run red team tools to demonstrate attack
4. Run blue team tools to show detection
5. Reference slides for technical explanation

---

## 🎯 Demo Philosophy

Each demo follows these principles:

✅ **Dual Perspective** - Shows both attack and defense  
✅ **Self-Contained** - All dependencies and docs included  
✅ **Reproducible** - Clear setup with consistent results  
✅ **Educational** - Focuses on learning and awareness  
✅ **Practical** - Real-world attack scenarios  
✅ **Ethical** - Includes legal notices and responsible use guidelines

---

## 📚 Documentation

### By Demo
Each demo has comprehensive documentation:
- **README.md** - Quick start and overview
- **QUICKSTART.md** - 5-minute setup guide  
- **Detailed guides** - Attack and defense strategies

### General Resources
- **This README** - Repository overview
- **slides/** - Presentation materials
- **.gitignore** - Excludes presenter support files

---

## 🛡️ Security & Legal

### Responsible Use

**These demonstrations are for authorized testing and education ONLY.**

✅ **Permitted Uses:**
- Security conferences and presentations
- Authorized red team exercises
- Security training programs
- Personal learning in test environments
- Academic research

❌ **Prohibited Uses:**
- Unauthorized access to systems
- Malicious activities
- Violation of computer fraud laws
- Testing without explicit permission

### Disclaimer

By using these tools, you agree to:
1. Only test on systems you own or have explicit permission to test
2. Comply with all applicable laws and regulations
3. Use findings responsibly and ethically
4. Report vulnerabilities through proper channels

**The authors assume no liability for misuse of these demonstrations.**

---

## 🤝 Contributing

This repository is primarily for conference presentation. If you'd like to:
- Report issues or bugs
- Suggest improvements
- Share related research

Please open an issue or submit a pull request.

---

## 📝 Project Information

**Event:** BugCon 2025  
**Author:** Benigno Gutiérrez  
**Date:** November 2025  
**Purpose:** Security education and awareness

---

## 🎓 Learning Outcomes

After working through these demos, participants will understand:

### Technical Skills
- ✅ How browser debugging protocols work
- ✅ Session hijacking techniques
- ✅ Detection methods for common attacks
- ✅ Defensive monitoring strategies

### Security Principles
- ✅ Defense in depth
- ✅ Assume breach mentality
- ✅ Importance of process monitoring
- ✅ Balancing security and usability

---

## 📚 Infostealer Families Reference Guide

### Quick Reference: Active Threats

| Family | Tier | Technique | Status | Key Stat |
|--------|------|-----------|--------|----------|
| **LUMMA** | 1 | Memory scanning (obfuscated patterns) | Active (Oct 2025) | 51% market share, 394K infections, 400+ customers |
| **STEALC** | 1 | ChromeKatz memory dumping | Active | #2 position, $400 pricing |
| **VIDAR** | 1 | ChromeKatz + polymorphic builder | Active (v2.0 Oct 2025) | $300 lifetime, 17% of cases |
| **METASTEALER** | 2 | COM exploitation (CLSID abuse) | Active | Requires elevation |
| **PHEMEDRONE** | 3 | CDP WebSocket (simplest) | Active | First CDP bypass (Sept 12, 2024) |

### Advanced & Historical Families

| Family | Tier | Technique | Status | Key Stat |
|--------|------|-----------|--------|----------|
| **XENOSTEALER** | 2 | COM + code injection | Active | Chrome 127+ support (Sept 26, 2024) |
| **FLESHSTEALER** | 3 | Crypto + traditional | Active | 70+ wallet targets, Chrome 131+ |
| **MYTH STEALER** | 3 | Rust-based, multi-browser | Active (Dec 2024) | Newcomer, MaaS model |
| **REDLINE** | Historical | DPAPI-based (deprecated) | Disrupted (Oct 28, 2024) | 9.9M infections, couldn't adapt to Chrome 127 |

### Key Definitions

**Tier 1 (Highest Sophistication)**: Advanced memory scanning techniques, pattern-based detection bypass, professional MaaS operations, custom development, rapid Chrome adaptation.

**Tier 2 (High Sophistication)**: COM exploitation, code injection, elevation requirements, hybrid approaches, less observable than Tier 1.

**Tier 3 (Moderate)**: Simplified techniques, open-source or easy-to-use tools, more detectable, focused specialization (crypto, specific browsers).

**Historical**: Disrupted by law enforcement or superseded by newer families. Documented for historical context and ecosystem evolution understanding.

### Further Reading

- **45-Day Arms Race**: See presentation slides for timeline of how families adapted to Chrome 127 (July 30 - September 12, 2024)
- **Technical Analysis**: Detailed reverse engineering documentation in research materials
- **Detection Strategies**: See "Defense & Detection" slides for detection methods specific to each family
- **Complete glossary**: Available in presentation slides with color-coded threat levels

---

## 🔗 Additional Resources

### Chrome DevTools Protocol
- [Official Documentation](https://chromedevtools.github.io/devtools-protocol/)
- [Security Considerations](https://github.com/ChromeDevTools/devtools-protocol/issues)

### Security Frameworks
- [MITRE ATT&CK](https://attack.mitre.org/) - T1185 (Browser Session Hijacking)
- [OWASP](https://owasp.org/) - Session Management

---

## 📊 Demo Statistics

| Metric | Value |
|--------|-------|
| Total Demos | 1 (expandable) |
| Demo Time | 3-4 minutes each |
| Setup Time | 5 minutes |
| Skill Level | Medium |
| Impact Level | Critical |

---

## ✅ Status

**Development:** Complete  
**Testing:** Verified  
**Documentation:** Comprehensive  
**Presentation Ready:** Yes

---

*For demo-specific information, see individual demo README files in the `demos/` directory.*
