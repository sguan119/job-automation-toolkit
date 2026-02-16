---
name: job-processor
description: End-to-end job application processor. Orchestrates the complete pipeline - receives JDs, triggers cover-letter-generator skill to send to n8n, waits for PDF generation, then runs job-application-tracker skill to organize files and update Excel. Use when user says "帮我处理这些JD", "process these jobs", "生成简历和cover letter", or when user provides one or more job descriptions for full end-to-end processing.
---

# Job Processor

Orchestrate the complete job application workflow: JDs in -> cover letters & resumes generated -> files organized.

## Pipeline

```
Input (Excel/Text/Direct)
  -> cover-letter-generator skill (curl triggers to n8n, 30s intervals)
  -> Wait for completion (~90s per job)
  -> Extract PDFs from Docker container via docker cp
  -> job-application-tracker skill (organize files + update Excel)
```

## Input Formats

### Excel File
Use `cover-letter-generator` skill's parse_input.py:
```bash
python .claude/skills/cover-letter-generator/scripts/parse_input.py jobs.xlsx
```

### Text File (structured)
```
COMPANY: Nokia
POSITION: Software Engineer Intern
JD:
Full job description...

---

COMPANY: Google
POSITION: Data Analyst
JD:
Another job description...
```

### Direct Text Input
Parse company and position from the JD, create temp file, run pipeline.

## Orchestration Steps

### Step 1: Send JDs via cover-letter-generator
Invoke the `cover-letter-generator` skill to:
- Parse input file
- Compute globally unique keys via `exp_lib/.next_key`
- Trigger workflow for each JD via curl (30s interval)
- Wait for completion and extract PDFs from Docker via `docker cp`
- Generate `batch_order_*.json` in `exp_lib/`
- Update `.next_key` counter

### Step 2: Verify Files
Confirm `{key}-R.pdf` and `{key}-CL.pdf` exist in `exp_lib/` with non-zero size:
- Files are extracted from Docker by cover-letter-generator (Step 3.5)
- If any missing, check `n8n_executions` for errors

### Step 3: Organize via job-application-tracker
Invoke the `job-application-tracker` skill to:
- Read order file
- Match files by key
- Move to dated folders with abbreviated names
- Update Excel tracker

### Step 4: Report
Summarize:
- Jobs processed count
- File locations: `cvs/resume and cover letters/YYYY-MM-DD/`
- Excel tracker updated

## Script (Legacy)

```bash
# From Excel file
python scripts/process_jobs.py jobs.xlsx "Company Name"

# With custom wait time
python scripts/process_jobs.py jobs.xlsx "Company" --wait-per-job 150
```

Note: Script references old agent paths. Prefer using skill orchestration directly.

## Expected Timing

| Jobs | Send Time | Generation (~90s/job) | Total    |
|------|-----------|----------------------|----------|
| 1    | 0s        | ~90s                 | ~2 min   |
| 5    | 2 min     | ~90s                 | ~3.5 min |
| 10   | 4.5 min   | ~90s                 | ~6 min   |

## Error Handling

- **cover-letter-generator fails:** Report error, do not proceed to tracker
- **Files don't appear after timeout:** Report partial completion, proceed with available files
- **job-application-tracker fails:** Report which jobs failed
