# Site Configuration Templates

Pre-configured settings for popular Workday-based career sites.

## How to Use

1. Copy the configuration for your target company
2. Modify the URL filters if needed (location, job type, etc.)
3. Provide to the agent when extracting jobs

## Banking & Financial Services

### CIBC (Canadian Imperial Bank of Commerce)

```javascript
{
  companyName: 'cibc',
  displayName: 'CIBC',

  // Campus Jobs - Canada
  baseUrl: 'https://cibc.wd3.myworkdayjobs.com/campus?locations=6ae210a714361001bdc6974bfa8c0000',

  // Technology Jobs - Toronto
  // baseUrl: 'https://cibc.wd3.myworkdayjobs.com/search?jobFamilyGroup=0c40f6bd1d8f10ae43ffaefd46dc7e78&locations=efa710d70dcc1001901a2e8aa5190000',

  pageWaitTime: 5000,
  jobWaitTime: 3000,
  requestInterval: 1000,
}
```

### RBC (Royal Bank of Canada)

```javascript
{
  companyName: 'rbc',
  displayName: 'RBC',

  // All Jobs - Canada
  baseUrl: 'https://jobs.rbc.com/ca/en/search-results?location=Canada',

  // Technology Jobs - Toronto
  // baseUrl: 'https://jobs.rbc.com/ca/en/search-results?location=Toronto&category=Technology',

  pageWaitTime: 5000,
  jobWaitTime: 3000,
  requestInterval: 1000,
}
```

### TD Bank

```javascript
{
  companyName: 'td',
  displayName: 'TD Bank',

  // Campus Jobs - Canada
  baseUrl: 'https://jobs.td.com/en-CA/campus/jobs/',

  // Technology Jobs
  // baseUrl: 'https://jobs.td.com/en-CA/jobs/?category=Technology&location=Canada',

  pageWaitTime: 5000,
  jobWaitTime: 3000,
  requestInterval: 1000,
}
```

### BMO (Bank of Montreal)

```javascript
{
  companyName: 'bmo',
  displayName: 'BMO',

  // Campus Jobs - Canada
  baseUrl: 'https://jobs.bmo.com/ca/en/search-results?category=Campus',

  // All Jobs - Toronto
  // baseUrl: 'https://jobs.bmo.com/ca/en/search-results?location=Toronto',

  pageWaitTime: 5000,
  jobWaitTime: 3000,
  requestInterval: 1000,
}
```

### Scotiabank

```javascript
{
  companyName: 'scotiabank',
  displayName: 'Scotiabank',

  // Campus Jobs - Canada
  baseUrl: 'https://jobs.scotiabank.com/search/?q=&locationsearch=Canada&optionsFacetsDD_department=Campus',

  pageWaitTime: 5000,
  jobWaitTime: 3000,
  requestInterval: 1000,
}
```

## Technology Companies

### Nokia

```javascript
{
  companyName: 'nokia',
  displayName: 'Nokia',

  // All Jobs - Canada
  baseUrl: 'https://jobs.nokia.com/jobs?location=Canada',

  // Software Jobs - Canada
  // baseUrl: 'https://jobs.nokia.com/jobs?location=Canada&category=Software',

  // Research Jobs - Ottawa
  // baseUrl: 'https://jobs.nokia.com/jobs?location=Ottawa&category=Research',

  pageWaitTime: 5000,
  jobWaitTime: 3000,
  requestInterval: 1000,
}
```

### IBM Canada

```javascript
{
  companyName: 'ibm',
  displayName: 'IBM Canada',

  // All Jobs - Canada
  baseUrl: 'https://www.ibm.com/employment/search/?country=CA',

  pageWaitTime: 6000,  // IBM pages load slower
  jobWaitTime: 4000,
  requestInterval: 1500,
}
```

### Microsoft Canada

```javascript
{
  companyName: 'microsoft',
  displayName: 'Microsoft Canada',

  // All Jobs - Canada
  baseUrl: 'https://jobs.careers.microsoft.com/global/en/search?lc=Canada',

  // Software Engineering - Vancouver
  // baseUrl: 'https://jobs.careers.microsoft.com/global/en/search?lc=Vancouver&pf=Software%20Engineering',

  pageWaitTime: 5000,
  jobWaitTime: 3000,
  requestInterval: 1000,
}
```

## Telecommunications

### Bell Canada

```javascript
{
  companyName: 'bell',
  displayName: 'Bell Canada',

  // Campus Jobs - Ontario
  baseUrl: 'https://bell.wd3.myworkdayjobs.com/Campus?locations=f34f40ef4a6e016dd65e44ec75510000',

  // All Jobs - Quebec
  // baseUrl: 'https://bell.wd3.myworkdayjobs.com/Bell_External_Career_Site?locations=f34f40ef4a6e016dd65e44ec75510001',

  pageWaitTime: 5000,
  jobWaitTime: 3000,
  requestInterval: 1000,
}
```

### Rogers Communications

```javascript
{
  companyName: 'rogers',
  displayName: 'Rogers Communications',

  // All Jobs - Canada
  baseUrl: 'https://jobs.rogers.com/ca/en/search-results?location=Canada',

  // Technology Jobs - Toronto
  // baseUrl: 'https://jobs.rogers.com/ca/en/search-results?location=Toronto&category=Technology',

  pageWaitTime: 5000,
  jobWaitTime: 3000,
  requestInterval: 1000,
}
```

### Telus

```javascript
{
  companyName: 'telus',
  displayName: 'Telus',

  // All Jobs - Canada
  baseUrl: 'https://telus.taleo.net/careersection/10000/jobsearch.ftl?lang=en',

  pageWaitTime: 6000,  // Taleo loads slower
  jobWaitTime: 4000,
  requestInterval: 1500,
}
```

## Retail & Consumer

### Best Buy Canada

```javascript
{
  companyName: 'bestbuy',
  displayName: 'Best Buy Canada',

  // Corporate Jobs - Canada
  baseUrl: 'https://jobs.bestbuy.com/bby?domain=bestbuy.com&country=Canada&job_type=Corporate',

  pageWaitTime: 5000,
  jobWaitTime: 3000,
  requestInterval: 1000,
}
```

### Walmart Canada

```javascript
{
  companyName: 'walmart',
  displayName: 'Walmart Canada',

  // All Jobs - Canada
  baseUrl: 'https://careers.walmart.com/results?q=&page=1&sort=rank&jobLocation=Canada',

  pageWaitTime: 5000,
  jobWaitTime: 3000,
  requestInterval: 1000,
}
```

### Loblaws

```javascript
{
  companyName: 'loblaws',
  displayName: 'Loblaws Companies Limited',

  // Corporate Jobs - Ontario
  baseUrl: 'https://jobs.loblaw.ca/search-jobs?orgIds=1&ac=19091&alp=6252001-5909050&alt=3',

  pageWaitTime: 5000,
  jobWaitTime: 3000,
  requestInterval: 1000,
}
```

## Healthcare & Pharma

### Shoppers Drug Mart / Pharmaprix

```javascript
{
  companyName: 'shoppers',
  displayName: 'Shoppers Drug Mart',

  // Corporate Jobs - Canada
  baseUrl: 'https://jobs.shoppersdrugmart.ca/en/corporate-jobs',

  pageWaitTime: 5000,
  jobWaitTime: 3000,
  requestInterval: 1000,
}
```

## Government & Public Sector

### Government of Canada

```javascript
{
  companyName: 'gc',
  displayName: 'Government of Canada',

  // All Jobs - IT category
  baseUrl: 'https://www.canada.ca/en/services/jobs/opportunities/government.html',

  // Note: GC jobs may require custom handling (not Workday)
  pageWaitTime: 7000,
  jobWaitTime: 5000,
  requestInterval: 2000,
}
```

## Energy & Utilities

### Hydro One

```javascript
{
  companyName: 'hydroone',
  displayName: 'Hydro One',

  // All Jobs - Ontario
  baseUrl: 'https://www.hydroone.com/careers',

  pageWaitTime: 5000,
  jobWaitTime: 3000,
  requestInterval: 1000,
}
```

## Insurance

### Manulife

```javascript
{
  companyName: 'manulife',
  displayName: 'Manulife',

  // All Jobs - Canada
  baseUrl: 'https://jobs.manulife.com/ca/en/search-results?location=Canada',

  pageWaitTime: 5000,
  jobWaitTime: 3000,
  requestInterval: 1000,
}
```

### Sun Life

```javascript
{
  companyName: 'sunlife',
  displayName: 'Sun Life',

  // All Jobs - Canada
  baseUrl: 'https://sunlife.wd3.myworkdayjobs.com/Campus?locations=2c8e9f4c0ec401000176c06b64be0000',

  pageWaitTime: 5000,
  jobWaitTime: 3000,
  requestInterval: 1000,
}
```

## Performance Configurations

### Fast Configuration (Good Network)

Use this for fast, reliable internet connections:

```javascript
{
  pageWaitTime: 3000,       // 3 seconds
  jobWaitTime: 2000,        // 2 seconds
  requestInterval: 500,     // 0.5 seconds
  maxRetries: 3,
  retryDelay: 2000,
  saveProgressInterval: 10,
  minJDLength: 500,
}
```

**Expected Performance:**
- ~200 jobs in 10-12 minutes
- Success rate: 98-99%

### Stable Configuration (Moderate Network)

Default configuration for most scenarios:

```javascript
{
  pageWaitTime: 5000,       // 5 seconds
  jobWaitTime: 3000,        // 3 seconds
  requestInterval: 1000,    // 1 second
  maxRetries: 3,
  retryDelay: 2000,
  saveProgressInterval: 10,
  minJDLength: 500,
}
```

**Expected Performance:**
- ~200 jobs in 15-18 minutes
- Success rate: 99%+

### Slow Configuration (Poor Network or Unstable Site)

Use for slow internet or sites with slow response times:

```javascript
{
  pageWaitTime: 7000,       // 7 seconds
  jobWaitTime: 5000,        // 5 seconds
  requestInterval: 2000,    // 2 seconds
  maxRetries: 5,
  retryDelay: 3000,
  saveProgressInterval: 5,  // Save more frequently
  minJDLength: 500,
}
```

**Expected Performance:**
- ~200 jobs in 25-30 minutes
- Success rate: 99.5%+
- More stable, fewer failures

## Custom URL Filters

### Filter by Location

Most Workday sites use location IDs in the URL:

```
# Toronto
?locations=efa710d70dcc1001901a2e8aa5190000

# Vancouver
?locations=bc33aa3152ec42d4995f4791a106ed09

# Montreal
?locations=bc33aa3152ec42d4995f4791a106ed0a

# Ontario (Province)
?locations=f34f40ef4a6e016dd65e44ec75510000

# Canada (Country)
?locations=6ae210a714361001bdc6974bfa8c0000
```

**How to get location ID:**
1. Go to company's career site
2. Apply location filter
3. Copy the `locations=` parameter from URL

### Filter by Job Family / Category

```
# Technology
?jobFamilyGroup=0c40f6bd1d8f10ae43ffaefd46dc7e78

# Engineering
?jobFamilyGroup=0c40f6bd1d8f10ae43ffaefd46dc7e79

# Finance
?jobFamilyGroup=0c40f6bd1d8f10ae43ffaefd46dc7e7a
```

**How to get job family ID:**
1. Apply job category filter on career site
2. Copy the `jobFamilyGroup=` parameter from URL

### Filter by Job Type

```
# Full-time
?jobType=Full%20time

# Intern
?jobType=Intern

# Contract
?jobType=Contract
```

### Combine Multiple Filters

```
# Example: CIBC Technology Jobs in Toronto, Full-time
https://cibc.wd3.myworkdayjobs.com/search?jobFamilyGroup=0c40f6bd1d8f10ae43ffaefd46dc7e78&locations=efa710d70dcc1001901a2e8aa5190000&jobType=Full%20time
```

## Workday Selector Reference

Common Workday selectors (usually consistent across sites):

```javascript
{
  selectors: {
    // Job listing page
    jobListing: '[data-automation-id="jobTitle"]',
    jobLocation: '[data-automation-id="locations"]',
    jobPostedDate: '[data-automation-id="postedOn"]',
    nextPage: '[data-uxi-widget-type="paginationNext"]',

    // Job detail page
    jobDescription: '[data-automation-id="jobPostingDescription"]',
    jobDetails: '[data-automation-id="job-details"]',
    applyButton: '[data-automation-id="applyButton"]',

    // Additional fields
    timeType: '[data-automation-id="timeType"]',
    employmentType: '[data-automation-id="workerSubType"]',
    weeklyHours: '[data-automation-id="scheduledWeeklyHours"]',
    applicationDeadline: '[data-automation-id="requisitionPostingEndDate"]',
  }
}
```

**Note**: These selectors are standard across most Workday sites. If a specific site has custom selectors, they can be overridden in the configuration.

## Troubleshooting Site-Specific Issues

### CIBC
- **Issue**: Some job pages load very slowly
- **Solution**: Increase `jobWaitTime` to 5000ms

### Nokia
- **Issue**: Pagination may skip some jobs
- **Solution**: Increase `pageWaitTime` to 6000ms, add extra scroll before clicking next

### Bell
- **Issue**: French-language job descriptions
- **Solution**: Filter by language or use bilingual extraction

### RBC
- **Issue**: External redirect for some jobs
- **Solution**: Handle redirects by checking URL change

### TD
- **Issue**: Some jobs require login to view full JD
- **Solution**: Extract what's available without login, flag restricted jobs

## Usage Examples

### Example 1: Extract CIBC jobs with custom config

```javascript
// User request:
"Extract CIBC technology jobs in Toronto with stable configuration"

// Agent uses:
{
  companyName: 'cibc',
  displayName: 'CIBC',
  baseUrl: 'https://cibc.wd3.myworkdayjobs.com/search?jobFamilyGroup=0c40f6bd1d8f10ae43ffaefd46dc7e78&locations=efa710d70dcc1001901a2e8aa5190000',

  // Stable config
  pageWaitTime: 5000,
  jobWaitTime: 3000,
  requestInterval: 1000,
  maxRetries: 3,
  retryDelay: 2000,
}
```

### Example 2: Extract Nokia jobs with fast config

```javascript
// User request:
"Extract all Nokia jobs in Canada quickly"

// Agent uses:
{
  companyName: 'nokia',
  displayName: 'Nokia',
  baseUrl: 'https://jobs.nokia.com/jobs?location=Canada',

  // Fast config
  pageWaitTime: 3000,
  jobWaitTime: 2000,
  requestInterval: 500,
  maxRetries: 3,
}
```

### Example 3: Multiple companies in sequence

```javascript
// User request:
"Extract jobs from CIBC, RBC, and TD, then merge the results"

// Agent extracts:
1. CIBC: 285 jobs → cibc_jobs_with_jd_final.json
2. RBC: 320 jobs → rbc_jobs_with_jd_final.json
3. TD: 198 jobs → td_jobs_with_jd_final.json

// Then merges:
{
  "allJobs": [...cibc, ...rbc, ...td],
  "totalJobs": 803,
  "byCompany": {
    "cibc": 285,
    "rbc": 320,
    "td": 198
  }
}
```

---

**Last Updated**: 2026-02-07
**Version**: 1.0.0
