# Form Auto-Filler Skill

An intelligent web form auto-filler using agent-browser (Vercel) with persistent memory.

## Features

- **Visible Browser**: Always shows the browser window (`--headed` mode)
- **Memory System**: Remembers all user information in USER_MEMORY.md
- **Smart Filling**: Auto-fills fields with known information
- **Confirmation Flow**: Asks when confidence < 95%
- **Multi-Page Support**: Automatically navigates through multi-page forms
- **Error Recovery**: Handles validation errors and asks for corrections
- **Apply Button Detection**: Automatically clicks Apply/Submit buttons
- **Token Efficient**: Uses ref-based snapshots for minimal context usage

## Usage

```
User: /form-auto-filler https://careers.company.com/apply/12345
```

Or simply provide a URL to a form:
```
User: Fill this form: https://jobs.example.com/apply
```

## How It Works

1. **Load Memory**: Reads stored user info from USER_MEMORY.md
2. **Navigate**: Opens URL in visible browser via `agent-browser open --headed`
3. **Analyze**: Captures interactive snapshot (`snapshot -i`), identifies form fields by refs
4. **Fill**: Matches fields to known user data, fills using `agent-browser fill @ref`
5. **Ask**: Prompts user for unknown or uncertain information
6. **Update Memory**: Saves new information for future use
7. **Navigate**: Clicks Next/Continue/Apply buttons via refs
8. **Repeat**: Continues until form is complete

## Agent-Browser Requirements

This skill requires agent-browser to be installed globally:

```bash
npm install -g agent-browser
agent-browser install    # downloads bundled Chromium
```

No MCP server configuration needed - agent-browser works via direct CLI/Bash calls.

## File Structure

```
form-auto-filler/
├── SKILL.md        # Main skill instructions
├── USER_MEMORY.md  # Stored user information
└── README.md       # This file
```

## Button Priority

When looking for navigation buttons, the skill checks in this order:

1. Apply / Apply Now / Submit Application
2. Next / Continue / Next Step
3. Submit / Save and Continue
4. (Chinese variants)

## Memory Categories

- Personal Information
- Address
- Employment (Current & Desired)
- Education
- Documents (Resume, Cover Letter)
- Online Profiles
- Work Authorization
- Skills & Languages
- References
- Custom Fields (learned during sessions)

## Security Notes

- Never stores passwords or SSN
- Always asks for sensitive financial information
- Requires user confirmation on final submission
- All data stored locally in USER_MEMORY.md
