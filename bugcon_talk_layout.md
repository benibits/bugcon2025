# BugCon 2025 Talk Layout
## "Abusing Chrome Remote Debugging: A Hands-On Guide for Attackers and Defenders"

---

## Talk Metadata
- **Duration**: 40-45 minutes
- **Format**: Technical presentation with live demonstrations
- **Audience Level**: Intermediate to Advanced
- **Language**: English (with Spanish terminology where relevant)

---

## Complete Talk Structure

### **Opening Hook (3 minutes)**

#### Objectives
- Capture immediate attention with impact demonstration
- Establish credibility and relevance
- Set expectations for the session

#### Content Flow
1. **Live Demo Teaser** (30 seconds)
   - Quick demonstration: "Watch me compromise a browser session through a debugging port"
   - Show actual cookie extraction or session hijacking
   - Leave audience wanting to know "how"

2. **Impact Statistics** (1 minute)
   - Recent crypto heists involving browser exploitation
   - Number of exposed debugging ports in the wild (Shodan data)
   - Infostealer malware statistics leveraging CDP

3. **Scope Setting** (1.5 minutes)
   - "This isn't just about Chrome..."
   - Show logos: Brave, Edge, Opera, Vivaldi, Electron apps
   - "Every Chromium-based application in your organization"

#### Speaker Notes
- Energy should be highest here
- Have backup video if live demo fails
- Practice the 30-second demo until flawless

---

### **Act 1: The Threat Landscape (7 minutes)**

#### Section 1.1: The Problem Space (3 minutes)

##### Technical Context
- **Chrome DevTools Protocol (CDP) Overview**
  - What it is and why it exists
  - Legitimate use cases (debugging, automation, testing)
  - How developers typically use it

- **The Attack Surface**
  - Default configurations that enable exploitation
  - Common misconfigurations in enterprise
  - Inheritance problem: All Chromium-based apps

##### Visual Elements
- Architecture diagram of CDP
- Tree showing Chromium family affected apps
- Configuration examples (good vs bad)

#### Section 1.2: Real-World Impact (4 minutes)

##### Case Studies
1. **Infostealer Evolution**
   - Raccoon Stealer's CDP module
   - RedLine's browser targeting techniques
   - MetaStealer's debugging abuse

2. **Crypto Wallet Attacks**
   - Specific incident analysis
   - Dollar amounts lost
   - Attack timeline visualization

3. **Enterprise Breaches**
   - Developer environment compromises
   - CI/CD pipeline attacks
   - Insider threat scenarios

##### Data Points
- Shodan/Censys statistics on exposed ports
- Geographic distribution of vulnerable systems
- Industry sectors most affected

#### Visual Elements
- World heat map of exposed debugging ports
- Timeline of major incidents
- Loss statistics infographic

---

### **Act 2: Technical Deep Dive (15 minutes)**

#### Section 2.1: Understanding the Attack Vector (5 minutes)

##### Core Concepts
- **The `--remote-debugging-port` Flag**
  ```bash
  chrome --remote-debugging-port=9222
  ```
  - What it enables
  - Default behaviors
  - Network exposure implications

- **WebSocket Communication**
  - Connection to `/json` endpoint
  - Protocol structure
  - Authentication (or lack thereof)

- **Key CDP Domains**
  - **Runtime**: JavaScript execution
  - **Page**: Navigation and lifecycle
  - **Network**: Request interception
  - **Storage**: Cookies and local storage
  - **Security**: Certificate handling

##### Technical Diagrams
- CDP communication flow
- WebSocket message structure
- Attack sequence diagram

#### Section 2.2: Live Demo - The Attacker's Playbook (7 minutes)

##### Demo Sequence

1. **Discovery Phase** (1 minute)
   ```python
   # Port scanning for 9222
   # HTTP probe for /json endpoint
   ```

2. **Initial Access** (1.5 minutes)
   - Connect to debugging port
   - Enumerate available targets
   - Select victim page

3. **Session Hijacking** (1.5 minutes)
   - Extract all cookies
   - Capture localStorage
   - Screenshot active tabs

4. **Persistence & Pivoting** (2 minutes)
   - Inject persistent JavaScript
   - Install service worker backdoor
   - Pivot to other applications

5. **Crypto Wallet Targeting** (1 minute)
   - Identify wallet extensions
   - Extract seed phrases from memory
   - Monitor for transactions

##### Demo Commands
```javascript
// Example CDP commands to show
Runtime.evaluate({expression: 'document.cookie'})
Network.getCookies()
Page.captureScreenshot()
```

#### Section 2.3: Code Walkthrough (3 minutes)

##### PoC Script Analysis
- Python automation script breakdown
- Key CDP commands explained
- Error handling and stability
- Modular attack functions

##### Code Quality Points
- Reliability over speed
- Logging for forensics
- Configurable targeting
- Clean, readable code

---

### **Act 3: Defense & Detection (12 minutes)**

#### Section 3.1: Detection Strategies (4 minutes)

##### Host-Based Detection
- **Process Monitoring**
  - Unusual Chrome process arguments
  - Debugging port flags
  - Parent process analysis

- **File System Indicators**
  - Chrome profile modifications
  - Temporary file creation patterns
  - Extension manipulation

##### Network-Based Detection
- **Traffic Analysis**
  - WebSocket connections to localhost
  - Unusual port 9222 activity
  - CDP protocol signatures

- **Behavioral Patterns**
  - Rapid cookie extraction
  - Mass data exfiltration
  - Automated browsing patterns

##### Detection Rules Examples
```yaml
# Sigma rule example
detection:
  selection:
    CommandLine|contains: '--remote-debugging-port'
  condition: selection
```

#### Section 3.2: Hardening Techniques (5 minutes)

##### Enterprise Policies
- **Chrome Enterprise Configuration**
  ```json
  {
    "RemoteDebuggingAllowed": false,
    "DeveloperToolsAvailability": 2
  }
  ```

- **Group Policy Settings**
  - Disable debugging features
  - Enforce security policies
  - Audit policy compliance

##### Network Security
- **Firewall Rules**
  - Block port 9222 externally
  - Segment developer networks
  - Monitor internal connections

- **Zero Trust Principles**
  - Authenticate all connections
  - Encrypt debugging traffic
  - Minimal privilege access

##### Application Security
- **Electron App Hardening**
  - Disable debugging in production
  - Code signing enforcement
  - Update mechanisms

- **Crypto Wallet Protection**
  - Hardware wallet preference
  - Browser isolation
  - Extension permissions audit

#### Section 3.3: Purple Team Exercise Design (3 minutes)

##### Exercise Framework
1. **Preparation Phase**
   - Safe testing environment setup
   - Success criteria definition
   - Team role assignments

2. **Execution Phase**
   - Red team attack simulation
   - Blue team detection practice
   - Real-time collaboration

3. **Analysis Phase**
   - Detection gap analysis
   - Control effectiveness
   - Improvement recommendations

##### Metrics to Track
- Time to detection
- False positive rate
- Coverage percentage
- Response effectiveness

---

### **Act 4: Beyond Chrome (5 minutes)**

#### Extended Attack Surface Analysis

##### Electron Applications
- Popular affected applications
  - VS Code, Discord, Slack, Teams
  - Attack vectors specific to each
  - Mitigation strategies

##### Cryptocurrency Ecosystem
- Browser-based wallets at risk
- DeFi application vulnerabilities
- Best practices for crypto users

##### Mobile Considerations
- Android Chrome debugging
- iOS remote debugging
- Mobile app testing implications

##### CI/CD Pipeline Risks
- Automated browser testing
- Headless Chrome in pipelines
- Container security considerations

#### Visual Elements
- Application vulnerability matrix
- Risk assessment heat map
- Mitigation checklist

---

### **Closing & Call to Action (3 minutes)**

#### Key Takeaways
1. **For Red Teamers**
   - New attack vector for assessments
   - Automation possibilities
   - Reporting recommendations

2. **For Blue Teamers**
   - Detection strategies to implement
   - Monitoring improvements
   - Incident response updates

3. **For Developers**
   - Secure configuration defaults
   - Production hardening checklist
   - Security testing additions

#### Resources Provided
- **GitHub Repository Structure**
  ```
  chrome-remote-debug-arsenal/
  ├── README.md
  ├── lab/
  ├── poc/
  ├── defense/
  └── slides/
  ```

- **Immediate Actions**
  - Check your environment NOW
  - Implement quick wins
  - Schedule deeper assessment

#### Q&A Preparation
- Anticipate common questions
- Have backup slides ready
- Time buffer for discussion

---

## Visual Design Specifications

### Slide Design Principles
- **Color Scheme**: Dark background (#1a1a1a), bright accent (#00ff41)
- **Typography**: Clean sans-serif, high contrast
- **Code Highlighting**: Syntax highlighting for readability
- **Animation**: Minimal, purposeful transitions

### Key Visual Elements
1. **Attack Flow Diagram**: Clean, step-by-step visualization
2. **Threat Matrix**: Grid showing affected platforms
3. **Detection Dashboard**: Mock security tool interface
4. **Before/After Comparisons**: Configuration changes
5. **Live Terminal**: Clear, readable command execution

---

## Demo Management Strategy

### Primary Demo Environment
- **Setup Requirements**
  - Two VMs: Attacker and Victim
  - Isolated network segment
  - Pre-configured vulnerable Chrome
  - Sample web applications

### Backup Plans
1. **Level 1**: Live demo with local network
2. **Level 2**: Pre-recorded video with live narration
3. **Level 3**: Static screenshots with detailed explanation
4. **Level 4**: Conceptual explanation with diagrams

### Demo Insurance Checklist
- [ ] Test on conference hardware spec
- [ ] Record all demos in advance
- [ ] Create screenshot sequence
- [ ] Prepare offline environment
- [ ] Test with degraded network
- [ ] Have USB with all materials
- [ ] Practice failure recovery

---

## Engagement Strategies

### Interactive Elements
- **Minute 10**: Audience poll - "Who has debugging enabled?"
- **Minute 20**: "Spot the vulnerability" challenge
- **Minute 30**: Live rule building with audience
- **Minute 40**: Quick security check together

### Memorable Moments
- "Debugging Port Bingo" game card
- Security mnemonic device
- "Taco defense layers" analogy
- Live "hack the speaker" segment

### Cultural Connections
- Reference regional incidents
- Use bilingual technical terms
- Include LATAM-specific examples
- Acknowledge local security community

---

## Time Management Guide

### Detailed Timeline
- **0:00-3:00**: Opening Hook
- **3:00-10:00**: Threat Landscape
- **10:00-25:00**: Technical Deep Dive
- **25:00-37:00**: Defense & Detection
- **37:00-42:00**: Beyond Chrome
- **42:00-45:00**: Closing & Q&A

### Flexibility Points
- Can skip case study 2 if running behind (-2 min)
- Can shorten code walkthrough (-1 min)
- Can skip mobile considerations (-1 min)
- Extra demo if ahead (+3 min)

### Transition Phrases
- "Now that we understand the threat..."
- "Let's see this in action..."
- "But how do we defend against this?"
- "Looking beyond just Chrome..."

---

## Speaker Notes Structure

### For Each Section
- Key technical points (bullets)
- Transition sentences (exact wording)
- Demo commands (copy-paste ready)
- Time markers (cumulative)
- Energy level indicators
- Backup plan triggers

### Emergency Procedures
- Demo failure recovery steps
- Audience management techniques
- Time recovery strategies
- Technical difficulty handling
- Q&A deflection for off-topic

---

## Pre-Conference Checklist

### One Month Before
- [ ] Complete all demo development
- [ ] Finish slide deck v1
- [ ] Record backup videos
- [ ] Create GitHub repository
- [ ] Test with sample audience

### One Week Before
- [ ] Final slide revision
- [ ] Practice full run-through
- [ ] Verify demo stability
- [ ] Prepare handout materials
- [ ] Check conference requirements

### Day Before
- [ ] Test on-site if possible
- [ ] Review speaker notes
- [ ] Prepare backup USB
- [ ] Check all equipment
- [ ] Rest and hydrate

### Day Of
- [ ] Arrive early for setup
- [ ] Test A/V connections
- [ ] Network connectivity check
- [ ] Quick demo verification
- [ ] Mental preparation routine

---

## Success Metrics

### Immediate Indicators
- Audience engagement level
- Question quantity and quality
- Social media activity
- Note-taking behavior
- Demo reaction intensity

### Follow-up Metrics
- GitHub stars/forks
- LinkedIn connections
- Follow-up emails
- Blog post references
- Tool adoption rates

### Long-term Impact
- Citation in other talks
- Security tool integration
- Policy changes reported
- Community contributions
- Speaking invitations

---

## Additional Resources

### Required Reading
- Chrome DevTools Protocol documentation
- Chromium security architecture
- Recent CDP vulnerability reports
- Electron security best practices

### Tools to Master
- Chrome DevTools
- Puppeteer/Playwright
- CDP client libraries
- Wireshark for WebSocket
- Browser security extensions

### Community Connections
- Browser security researchers
- Chrome security team
- Electron security group
- LATAM security community

---

*This layout serves as the master blueprint for developing the BugCon 2025 presentation on Chrome Remote Debugging abuse.*