# Quick Start Guide

Get up and running with Job Automation Toolkit in 10 minutes.

## Prerequisites

Before you begin, ensure you have:

- ✅ Node.js 18+ installed
- ✅ npm or pnpm package manager
- ✅ Anthropic API key ([Get one here](https://console.anthropic.com/))
- ✅ Claude Code CLI installed
- ✅ n8n instance (cloud or self-hosted)

## Step 1: Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/job-automation-toolkit.git
cd job-automation-toolkit

# Install dependencies
npm install

# Install agent-browser globally (optional)
npm install -g agent-browser
```

## Step 2: Configuration

### 2.1 Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your credentials
# Minimum required:
ANTHROPIC_API_KEY=sk-ant-api03-xxx
N8N_WEBHOOK_URL=https://your-n8n-instance.com/webhook/cover-letter-gen
```

### 2.2 Set Up n8n Workflow

1. Import the workflow:
   - Open n8n
   - Go to **Workflows** → **Import from File**
   - Select `n8n-workflows/cover-letter-generator.json`

2. Configure credentials:
   - Add your Anthropic API key in the workflow nodes
   - Activate the workflow

3. Get webhook URL:
   - Click on the Webhook node
   - Copy the **Production URL**
   - Paste into `.env` as `N8N_WEBHOOK_URL`

### 2.3 Configure User Profile (Optional)

For form auto-fill functionality:

```bash
# Copy the example user profile
cp examples/user-profile.example.yaml .claude/memory/USER_PROFILE.yaml

# Edit with your information
# This will be used by the form-auto-filler skill
```

## Step 3: Verify Setup

Test that everything is working:

```bash
# Test Anthropic API connection
node scripts/test-anthropic.js

# Test n8n webhook
node scripts/test-n8n-webhook.js
```

## Step 4: Your First Automation

### Extract Jobs from a Career Site

1. Open Claude Code
2. Run the extraction skill:
   ```
   /jd-extraction-orchestrator
   ```
3. Provide a career site URL (e.g., Workday URL)
4. Wait for extraction to complete
5. Check `output/` directory for results

### Filter Job Descriptions

1. Ensure you have extracted jobs or a CSV/Excel file with JDs
2. Run the batch processor:
   ```
   /batch-jd-processor
   ```
3. Provide the path to your file
4. Review color-coded results in the output Excel

### Generate Cover Letters & Resumes

1. Have one or more job descriptions ready
2. Run the job processor:
   ```
   /job-processor
   ```
3. Paste or provide JD(s)
4. Wait for generation (check n8n for progress)
5. Files will be organized in `cvs/resume and cover letters/YYYY-MM-DD/`

## Common Workflows

### Workflow 1: From Career Site to Application

```bash
1. Extract jobs       → /jd-extraction-orchestrator
2. Filter jobs        → /batch-jd-processor
3. Generate materials → /job-processor
4. Organize files     → (automatic)
```

### Workflow 2: LinkedIn Quick Filter

```bash
1. Get LinkedIn search URL
2. Run LinkedIn filter → /linkedin-job-filter
3. Watch as rejected jobs are auto-dismissed
```

### Workflow 3: Auto-Fill Application

```bash
1. Have target application URL
2. Run form filler → /form-auto-filler
3. Review and submit
```

## Tips for Success

### Performance Optimization

- **Batch Processing**: Process multiple JDs at once for efficiency
- **Parallel Agents**: Adjust `MAX_CONCURRENT_AGENTS` in `.env`
- **Caching**: Reuse extracted data to avoid re-scraping

### Best Practices

1. **Start Small**: Test with 5-10 jobs before batch processing hundreds
2. **Review Filters**: Check filtered results to tune your criteria
3. **Customize Templates**: Adjust resume/cover letter templates in n8n
4. **Backup Data**: The system creates backups of your Excel tracker

### Troubleshooting

**"API key invalid"**
- Verify your Anthropic API key in `.env`
- Check key has sufficient credits

**"n8n webhook not responding"**
- Ensure workflow is activated in n8n
- Check webhook URL is correct
- Verify n8n instance is accessible

**"Browser automation failing"**
- Install agent-browser: `npm install -g agent-browser`
- Check if site requires login (not supported for some sites)
- Try headed mode: `--headed` flag

**"Skills not found"**
- Ensure `.claude/skills/` directory exists
- Check `settings.local.json` configuration

## Next Steps

- 📖 Read the [Architecture Guide](architecture.md)
- 🛠️ Explore [Skills Documentation](skills-guide.md)
- ⚙️ Customize [Filter Criteria](../examples/filter-criteria.yaml)
- 🔧 Set up [Form Auto-Fill Profile](../examples/user-profile.example.yaml)

## Getting Help

- 📝 Check the [main README](../README.md)
- 🐛 [Report issues](https://github.com/yourusername/job-automation-toolkit/issues)
- 💬 [Ask questions](https://github.com/yourusername/job-automation-toolkit/discussions)

---

Happy automating! 🚀
