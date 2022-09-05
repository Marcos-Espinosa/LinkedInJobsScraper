#!/usr/bin/env python
# coding: utf-8

# Necessary Imports for LinkedIn Scraping

# In[1]:


import logging
from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events,EventData,EventMetrics
from linkedin_jobs_scraper.query import Query,QueryOptions,QueryFilters
from linkedin_jobs_scraper.filters import RelevanceFilters, TimeFilters,TypeFilters,ExperienceLevelFilters, RemoteFilters


# In[3]:


logging.basicConfig(level = logging.INFO)


# In[18]:


job_postings = []


# In[29]:


def on_data(data: EventData):
    job_postings.append([data.job_id,data.location,data.title,data.company,data.date,data.link,data.description])


# In[5]:


def on_error(error):
    print('[ON_ERROR]', error)


# In[6]:


def on_end():
    print('[ON_END]')


# In[7]:


chrome_driver_path = '/Users/marcosespinosa/Downloads/chromedriver'


# In[25]:


scraper = LinkedinScraper(
    chrome_executable_path=chrome_driver_path,
    chrome_options=None,
    headless=True,
    max_workers=1,
    slow_mo=1.3,
    page_load_timeout=20)


# In[9]:


scraper.on(Events.DATA, on_data)
scraper.on(Events.ERROR, on_error)
scraper.on(Events.END, on_end)


# In[13]:


queries = [
    Query(
        query='Python',
        options=QueryOptions(
            locations=['United States','Tampa,FL'],
            apply_link = True,
            limit = 27,
            filters=QueryFilters(
                relevance=RelevanceFilters.RECENT,
                time=TimeFilters.MONTH,
                type=[TypeFilters.FULL_TIME],
                experience=None,
            )
        )
    ),
]


# In[26]:


scraper.run(queries)


# In[27]: Create Pandas Dataframe from ON_DATE results


df = pd.DataFrame(job_postings,columns=['Job_ID','Location','Title','Company','Date','Link','Description'])


