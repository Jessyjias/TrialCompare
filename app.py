import streamlit as st
from st_copy_to_clipboard import st_copy_to_clipboard
from streamlit_echarts import st_echarts
from streamlit_extras.grid import grid 
from annotated_text import annotated_text
import leafmap.foliumap as leafmap

from markdownlit import mdlit
import pandas as pd
import numpy as np

from utils_ctg import *
from utils_llm import *

# from matplotlib.backends.backend_agg import RendererAgg
# _lock = RendererAgg.lock


# -- Set page config
apptitle = 'TrialExplore'

st.set_page_config(page_title=apptitle, page_icon=":eyeglasses:")

## -- set some cache functions 

## -- set some states 
if "demo_search_clicked" not in st.session_state:
    st.session_state.demo_search_clicked = False
if 'form_submit_clicked' not in st.session_state:
    st.session_state.form_submit_clicked = False
if 'df_ct' not in st.session_state:
    st.session_state.df_ct = pd.DataFrame()
if 'trial_index' not in st.session_state:
    st.session_state.trial_index = 0 
if 'search_params' not in st.session_state:
    st.session_state.search_params = []
if "next_trial_clicked" not in st.session_state:
    st.session_state.next_trial_clicked = False
if "prev_trial_clicked" not in st.session_state:
    st.session_state.prev_trial_clicked = False

## some css modifications 
st.markdown("""
    <style>
        .stMultiSelect [data-baseweb=select] span{
            max-width: 300px;
            font-size: 0.8rem;
        }
    </style>
    """, unsafe_allow_html=True)

# button callbacks 
def callback_formsubmit():
    st.session_state.form_submit_clicked = True
def callback_demosearch():
    st.session_state.demo_search_clicked = True
def callback_prevtrial():
    st.session_state.prev_trial_clicked = True
def callback_nexttrial():
    st.session_state.next_trial_clicked = True

def main():

    # <------------- side bar --------------> 
    sb = st.sidebar

    if 'OPENAI_API_KEY' in st.secrets:
        st.success('API key already provided!', icon='✅')
        openai_api_key = st.secrets['OPENAI_API_KEY']
    else:
        openai_api_key = st.text_input('Enter OpenAI API token:', type='password')
        if not (openai_api_key.startswith('sk-') and len(openai_api_key)==51):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to playing with the app!', icon='👉')

    sb.title('Get Trial Records Settings')
    sb_expander = sb.expander("Search Parameters", expanded=True)
    ctg_search_form = sb_expander.form("search_trials_form")
    
    input_condition = ctg_search_form.text_input(
    "Condition/Disease  \n Ex) Breast Cancer",
    help="Describe the disease/condition. Ex. Breast cancer",
    key='input_condition'
    )
    input_intr = ctg_search_form.text_input(
        "Type of Intervention  \n Ex) Drug, medical device...",
        help='Describe the type of intervention in the trial. This can be general such as limiting search involving a drug by inputing "DRUG", or entering a specific drug name.',
        key='input_intr'
    )
    input_loc = ctg_search_form.text_input(
        "Location  \n Ex) US, San Francisco, or California",
        help='This can be a country name, state name or city name.',
        key='input_loc'
    )
    multiselect_status = ctg_search_form.multiselect(
        "Status of the trial  \n Ex) Recruiting, Invitation needed...",
        ['RECRUITING', 'ENROLLING_BY_INVITATION','NOT_YET_RECRUITING','ACTIVE_NOT_RECRUITING', 'COMPLETED', 'SUSPENDED', 'TERMINATED', 'WITHDRAWN', 'AVAILABLE', 'NO_LONGER_AVAILABLE', 'TEMPORARILY_NOT_AVAILABLE', 'APPROVED_FOR_MARKETING', 'WITHHELD', 'UNKNOWN'],
        default=['RECRUITING', 'ENROLLING_BY_INVITATION'],
        help='Filter results by the trial status. Default to presenting only recruiting trials, whether it is by invite or open to public.', 
        key='multiselect_status'
    )
    # demoSearch = sb.button(label="demo search", on_click=callback_demosearch)
    # if demoSearch or st.session_state.demo_search_clicked:
    #     input_condition, input_intr, input_loc, multiselect_status = 'Breast Cancer', 'Drug', 'California', ['RECRUITING', 'ENROLLING_BY_INVITATION']
    #     # if know this would work: st.session_state['text'] = autofill_value
    #     # st.session_state.demo_search_clicked = False

    form_submit = ctg_search_form.form_submit_button(label="Submit", on_click=callback_formsubmit)
    sb.divider()
    saved_trials = sb.title('Saved trial IDs')
    sb.subheader('Copy and paste for later') 
                        # on_click=get_ctg_records, 
                        # args=(input_condition, input_intr, input_loc, multiselect_status), 
                        # kwargs=None,use_container_width=False)
    if st.session_state.search_params == []:
        st.session_state.search_params = [input_condition, input_intr, input_loc, multiselect_status]
    
    # <------------- calling api for getting results: first search or when parameters change --------------> 
    if (st.session_state.df_ct.empty) or st.session_state.search_params != [input_condition, input_intr, input_loc, multiselect_status]: 
        if (form_submit or st.session_state.form_submit_clicked): 
            sb.divider()
            sb.write(input_condition, input_intr, input_loc, multiselect_status)
            # <------------- main section display --------------> 
            with st.spinner("Pulling data... (if it takes too long, try to put in more detailed search parameters. )"):
                df_res = get_ctg_records(input_condition, input_intr, input_loc, multiselect_status)
                st.session_state.df_ct = df_res
            
            st.session_state.trial_index = 0
            st.session_state.search_params = [input_condition, input_intr, input_loc, multiselect_status]
            # st.session_state.form_submit_clicked = False
            

    # <------------- display after the dataframe is stored in state --------------> 
    if not st.session_state.df_ct.empty: 
        df = st.session_state.df_ct
    # <------------- main section display: sec 1 analytics --------------> 
        # Graphs
        st.header('Data Summary', divider='rainbow')
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            data_st = df['Study Type'].value_counts().to_dict()
            st.header('Study Type')
            st_echarts(options=get_pie_graph_options('Study Types', data=data_st), height="400px")
        with col2:
            df_p = df['Phases'].value_counts().reset_index(name='counts')
            non_phases_terms = [term for term in df_p['Phases'].values if 'phase' not in term.lower()]
            df_p.loc[len(df_p.index)] = ['N/A', df_p[df_p['Phases'].isin(non_phases_terms)].counts.sum()] 
            df_p = df_p[~df_p['Phases'].isin(non_phases_terms)]
            df_p = pd.Series(df_p.counts.values,index=df_p.Phases).to_dict()
            st.header('Study Phase')
            st_echarts(options=get_pie_graph_options('Study Phases', data=df_p), height="450px")
        with col3:
            st.header('Recruiting Sex')
            df_s = df['Sex'].dropna().value_counts().to_dict()
            st_echarts(options=get_pie_graph_options('Sex', data=df_s), height="400px")

        # Map 
        df_locs_map = get_locations_df(df)
        # with st.expander('map'):
        st.map(df_locs_map,
            latitude='lat',
            longitude='lng',
            size='counts')
        

    if not st.session_state.df_ct.empty: 
        # <------------- main section display: sec 2 available data + explore in flashcard type view --------------> 
        st.header('Filter Result Clinical Trials', divider='rainbow')
        st.dataframe(data=df)


        st.header('Explore Filtered Trials', divider='rainbow')
        df = st.session_state.df_ct
        prev_trial = st.button("Previous trial", on_click=callback_prevtrial, key="prev_trial", use_container_width=True) 
        if prev_trial or st.session_state.prev_trial_clicked:
            st.session_state.trial_index -= 1
            st.session_state.prev_trial_clicked = False
        next_trial = st.button("Next trial", on_click=callback_nexttrial, key="next_trial", use_container_width=True) 
        if next_trial or st.session_state.next_trial_clicked:
            st.session_state.trial_index += 1
            st.session_state.next_trial_clicked = False
        
        cur_row = df.loc[st.session_state.trial_index]

        # TODO: check if the index is valid - 0 to max leng

        print(st.session_state.trial_index)
        st.markdown(
            f'<h3><span style="color:black"> {cur_row.briefTitle}</span></h3>',
            unsafe_allow_html=True,
        )
        annotated_text((str(st.session_state.trial_index), "form index", "#CEE6F2"), '   ',
                        (cur_row['NCT ID'], "NCT ID", "#CEE6F2"), '  \n',
                        [(intervent, "Interventions", "#6AB187") for intervent in cur_row['Interventions'].split(', ')], '  \n',
                    [(cond, "condition", "#FFBB00") for cond in cur_row['Conditions'].split(', ')], '  \n')
        
        with st.expander('View Trial Details', expanded=True): 
            mdlit('#### Brief Summary')
            # mdlit(cur_row['briefSummary'])
            mdlit(summarizer(openai_api_key, cur_row['briefSummary'], type='briefSummary'))
            
            mdlit('#### Eligibility Criteria')
            # mdlit(cur_row['Eligibility Criteria'])
            mdlit(summarizer(openai_api_key, cur_row['Eligibility Criteria'], type='eligCriteria'))

            mdlit('#### Contacts')
            contacts = [cont for cont in cur_row['Contacts'].split(', ')]
            if len(contacts)<1: 
                mdlit("Inadequate contact information. Please refer to original record of the trial. ")
            else:
                for contact in contacts: 
                    contact_info = contact.split(' - ')
                    if len(contact_info)<5:
                        mdlit("Inadequate contact information. Please refer to original record of the trial. ")
                        break
                    else:
                        mdlit('* Name: '+contact_info[0] + "  \n" 
                            +'* Phone Number: '+contact_info[2]  + "  \n" + '* Email: '+contact_info[4] + "  \n" ) #+'* Role: '+contact_info[1] + "  \n" 
                        # TODO: send email logic 
            st.link_button("View Complete Trial Record", f"https://clinicaltrials.gov/study/{cur_row['NCT ID']}")


if __name__=="__main__": 
    main() 