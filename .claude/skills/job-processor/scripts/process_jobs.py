#!/usr/bin/env python3
"""
Job Processor - End-to-end job application processing
Orchestrates cover-letter-generator and job-application-tracker agents
"""

import subprocess
import sys
import time
import json
import argparse
from pathlib import Path
from datetime import datetime

# Paths
BASE_DIR = Path("/Users/samguan/Desktop/project/n8n-resume-generator")
EXP_LIB_DIR = BASE_DIR / "exp_lib"
COVER_LETTER_SCRIPT = BASE_DIR / ".claude/agents/cover-letter-generator/scripts/batch_process_jds.py"
TRACKER_SCRIPT = BASE_DIR / ".claude/agents/job-application-tracker/scripts/batch_organize.py"

# Timing
DEFAULT_WAIT_PER_JOB = 120  # seconds


def run_cover_letter_generator(input_file, company=None):
    """Run cover-letter-generator agent."""
    print("\n" + "=" * 60)
    print("Step 1: Running cover-letter-generator")
    print("=" * 60)

    cmd = ["python3", str(COVER_LETTER_SCRIPT), str(input_file)]
    if company:
        cmd.append(company)

    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)

    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return None, 0

    # Extract job count and order file from output
    job_count = 0
    order_file = None

    for line in result.stdout.split('\n'):
        if 'Found' in line and 'job(s)' in line:
            try:
                job_count = int(line.split()[1])
            except:
                pass
        if 'Order file saved:' in line:
            order_file = line.split(': ')[1].strip()

    return order_file, job_count


def wait_for_files(expected_count, timeout_per_job=DEFAULT_WAIT_PER_JOB):
    """Wait for files to be generated in exp_lib."""
    print("\n" + "=" * 60)
    print("Step 2: Waiting for file generation")
    print("=" * 60)

    total_timeout = expected_count * timeout_per_job
    start_time = time.time()
    check_interval = 15  # seconds

    print(f"Expecting {expected_count} pairs of files")
    print(f"Timeout: {total_timeout}s (~{timeout_per_job}s per job)")

    while time.time() - start_time < total_timeout:
        resume_files = list(EXP_LIB_DIR.glob("R-*.pdf"))
        cl_files = list(EXP_LIB_DIR.glob("CL-*.pdf"))

        elapsed = int(time.time() - start_time)
        print(f"  [{elapsed}s] R: {len(resume_files)}, CL: {len(cl_files)} / {expected_count}")

        if len(resume_files) >= expected_count and len(cl_files) >= expected_count:
            print(f"\nAll {expected_count} pairs ready!")
            return True

        time.sleep(check_interval)

    print(f"\nTimeout reached. Found R: {len(resume_files)}, CL: {len(cl_files)}")
    return len(resume_files) > 0 and len(cl_files) > 0


def run_job_application_tracker():
    """Run job-application-tracker agent."""
    print("\n" + "=" * 60)
    print("Step 3: Running job-application-tracker")
    print("=" * 60)

    # Auto-confirm with 'y'
    result = subprocess.run(
        ["python3", str(TRACKER_SCRIPT)],
        input="y\n",
        capture_output=True,
        text=True
    )
    print(result.stdout)

    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False

    return True


def create_temp_file_from_text(company, position, jd_text):
    """Create a temporary file from direct text input."""
    temp_file = Path("/tmp") / f"jd_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    content = f"""COMPANY: {company}
POSITION: {position}
JD:
{jd_text}
"""
    temp_file.write_text(content)
    return temp_file


def main():
    parser = argparse.ArgumentParser(description='Process job descriptions end-to-end')
    parser.add_argument('input_file', help='Excel or text file with job descriptions')
    parser.add_argument('company', nargs='?', default=None, help='Default company name')
    parser.add_argument('--wait-per-job', type=int, default=DEFAULT_WAIT_PER_JOB,
                        help=f'Seconds to wait per job (default: {DEFAULT_WAIT_PER_JOB})')

    args = parser.parse_args()

    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        sys.exit(1)

    print("=" * 60)
    print("Job Processor - End-to-end Processing")
    print("=" * 60)
    print(f"Input: {input_path}")
    if args.company:
        print(f"Company: {args.company}")
    print(f"Wait per job: {args.wait_per_job}s")

    # Step 1: Run cover-letter-generator
    order_file, job_count = run_cover_letter_generator(input_path, args.company)

    if not order_file or job_count == 0:
        print("\nFailed to process jobs. Exiting.")
        sys.exit(1)

    print(f"\nJobs sent: {job_count}")
    print(f"Order file: {order_file}")

    # Step 2: Wait for files
    files_ready = wait_for_files(job_count, args.wait_per_job)

    if not files_ready:
        print("\nWarning: Not all files generated. Proceeding with available files.")

    # Step 3: Run job-application-tracker
    success = run_job_application_tracker()

    # Summary
    print("\n" + "=" * 60)
    print("Processing Complete!")
    print("=" * 60)

    if success:
        print(f"Successfully processed {job_count} job(s)")
        print(f"Check: cvs/resume and cover letters/{datetime.now().strftime('%Y-%m-%d')}/")
        print(f"Excel: cvs/Excel/job-applications.xlsx")
    else:
        print("Some jobs may have failed. Check output above.")


if __name__ == "__main__":
    main()
