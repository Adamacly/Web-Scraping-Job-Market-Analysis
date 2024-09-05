import models as m
import pandas as pd
import streamlit as st

@st.cache_data
def get_dataframe(job_title):
    df=m.scrape_jobs(job_title)
    return df

#@st.cache_data
def divise_df(df, n):
    return (df[df.index % n == i] for i in range(n))


st.markdown("<h1 style='text-align: center;'>JOB OFFERS FROM TIMESJOBS.COM</h1>", unsafe_allow_html=True)
st.caption("The informations in this web application have been scraped from [Timesjobs](https://www.timesjobs.com/)")

sb = st.sidebar
sb.markdown("<h1 style='text-align: center'>JOB TITLE</h1>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Home", "Jobs", "Companies", "Localisation", "Skills"])

tab1.image("capture.png", caption="Screenshot of the homepage of www.timesjobs.com")

sdbar=st.sidebar
sdb_form=sdbar.form("Form1")
job_title=sdb_form.text_input(label="Give a job title, skill, designation:")
btn=sdb_form.form_submit_button(label="Search")

if btn and job_title!="": 

    df=m.scrape_jobs(job_title)    

    tab2.subheader("Most frequent jobs:")
    tab2.plotly_chart(m.jobs_fig(df))
    tab2.markdown("---")
    tab2.subheader("More informations:")
    tab2.dataframe(df[["Job Title", "Company", "Date","Skills"]])
    tab2.caption(f"{df.shape[0]} posts found")
    
    fig_c, df_c = m.companies_fig_df(df)
    df_c0, df_c1 = divise_df(df_c, 2)
    tab3.subheader("Most frequent companies:")
    tab3.plotly_chart(fig_c)
    tab3.markdown("---")
    tab3.subheader("More companies:")
    col_c1, col_c2 = tab3.columns(2)
    col_c1.dataframe(df_c0)
    col_c2.dataframe(df_c1)
    
    fig_l, df_l = m.localizations_fig_df(df)
    df_l0, df_l1 = divise_df(df_l, 2)
    tab4.subheader("Most frequent localizations:")
    tab4.plotly_chart(fig_l)
    tab4.markdown("---")
    tab4.subheader("More localizations:")
    col_l0, col_l1 = tab4.columns(2)
    col_l0.dataframe(df_l0)
    col_l1.dataframe(df_l1)

    fig_s, df_s = m.skills_fig_df(df)
    df_s0, df_s1, df_s2 = divise_df(df_s, 3)
    tab5.markdown("Most popular skills: ")
    tab5.plotly_chart(fig_s)
    tab5.markdown("---")
    tab5.subheader("More skills: ")
    col_s0, col_s1, col_s2 = tab5.columns(3)
    col_s0.dataframe(df_s0)
    col_s1.dataframe(df_s1)
    col_s2.dataframe(df_s2)

