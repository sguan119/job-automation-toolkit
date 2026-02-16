---
name: batch-jd-processor
description: Batch job description processor using MANUAL REVIEW by parallel subagents. NO automated scripts allowed. Reads Excel/CSV with job data, splits into groups, launches max subagents for human-like analysis against user filter criteria. Outputs color-coded Excel with PASS/REJECT/ERROR classifications and detailed reasoning. Triggers include "批量处理这些JD", "帮我筛选这些职位", "处理Excel里的职位", "batch filter jobs", "用batch jd process".
---

# Batch JD Processor

Process job batches through **parallel manual review** by subagents. Each subagent reads jobs like a human and applies user's filter criteria.

## Core Rules

### ⛔ Prohibitions
- NO automated scripts (no `filter_all_jobs.py`, no regex scripts)
- NO keyword extraction scripts

### ✅ Required Approach
- Split jobs into groups (5 per group)
- Launch ALL subagents in SINGLE message
- Each subagent manually reads every job (5 jobs per agent)
- Provide detailed reasoning for every decision

## Three-Tier Classification

**PASS** - Meets all criteria, recommend applying
**REJECT** - Fails filter criteria (location/experience/cert/position type)
**ERROR** - Cannot evaluate (missing JD, corrupted data, missing fields)

**Critical:** Use ERROR for data problems, REJECT for criteria failures.

Examples:
```json
{"filter_result": "ERROR", "reason": "JD内容缺失，无法评估职位要求"}
{"filter_result": "REJECT", "reason": "要求3年经验，用户需要0年entry-level"}
{"filter_result": "PASS", "reason": "Entry-level Data Analyst，匹配理想岗位，位于Toronto"}
```

## Workflow

### Step 0: Display Filter Criteria
Read and display `user_filter.json` showing location, experience, certifications, ideal positions, avoid categories.

### Step 1: Load Data
Parse Excel/CSV into JSON for subagents:
```python
import pandas as pd, json

df = pd.read_csv('input.csv') if file.endswith('.csv') else pd.read_excel('input.xlsx')
jobs = [{
    'job_id': str(row.get('Job ID', f'job_{idx}')),
    'title': row.get('Title', ''),
    'location': row.get('Location', ''),
    'url': row.get('URL', ''),
    'full_jd': row.get('Job Description', ''),
    'posted_date': row.get('Posted Date', '')
} for idx, row in df.iterrows()]

with open('all_jobs.json', 'w', encoding='utf-8') as f:
    json.dump(jobs, f, indent=2, ensure_ascii=False)
```

### Step 2: Split into Groups
Calculate subagents: **num_agents = JD总数 / 5** (每个agent处理5个JD)

```python
import math
num_agents = max(1, math.ceil(len(jobs) / 5))  # 每5个JD分配1个agent
jobs_per_agent = math.ceil(len(jobs) / num_agents)

for i in range(num_agents):
    group = jobs[i*jobs_per_agent : (i+1)*jobs_per_agent]
    with open(f'jobs_group_{i+1}.json', 'w', encoding='utf-8') as f:
        json.dump(group, f, indent=2, ensure_ascii=False)
```

### Step 3: Launch Subagents (In SINGLE Message)

**Prompt template for each subagent:**
```
Review Group {N}: /path/to/jobs_group_{N}.json
Filter: /path/to/user_filter.json

For EACH job:
1. Check data quality first - Missing JD/fields? → ERROR
2. Read title and full JD carefully
3. Check ALL criteria: location, experience, certs, position type, avoid categories
4. Classify as PASS/REJECT/ERROR with specific reason

Output JSON: [{job_id, title, url, location, filter_result, reason}]
Save to: /path/to/group_{N}_results.json

Rules:
- NO scripts, manual reading only
- ERROR for data issues, REJECT for criteria failures
- Specific reasons (e.g. "要求2年经验" not "不符合")
```

### Step 4: Merge & Generate Excel

```python
import json, pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Font, Alignment

# Merge results
all_results = []
for i in range(1, num_agents + 1):
    with open(f'group_{i}_results.json', 'r', encoding='utf-8') as f:
        all_results.extend(json.load(f))

# Statistics
pass_count = sum(1 for r in all_results if r['filter_result'] == 'PASS')
reject_count = sum(1 for r in all_results if r['filter_result'] == 'REJECT')
error_count = sum(1 for r in all_results if r['filter_result'] == 'ERROR')

# Create Excel
df = pd.DataFrame(all_results)
df['sort_key'] = df['filter_result'].map({'PASS': 0, 'REJECT': 1, 'ERROR': 2})
df = df.sort_values('sort_key').drop('sort_key', axis=1)
df.to_excel('output.xlsx', index=False)

# Color code
wb = load_workbook('output.xlsx')
ws = wb.active
green = PatternFill(start_color='C6EFCE', end_color='C6EFCE', fill_type='solid')
red = PatternFill(start_color='FFC7CE', end_color='FFC7CE', fill_type='solid')
yellow = PatternFill(start_color='FFEB9C', end_color='FFEB9C', fill_type='solid')

for row in ws.iter_rows(min_row=2):
    result = row[4].value
    row[4].fill = green if result == 'PASS' else red if result == 'REJECT' else yellow

wb.save('output.xlsx')
```

### Step 5: Present Results

```
📊 批量筛选完成！
总职位: {total} | ✅ PASS: {pass} | ❌ REJECT: {reject} | ⚠️ ERROR: {error}

🎯 推荐申请职位（Top 5）:
[List PASS jobs with title, location, reason, URL]

📋 拒绝原因统计:
[Group REJECT by reason with counts]

⚠️ 错误统计:
[Group ERROR by reason with counts]

[Excel download link]
```

## Subagent Quality Checklist

✅ Read data quality first (missing JD → ERROR, not REJECT)
✅ Read full job description, don't skim
✅ Check ALL criteria (location, experience, certs, position type, avoid)
✅ Specific reasoning ("要求3年经验" not "不符合要求")
✅ Handle edge cases (bilingual, "Associate" titles, "preferred" vs "required")

## Common Mistakes

❌ Using scripts instead of manual review
❌ Launching subagents sequentially (launch ALL in one message)
❌ Vague reasoning
❌ ERROR for criteria failures (use ERROR only for data issues)

## Performance

| Batch Size | Agents | Jobs/Agent | Estimated Time |
|------------|--------|------------|----------------|
| 25         | 5      | 5          | 2-3min |
| 50         | 10     | 5          | 3-5min |
| 100        | 20     | 5          | 5-8min |
| 200        | 40     | 5          | 10-15min |

Manual review is slower than scripts but catches nuances and context-dependent requirements. Each agent processes exactly 5 JDs for consistent workload distribution.
