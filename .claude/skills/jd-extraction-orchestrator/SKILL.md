---
name: jd-extraction-orchestrator
description: Extract job listings and full JDs from any career site (Workday, Greenhouse, Lever, custom). Use when user provides a career URL, says "extract jobs", "提取职位", "提取链接", "提取JD", "scrape career site", or any Workday URL (wd3.myworkdayjobs.com). Handles site detection, pagination, full JD extraction, self-check, retry, validation, and JSON/CSV/Excel output. Supports 20+ pre-configured Workday company templates.
---

# JD Extraction Orchestrator

URL → detect site type → extract all jobs with full JDs → validate → output files.

## Startup

**ALWAYS** load lessons learned first:
```
Read: .claude/skills/jd-extraction-orchestrator/references/lessons-learned.md
```

## Site Detection

| URL Pattern | Type | Method |
|-------------|------|--------|
| `*.wd3.myworkdayjobs.com`, `*.wd5.myworkdayjobs.com` | Workday | `eval` with DOM selector |
| `jobs.nokia.com`, `jobs.rbc.com`, `jobs.td.com`, etc. | Workday | `eval` with DOM selector |
| `boards.greenhouse.io`, `jobs.lever.co` | ATS | snapshot + get text |
| Other career sites | Generic | snapshot + get text |

Pre-configured Workday company templates (CIBC, RBC, TD, BMO, Nokia, Bell, etc.):
```
Read: .claude/skills/jd-extraction-orchestrator/references/site-configs.md
```

## Model Selection

| Job Count | Model |
|-----------|-------|
| < 30 | Sonnet OK |
| 30-70 | **Opus recommended** |
| 70+ | **Opus required** |

## Workflow

### Phase 1: Setup
1. Open URL, snapshot, estimate job count
2. Report: "Found ~N jobs. Time: ~X min. Proceed?"

### Phase 2: Extract Job Links
```bash
agent-browser --session extract --headed open "{url}"
agent-browser --session extract snapshot -i
```
Loop all pages: snapshot → collect job titles/locations/URLs → click pagination next → wait 2s → repeat. Deduplicate by jobId.

### Phase 3: Extract Full JDs

**Workday sites** (CRITICAL - use `eval`):
```bash
agent-browser --session extract open "{job_url}"
# Wait 2s for dynamic content
agent-browser --session extract eval "document.querySelector('[data-automation-id=\"jobPostingDescription\"]')?.innerText || ''"
```

**Non-Workday sites** (use snapshot + get text):
```bash
agent-browser --session extract open "{job_url}"
agent-browser --session extract snapshot -i
agent-browser --session extract get text @{jd_element_ref}
```

For >3 jobs on generic sites, use Task tool subagents for parallel extraction.

Save progress every 10 jobs. Report every 50 jobs.

### Phase 4: Self-Check & Retry
Count failed or short JDs (< 500 chars). Retry up to 3 times with 2s delay.

### Phase 5: Validate & Report
```
========================================
    {Company} Extraction Report
========================================
Count: Expected N, Extracted M (X%)
Quality: Complete JDs N, Short N, Failed N
JD Length: Min X, Max X, Avg X chars
Output Files: .json, .csv, _report.txt
Overall: PASS/FAIL
========================================
```
If < 95% success → retry failed → re-validate.

### Phase 6: Output
1. `{company}_jobs_with_jd_final.json` - Complete JSON array
2. `{company}_jobs_final.csv` - Excel-friendly CSV (BOM-encoded)
3. `{company}_extraction_report.txt` - Validation report

### Phase 7: Update lessons-learned.md (only if new actionable insights)

## Workday Selectors (Standard)

```
jobTitle:        [data-automation-id="jobTitle"]
locations:       [data-automation-id="locations"]
postedOn:        [data-automation-id="postedOn"]
paginationNext:  [data-uxi-widget-type="paginationNext"]
jobDescription:  [data-automation-id="jobPostingDescription"]
timeType:        [data-automation-id="timeType"]
```

## Extracted Fields

jobId, title, location, postedDate, url, jobDescription, timeType, status, extractedAt

## Generic Site Navigation Patterns

### Pattern: Job Listing → Detail → Back
```
snapshot → find job links → click each → get text for JD → back to results
```

### Pattern: Pagination
```
Click "next" / "page N" or use URL offset (?offset=0, 20, 40...)
```

### Pattern: Category Filters ("继续")
When user says "继续": extract new category → merge into SAME file → add Category column.

### Excel Output (Generic sites)
```python
headers = ['Job ID', 'Job Title', 'Location', 'Posted', 'Job URL', 'Full JD']
# Full JD with wrap_text=True, column width=120
```

## Critical Rules

### ALWAYS
- Use `agent-browser eval` with `data-automation-id="jobPostingDescription"` for Workday
- Add 2s delay after page load
- Delete progress files before fresh extraction
- Use `--session` flag with agent-browser
- ONE combined output file (don't create multiple)

### NEVER
- Don't use `get text body` + regex for Workday - breaks after ~20 jobs
- Don't use Sonnet for 70+ job Workday extractions

## Error Handling

- **Browser fails**: `agent-browser --version`, reinstall if needed
- **Site blocks**: Increase all waits by 2x
- **Timeout**: Save progress, report partial, offer resume
- **Unknown structure**: Take screenshots, try generic extraction

## References

- [site-configs.md](references/site-configs.md) - 20+ company templates
- [lessons-learned.md](references/lessons-learned.md) - Failure patterns and solutions
