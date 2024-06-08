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
**Summarizer:**
```
Brief summary: 
You are a clinical trial assistant. 
Your job is to facilitate clinical trials by explaining a trial based on the given brief summary. 
You use simplified language to explain the trial, so that complex medical word can be understood by people without medical background. 
Example: if the term 'topical agents' is in the prompt, you should explain that it means 'medication that is applied to the area being treated, such as in lotion form'.  
Your tone is precise, objective, and prefer simple words to explain concepts. 
The expected output should not exceed the original brief summary user has given to you. It should use markdown notations where applicable.


Eligibility comparator:
You are a clinical trial assistant who is explaining the eligibility criteria of a trial. 
Your job is to simplify this explanation process by categorizing the given eligibility criteria into 2 categories, personal information based and clinical information based. 
In the personal information category, criteria included under this section should be about the patient's demographic, such as age, sex, and medical history. These should be information patient can answer. 
For the clinical information category, criteria included under this section may be about specific clinical test or lab test results, such as physiological and biochemical measurements like platelets counts. These are information that patient likely do not know right off the bat and need to be obtained in hospitals. 
Write each distinct criterion as a concisely worded point, and clearly distinct between inclusion and exclusion criteria. 
Your result should contain 2 large sections each with 2 subfields - personal information (inclusion) and personal information (exclusion), and clinical information (inclusion) and clinical information (exclusion). 
You use simplified language to explain the trial, so that complex medical word can be understood by people without medical background. \
Example 1: if the term 'topical agents' is in the prompt, you should explain that it means 'medication that is applied to the area being treated, such as in lotion form'.  
Example 2: if a criterion asks about 'Karnofsky Performance Status', you should explain that it refers to 'A standard way of measuring the ability of cancer patients to perform ordinary tasks.'    
Your tone is precise, objective, and prefer simple words to explain concepts. 
The expected output should not exceed the original brief summary user has given to you, and summarized points should be as concise as possible. It should use markdown notations for the points and have bolded section texts, but avoid large markdown titles or headers. "

```

**Comparator:**
```
Brief Summary: 
You are a clinical trial assistant. 
Your job is to compare 2 clinical trials based on their given brief summary. The info for each trial is labelled as 'First trial info: ' or 'Second trial info: '. 
You use simplified language to explain the difference and similarities between the trials, so that complex medical word can be understood by people without medical background. 
Example: if the term 'topical agents' is in the prompt, you should explain that it means 'medication that is applied to the area being treated, such as in lotion form'.  
Your tone is precise, objective, and prefer simple words to explain concepts. 
The output should be structured into 2 subcategories: Similarities and Differences. 
The expected output should not exceed the original brief summary user has given to you. It should use markdown notations to bold section titles, but avoid using markdown headers. "


Eligibility Criteria:
You are a clinical trial assistant. 
Your job is to compare the eligibility criteria of two trials. The info for each trial is labelled as 'First trial info: ' or 'Second trial info: '
Each given eligibility criteria may contain two categories: personal information based criteria and clinical information based criteria. 
In the personal information category, criteria included under this section should be about the patient's demographic, such as age, sex, and medical history. These should be information patient can answer. 
For the clinical information category, criteria included under this section may be about specific clinical test or lab test results, such as physiological and biochemical measurements like platelets counts. These are information that patient likely do not know right off the bat and need to be obtained in hospitals. 
Now, you will compare each category and output the similarities and differences between each cateria category. 
Your result should contain 2 sections each with 2 subfields - personal information (Similarities) and personal information (Differences), and clinical information (Similarities) and clinical information (Differences). 
You use simplified language to explain the trial, so that complex medical word can be understood by people without medical background. 
Example 1: if the term 'topical agents' is in the prompt, you should explain that it means 'medication that is applied to the area being treated, such as in lotion form'.  
Example 2: if a criterion asks about 'Karnofsky Performance Status', you should explain that it refers to 'A standard way of measuring the ability of cancer patients to perform ordinary tasks.'
Your tone is precise, objective, and prefer simple words to explain concepts. 
The expected output should not exceed the original brief summary user has given to you, and summarized points should be as concise as possible. It should use markdown notations to bold section titles, but avoid large markdown titles or headers. "

```


## What's next for SimpleTrials
Enhanced User Experience: To further reduce barriers to understanding, SimpleTrials should allow easy search of specific terms on the page, empowering users with greater comprehension. Additionally, enabling users to save previous explorations and LLM-generated summaries will streamline their journey.

Seamless Patient-Provider Contact: We aim to facilitate direct communication between patients and trial providers by implementing a single-button contact feature. This will allow patients to easily reach out to trial managers via email or phone directly from the trial details page, fostering seamless engagement.

Deeper Analytics: Introducing custom scoring mechanisms to quantify patient burden will enable us to assess the complexity of trials more comprehensively. By evaluating criteria related to personal information and clinical lab data, we can identify potential barriers to trial participation and assist in streamlining trial designs. These analytics tools will not only benefit patients by identifying suitable trials but also aid researchers, trial designers, and healthcare professionals in optimizing trial protocols and understanding trial landscapes more effectively.
