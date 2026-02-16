---
name: job-application-tracker
description: Organize job application materials (resume/cover letter PDFs) and maintain Excel tracking system. Reads order files from cover-letter-generator, matches files by key-based naming, creates date-based folder structure, moves files, generates abbreviated filenames, and updates Excel tracker with hyperlinks. Use when user says "organize the files", "organize resumes", "organize application materials", or after cover-letter-generator has finished generating files. Also use when user wants to update the job applications Excel tracker.
---

# Job Application Tracker

Organize generated resume/cover letter files and maintain an Excel tracking system using order files from cover-letter-generator.

## Workflow

### 1. Find Order File

Locate latest `batch_order_*.json` in `exp_lib/`:
```python
python scripts/batch_organize.py [exp_lib_dir] [cvs_dir]
```

Default paths:
- `exp_lib`: `exp_lib/` in project root
- `cvs`: `cvs/` in project root

### 2. File Matching

**Key-based (current):** Order file contains `key` field mapping to `{key}-R.pdf` and `{key}-CL.pdf`:
```
0-R.pdf  -> Job with key=0
0-CL.pdf -> Job with key=0
1-R.pdf  -> Job with key=1
```

**Timestamp-based (legacy fallback):** For order files without `key` field, matches by filename timestamp order.

### 3. Organize Files

For each matched job:
1. Create folder: `cvs/resume and cover letters/YYYY-MM-DD/Company - Position/`
2. Move (not copy) files with abbreviated names: `CompanyAbbr - PosAbbr - R.pdf`

### 4. Update Excel Tracker

For each job, add a row to `cvs/job-applications.xlsx`:

| Column | Value | Source |
|--------|-------|--------|
| Company | Company name | order file `jobs[].company` |
| Position | Job title | order file `jobs[].position` |
| Job Description | **FULL original JD text** | order file `jobs[].jd` |
| Application Date | Today (YYYY-MM-DD) | current date |
| Files | Folder path | created in step 3 |

**CRITICAL:** The "Job Description" column MUST contain the complete, unmodified JD text from the order file's `jd` field. NEVER summarize, truncate, or paraphrase. Copy the entire string as-is.

### 5. Archive Order File

Move processed order file to `exp_lib/archive/`.

## Scripts

### batch_organize.py (Batch Mode)
```bash
python scripts/batch_organize.py                          # defaults
python scripts/batch_organize.py /path/to/exp_lib /path/to/cvs  # custom paths
```
Reads order file, shows matching preview, asks confirmation, organizes all jobs.

### process_job_application.py (Single Job)
```bash
python scripts/process_job_application.py <base_dir> "<Company>" "<Position>" "<JD_Text>" [exp_lib_dir]
```
Process a single job: find latest files, organize, update Excel.

## File Naming Convention

Abbreviated names: `CompanyAbbr - PositionAbbr - R/CL.pdf`
- `FGF - AISECO - R.pdf` (FGF Brands - AI Solutions Engineer Co-Op)
- `NOK - SDE - CL.pdf` (Nokia - Software Development Engineer)

## Excel Tracker

**File:** `cvs/job-applications.xlsx`

**Columns:** Company | Position | Job Description | Application Date | Files (hyperlink)

**Job Description column:** Always the COMPLETE JD from `order_file.jobs[].jd`. Never summarize.

**Backup:** Auto-backup before every modification to `cvs/Excel/backups/`.

## Dependencies

```bash
pip install openpyxl pandas
```

## Error Handling

- **No order file:** Run cover-letter-generator first
- **Not enough files:** Partial matching, remaining jobs get empty folders
- **"Operation not permitted":** Use MCP tool `mcp__cowork__allow_cowork_file_delete`
