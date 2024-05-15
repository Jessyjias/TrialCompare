import pandas as pd 
import numpy as np 

from openai import OpenAI
import openai
import os 

import streamlit as st

DESC_SUMMARIZER_SYS_PROMPT = "You are a clinical trial assistant. \
        Your job is to facilitate clinical trials by explaining a trial based on the given brief summary. \
        You use simplified language to explain the trial, so that complex medical word can be understood by people without medical background. \
        Example: if the term 'topical agents' is in the prompt, you should explain that it means 'medication that is applied to the area being treated, such as in lotion form'.  \
        Your tone is precise, objective, and prefer simple words to explain concepts. \
        The expected output should not exceed the original brief summary user has given to you. It should use markdown notations where applicable. "

ELIG_SUMMARIZER_SYS_PROMPT = "You are a clinical trial assistant who is explaining the eligibility criteria of a trial. \
     Your job is to simplify this explanation process by categorizing the given eligibility criteria into 2 categories, personal information based and clinical information based. \
     In the personal information category, criteria included under this section should be about the patient's demographic, such as age, sex, and medical history. These should be information patient can answer. \
     For the clinical information category, criteria included under this section may be about specific clinical test or lab test results, such as physiological and biochemical measurements like platelets counts. These are information that patient likely do not know right off the bat and need to be obtained in hospitals. \
     Write each distinct criterion as a concisely worded point, and clearly distinct between inclusion and exclusion criteria. \
     Your result should contain 2 large sections each with 2 subfields - personal information (inclusion) and personal information (exclusion), and clinical information (inclusion) and clinical information (exclusion). \
     You use simplified language to explain the trial, so that complex medical word can be understood by people without medical background. \
     Example 1: if the term 'topical agents' is in the prompt, you should explain that it means 'medication that is applied to the area being treated, such as in lotion form'.  \
     Example 2: if a criterion asks about 'Karnofsky Performance Status', you should explain that it refers to 'A standard way of measuring the ability of cancer patients to perform ordinary tasks.'    \
    Your tone is precise, objective, and prefer simple words to explain concepts. \
     The expected output should not exceed the original brief summary user has given to you, and summarized points should be as concise as possible. It should use markdown notations for the points and have bolded section texts, but avoid large markdown titles or headers. "

DESC_COMPARER_SYS_PROMPT = "You are a clinical trial assistant. \
        Your job is to compare 2 clinical trials based on their given brief summary. The info for each trial is labelled as 'First trial info: ' or 'Second trial info: '. \
        You use simplified language to explain the difference and similarities between the trials, so that complex medical word can be understood by people without medical background. \
        Example: if the term 'topical agents' is in the prompt, you should explain that it means 'medication that is applied to the area being treated, such as in lotion form'.  \
        Your tone is precise, objective, and prefer simple words to explain concepts. \
        The output should be structured into 2 subcategories: Similarities and Differences. \
        The expected output should not exceed the original brief summary user has given to you. It should use markdown notations to bold section titles, but avoid using markdown headers. "

ELIG_COMPARER_SYS_PROMPT = "You are a clinical trial assistant. \
     Your job is to compare the eligibility criteria of two trials. The info for each trial is labelled as 'First trial info: ' or 'Second trial info: '\
     Each given eligibility criteria may contain two categories: personal information based criteria and clinical information based criteria. \
     In the personal information category, criteria included under this section should be about the patient's demographic, such as age, sex, and medical history. These should be information patient can answer. \
     For the clinical information category, criteria included under this section may be about specific clinical test or lab test results, such as physiological and biochemical measurements like platelets counts. These are information that patient likely do not know right off the bat and need to be obtained in hospitals. \
     Now, you will compare each category and output the similarities and differences between each cateria category. \
     Your result should contain 2 sections each with 2 subfields - personal information (Similarities) and personal information (Differences), and clinical information (Similarities) and clinical information (Differences). \
     You use simplified language to explain the trial, so that complex medical word can be understood by people without medical background. \
     Example 1: if the term 'topical agents' is in the prompt, you should explain that it means 'medication that is applied to the area being treated, such as in lotion form'.  \
     Example 2: if a criterion asks about 'Karnofsky Performance Status', you should explain that it refers to 'A standard way of measuring the ability of cancer patients to perform ordinary tasks.'    \
    Your tone is precise, objective, and prefer simple words to explain concepts. \
     The expected output should not exceed the original brief summary user has given to you, and summarized points should be as concise as possible. It should use markdown notations to bold section titles, but avoid large markdown titles or headers. "


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

    # summary='This clinical trial compares two supplemental topical agents (Aquaphor and Miaderm) for the treatment of acute radiation dermatitis in patients with breast cancer undergoing radiation therapy. Radiation dermatitis is a radiation-induced skin reaction which can cause itching, swelling, pain, and general discomfort. Aquaphor is a commonly available, inexpensive, petrolatum-based multi-purpose ointment designed to protect and sooth extremely dry skin, chapped lips, cracked hands and feet, minor cuts and burns, and many other skin irritations. Miaderm is a water-based cream and contains ingredients like calendula, hyaluronate, and aloe vera which may help reduce occurrence and severity of radiation dermatitis. Both are commonly recommended and used by breast cancer patients undergoing external beam radiation therapy (EBRT). However, it is not known whether one is better than the other in treating or preventing radiation dermatitis.'

    simple_summarizer = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": choose_prompt[type]},
        {"role": "user", "content": "Summarize and explain this trial based on the brief summary: "+summary}
    ]
    )

    # print(simple_summarizer.choices[0].message.content)

    return simple_summarizer.choices[0].message.content


@st.cache_data
def comparator(key, sum_list, type='briefSummary'):
    openai.api_key = key
    client = OpenAI()
    choose_prompt = { 
        'briefSummary': DESC_COMPARER_SYS_PROMPT, 
        'eligCriteria': ELIG_COMPARER_SYS_PROMPT, 
    }

    # summary='This clinical trial compares two supplemental topical agents (Aquaphor and Miaderm) for the treatment of acute radiation dermatitis in patients with breast cancer undergoing radiation therapy. Radiation dermatitis is a radiation-induced skin reaction which can cause itching, swelling, pain, and general discomfort. Aquaphor is a commonly available, inexpensive, petrolatum-based multi-purpose ointment designed to protect and sooth extremely dry skin, chapped lips, cracked hands and feet, minor cuts and burns, and many other skin irritations. Miaderm is a water-based cream and contains ingredients like calendula, hyaluronate, and aloe vera which may help reduce occurrence and severity of radiation dermatitis. Both are commonly recommended and used by breast cancer patients undergoing external beam radiation therapy (EBRT). However, it is not known whether one is better than the other in treating or preventing radiation dermatitis.'

    simple_comparer = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": choose_prompt[type]},
        {"role": "user", "content": "First trial info: "+sum_list[0] + "\n\n" + "Second trial info: "+sum_list[1] }
    ]
    )

    # print(simple_summarizer.choices[0].message.content)

    return simple_comparer.choices[0].message.content