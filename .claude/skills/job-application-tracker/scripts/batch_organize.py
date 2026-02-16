#!/usr/bin/env python3
"""
Batch Organize Files
Reads the order file from cover-letter-generator and matches files by timestamp.
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
import subprocess

EXP_LIB_DIR = "/Users/samguan/Desktop/project/n8n-resume-generator/exp_lib"
CVS_DIR = "/Users/samguan/Desktop/project/n8n-resume-generator/cvs"
SCRIPT_DIR = Path(__file__).parent


def find_latest_order_file(exp_lib_dir):
    """Find the most recent batch_order_*.json file."""
    exp_lib_path = Path(exp_lib_dir)
    order_files = list(exp_lib_path.glob("batch_order_*.json"))

    if not order_files:
        return None

    # Sort by modification time, newest first
    order_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return order_files[0]


def get_pdf_files_by_key(exp_lib_dir):
    """
    Get all PDF files and organize them by key.

    New naming convention: {key}-R.pdf and {key}-CL.pdf (e.g., 0-R.pdf, 0-CL.pdf)
    Falls back to timestamp-based naming for backwards compatibility.
    """
    exp_lib_path = Path(exp_lib_dir)

    # New key-based naming: {key}-R.pdf, {key}-CL.pdf
    key_resume_files = {}
    key_cl_files = {}

    # Find files with new naming convention
    for f in exp_lib_path.glob("*-R.pdf"):
        name = f.stem  # e.g., "0-R"
        try:
            key = int(name.split('-')[0])
            key_resume_files[key] = f
        except (ValueError, IndexError):
            pass

    for f in exp_lib_path.glob("*-CL.pdf"):
        name = f.stem  # e.g., "0-CL"
        try:
            key = int(name.split('-')[0])
            key_cl_files[key] = f
        except (ValueError, IndexError):
            pass

    return key_resume_files, key_cl_files


def get_pdf_files_sorted_by_time(exp_lib_dir):
    """
    Legacy: Get all R-*.pdf and CL-*.pdf files sorted by timestamp in filename.

    Files are named like: R-2026-01-27_21-33-01-091Z.pdf
    The timestamp in the filename is used for sorting, not file modification time.
    """
    exp_lib_path = Path(exp_lib_dir)

    resume_files = list(exp_lib_path.glob("R-*.pdf"))
    cl_files = list(exp_lib_path.glob("CL-*.pdf"))

    def extract_timestamp(filepath):
        """Extract timestamp from filename for sorting."""
        name = filepath.stem  # e.g., "R-2026-01-27_21-33-01-091Z"
        # Remove prefix (R- or CL-)
        ts_part = name[2:] if name.startswith('R-') else name[3:]
        return ts_part

    # Sort by timestamp in filename
    resume_files.sort(key=extract_timestamp)
    cl_files.sort(key=extract_timestamp)

    return resume_files, cl_files


def match_files_to_jobs_by_key(order_data, key_resume_files, key_cl_files):
    """
    Match files to jobs using key-based naming.

    Logic: Each job has a 'key' field that directly maps to {key}-R.pdf and {key}-CL.pdf
    """
    jobs = order_data.get("jobs", [])
    matched = []

    for job in jobs:
        key = job.get("key")
        if key is None:
            # Fallback to order-based index (order is 1-based, so subtract 1)
            key = job.get("order", 1) - 1

        resume = key_resume_files.get(key)
        cl = key_cl_files.get(key)

        matched.append({
            "key": key,
            "order": job.get("order", key + 1),
            "company": job.get("company", "Unknown"),
            "position": job.get("position", "Unknown"),
            "jd": job.get("jd", ""),
            "resume_file": str(resume) if resume else None,
            "cl_file": str(cl) if cl else None,
            "expected_files": job.get("expected_files", {})
        })

    return matched


def match_files_to_jobs(order_data, resume_files, cl_files):
    """
    Legacy: Match files to jobs based on order (timestamp-based).

    Logic: The first job sent gets the first pair of files generated (by timestamp).
    """
    jobs = order_data.get("jobs", [])
    matched = []

    for i, job in enumerate(jobs):
        resume = resume_files[i] if i < len(resume_files) else None
        cl = cl_files[i] if i < len(cl_files) else None

        matched.append({
            "order": job.get("order", i + 1),
            "company": job.get("company", "Unknown"),
            "position": job.get("position", "Unknown"),
            "jd": job.get("jd", ""),
            "resume_file": str(resume) if resume else None,
            "cl_file": str(cl) if cl else None
        })

    return matched


def organize_single_job(base_dir, company, position, jd, resume_file, cl_file, exp_lib_dir):
    """Call process_job_application.py to organize a single job."""
    script_path = SCRIPT_DIR / "process_job_application.py"

    # We need to temporarily "plant" the files as the latest in exp_lib
    # so that process_job_application.py can find them.
    # Actually, let's modify the approach - pass files directly via env vars

    # Set environment variables for the files
    env = os.environ.copy()
    if resume_file:
        env['RESUME_FILE'] = resume_file
    if cl_file:
        env['CL_FILE'] = cl_file

    result = subprocess.run(
        ['python3', str(script_path), base_dir, company, position, jd, exp_lib_dir],
        capture_output=True,
        text=True,
        env=env
    )

    return result.returncode == 0, result.stdout, result.stderr


def main():
    # Parse arguments
    exp_lib_dir = sys.argv[1] if len(sys.argv) > 1 else EXP_LIB_DIR
    cvs_dir = sys.argv[2] if len(sys.argv) > 2 else CVS_DIR

    print("=" * 60)
    print("Batch File Organizer")
    print("=" * 60)

    # Find latest order file
    order_file = find_latest_order_file(exp_lib_dir)
    if not order_file:
        print(f"Error: No batch_order_*.json found in {exp_lib_dir}")
        print("Run cover-letter-generator first to create an order file.")
        sys.exit(1)

    print(f"\n📋 Found order file: {order_file.name}")

    # Load order data
    with open(order_file, 'r', encoding='utf-8') as f:
        order_data = json.load(f)

    total_jobs = order_data.get("total_jobs", 0)
    print(f"   Batch ID: {order_data.get('batch_id', 'unknown')}")
    print(f"   Total jobs: {total_jobs}")

    # Check if jobs have 'key' field (new format)
    jobs = order_data.get("jobs", [])
    use_key_based = any(job.get("key") is not None for job in jobs)

    if use_key_based:
        # New key-based matching: {key}-R.pdf, {key}-CL.pdf
        key_resume_files, key_cl_files = get_pdf_files_by_key(exp_lib_dir)
        print(f"\n📁 Found files in exp_lib (key-based naming):")
        print(f"   Resumes: {len(key_resume_files)} (keys: {sorted(key_resume_files.keys())})")
        print(f"   Cover Letters: {len(key_cl_files)} (keys: {sorted(key_cl_files.keys())})")

        if len(key_resume_files) < total_jobs or len(key_cl_files) < total_jobs:
            print(f"\n⚠️  Warning: Not enough files for all jobs!")
            print(f"   Expected: {total_jobs} pairs")
            print(f"   Found: {min(len(key_resume_files), len(key_cl_files))} pairs")
            print("   Some jobs may not have files assigned.")

        # Match files to jobs by key
        matched = match_files_to_jobs_by_key(order_data, key_resume_files, key_cl_files)
    else:
        # Legacy timestamp-based matching
        resume_files, cl_files = get_pdf_files_sorted_by_time(exp_lib_dir)
        print(f"\n📁 Found files in exp_lib (timestamp-based naming):")
        print(f"   Resumes: {len(resume_files)}")
        print(f"   Cover Letters: {len(cl_files)}")

        if len(resume_files) < total_jobs or len(cl_files) < total_jobs:
            print(f"\n⚠️  Warning: Not enough files for all jobs!")
            print(f"   Expected: {total_jobs} pairs")
            print(f"   Found: {min(len(resume_files), len(cl_files))} pairs")
            print("   Some jobs may not have files assigned.")

        # Match files to jobs by timestamp order
        matched = match_files_to_jobs(order_data, resume_files, cl_files)

    print(f"\n📊 Matching preview:")
    print("-" * 60)
    for m in matched:
        r_name = Path(m['resume_file']).name if m['resume_file'] else "❌ Missing"
        cl_name = Path(m['cl_file']).name if m['cl_file'] else "❌ Missing"
        key_str = f"Key={m['key']} | " if 'key' in m else ""
        print(f"[{m['order']}] {key_str}{m['company']} - {m['position'][:40]}")
        print(f"     R:  {r_name}")
        print(f"     CL: {cl_name}")

    # Confirm with user
    print("\n" + "-" * 60)
    response = input("Proceed with organizing files? [Y/n]: ").strip().lower()
    if response and response != 'y':
        print("Cancelled.")
        sys.exit(0)

    # Process each job
    print("\n" + "=" * 60)
    print("Organizing files...")
    print("=" * 60)

    success_count = 0
    fail_count = 0

    for m in matched:
        print(f"\n[{m['order']}/{total_jobs}] {m['company']} - {m['position'][:40]}")

        success, stdout, stderr = organize_single_job(
            cvs_dir,
            m['company'],
            m['position'],
            m['jd'],
            m['resume_file'],
            m['cl_file'],
            exp_lib_dir
        )

        if success:
            print("         ✅ Success")
            # Print key info from stdout
            for line in stdout.split('\n'):
                if 'Organized' in line or 'Added' in line:
                    print(f"         {line.strip()}")
            success_count += 1
        else:
            print(f"         ❌ Failed")
            if stderr:
                print(f"         Error: {stderr[:200]}")
            fail_count += 1

    # Archive the order file
    archive_path = Path(exp_lib_dir) / "archive"
    archive_path.mkdir(exist_ok=True)
    archived_order = archive_path / order_file.name
    order_file.rename(archived_order)
    print(f"\n📦 Order file archived to: {archived_order}")

    # Summary
    print("\n" + "=" * 60)
    print("Batch organizing complete!")
    print(f"  Successful: {success_count}")
    print(f"  Failed: {fail_count}")
    print(f"  Total: {total_jobs}")


if __name__ == "__main__":
    main()
