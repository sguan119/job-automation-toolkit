#!/usr/bin/env python3
"""
Parse job descriptions from Excel or text files.
Outputs JSON array to stdout for use by Claude MCP workflow.
"""

import sys
import json
import os


def process_excel(excel_path):
    """Read jobs from Excel file. Requires pandas + openpyxl."""
    try:
        import pandas as pd
    except ImportError:
        print("Error: pandas required. Install with: pip install pandas openpyxl", file=sys.stderr)
        sys.exit(1)

    df = pd.read_excel(excel_path)

    jd_col = position_col = company_col = filter_col = None

    for col in df.columns:
        col_lower = col.lower()
        if 'full jd' in col_lower or 'job description' in col_lower or col_lower == 'jd':
            jd_col = col
        elif 'position' in col_lower or 'job title' in col_lower or 'title' in col_lower:
            position_col = col
        elif 'company' in col_lower:
            company_col = col
        elif 'filter' in col_lower or 'result' in col_lower:
            filter_col = col

    if not jd_col:
        print(f"Error: No JD column found. Available: {df.columns.tolist()}", file=sys.stderr)
        sys.exit(1)
    if not position_col:
        print(f"Error: No Position column found. Available: {df.columns.tolist()}", file=sys.stderr)
        sys.exit(1)

    if filter_col:
        df = df[df[filter_col] == 'PASS']

    jobs = []
    for _, row in df.iterrows():
        company = str(row[company_col]) if company_col and pd.notna(row[company_col]) else "Unknown Company"
        position = str(row[position_col]) if pd.notna(row[position_col]) else "Unknown Position"
        jd = str(row[jd_col]) if pd.notna(row[jd_col]) else ""
        if jd.strip():
            jobs.append({"company": company, "position": position.replace('/', '-'), "jd": jd})

    return jobs


def process_text(filepath, default_company="Unknown Company"):
    """Read jobs from text file with COMPANY/POSITION/JD format."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    jobs = []
    for section in content.split('\n---\n'):
        section = section.strip()
        if not section:
            continue

        company = default_company
        position = "Unknown Position"
        lines = section.split('\n')
        jd_start = 0

        for i, line in enumerate(lines):
            if line.startswith('COMPANY:'):
                company = line[8:].strip()
                jd_start = i + 1
            elif line.startswith('POSITION:'):
                position = line[9:].strip().replace('/', '-')
                jd_start = i + 1
            elif line.startswith('JD:'):
                jd_start = i + 1
                break

        if position == "Unknown Position" and lines:
            position = lines[0][:80].replace('/', '-')
            jd = section
        else:
            jd = '\n'.join(lines[jd_start:]).strip()

        if jd:
            jobs.append({"company": company, "position": position, "jd": jd})

    return jobs


def main():
    if len(sys.argv) < 2:
        print("Usage: python parse_input.py <file.xlsx|file.txt> [default_company]", file=sys.stderr)
        print("Outputs JSON array of {company, position, jd} to stdout", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    default_company = sys.argv[2] if len(sys.argv) > 2 else "Unknown Company"

    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    if filepath.endswith(('.xlsx', '.xls')):
        jobs = process_excel(filepath)
    else:
        jobs = process_text(filepath, default_company)

    print(json.dumps(jobs, ensure_ascii=False))


if __name__ == "__main__":
    main()
