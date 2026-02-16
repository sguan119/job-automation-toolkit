---
name: linkedin-job-filter
description: LinkedIn job auto-filter tool. Uses agent-browser (--headed) to open LinkedIn job search pages, clicks each job to view full JD, calls jd-filter for evaluation, and clicks dismiss (X) button for rejected jobs. Triggers include "filter LinkedIn jobs", "linkedin job filter", or when user provides a LinkedIn Jobs search URL.
allowed-tools: Bash(agent-browser:*), Skill(jd-filter)
---

# LinkedIn Job Filter Skill

Automatically filter LinkedIn job search results by viewing each job detail, using jd-filter for evaluation, and auto-dismissing jobs that don't meet criteria.

## Use Cases

- User provides LinkedIn Jobs search results URL (e.g., `https://www.linkedin.com/jobs/search/...`)
- User says "help me filter LinkedIn jobs" or "filter LinkedIn jobs"
- User has already searched jobs on LinkedIn and wants to batch filter

## Prerequisites

- `agent-browser` installed and in PATH
- User logged into LinkedIn (requires agent-browser state or manual login)
- `jd-filter` skill's `user_filter.json` configured

## Limitations

- **No pagination support** - Only processes jobs visible on current page
- Requires user to be logged into LinkedIn (if not logged in, prompt user to login manually)

## Workflow

### Step 0: Load Filter Criteria

Read jd-filter's filter criteria:
```
.claude/skills/jd-filter/user_filter.json
```
If doesn't exist, prompt user to set filter first (using jd-filter skill).

### Step 1: Open LinkedIn Page

```bash
agent-browser --session linkedin --headed open "<linkedin-jobs-url>"
agent-browser --session linkedin wait --load networkidle
agent-browser --session linkedin wait 3000
```

**Important:** Must use `--headed`, user needs to see browser window.

### Step 2: Check Login Status

```bash
agent-browser --session linkedin snapshot -i
```

Check snapshot output:
- If see "Sign in" / "Join now" buttons → Prompt user to login manually
- If see job listings → Continue to next step

If login required:
1. Prompt user to manually complete login in browser
2. Wait for user to confirm logged in
3. Re-navigate to job search URL
4. Snapshot again to confirm

### Step 3: Get Job Listings

```bash
agent-browser --session linkedin snapshot -i
```

From snapshot, identify all job cards. LinkedIn search results typically contain:
- Job title link (clickable)
- Company name
- Location
- Posted time
- Dismiss button (X icon)

Record for each job:
- **title_ref**: Job title's @ref (for clicking to view details)
- **dismiss_ref**: X button's @ref (for dismissing unqualified jobs)
- **title_text**: Job title text
- **company_text**: Company name

Save all job info to in-memory list, ready to process one by one.

### Step 4: Process Each Job

For each job in the list, execute the following workflow:

#### 4a: Click Job to View Details

```bash
agent-browser --session linkedin click @title_ref
agent-browser --session linkedin wait --load networkidle
agent-browser --session linkedin wait 2000
```

After clicking, LinkedIn right panel will display job details.

#### 4b: Extract JD Text

```bash
agent-browser --session linkedin snapshot -i
```

From snapshot, find job description area. LinkedIn JD is usually in:
- Under `jobs-description__content` class
- Or under `jobs-box__html-content` class

After finding JD content's @ref:
```bash
agent-browser --session linkedin get text @jd_ref
```

Also extract:
- Job title
- Company name
- Location
- Job type (Full-time, Contract, etc.)
- Remote/Hybrid/On-site

#### 4c: Call jd-filter for Evaluation

Pass extracted JD text to jd-filter for evaluation. jd-filter will return:
- **PASS** - Job meets user requirements
- **REJECT** - Job doesn't meet user requirements

#### 4d: Handle Filter Results

**If REJECT:**
1. Find the dismiss (X) button for this job in current snapshot
2. Need to re-snapshot to get latest refs:
   ```bash
   agent-browser --session linkedin snapshot -i
   ```
3. Find dismiss button's @ref (usually a small X icon button in top-right corner of job card)
4. Click dismiss:
   ```bash
   agent-browser --session linkedin click @dismiss_ref
   agent-browser --session linkedin wait 1000
   ```
5. Output: `REJECT - [Job Title] @ [Company] - [Rejection Reason]`

**If PASS:**
1. Take no action, keep the job
2. Output: `PASS - [Job Title] @ [Company] - [Match Reason]`

#### 4e: Prepare for Next Job

```bash
agent-browser --session linkedin snapshot -i
```

Re-get snapshot, because dismiss action may have changed page structure and refs.
Find next unprocessed job, repeat 4a-4d.

### Step 5: Output Summary Report

After all jobs processed, output summary:

```
## LinkedIn Job Filter Report

Total Processed: X jobs
- PASS: Y jobs
- REJECT: Z jobs

### PASS Jobs:
1. [Job Title] @ [Company] - [Location]
2. ...

### REJECT Jobs:
1. [Job Title] @ [Company] - [Rejection Reason]
2. ...
```

### Step 6: Keep Browser Open

**Don't close browser** - Keep browser open after processing, user may need to continue operations.

## LinkedIn Page Structure Reference

### Job Listings Page

Typical LinkedIn search results page structure:
- Left side: Job card list (scrollable)
- Right side: Selected job's detailed information panel

### Common Elements

| Element | Description | How to Find |
|---------|-------------|-------------|
| Job Title | Clickable link | `<a>` tag in snapshot, text is job name |
| Company Name | Text | Below job title |
| Location | Text | Below company name |
| Dismiss Button | X icon | Button in top-right corner of job card, usually has `dismiss` related attribute |
| JD Content | Detail panel | Main text area in right panel |
| "Show more" Button | Expand full JD | Bottom of JD area |

### Expand Full JD

LinkedIn shows only partial JD by default, need to click "Show more" / "See more" to expand:

```bash
# Find "Show more" button in JD panel
agent-browser --session linkedin snapshot -i
# If found "Show more" / "...more" / "See more" button
agent-browser --session linkedin click @show_more_ref
agent-browser --session linkedin wait 1000
agent-browser --session linkedin snapshot -i
# Now can get full JD
agent-browser --session linkedin get text @full_jd_ref
```

## Key Principles

1. **Must use --headed** - User needs to see browser
2. **Re-snapshot after each action** - LinkedIn is SPA, DOM changes frequently
3. **Moderate speed** - Wait 1-2 seconds between jobs, avoid rate limiting
4. **Don't stop on errors** - If job extraction fails, log error and continue to next
5. **Snapshot before action** - Never use stale @ref
6. **Expand JD** - Click "Show more" to get full description before filtering
7. **Re-locate after dismiss** - After dismissing a job, list changes, need to re-snapshot
8. **Don't close browser** - Keep browser open after processing, user may continue

## Processing Efficiency Optimization

### Efficient Processing Strategy
- **Obviously irrelevant jobs**: For retail, part-time, healthcare etc. that are clearly unrelated, can dismiss based on title alone without reading full JD
- **Prioritization**: Only jobs that look promising from title need full JD reading, saves time

### Behavior After Dismiss
- After dismissing a job, LinkedIn auto-shows new job to fill the gap
- **Must track newly appeared jobs** - Don't miss jobs that appear after dismiss
- When re-snapshotting, check list and process all unprocessed jobs

## Error Handling

| Error Type | Handling |
|------------|----------|
| Not logged in | Prompt user to login manually, wait for confirmation |
| Job details load failure | Wait 3 seconds and retry once, still fails then skip |
| JD text empty | Try clicking "Show more", still empty then skip |
| Dismiss button not found | Skip dismiss, mark for manual processing |
| Page rate limit/CAPTCHA | Pause, prompt user to complete verification then continue |
| Snapshot timeout | Wait 5 seconds then retry |

## Usage Example

```
User: Help me filter jobs on this LinkedIn page https://www.linkedin.com/jobs/search/?keywords=software%20engineer&location=Toronto