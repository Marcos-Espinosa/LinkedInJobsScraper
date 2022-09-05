#!/usr/bin/env python
# coding: utf-8

# Necessary Imports for LinkedIn Scraping


import logging
from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events,EventData,EventMetrics
from linkedin_jobs_scraper.query import Query,QueryOptions,QueryFilters
from linkedin_jobs_scraper.filters import RelevanceFilters, TimeFilters,TypeFilters,ExperienceLevelFilters, RemoteFilters

import pandas as pd

logging.basicConfig(level = logging.INFO)

job_postings = []

def on_data(data: EventData):
    job_postings.append([data.job_id,data.location,data.title,data.company,data.date,data.link,data.description])

def on_error(error):
    print('[ON_ERROR]', error)

def on_end():
    print('[ON_END]')

chrome_driver_path = '/Users/marcosespinosa/Downloads/chromedriver'

scraper = LinkedinScraper(
    chrome_executable_path=chrome_driver_path,
    chrome_options=None,
    headless=True,
    max_workers=1,
    slow_mo=0.5,
    page_load_timeout=20)

scraper.on(Events.DATA, on_data)
scraper.on(Events.ERROR, on_error)
scraper.on(Events.END, on_end)

queries = [
    Query(
        query='Python',
        options=QueryOptions(
            locations=['United States','Tampa'],
            apply_link = True,
            limit = 50,
            filters=QueryFilters(
                relevance=RelevanceFilters.RECENT,
                time=TimeFilters.MONTH,
                type=[TypeFilters.FULL_TIME],
                experience=None,
            )
        )
    ),
]

scraper.run(queries)

# Create Pandas Dataframe from ON_DATE results

df = pd.DataFrame(job_postings,columns=['Job_ID','Location','Title','Company','Date','Link','Description'])

df.to_csv('Job_Postings.csv',index=False)