# JD Extraction - Lessons Learned

Only actionable insights that improve future extractions. Focus on: what failed, what worked, how to improve.

## Critical Rules for Workday Extractions

### ✅ ALWAYS DO
1. **Use `agent-browser eval` with DOM selector** - NOT `get text` + regex
   ```javascript
   agent-browser eval "document.querySelector('[data-automation-id=\"jobPostingDescription\"]')?.innerText || ''"
   ```
2. **Use Opus 4.6 model** for complex extractions (71+ jobs)
3. **Add 2s delay** after page load for dynamic content
4. **Delete progress files** before fresh extraction to avoid misalignment

### ❌ NEVER DO
1. **Don't use `get text body` + regex parsing** - fails after ~20 jobs due to:
   - Browser session becomes unstable with repeated navigation
   - Regex patterns are fragile, break on page structure changes
   - No direct DOM access causes state loss
2. **Don't use Sonnet 4.5** for large Workday extractions - demonstrated 47.5% success rate vs Opus's 100%

## Failures & Solutions

### Element Fleet - 2026-02-11 (Sonnet 4.5 FAILED)
- **Issue**: Used `get text` + regex method, failed 21/40 jobs (47.5% success)
  - Only found 40 jobs instead of 71 (incomplete pagination)
  - Browser session lost after 19 jobs
  - Errors: `ERR_ABORTED`, `Link not found`
- **Root cause**: Text parsing method requires multiple page interactions, accumulating instability
- **Solution**: Switched to Opus 4.6 with `eval` method
- **Result**: 71/71 jobs (100% success), 5s per job, complete JD avg 4950 chars

### Element Fleet - 2026-02-11 (Opus 4.6 SUCCESS)
- **Method**: `agent-browser eval` with `data-automation-id="jobPostingDescription"`
- **Result**: 71/71 (100%), Min 2917 chars, Max 12336 chars, Avg 4950 chars
- **Timing**: ~5s per job, ~6 min total for 71 jobs
- **Key**: Direct DOM access = atomic operation, no state loss

## Model Selection Rule

| Jobs | Complexity | Model |
|------|------------|-------|
| < 30 | Simple | Sonnet OK |
| 30-70 | Medium | **Opus recommended** |
| 70+ | Complex | **Opus required** |

**Why Opus wins**: Better strategy selection, implements proven `eval` method instead of fragile regex parsing.
