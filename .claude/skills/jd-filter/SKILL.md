---
name: jd-filter
description: Job description filtering and analysis tool. Analyzes JDs against user-defined filter criteria, outputs structured summaries with PASS/REJECT decisions, and saves/updates user preferences. Use when user says "analyze this JD", "is this job good", pastes a job description, or wants to "set/update my filter criteria".
---

# JD Filter - Job Description Analysis Tool

Quickly evaluate job descriptions against user-defined filter criteria and output structured summaries.

## Workflow

### 1. Check Filter at Start of Conversation

**First use or when explicitly requested:**
- Read `user_filter.json` to get user's filter criteria
- If filter not set, prompt user to configure it first

**Daily use:**
- Auto-read `user_filter.json` before analyzing JD
- No need to confirm with user each time, apply saved criteria directly

### 2. Auto-Detect and Update Filter

**Trigger conditions:**
When user mentions new filter requirements in conversation. Trigger keywords include:
- "My requirements are...", "I want...", "I don't want..."
- "Filter for...", "Only look at...", "Exclude..."
- "Salary must be...", "Location must be...", "Cannot have..."
- "Update my filter", "Modify filter criteria", "Save my preferences"

**Update process:**
1. Read current `user_filter.json`
2. Parse new requirements from user
3. Merge into existing filter (new requirements take priority)
4. Update `user_filter.json` file
5. Briefly confirm: "✅ Filter criteria updated and saved"
6. **Then continue processing JD analysis** (if user provided JD simultaneously)

**Common filter categories:**
- **location**: Location requirements (must_include, must_exclude)
- **requirements**: Hard requirements (certifications, student_status, experience, etc.)
- **application_philosophy**: Application strategy (approach, threshold, avoid list)
- **user_background**: User background (education, skills, projects)
- **ideal_positions**: List of ideal position types
- **salary_range**: Salary range
- **work_authorization**: Visa/work permit requirements
- **company_preferences**: Company preferences (size, industry, exclude list)

**Example:**
User says: "I don't want to apply to positions paying less than $25/hour"
→ Auto-update `salary_range.minimum` to 25 in `user_filter.json`
→ Reply: "✅ Filter criteria updated and saved: Minimum salary requirement $25/hour"
→ If user provided JD simultaneously, continue with analysis

### 3. Analyze JD

When user pastes a JD, process with following steps:

#### Step 1: Extract Key Information
Extract from JD:
- Location (city, remote policy)
- Job Scope (core responsibilities, 2-3 sentence summary)
- Requirements (must-have vs nice-to-have, education, experience, skills)
- Visa/Sponsorship information (if mentioned)
- Other filter-relevant information

#### Step 2: Compare Against Filter
Compare extracted information against user's filter criteria point by point.

#### Step 3: Output Results

**Output format (REJECT):**

```
## 🔴 REJECT

**Rejection Reasons:**
- [Core reason 1: Field mismatch/Skill waste/Career regression, etc.]
- [Core reason 2 (if applicable)]

**📍 Location:** [Location] (✅/❌)
**💼 Job Scope:** [1-2 sentence core responsibilities]
**📋 Requirements:** [3-5 key requirements, comma-separated]
```

**Output format (PASS):**

```
## 🟢 PASS

**📍 Location:** [Location] (✅)
**💼 Job Scope:** [1-2 sentence core responsibilities]
**📋 Requirements:** [3-5 key requirements, comma-separated]

**Match Score:** [Why suitable, 1-2 sentences]
**Application Tip:** [Cover letter key points, 1 sentence]
```

## Filtering Philosophy

User's filtering strategy:
- **Threshold**: `minimum_requirements_met` - Apply if minimum requirements are met
- **Don't over-filter**: If user meets minimum qualifications, should PASS
- **Avoid subjective judgment**: Don't judge position "quality", "whether it's real data analysis", etc.
- **Example**: If JD requires "Bachelor's in Statistics, SQL, Excel" and user has Master's in Statistics, knows SQL and Excel, even if position is mainly reporting rather than advanced analytics, should still PASS

**Common over-filtering mistakes:**
- ❌ "This position seems more like reporting than real data analysis" → PASS if user meets requirements
- ❌ "Meets requirements but position quality is low" → Not our scope to judge
- ❌ "Position tech stack not cutting-edge enough" → Only check filter compliance, don't evaluate position value

## Important Notes

- Base judgment on explicitly stated JD information, don't speculate
- If JD doesn't mention filter-relevant info (e.g., sponsorship not mentioned), mark as "Not mentioned"
- Keep summaries concise, each section within 2-3 lines
- Output in English, but preserve proper nouns from JD (position titles, company names, tech stack)
