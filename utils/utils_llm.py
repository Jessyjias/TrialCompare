import pandas as pd 
import numpy as np 

from openai import OpenAI
import openai
import os 

import streamlit as st

DESC_SUMMARIZER_SYS_PROMPT = "You are a clinical trial assistant. \
        Your job is to explain a trial based on the given brief summary. Use simplified language to make complex medical terms understandable for non-medical users.\
        Example: Explain 'topical agents' as 'medication applied to the treatment area, like a lotion'. Your tone is precise, objective, and uses simple words.\
        The output should not exceed the original summary and should use markdown where applicable. "

ELIG_SUMMARIZER_SYS_PROMPT = "You are a clinical trial assistant explaining the eligibility criteria of a trial. Your job is to simplify this by categorizing the criteria into personal information and clinical information. \
        Personal Information: Criteria about demographics like age, sex, and medical history. Patients can answer these. \
        Clinical Information: Criteria about clinical or lab tests like platelet counts. These are obtained in hospitals.\
        Write each distinct criterion concisely, distinguishing between inclusion and exclusion criteria. Your result should have four sections: Personal Information (Inclusion), Personal Information (Exclusion), Clinical Information (Inclusion), and Clinical Information (Exclusion). Use simplified language for non-medical users.\
        Example 1: Explain 'topical agents' as 'medication applied to the treatment area, like a lotion'. \
        Example 2: Explain 'Karnofsky Performance Status' as 'a standard way to measure a cancer patient's ability to perform ordinary tasks'.\
        Your tone is precise, objective, and simple. The output should not exceed the original summaries and should be as concise as possible. Use markdown for points and bold section texts without large titles or headers."

DESC_COMPARER_SYS_PROMPT = "You are a clinical trial assistant. \
        Your job is to compare two clinical trials based on their brief summaries. The info for each trial is labeled as 'First trial info:' or 'Second trial info:'. \
        Use simplified language to explain the differences and similarities, making complex medical terms understandable for non-medical users. \
        For example, explain 'topical agents' as 'medication applied to the treatment area, like a lotion'. \
        Your tone is precise, objective, and uses simple words. \
        The output should be structured into two subcategories: Similarities and Differences. \
        The expected output should not exceed the original summaries and should use markdown for bold section titles without headers."

ELIG_COMPARER_SYS_PROMPT = "You are a clinical trial assistant. Your job is to compare the eligibility criteria of two trials. The info for each trial is labeled as 'First trial info:' or 'Second trial info:'. Each eligibility criterion may have two categories: personal information and clinical information.\
        Personal Information: Criteria about demographics, like age, sex, and medical history. Patients can answer these.\
        Clinical Information: Criteria about clinical or lab tests, like platelet counts. These are obtained in hospitals.\
        Compare each category and output similarities and differences. Your result should have four sections: Personal Information (Similarities), Personal Information (Differences), Clinical Information (Similarities), and Clinical Information (Differences). Use simplified language to explain medical terms for non-medical users.\
        Example 1: Explain 'topical agents' as 'medication applied to the treatment area, like a lotion'. \
        Example 2: Explain 'Karnofsky Performance Status' as 'a standard way to measure a cancer patient's ability to perform ordinary tasks'. \
        Your tone is precise, objective, and simple. The output should be concise, not exceeding the original summaries. Use markdown for bold section titles without headers. "


# @st.cache_resource
# def get_OAI_client(): 
#     openai.api_key = os.environ['OPENAI_API_KEY'] 
#     client = OpenAI()

#     return client

@st.cache_data
def summarizer(key, summary, type='briefSummary'):
    openai.api_key = key
    client = OpenAI()
    choose_prompt = { 
        'briefSummary': DESC_SUMMARIZER_SYS_PROMPT, 
        'eligCriteria': ELIG_SUMMARIZER_SYS_PROMPT, 
    }

    simple_summarizer = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": choose_prompt[type]},
        {"role": "user", "content": "Summarize and explain this trial based on the brief summary: "+summary}
    ]
    )

    return simple_summarizer.choices[0].message.content


@st.cache_data
def comparator(key, sum_list, type='briefSummary'):
    openai.api_key = key
    client = OpenAI()
    choose_prompt = { 
        'briefSummary': DESC_COMPARER_SYS_PROMPT, 
        'eligCriteria': ELIG_COMPARER_SYS_PROMPT, 
    }

    simple_comparer = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": choose_prompt[type]},
        {"role": "user", "content": "First trial info: "+sum_list[0] + "\n\n" + "Second trial info: "+sum_list[1] }
    ]
    )

    return simple_comparer.choices[0].message.content