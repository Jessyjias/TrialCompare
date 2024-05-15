import streamlit as st
from st_copy_to_clipboard import st_copy_to_clipboard
from streamlit_echarts import st_echarts
from streamlit_extras.grid import grid 
from annotated_text import annotated_text
import leafmap.foliumap as leafmap
from streamlit_extras.dataframe_explorer import dataframe_explorer 

from markdownlit import mdlit
import pandas as pd
import numpy as np
import time

from utils_ctg import *
from utils_llm import *

def show_trial_detail(cur_row): 
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
        # mdlit(summarizer(openai_api_key, cur_row['briefSummary'], type='briefSummary'))
        
        mdlit('#### Eligibility Criteria')
        # mdlit(cur_row['Eligibility Criteria'])
        # mdlit(summarizer(openai_api_key, cur_row['Eligibility Criteria'], type='eligCriteria'))

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

# from matplotlib.backends.backend_agg import RendererAgg
# _lock = RendererAgg.lock


# -- Set page config
apptitle = 'SimpleTrials'

st.set_page_config(page_title=apptitle, page_icon=":sparkles:")

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
if "nctformsubmit_clicked" not in st.session_state: 
    st.session_state.nctformsubmit_clicked = False

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
def callback_nctformsubmit(): 
    st.session_state.nctformsubmit_clicked = True
def callback_prevtrial():
    st.session_state.prev_trial_clicked = True
def callback_nexttrial():
    st.session_state.next_trial_clicked = True

def main():

    # <------------- side bar --------------> 
    sb = st.sidebar

    sb.title('Get Trial Records Settings')
    sb_expander = sb.expander("Search Parameters", expanded=True)
    demoSearch = sb_expander.button(label="Demo Search  :wave:", on_click=callback_demosearch)
    # demoSearch = sb.button(label="demo parameters", on_click=callback_demosearch)
    # if demoSearch or st.session_state.demo_search_clicked:
    #     default_cond, default_intr, default_loc, default_multiselect_status = 'Breast Cancer', 'Drug', 'California', ['RECRUITING', 'ENROLLING_BY_INVITATION']
    # else: 
    #     default_cond, default_intr, default_loc, default_multiselect_status = '', '', '', ['RECRUITING', 'ENROLLING_BY_INVITATION']
    default_cond, default_intr, default_loc, default_multiselect_status = 'Breast Cancer', 'Drug', 'California', ['RECRUITING', 'ENROLLING_BY_INVITATION']
    ctg_search_form = sb_expander.form("search_trials_form")
    

    input_condition = ctg_search_form.text_input(
    "Condition/Disease  \n Ex) Breast Cancer",
    help="Describe the disease/condition. Ex. Breast cancer",
    key='input_condition', placeholder=default_cond
    )
    input_intr = ctg_search_form.text_input(
        "Type of Intervention  \n Ex) Drug, medical device...",
        help='Describe the type of intervention in the trial. This can be general such as limiting search involving a drug by inputing "DRUG", or entering a specific drug name.',
        key='input_intr', placeholder=default_intr
    )
    input_loc = ctg_search_form.text_input(
        "Location  \n Ex) US, San Francisco, or California",
        help='This can be a country name, state name or city name.',
        key='input_loc', placeholder=default_loc
    )
    multiselect_status = ctg_search_form.multiselect(
        "Status of the trial  \n Ex) Recruiting, Invitation needed...",
        ['RECRUITING', 'ENROLLING_BY_INVITATION','NOT_YET_RECRUITING','ACTIVE_NOT_RECRUITING', 'COMPLETED', 'SUSPENDED', 'TERMINATED', 'WITHDRAWN', 'AVAILABLE', 'NO_LONGER_AVAILABLE', 'TEMPORARILY_NOT_AVAILABLE', 'APPROVED_FOR_MARKETING', 'WITHHELD', 'UNKNOWN'],
        # default=['RECRUITING', 'ENROLLING_BY_INVITATION'],
        help='Filter results by the trial status. Default to presenting only recruiting trials, whether it is by invite or open to public.', 
        key='multiselect_status', default=default_multiselect_status
    )
    if demoSearch or st.session_state.demo_search_clicked:
        input_condition, input_intr, input_loc, multiselect_status = ['Breast Cancer', 'Drug', 'California', ['RECRUITING', 'ENROLLING_BY_INVITATION']]
        # st.session_state.search_params = ['Breast Cancer', 'Drug', 'California', ['RECRUITING', 'ENROLLING_BY_INVITATION']]
        st.session_state.demo_search_clicked = False
    
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
    # print('heree', input_condition, input_intr, input_loc, multiselect_status, st.session_state.form_submit_clicked)
    
    if (form_submit or st.session_state.form_submit_clicked) or (demoSearch or st.session_state.demo_search_clicked):
        if (st.session_state.df_ct.empty) or st.session_state.search_params != [input_condition, input_intr, input_loc, multiselect_status]: 
            sb.divider()
            # <------------- main section display --------------> 
            with st.spinner("Pulling data... (if it takes too long, try to put in more detailed search parameters. )"):
                df_res = get_ctg_records(input_condition, input_intr, input_loc, multiselect_status)
                st.session_state.df_ct = df_res
            
            st.session_state.trial_index = 0
            st.session_state.search_params = [input_condition, input_intr, input_loc, multiselect_status]
            st.session_state.form_submit_clicked = False
        # print(f'{input_condition}, {input_intr}, {input_loc}, {multiselect_status}')
            

    # <------------- display after the dataframe is stored in state --------------> 
    if not st.session_state.df_ct.empty: 
        df = st.session_state.df_ct
    # <------------- main section display: sec 1 analytics --------------> 
        # Graphs
        # mdlit(f'Displaying search result for:  \n Condition: {input_condition}  \n \
        #       Intervention: {input_intr}  \n Location: {input_loc}  \n Status Filters: {multiselect_status}')
        st.header('Data Summary', divider='rainbow')
        annotated_text('Displaying search result for:  \n',
                (input_condition, "condition", "#FFBB00"), '   ',
                (input_intr, "Interventions", "#6AB187"), '   ',
                (input_loc, "Location", "#D2D7D3"), '   \n',
                [(status, "Status", "#fbf3ea") for status in multiselect_status], '  \n')

        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            data_st = df['Study Type'].value_counts().to_dict()
            st.markdown(
                f'<h3><span style="color:black"> Study Type </span></h3>',
                unsafe_allow_html=True,
            )
            st_echarts(options=get_pie_graph_options('Study Types', data=data_st), height="400px")
        with col2:
            df_p = df['Phases'].value_counts().reset_index(name='counts')
            non_phases_terms = [term for term in df_p['Phases'].values if 'phase' not in term.lower()]
            df_p.loc[len(df_p.index)] = ['N/A', df_p[df_p['Phases'].isin(non_phases_terms)].counts.sum()] 
            df_p = df_p[~df_p['Phases'].isin(non_phases_terms)]
            df_p = pd.Series(df_p.counts.values,index=df_p.Phases).to_dict()
            st.markdown(
                f'<h3><span style="color:black"> Study Phase </span></h3>',
                unsafe_allow_html=True,
            )
            st_echarts(options=get_pie_graph_options('Study Phases', data=df_p), height="400px")
        with col3:
            st.markdown(
                f'<h3><span style="color:black"> Recruiting Sex </span></h3>',
                unsafe_allow_html=True,
            )
            df_s = df['Sex'].dropna().value_counts().to_dict()
            st_echarts(options=get_pie_graph_options('Sex', data=df_s), height="400px")

        # Map 
        df_locs_map = get_locations_df(df)
        # with st.expander('map'):
        st.markdown(
                f'<h3><span style="color:black"> Trial Locations </span></h3>',
                unsafe_allow_html=True,
            )
        st.map(df_locs_map,
            latitude='lat',
            longitude='lng',
            size='counts')
        

    if not st.session_state.df_ct.empty: 
        # <------------- main section display: sec 2 available data + explore in flashcard type view --------------> 
        st.header('Filter and Explore Trials', divider='rainbow')
        # st.dataframe(data=df)
        df_display = df[['NCT ID', 'Acronym', 'Study Type', 'briefTitle', 'Overall Status', 'Start Date', 
                'Conditions', 'Interventions', 'Locations', 'Contacts', 
                'Phases', 'Eligibility Criteria', 'Sex', 'Min Age', 'Max Age']]
        df_display = df_display.reindex(columns = ['favourite']+df_display.columns.tolist() )
        df_display['favourite'] = [False]*len(df_display)

        filtered_df = dataframe_explorer(df_display, case=False)
        # st.dataframe(filtered_df, use_container_width=True)

        edited_df = st.data_editor(
            filtered_df,
            column_config={
                "favourite": st.column_config.CheckboxColumn(
                    "Shortlist?",
                    help="Shortlist your **favorite** trials",
                    default=False,
                )
            },
            # disabled=["widgets"],
            # hide_index=True,
        )
        ## TODO: allow edited_df to be used for downstream exploration
        # st.session_state.df_ct = edited_df.reset_index()
        st.header('Learn Trial - Explain to me', divider='rainbow')
        tab1, tab2 = st.tabs(['All - Show me 1 by 1', 'Search and Compare by NCT ID'])
        # st.header('Explore Trials', divider='rainbow')
        with tab1:
            df = st.session_state.df_ct
            trialnav_col1, trialnav_col2 = st.columns(2)
            with trialnav_col1:
                prev_trial = st.button("Previous trial", on_click=callback_prevtrial, key="prev_trial", use_container_width=True) 
            with trialnav_col2:
                next_trial = trialnav_col2.button("Next trial", on_click=callback_nexttrial, key="next_trial", use_container_width=True) 
            if prev_trial or st.session_state.prev_trial_clicked:
                if st.session_state.trial_index-1 >= 0 and st.session_state.trial_index-1 < len(df):
                    st.session_state.trial_index -= 1
                else: 
                    st.warning('No previous trials. Currently displaying the first trial from search. ')
                st.session_state.prev_trial_clicked = False
            if next_trial or st.session_state.next_trial_clicked:
                if st.session_state.trial_index+1 >= 0 and st.session_state.trial_index+1 < len(df):
                    st.session_state.trial_index += 1
                else: 
                    st.warning('No next trials. Currently displaying the last trial from search. ')
                st.session_state.next_trial_clicked = False
            
            cur_row = df.loc[st.session_state.trial_index]
            print(st.session_state.trial_index)
            # 
            show_trial_detail(cur_row)
        
        with tab2:
            nctid_form = st.form('NCT IDs')
            nctid_1 = nctid_form.text_input('Enter 1st NCT ID: ')
            nctid_2 = nctid_form.text_input('Enter 2nd NCT ID: ')

            nctid_form_submit = nctid_form.form_submit_button(label="Search Trial(s)", on_click=callback_nctformsubmit)

            if nctid_form_submit or st.session_state.nctformsubmit_clicked: 
                df_ncts = get_ctg_by_ids([nctid_1, nctid_2])
                df_ncts = df_ncts[df_ncts['NCT ID'].isin([nctid_1, nctid_2])].drop_duplicates().reset_index()
                st.info('Displaying either unique trial result or two distinct trial.  ')
                        # \n If you expect 2 distinct trial results, please check if they are unique.')
                st.dataframe(df_ncts)
                print(len(df_ncts))
                if len(df_ncts)==2: 
                    col1, col2 = st.columns(2)
                    with col1: 
                        show_trial_detail(df_ncts.loc[0])
                    with col2: 
                        show_trial_detail(df_ncts.loc[1])
                    ## compare the eligibility criteria 
                else: 
                    for row_ind in range(0, len(df_ncts)): 
                        cur_row = df_ncts.loc[row_ind]
                        show_trial_detail(cur_row)
                st.session_state.nctformsubmit_clicked = False ## reset back of false to prevent other actions inferences 
            
            ## 




if __name__=="__main__": 
    if 'OPENAI_API_KEY' in st.secrets:
        # msg = st.success('App and API Rendered Successfully! Use Sidebar to initiate search. ', icon='✅')
        openai_api_key = st.secrets['OPENAI_API_KEY']
    else:
        openai_api_key = st.text_input('Enter OpenAI API token:', type='password')
        if not (openai_api_key.startswith('sk-') and len(openai_api_key)==51):
            msg = st.warning('Please enter your credentials!', icon='⚠️')
        else:
            msg = st.success('Proceed to playing with the app!', icon='👉')
    # time.sleep(1.5)
    # msg.empty()

    main() 