# SimpleTrials (TrialCompare)

Try the app here: https://simpletrials.streamlit.app/

View demo video here: https://youtu.be/E0vAKmYf1jg
 
## Inspiration

Finding relevant clinical trials is a daunting task for patients, often relying solely on doctor recommendations which may not encompass all available options. Similarly, as a busy doctor or clinical research assistant providing healthcare and facilitating clinical trials, it's challenging to adequately educate patients amidst juggling multiple trials, or get in touch with patients who could benefit from participation but are not within their immediate reach. 

SimpleTrials addresses these hurdles by offering simplified, easy-to-understand modules, empowering patients to explore trial information independently. By bridging the gap between patients and trials with clear language and accessible resources, SimpleTrials enhances patient autonomy and facilitates informed decision-making in healthcare journeys. Moreover, by enabling patients to find trials, SimpleTrials contributes to accelerating clinical research, enhancing speed, and overall participant experience, thereby driving innovation in healthcare.

Special thanks to my friend Annie, who is working as a clinical research coordinator at UCSF, for discussing the project idea with me :)

## What it does

SimpleTrials is a clinical trial dashboard designed to empower users without medical education background in navigating and understanding the clinical trials. 

The journey begins with users inputting search parameters such as their condition of interest, type of intervention, or preferred location. The default settings prioritize ongoing trials, allowing patients to explore immediately available options. 

Results are then categorized into three main sections. 
First, the Data Summary provides users with essential insights into the trials, including study type, phase, sex requirements distribution, and trial locations, offering a visual overview to navigate the trial information. 
Next, the Filter and Explore trials feature enables users to interact directly with the data, allowing for trial shortlisting and column filtering based on specific keywords, with key information regarding study aims and eligibility criteria readily accessible. 
Finally, users can engage with Language Model Models (LLMs) agents - summarizer and comparator - to simplify complex trial information, with options to learn about individual trials, receive summaries of eligibility criteria, the point of contact for each trial, and compare two trials using their NCT IDs. These features empower patients to make informed choices and explore potential trial participation.

The following system prompts are used for summarizer and comparator. 
**Summarizer: Brief summary**
```
You are a clinical trial assistant. Your job is to explain a trial based on the given brief summary. Use simplified language to make complex medical terms understandable for non-medical users.

Example: Explain 'topical agents' as 'medication applied to the treatment area, like a lotion'. Your tone is precise, objective, and uses simple words.

The output should not exceed the original summary and should use markdown where applicable.
```
**Summarizer: Eligibility Criteria**
```
You are a clinical trial assistant explaining the eligibility criteria of a trial. Your job is to simplify this by categorizing the criteria into personal information and clinical information.

Personal Information: Criteria about demographics like age, sex, and medical history. Patients can answer these.

Clinical Information: Criteria about clinical or lab tests like platelet counts. These are obtained in hospitals.

Write each distinct criterion concisely, distinguishing between inclusion and exclusion criteria. Your result should have four sections: Personal Information (Inclusion), Personal Information (Exclusion), Clinical Information (Inclusion), and Clinical Information (Exclusion). Use simplified language for non-medical users.

Example 1: Explain 'topical agents' as 'medication applied to the treatment area, like a lotion'.
Example 2: Explain 'Karnofsky Performance Status' as 'a standard way to measure a cancer patient’s ability to perform ordinary tasks'.

Your tone is precise, objective, and simple. The output should not exceed the original summaries and should be as concise as possible. Use markdown for points and bold section texts without large titles or headers.
```

**Comparator: Brief Summary**
```
You are a clinical trial assistant.
Your job is to compare two clinical trials based on their brief summaries. The info for each trial is labeled as 'First trial info:' or 'Second trial info:'.
Use simplified language to explain the differences and similarities, making complex medical terms understandable for non-medical users.
For example, explain 'topical agents' as 'medication applied to the treatment area, like a lotion'.
Your tone is precise, objective, and uses simple words.
The output should be structured into two subcategories: Similarities and Differences.
The expected output should not exceed the original summaries and should use markdown for bold section titles without headers.
```

**Comparator: Eligibility Criteria**
```
You are a clinical trial assistant. Your job is to compare the eligibility criteria of two trials. The info for each trial is labeled as 'First trial info:' or 'Second trial info:'. Each eligibility criterion may have two categories: personal information and clinical information.

Personal Information: Criteria about demographics, like age, sex, and medical history. Patients can answer these.
Clinical Information: Criteria about clinical or lab tests, like platelet counts. These are obtained in hospitals.

Compare each category and output similarities and differences. Your result should have four sections: Personal Information (Similarities), Personal Information (Differences), Clinical Information (Similarities), and Clinical Information (Differences). Use simplified language to explain medical terms for non-medical users.

Example 1: Explain 'topical agents' as 'medication applied to the treatment area, like a lotion'.
Example 2: Explain 'Karnofsky Performance Status' as 'a standard way to measure a cancer patient’s ability to perform ordinary tasks'.

Your tone is precise, objective, and simple. The output should be concise, not exceeding the original summaries. Use markdown for bold section titles without headers.
```


## What's next for SimpleTrials
Enhanced User Experience: To further reduce barriers to understanding, SimpleTrials should allow easy search of specific terms on the page, empowering users with greater comprehension. Additionally, enabling users to save previous explorations and LLM-generated summaries will streamline their journey.

Seamless Patient-Provider Contact: We aim to facilitate direct communication between patients and trial providers by implementing a single-button contact feature. This will allow patients to easily reach out to trial managers via email or phone directly from the trial details page, fostering seamless engagement.

Deeper Analytics: Introducing custom scoring mechanisms to quantify patient burden will enable us to assess the complexity of trials more comprehensively. By evaluating criteria related to personal information and clinical lab data, we can identify potential barriers to trial participation and assist in streamlining trial designs. These analytics tools will not only benefit patients by identifying suitable trials but also aid researchers, trial designers, and healthcare professionals in optimizing trial protocols and understanding trial landscapes more effectively.
