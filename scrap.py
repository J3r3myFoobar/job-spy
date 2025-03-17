import csv
import os
import shutil
from datetime import datetime, timedelta

import pandas as pd

from environment_utils import Env
from job_scrapper import JobScrapper
from resume_reader import Resume
from text_analysis import TextAnalyser

# Define a constant for the job CSV file path
JOBS_CSV_FILE = "jobs.csv"


def backup_historical_job_csv_if_required():
    if os.path.exists(JOBS_CSV_FILE):
        timestamp = datetime.now().isoformat()
        backup_filename = f"jobs.csv-{timestamp}"
        shutil.copy(JOBS_CSV_FILE, backup_filename)


def filter_out_duplicate(df):
    df["date_posted"] = pd.to_datetime(df["date_posted"])
    cutoff_date = datetime.today() - timedelta(days=30)
    df_filtered = df[df["date_posted"] >= cutoff_date]
    df_filtered = df_filtered.drop_duplicates(subset=["title", "company"], keep="first")
    df_filtered = df_filtered.drop_duplicates(subset=["id"], keep="first")
    return df_filtered


def add_similarity_number(df):
    env = Env()
    resume_file_path = env.get_key("RESUME")
    resume = Resume(resume_file_path).get_resume()
    openai_key = env.get_key("OPENAI_API_KEY")
    text_analyser = TextAnalyser(openai_key, resume)

    similarity_values = []
    for job_description in df["description"]:
        similarity = text_analyser.get_similarity(job_description)
        similarity_values.append(similarity)

    result = df.copy()
    result.insert(2, "similarity", similarity_values)
    return result


def filter_by_similarity(df):
    return df[df["similarity"] >= 0.81]


def print_summary(df):
    print(f"Number of jobs: {len(df)}")
    selected_columns = ["job_url", "title", "company"]
    print(df[selected_columns].head())


def update_historical_job_csv(jobs):
    existing_jobs = (
        pd.read_csv(JOBS_CSV_FILE) if os.path.exists(JOBS_CSV_FILE) else pd.DataFrame()
    )
    updated_jobs = pd.concat([existing_jobs, jobs], ignore_index=True)
    updated_jobs = filter_out_duplicate(updated_jobs)
    updated_jobs.to_csv(
        JOBS_CSV_FILE, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False
    )
    print(f"Updated job list with {len(updated_jobs)} jobs.")


def main():
    backup_historical_job_csv_if_required()

    scrapper = JobScrapper()
    search_terms = [
        "software engineer",
        "software developer",
        "java developer",
        "it architect",
        "software architect",
        "solution architect",
        "aws architect",
        "aws developer",
    ]

    jobs = scrapper.fetch(search_terms)
    jobs = filter_out_duplicate(jobs)
    jobs = add_similarity_number(jobs)
    currated_jobs = filter_by_similarity(jobs)

    currated_jobs.to_csv(
        "jobs_curated.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False
    )
    print_summary(currated_jobs)

    update_historical_job_csv(jobs)


if __name__ == "__main__":
    main()
