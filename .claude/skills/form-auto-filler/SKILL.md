---
name: form-auto-filler
description: Auto-fill web forms using agent-browser (Vercel) with memory. Use when user provides a URL and wants to auto-fill job applications, registration forms, or any multi-page forms. Remembers user information across sessions. Triggers include "fill form", "auto fill", "apply job", "submit application", or when user provides a URL to a form page.
---

# Form Auto-Filler Skill

## Overview

This skill automates filling web forms using agent-browser CLI with a visible browser window. It remembers user information and intelligently fills forms across multiple pages.

## Core Principles

1. **Always use visible browser** - Use `--headed` flag. User must see the browser window.
2. **Memory-first approach** - Always check stored user info before asking
3. **Ask when uncertain** - If confidence < 95%, ask the user
4. **Persistent navigation** - Keep clicking "Next" / "Continue" / "Apply" until completion
5. **Error recovery** - If form submission fails due to missing fields, identify and ask user

## Workflow

### Step 1: Load User Memory

Before starting, read the user's stored information from:
```
.claude/skills/form-auto-filler/USER_MEMORY.md
```

If the file doesn't exist, create it with an empty structure.

### Step 2: Navigate to URL

Use agent-browser to open the URL provided by the user:
```bash
agent-browser open "https://example.com" --headed
```

### Step 3: Analyze the Form

For each page:
1. Use `agent-browser snapshot -i` to capture interactive elements with refs
2. Identify all form fields (input, select, textarea, checkbox, radio) from the ref list
3. Match fields to known user information

### Step 4: Fill Form Fields

For each field:
1. Check if we have the information in USER_MEMORY.md
2. If YES and confidence >= 95%: Fill automatically
3. If NO or confidence < 95%: **ASK THE USER**

**Field Mapping Strategy:**
- Name fields: firstName, lastName, fullName
- Contact: email, phone, mobile
- Address: street, city, state, zip, country
- Employment: currentCompany, currentTitle, yearsExperience
- Education: degree, university, graduationYear
- Documents: resume path, cover letter path
- Social: linkedin, github, portfolio
- Other: any custom fields

### Step 5: Ask User for Unknown Information

When asking the user:
1. Clearly state what field needs to be filled
2. Provide context (field label, placeholder text)
3. Wait for user response
4. **UPDATE USER_MEMORY.md immediately after receiving answer**

Example question format:
```
I need the following information to continue:

Field: [Field Label]
Context: [Any placeholder or hint text]
Current page: [Page title or URL]

What value should I enter?
```

### Step 6: Navigate to Next Page

After filling all fields on current page:
1. Look for and click buttons in this priority order:
   - "Apply" / "Apply Now" / "Submit Application"
   - "Next" / "Continue" / "Next Step"
   - "Submit" / "Save and Continue"
2. Wait for page load
3. Check if we're on a new page or if there are validation errors

### Step 7: Handle Validation Errors

If clicking next returns us to the same page:
1. Identify which fields have errors (look for error messages, red borders)
2. Ask user for the missing/incorrect information
3. Update USER_MEMORY.md
4. Re-fill the field
5. Try navigating again

### Step 8: Completion Detection

Form is complete when:
- Confirmation page is shown (thank you, application submitted, etc.)
- No more "Next" or "Submit" buttons
- URL contains "confirmation", "success", "thank-you"

## Agent-Browser Commands

### Essential Commands

```bash
# Navigate to URL (visible browser)
agent-browser open "https://example.com" --headed

# Get page snapshot (interactive elements only - saves tokens)
agent-browser snapshot -i

# Fill a text field using ref from snapshot
agent-browser fill @e2 "user@email.com"

# Click a button using ref
agent-browser click @e1

# Select dropdown option
agent-browser select @e7 "Canada"

# Check checkbox
agent-browser check @e6

# Type text (keystroke by keystroke)
agent-browser type @e4 "some text"

# Get current URL
agent-browser get url

# Get element text
agent-browser get text @e5

# Take screenshot for verification
agent-browser screenshot form-progress.png
```

### Waiting for Elements

```bash
# Wait for page to fully load, then snapshot
agent-browser wait --load networkidle && agent-browser snapshot -i
```

### File Upload

For file uploads, use the ref from the snapshot:
```bash
# Note: file upload support depends on agent-browser version
# If direct upload not supported, alert user to upload manually
```

## User Memory Structure

The USER_MEMORY.md file should be structured as:

```markdown
# User Information Memory

## Personal Information
- First Name:
- Last Name:
- Full Name:
- Email:
- Phone:
- Date of Birth:

## Address
- Street Address:
- City:
- State/Province:
- Postal/ZIP Code:
- Country:

## Employment
- Current Company:
- Current Job Title:
- Years of Experience:
- Desired Salary:
- Available Start Date:

## Education
- Highest Degree:
- University/College:
- Field of Study:
- Graduation Year:
- GPA:

## Documents
- Resume Path:
- Cover Letter Path:

## Online Profiles
- LinkedIn URL:
- GitHub URL:
- Portfolio URL:
- Personal Website:

## Work Authorization
- Authorized to Work:
- Require Sponsorship:
- Citizenship:

## Additional Information
- Languages:
- Skills:
- Certifications:

## Custom Fields
(Add any site-specific fields here as they are learned)
```

## Important Rules

1. **NEVER guess sensitive information** - Always ask for SSN, banking info, passwords
2. **NEVER submit without user confirmation** on final page
3. **ALWAYS update USER_MEMORY.md** when learning new information
4. **ALWAYS show browser window** - use `--headed` flag
5. **ALWAYS click Apply/Submit buttons** when they appear
6. **ALWAYS continue to next page** until form is complete

## Error Handling

| Error Type | Action |
|------------|--------|
| Field validation error | Read error message, ask user for correct value |
| Page timeout | Retry navigation, if fails ask user |
| Element not found | Use snapshot to find alternative ref |
| File upload fails | Ask user to verify file path exists |
| CAPTCHA detected | Alert user to solve manually, then continue |

## Session Flow Example

```
1. User provides URL: "https://careers.company.com/apply/12345"
2. Load USER_MEMORY.md
3. agent-browser open "https://careers.company.com/apply/12345" --headed
4. agent-browser snapshot -i → identify fields and refs
5. Fill known fields automatically using refs
6. Ask: "What is your desired salary for this position?"
7. User responds: "$120,000"
8. Update USER_MEMORY.md with salary
9. agent-browser fill @e8 "$120,000"
10. agent-browser click @e12 (Next button)
11. agent-browser wait --load networkidle && agent-browser snapshot -i
12. New page loads, repeat steps 4-11
13. Final page: "Click Submit to complete application?"
14. User confirms
15. agent-browser click @e5 (Submit button)
16. agent-browser snapshot -i → confirm success page shown
17. Report completion to user
18. agent-browser close
```

## Updating This Skill

After each session, if new field types are discovered:
1. Add them to the Custom Fields section in USER_MEMORY.md
2. Consider updating this SKILL.md with new field mappings
