from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from io import BytesIO
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st


@st.cache(suppress_st_warning=True)
def take_screenshot(driver):
    return driver.get_screenshot_as_png()


@st.cache_data 
def scrape_jobs(job_title):

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    os.environ["PATH"] += r"C:\\Program Files (x86)"
    driver.get('https://www.timesjobs.com/')
    driver.implicitly_wait(3)
   
    dict_jobs={
        "Job Title":[],
        "Company":[],
        "Description":[],
        "Skills":[],
        "Localization":[],
        "Link":[],
        "Date":[]
    }

    for i in range(1,11):
        jobs, companies, descriptions, skills, localizations, dates=[], [], [], [], [], []

        
        
        try:
            driver.get(f'https://www.timesjobs.com/candidate/job-search.html?from=submit&luceneResultSize=25&txtKeywords={job_title.replace(" ", "+")}&postWeek=60&searchType=personalizedSearch&actualTxtKeywords={job_title.replace(" ", "+")}&searchBy=0&rdoOperator=OR&pDate=I&sequence={i}&startPage=1')
        except:
            break
            
        try:      
            driver.find_element(by=By.XPATH, value='//*[@id="closeSpanId"]').click()
        except NoSuchElementException:
            pass
        jobs.extend(driver.find_elements(by=By.XPATH, value='//*[@id="searchResultData"]/ul//li/header/h2/a'))
        companies.extend(driver.find_elements(by=By.XPATH, value='//*[@id="searchResultData"]/ul/li/header/h3'))
        descriptions.extend(driver.find_elements(by=By.XPATH, value='//*[@id="searchResultData"]/ul/li/ul[2]/li[1]'))
        skills.extend(driver.find_elements(by=By.XPATH, value='//*[@id="searchResultData"]/ul/li/ul[2]/li[2]/span'))
        localizations.extend(driver.find_elements(by=By.XPATH, value='//*[@id="searchResultData"]/ul/li/ul[1]/li[last()]/span'))
        dates.extend(driver.find_elements(by=By.XPATH, value='//*[@id="searchResultData"]/ul/li/div/div/div/span[2]/span[last()]'))

        
        dict_jobs["Job Title"].extend(job.text.capitalize() for job in jobs)
        dict_jobs["Company"].extend(company.text if company.text[-11:]!="(More Jobs)" else company.text[:-11] for company in companies)
        dict_jobs["Description"].extend(description.text[16:] for description in descriptions)
        dict_jobs["Skills"].extend(skill.text for skill in skills)
        dict_jobs["Localization"].extend(localization.text for localization in localizations)
        dict_jobs["Link"].extend(job.get_attribute("href") for job in jobs)
        dict_jobs["Date"].extend(date.text for date in dates)
        
    return pd.DataFrame(dict_jobs)

@st.cache_data
def occurrence_skill(my_serie):
   my_dict = {}
   skill_list = []
   for my_string in my_serie:
      skill_list += my_string.split(",")
   for sk in skill_list:
      if sk in my_dict.keys():
         my_dict[sk]+=1
      else:
         my_dict[sk]=1
   return my_dict

@st.cache_data
def skills_fig_df(df):
    skills_dict = dict(sorted(occurrence_skill(df["Skills"]).items(), key=lambda item: item[1], reverse=True))
    try:
        skills_dict.pop(".")
    except:
        pass
    try:
        skills_dict.pop(" ")
    except:
        pass
    skill_keys = list(skills_dict.keys())
    skill_vals = list(skills_dict.values())
    skill_df = pd.DataFrame({"Skills": skill_keys, "Nbr of job offer": skill_vals})
    fig = px.histogram(data_frame=skill_df[:20], x="Nbr of job offer", y="Skills", template="ggplot2")
    #fig.show()
    return fig, skill_df

@st.cache_data
def localizations_fig_df(df_jobs):
    loc_dict = df_jobs["Localization"].value_counts().to_dict()
    try:
        loc_dict.pop("")
    except:
        pass
    loc_keys = list(loc_dict.keys())
    loc_vals = list(loc_dict.values())
    loc_df = pd.DataFrame({"Localizations": loc_keys, "Nbr of job offer": loc_vals})
    fig = px.histogram(data_frame=loc_df.iloc[:20, :], x="Nbr of job offer", y="Localizations", template="ggplot2")
    #fig.show()
    return fig, loc_df

@st.cache_data
def companies_fig_df(df_jobs):
    comp_dict = df_jobs["Company"].value_counts().to_dict()
    comp_keys = list(comp_dict.keys())
    comp_vals = list(comp_dict.values())
    comp_df = pd.DataFrame({"Company name": comp_keys, "Nbr of job offer": comp_vals})
    fig = px.histogram(data_frame=comp_df.iloc[:20,:], x="Nbr of job offer", y="Company name", template="ggplot2")
    #fig.show()
    return fig, comp_df

@st.cache_data
def jobs_fig(df_jobs):
    job_dict = df_jobs["Job Title"].value_counts().to_dict()
    job_keys = list(job_dict.keys())[:20]
    job_vals = list(job_dict.values())[:20]
    job_df = pd.DataFrame({"Job Title": job_keys, "Nbr of job offer": job_vals})
    fig = px.histogram(data_frame=job_df, x="Nbr of job offer", y="Job Title", template="ggplot2")
    return fig
