# BugCon 2025 Presentation
## Abusing Chrome Remote Debugging - reveal.js Slides

---

## 🚀 Quick Start (2 Options)

### Option 1: Open Directly in Browser (Easiest)

Simply **double-click `index.html`** to open in your browser.

**That's it!** The presentation loads everything from CDN and works offline once cached.

---

### Option 2: Run with Local Server (Recommended for Development)

If you want live-reload while editing or better speaker notes:

**Using Python (already installed on your system):**

```bash
# Navigate to the slides directory
cd slides

# Python 3
python -m http.server 8000

# Then open: http://localhost:8000
```

**Using Node.js (if you have it):**

```bash
# Install simple server globally
npm install -g http-server

# Run in slides directory
http-server

# Opens automatically
```

---

## 🎮 Presentation Controls

| Key | Action |
|-----|--------|
| **Space** or **→** | Next slide |
| **←** | Previous slide |
| **F** | Fullscreen mode |
| **S** | Speaker notes view (IMPORTANT!) |
| **O** or **Esc** | Overview mode |
| **B** | Blackout screen |
| **?** | Show help |

**Most Important:** Press **S** to open **speaker notes view** - this shows:
- Your notes for each slide
- Next slide preview
- Timer
- Current slide view

---

## ✏️ Editing the Slides

### The slides are written in Markdown inside the HTML file.

**To edit:**

1. Open `index.html` in your code editor (Cursor, VS Code, etc.)
2. Find the `<section data-markdown>` blocks
3. Edit the content between `<textarea data-template>` tags
4. Save and refresh your browser

**Example slide structure:**

```html
<section data-markdown>
    <textarea data-template>
        ## Slide Title
        
        Your content here
        
        - Bullet point 1
        - Bullet point 2
        
        ```python
        # Code blocks work great
        print("Hello BugCon!")
        ```
        
        ---
        
        Note: These are speaker notes - press S to see them!
    </textarea>
</section>
```

---

## 🎨 Custom Styling Features

### Built-in CSS Classes:

**Two-column layout:**
```html
<div class="two-column">
<div>Left content</div>
<div>Right content</div>
</div>
```

**Terminal effect:**
```html
<div class="terminal">
python chrome_hijack_basic.py
</div>
```

**Warning box:**
```html
<div class="warning-box">
Critical security finding!
</div>
```

**Success box:**
```html
<div class="success-box">
Detection successful!
</div>
```

**Impact statistics:**
```html
<p class="impact-stat">12,847</p>
```

**Red Team / Blue Team colors:**
```html
<span class="red-team">Attacker perspective</span>
<span class="blue-team">Defender perspective</span>
```

**Critical (pulsing) text:**
```html
<span class="critical">IMMEDIATE ACTION REQUIRED</span>
```

---

## 🎭 Fragments (Progressive Reveal)

Make content appear step-by-step:

```html
<div class="fragment">Appears first</div>
<div class="fragment">Appears second</div>
<div class="fragment">Appears third</div>
```

**Useful for:**
- Building suspense
- Revealing statistics gradually
- Step-by-step demonstrations

---

## 📝 Adding Speaker Notes

Speaker notes are CRITICAL for your presentation. Add them after `---` on each slide:

```html
<section data-markdown>
    <textarea data-template>
        ## Your Slide Content
        
        Visible to audience
        
        ---
        
        Note: These are your speaker notes. Only you see these.
        Press S during presentation to view them!
        
        - Talk about X
        - Emphasize Y
        - Transition to next slide with Z
    </textarea>
</section>
```

---

## 🖼️ Adding Images

**Option 1: Use online images:**
```html
![Description](https://example.com/image.png)
```

**Option 2: Local images:**
```html
<!-- Create an 'images' folder next to index.html -->
![Description](images/screenshot.png)
```

---

## 📊 Current Slide Structure

Your presentation currently has **~35 slides** organized in **4 Acts:**

### Act 1: Threat Landscape (8 slides)
- Opening hook
- Impact statistics
- Attack surface
- Real-world cases

### Act 2: Technical Deep Dive (8 slides)
- How CDP works
- Attack mechanics
- **LIVE DEMO - Red Team** 🔴
- Demo recap

### Act 3: Defense & Detection (10 slides)
- **LIVE DEMO - Blue Team** 🔵
- Detection strategies
- Sigma rules
- Hardening techniques

### Act 4: Beyond Chrome (4 slides)
- Electron apps
- Crypto ecosystem
- CI/CD risks

### Closing (3 slides)
- Key takeaways
- Resources
- Q&A

### Backup Slides (2 slides)
- Technical details
- Mobile platforms

---

## 🎯 What You Need to Do Next

### 1. **Customize Personal Info** (5 minutes)

Replace placeholders in the title slide:
- `[Your Name]`
- `[Your Title/Company]`
- `[@YourTwitter]`
- `[github.com/yourrepo]`
- `your.email@example.com`

### 2. **Review Every Slide** (30 minutes)

- Read through each slide
- Verify technical accuracy
- Adjust wording to your style
- Add/remove content as needed

### 3. **Expand Speaker Notes** (1 hour)

Each slide has basic notes, but you should expand them with:
- Exact phrases you want to say
- Timing markers
- Transition sentences
- Demo cues
- Important points to emphasize

### 4. **Add Screenshots** (30 minutes)

From your working demos:
- Screenshot of successful attack
- Screenshot of detection tool output
- Terminal output examples
- Chrome debugging interface

### 5. **Practice with Speaker Notes** (2-3 hours)

- Press **S** to open speaker view
- Practice your timing
- Refine your delivery
- Adjust content based on timing

---

## 🎬 Demo Integration

### Red Team Demo Slide

Located at slide ~15. This is where you'll:
1. Switch to your terminal
2. Run `start_chrome_debug.bat`
3. Run `python chrome_hijack_basic.py`
4. Narrate what's happening
5. Show the screenshot output

**Backup plan:** If demo fails, you have static screenshots to show.

### Blue Team Demo Slide

Located at slide ~20. This is where you'll:
1. Run `python chrome_debug_detector.py`
2. Show the detection in action
3. Highlight the risk assessment
4. Discuss remediation

---

## 🚨 Troubleshooting

**Slides don't load:**
- Check that you have internet connection (for CDN resources)
- Try opening in a different browser
- Check browser console for errors (F12)

**Code highlighting doesn't work:**
- Ensure you're using triple backticks with language: ` ```python `
- Check that RevealHighlight plugin is loaded

**Speaker notes don't show:**
- Press **S** key
- Check that RevealNotes plugin is loaded
- Try refreshing the page

**Transitions are choppy:**
- Close other browser tabs
- Disable browser extensions
- Try a different browser (Chrome/Firefox recommended)

---

## 📦 Files Included

```
slides/
├── index.html          <- Main presentation file (this is everything!)
└── README.md          <- This file
```

That's it! Everything is self-contained in one HTML file.

**Optional to add:**
```
slides/
├── index.html
├── README.md
├── images/            <- Your demo screenshots
│   ├── attack-demo.png
│   ├── detection-demo.png
│   └── architecture.png
└── videos/            <- Backup demo recordings
    ├── red-team-demo.mp4
    └── blue-team-demo.mp4
```

---

## 🎨 Customizing Colors

The presentation uses a **dark hacker theme** with green accents. To change:

**In `index.html`, find the `:root` CSS section:**

```css
:root {
    --hacker-green: #00ff41;    /* Change to your color */
    --dark-bg: #0a0e14;         /* Background color */
    --code-bg: #1a1d23;         /* Code block background */
}
```

---

## 💾 Exporting to PDF

**For backup or sharing:**

1. Open presentation in browser
2. Add `?print-pdf` to the URL:
   ```
   http://localhost:8000/?print-pdf
   ```
3. Use browser's Print function
4. Select "Save as PDF"
5. **Make sure to select "Background graphics"**

**Or use this command:**
```bash
# Using decktape (requires Node.js)
npm install -g decktape
decktape reveal http://localhost:8000 slides.pdf
```

---

## ⏱️ Timing Your Presentation

**Current slide count:** ~35 slides
**Target time:** 40-45 minutes

**Recommended pace:**
- Opening Hook: 3 minutes (3 slides)
- Act 1: 7 minutes (8 slides)
- Act 2: 15 minutes (8 slides) - includes live demo
- Act 3: 12 minutes (10 slides) - includes live demo
- Act 4: 5 minutes (4 slides)
- Closing: 3 minutes (3 slides)

**Tips:**
- Don't rush the demos (they're your "wow" moments)
- Slow down on complex technical slides
- Speed up on slides that are just context
- Leave 2-3 minutes buffer for transitions

---

## 🎤 Presentation Day Checklist

- [ ] Test presentation on conference hardware (if possible)
- [ ] Verify speaker notes work (press S)
- [ ] Check that code highlighting is visible on projector
- [ ] Have backup screenshots ready
- [ ] Test in both Chrome and Firefox
- [ ] Export PDF backup (in case of technical issues)
- [ ] Practice with clicker/keyboard shortcuts
- [ ] Test the demos one more time
- [ ] Bring USB with all files

---

## 🔗 Useful Resources

**reveal.js Documentation:**
- https://revealjs.com/

**Markdown Cheatsheet:**
- https://www.markdownguide.org/cheat-sheet/

**Speaker Notes Best Practices:**
- Keep notes concise
- Use bullet points
- Include timing markers
- Add transition cues
- Note demo triggers

---

## ✅ Your Next Steps

1. **NOW:** Open `index.html` and review all slides
2. **Next 30 min:** Customize with your personal info
3. **Next 1 hour:** Expand speaker notes
4. **Next 2 hours:** Add screenshots and polish content
5. **Tomorrow:** Practice run-through with speaker notes
6. **Monday:** Final polish and backup materials

---

**You've got a professional, conference-ready presentation!**

Now it's just about making it yours and practicing your delivery. 🚀

**Questions or issues?** Check the reveal.js docs or ask for help!

Good luck at BugCon 2025! 🔐
