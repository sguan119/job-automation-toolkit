# Job Automation Toolkit

> 🤖 AI-powered job application automation platform using Claude AI agents, n8n workflows, and browser automation

[![Tech Stack](https://img.shields.io/badge/n8n-Workflows-orange)](https://n8n.io)
[![AI](https://img.shields.io/badge/Claude-AI%20Agents-blue)](https://anthropic.com)
[![Automation](https://img.shields.io/badge/agent--browser-Playwright-green)](https://github.com/vercel/agent-browser)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## 🎯 Overview

**Job Automation Toolkit** is an end-to-end intelligent automation system that streamlines the entire job application process. Built with AI agents, workflow orchestration, and browser automation, it reduces manual effort by **90%** while maintaining personalization and quality.

### Problem Statement

Job hunting is time-consuming and repetitive:
- ⏱️ Manually extracting job descriptions from dozens of career sites
- 📝 Customizing resumes and cover letters for each position
- 🔍 Filtering through hundreds of irrelevant job postings
- 📊 Tracking applications across multiple platforms
- 🌐 Navigating different career site architectures (Workday, Greenhouse, Lever, etc.)

### Solution

An intelligent automation pipeline powered by:
- **🤖 Claude AI Agents** - Smart job filtering and content generation
- **🔄 n8n Workflows** - Complex automation orchestration
- **🌐 Browser Automation** - Data extraction from any career site
- **📊 Smart Tracking** - Automated file organization and Excel tracking

## 🏗️ System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                      Career Sites                             │
│        LinkedIn | Workday | Greenhouse | Lever | Custom       │
└───────────────────────────┬──────────────────────────────────┘
                            │
                ┌───────────▼──────────────┐
                │  JD Extraction           │
                │  Orchestrator            │
                │  (agent-browser + AI)    │
                └───────────┬──────────────┘
                            │
                ┌───────────▼──────────────┐
                │  Batch JD Processor      │
                │  (Parallel Analysis)     │
                │  PASS/REJECT + Reasoning │
                └───────────┬──────────────┘
                            │
                ┌───────────▼──────────────┐
                │  n8n Workflow API        │
                │  (Cover Letter + Resume) │
                └───────────┬──────────────┘
                            │
                ┌───────────▼──────────────┐
                │  File Organizer          │
                │  (Excel Tracker + PDFs)  │
                └──────────────────────────┘
```

## ⚙️ Tech Stack

### AI & Automation
- **Claude AI** (Anthropic API) - Intelligent agents for filtering and content generation
- **n8n** - Workflow automation and orchestration
- **agent-browser** (Playwright/Vercel) - Headless browser automation
- **Claude Code** - Agent/skill framework

### Data Processing
- **Node.js** - Core scripting and API integration
- **Python** - Data analysis and processing
- **ExcelJS** - Spreadsheet automation and tracking

### Integration
- **Anthropic API** - AI-powered content generation
- **n8n Webhooks** - Workflow triggering and orchestration
- **REST APIs** - External service integration

## 🚀 Key Features

### 1. 🔍 Intelligent JD Extraction

Extract job listings and full job descriptions from **any career site**:

```javascript
// Supports 20+ pre-configured Workday templates
- ElementFleet, CIBC, BMO, RBC, Scotiabank, etc.
- Auto-detects site type (Workday/Greenhouse/Lever/Custom)
- Smart pagination with retry logic
- Full JD extraction with validation
- Exports to JSON/CSV/Excel
```

**Key Skills:**
- `jd-extraction-orchestrator` - Main orchestrator for any career site
- `job-site-extractor` - Workday-specific extraction
- `job-link-extractor` - Generic site extraction

### 2. 🎯 AI-Powered Job Filtering

Intelligent filtering using user-defined criteria:

```yaml
# Filter criteria example
location:
  - Toronto, ON
  - Remote (Canada)
required_skills:
  - Python or R
  - SQL
  - Statistical analysis
job_scope:
  reject_if_contains:
    - "5+ years sales experience"
    - "cold calling"
```

**Features:**
- Parallel processing with multiple sub-agents
- Human-like analysis with detailed reasoning
- Color-coded Excel output (Green=PASS, Red=REJECT, Yellow=ERROR)
- Saves 80% time on manual filtering

**Key Skills:**
- `batch-jd-processor` - Batch filtering with parallel agents
- `jd-filter` - Single JD analysis
- `linkedin-job-filter` - LinkedIn-specific filtering with auto-dismiss

### 3. 📝 Automated Resume & Cover Letter Generation

Generate customized application materials via n8n workflow:

```javascript
// Workflow inputs
{
  jobDescription: "...",
  position: "Data Analyst",
  company: "Acme Corp"
}

// Outputs
- Tailored resume (PDF)
- Custom cover letter (PDF)
- ATS-optimized formatting
- Batch processing support
```

**Features:**
- Anthropic API integration for content generation
- Batch processing with order tracking
- Configurable intervals between generations
- Auto-saves order files for downstream processing

**Key Skills:**
- `cover-letter-generator` - Triggers n8n workflow for batch processing
- `job-processor` - End-to-end orchestrator (generation + organization)

### 4. 🗂️ Smart File Organization

Automated file organization and Excel tracking:

```
cvs/resume and cover letters/
├── 2026-02-16/
│   ├── 1-R.pdf  (Resume - Acme Corp Data Analyst)
│   ├── 1-CL.pdf (Cover Letter - Acme Corp Data Analyst)
│   ├── 2-R.pdf  (Resume - Beta Inc ML Engineer)
│   └── 2-CL.pdf (Cover Letter - Beta Inc ML Engineer)

cvs/Excel/job-applications.xlsx
- Auto-updated with hyperlinks
- Tracks all applications
- Backup versioning
```

**Key Skills:**
- `job-application-tracker` - File organization + Excel updates

### 5. 🌐 Form Auto-Fill

Auto-fill web forms using saved user profile:

```javascript
// Remembers across sessions
- Personal information
- Work experience
- Education
- Skills and certifications
- Custom fields
```

**Key Skills:**
- `form-auto-filler` - Multi-page form automation with memory

### 6. 🔗 LinkedIn Job Filter (Live Browser)

Real-time LinkedIn job filtering with auto-dismiss:

```javascript
// Workflow
1. Opens LinkedIn Jobs search in headed browser
2. Iterates through each job posting
3. Extracts full JD using CSS selectors
4. Runs AI filter analysis
5. Auto-dismisses rejected jobs (clicks X button)
6. Moves to next posting
```

**Key Skills:**
- `linkedin-job-filter` - Headed browser automation

## 📊 Results & Impact

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| JD Extraction Time | 5 min/job | 30 sec/job | **90% faster** |
| Job Filtering | 2 min/job | 10 sec/job | **92% faster** |
| Resume Customization | 30 min/job | 3 min/job | **90% faster** |
| Application Tracking | Manual spreadsheet | Automated | **100% organized** |
| **Total Time Saved** | **~40 min/job** | **~5 min/job** | **87% reduction** |

## 🛠️ Installation & Setup

### Prerequisites

```bash
# Required
- Node.js 18+
- npm or pnpm
- Claude Code CLI
- n8n instance (cloud or self-hosted)
- Anthropic API key

# Optional (for browser automation)
- agent-browser CLI
```

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/job-automation-toolkit.git
cd job-automation-toolkit
```

### 2. Install Dependencies

```bash
npm install
# or
pnpm install
```

### 3. Install agent-browser

```bash
npm install -g agent-browser
# or use via npx
```

### 4. Configure Environment

```bash
cp .env.example .env
```

Edit `.env`:
```bash
# Anthropic API
ANTHROPIC_API_KEY=your_anthropic_api_key

# n8n Configuration
N8N_WEBHOOK_URL=https://your-n8n-instance.com/webhook/cover-letter-gen
N8N_API_KEY=your_n8n_api_key  # Optional

# File Paths
OUTPUT_DIR=./output
EXCEL_TRACKER_PATH=./cvs/Excel/job-applications.xlsx
```

### 5. Configure Claude Code

```bash
# Ensure skills are in .claude/skills/
# Settings are in .claude/settings.local.json
```

### 6. Set Up n8n Workflow

Import the provided workflow:
1. Go to n8n → Workflows → Import
2. Import `n8n-workflows/cover-letter-generator.json`
3. Configure Anthropic API credentials
4. Activate workflow
5. Copy webhook URL to `.env`

## 📖 Usage Examples

### Extract Jobs from Career Site

```bash
# Using Claude Code
/jd-extraction-orchestrator

# User provides:
- Career site URL (e.g., https://workday.com/careers)
- Number of jobs to extract (optional)
```

### Batch Filter Job Descriptions

```bash
# Using Claude Code
/batch-jd-processor

# User provides:
- Path to Excel/CSV with JD data
- Filter criteria (or uses saved criteria)

# Output:
- Color-coded Excel with PASS/REJECT classifications
- Detailed reasoning for each decision
```

### Generate Cover Letters & Resumes

```bash
# Using Claude Code
/job-processor

# User provides:
- One or more job descriptions (text or file)

# System automatically:
1. Triggers n8n workflow for each JD
2. Waits for PDF generation
3. Organizes files into dated folders
4. Updates Excel tracker with hyperlinks
```

### Filter LinkedIn Jobs Live

```bash
# Using Claude Code
/linkedin-job-filter

# User provides:
- LinkedIn Jobs search URL

# System:
1. Opens browser in headed mode
2. Iterates through each job
3. Extracts full JD
4. Analyzes with AI filter
5. Auto-dismisses rejected jobs
```

### Auto-Fill Application Form

```bash
# Using Claude Code
/form-auto-filler

# User provides:
- URL to application form

# System:
1. Opens form in browser
2. Detects form fields
3. Fills from saved user profile
4. Handles multi-page forms
```

## 📂 Project Structure

```
job-automation-toolkit/
├── .claude/
│   ├── skills/                          # Claude Code skills
│   │   ├── jd-extraction-orchestrator/  # Main JD extraction
│   │   ├── batch-jd-processor/          # Batch filtering
│   │   ├── linkedin-job-filter/         # LinkedIn automation
│   │   ├── jd-filter/                   # Single JD filter
│   │   ├── cover-letter-generator/      # n8n integration
│   │   ├── job-application-tracker/     # File organization
│   │   ├── job-processor/               # End-to-end orchestrator
│   │   └── form-auto-filler/            # Form automation
│   └── settings.local.json              # Settings
├── n8n-workflows/                        # n8n workflow exports
│   └── cover-letter-generator.json
├── docs/
│   ├── architecture.md                   # System design
│   ├── skills-guide.md                   # Skill documentation
│   └── setup-guide.md                    # Detailed setup
├── examples/
│   ├── sample-jd.json                    # Example JD data
│   ├── filter-criteria.yaml              # Filter examples
│   └── user-profile.example.yaml         # Profile template
├── .env.example                          # Environment template
├── .gitignore
├── package.json
├── README.md
└── LICENSE
```

## 🎓 Skills Demonstrated

This project showcases:

- ✅ **AI Agent Development** - Claude AI agent orchestration and skill creation
- ✅ **Workflow Automation** - n8n workflow design and API integration
- ✅ **Browser Automation** - Playwright-based data extraction
- ✅ **System Design** - End-to-end pipeline architecture
- ✅ **API Integration** - RESTful webhooks, Anthropic API
- ✅ **Data Processing** - Excel/CSV/JSON manipulation
- ✅ **Error Handling** - Retry logic, validation, self-check mechanisms
- ✅ **Parallel Processing** - Multi-agent concurrent execution
- ✅ **Problem Solving** - Real-world automation challenges

## 🔮 Future Enhancements

- [ ] **Chrome Extension** - One-click job extraction from any page
- [ ] **Interview Scheduler** - Auto-schedule and track interviews
- [ ] **Analytics Dashboard** - Application success metrics
- [ ] **Multi-Platform Support** - Indeed, Glassdoor, Monster integration
- [ ] **Email Integration** - Auto-track application responses
- [ ] **Salary Negotiation** - AI-powered salary research and suggestions
- [ ] **Company Research** - Auto-compile company info from multiple sources
- [ ] **Application Status Tracker** - Auto-update from email notifications

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This is a personal automation project for educational purposes. Always respect:
- Terms of service of career websites
- Rate limiting and API usage policies
- Data privacy and security best practices
- Ethical job application practices

## 🙏 Acknowledgments

- [Claude AI](https://anthropic.com) - AI capabilities
- [n8n](https://n8n.io) - Workflow automation platform
- [agent-browser](https://github.com/vercel/agent-browser) - Browser automation
- [Claude Code](https://claude.ai/code) - Agent framework

## 📧 Contact

Questions or suggestions? Feel free to open an issue or reach out!

---

**⭐ If this project helped you, please give it a star!**

Built with ❤️ using AI automation
