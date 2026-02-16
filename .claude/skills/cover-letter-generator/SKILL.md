---
name: cover-letter-generator
description: Batch process job descriptions by triggering the n8n cover-letter-generator workflow via n8n MCP tools. Reads JDs from Excel/text files, triggers workflow for each JD with intervals, generates order files for tracking. Use when the user wants to generate cover letters and resumes for multiple positions. Triggers include "batch generate these", "process these JDs", "generate cover letters for these positions", "send job descriptions to n8n", or when the user provides multiple job descriptions for batch processing.
---

# Cover Letter Generator

Batch process multiple JDs by triggering the n8n cover-letter-generator workflow via MCP tools.

## Workflow

### 1. Parse Input File

**Excel (.xlsx/.xls):**
```bash
python scripts/parse_input.py jobs.xlsx
```
- Auto-detects columns: `Job Title`/`Position`, `Full JD`/`Job Description`, `Company`
- Filters for `PASS` if `Filter Result` column exists
- Outputs JSON array to stdout

**Text (.txt):**
```bash
python scripts/parse_input.py jds.txt "CompanyName"
```
- Format: sections separated by `---`, with `COMPANY:`, `POSITION:`, `JD:` headers
- Second arg is default company name

**Output format:**
```json
[{"company": "X", "position": "Y", "jd": "..."}]
```

### 2. Find the Workflow

Use n8n MCP to locate the cover-letter-generator workflow:
```
n8n_list_workflows → search for "cover-letter" or "Cover Letter Generator"
```
Note the `workflowId` for triggering.

If workflow not found, inform user to check n8n.

### 2.5. Compute Unique Keys

Keys MUST be globally unique across all batches. Read the counter file to determine starting key:

```bash
# Read next available key (default 0 if file doesn't exist)
cat exp_lib/.next_key 2>/dev/null || echo 0
```

Assign keys sequentially: if starting key is 15 and batch has 3 jobs, keys are 15, 16, 17.

After generating the order file (Step 4), update the counter:
```bash
echo <next_unused_key> > exp_lib/.next_key
```

Example: batch used keys 15-17, write `18` to `.next_key`.

### 3. Trigger Workflow for Each JD

**CRITICAL: Use `curl` in background, NOT `n8n_test_workflow` MCP tool.**

The webhook uses `responseMode: lastNode` and takes ~85 seconds to complete. The MCP `n8n_test_workflow` tool has a 30-second timeout and will report "No response" even though the workflow was successfully triggered. This leads to duplicate triggers and wasted API credits.

For each job, trigger via curl in the Bash tool (run_in_background=true):
```bash
curl -X POST "http://localhost:5678/webhook/cover-letter-generator" \
  -H "Content-Type: application/json" \
  -d '{"jobDescription": "<full JD text>", "key": <globally_unique_key>}' \
  --max-time 300
```

**Important:**
- Use the globally unique key from Step 2.5, NOT a 0-based index
- Wait **30 seconds** between each trigger to avoid overwhelming n8n
- Report progress: `[1/N] Key=15 | Company - Position... Sent`
- **NEVER retry** if curl times out — check execution status first (see Step 3.5)
- If a trigger fails, check `n8n_executions` before retrying

### 3.5. Wait for Completion & Extract PDFs

After triggering all JDs, wait ~90 seconds per job, then verify completion:
```javascript
n8n_executions({
  action: "list",
  workflowId: "<workflow-id>",
  limit: <number_of_jobs_sent>
})
```

Confirm all executions show `status: "success"`. If any show `status: "error"`, check details before retrying.

**Extract PDFs from Docker container** (PDFs are generated inside `n8n-n8n-1` container):
```bash
docker cp n8n-n8n-1:/home/node/.n8n-files/data/<key>-R.pdf exp_lib/<key>-R.pdf
docker cp n8n-n8n-1:/home/node/.n8n-files/data/<key>-CL.pdf exp_lib/<key>-CL.pdf
```

Do this for each key. Verify file sizes are non-zero.

### 4. Generate Order File

After all JDs are sent, write the order file using the Write tool to `exp_lib/batch_order_<timestamp>.json`:

```json
{
  "batch_id": "2026-01-27_16-45-00",
  "created_at": "2026-01-27T16:45:00",
  "total_jobs": 2,
  "interval_seconds": 30,
  "jobs": [
    {
      "key": 15,
      "order": 1,
      "sent_at": "2026-01-27T16:45:00",
      "company": "Company A",
      "position": "Job Title A",
      "jd": "...",
      "status": "sent",
      "expected_files": {
        "resume": "15-R.pdf",
        "cover_letter": "15-CL.pdf"
      }
    },
    {
      "key": 16,
      "order": 2,
      "sent_at": "2026-01-27T16:45:30",
      "company": "Company B",
      "position": "Job Title B",
      "jd": "...",
      "status": "sent",
      "expected_files": {
        "resume": "16-R.pdf",
        "cover_letter": "16-CL.pdf"
      }
    }
  ]
}
```

### 5. Report Summary

Print summary:
- Total sent / failed count
- Order file path
- Remind user: wait ~2-3 min per job for n8n to generate PDFs
- Next step: use `job-application-tracker` skill to organize files

## Notes

- **DO NOT use `n8n_test_workflow`** — it will timeout and mislead you into retrying
- 30-second interval between triggers prevents overwhelming n8n's async processing
- Each trigger starts async generation (~85 seconds per JD)
- Order file enables correct file-to-position matching
- PDF naming: `{key}-R.pdf` (resume), `{key}-CL.pdf` (cover letter)
- PDFs are generated inside Docker container `n8n-n8n-1` at `/home/node/.n8n-files/data/`
- Must use `docker cp` to extract PDFs to local `exp_lib/` before organizing
- Workflow ID for Cover Letter Generator: `O77JGewQqhwqvBdZ2LzYa`
