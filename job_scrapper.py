import pandas as pd
from jobspy import scrape_jobs


class JobScrapper:
    SITES_NAME = ["indeed", "linkedin", "glassdoor"]
    LOCATION = "Geneva"
    MAX_DISTANCE = 10
    NB_RESULTS_WANTED = 50
    HOURS_OLD = 24
    COUNTRY_INDEED = "Switzerland"

    def fetch(self, search_terms):
        results_list = []  # Collect non-empty results here

        for term in search_terms:
            result = scrape_jobs(
                site_name=self.SITES_NAME,
                search_term=term,
                location=self.LOCATION,
                distance=self.MAX_DISTANCE,
                results_wanted=self.NB_RESULTS_WANTED,
                hours_old=self.HOURS_OLD,
                country_indeed=self.COUNTRY_INDEED,
                linkedin_fetch_description=True,  # gets more info such as description, direct job url (slower)
                verbose=0,
            )
            # Print the number of jobs found for each search term
            print(f"{len(result)} jobs has been found when looking for the term {term}")

            if not result.empty:  # Only store non-empty results
                results_list.append(result)

        # Concatenate all valid results at once
        if results_list:
            jobs = pd.concat(
                [df for df in results_list if not df.isna().all().all()],
                ignore_index=True,
            )
            return jobs.drop_duplicates(subset=["id"], keep="first")
        else:
            return pd.DataFrame()  # Return empty DataFrame if no jobs found


if __name__ == "__main__":
    scrapper = JobScrapper()
    terms = ["software developer", "java developer"]
    print(scrapper.fetch(terms))
