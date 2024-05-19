import requests
import pandas as pd


def get_ctg_records(cond, intr, locn, status):
    # Initial URL for the first API call
    base_url = "https://clinicaltrials.gov/api/v2/studies"
    params = {
        "query.cond": cond,
        "query.intr": intr,
        'query.locn': locn, 
        'filter.overallStatus':  '|'.join(status) ,
        "pageSize": 100, 
    }

    # Initialize an empty list to store the data
    data_list = []

    # Loop until there is no nextPageToken
    # while True:
    # max 1000 entries 
    n_page = 0
    while n_page<10 and True:
        # Print the current URL (for debugging purposes)
        n_page += 1
        print("Fetching data from:", base_url + '?' + '&'.join([f"{k}={v}" for k, v in params.items()]))
        
        # Send a GET request to the API
        response = requests.get(base_url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()  # Parse JSON response
            studies = data.get('studies', [])  # Extract the list of studies

            # Loop through each study and extract specific information
            for study in studies:
                # Safely access nested keys
                nctId = study['protocolSection']['identificationModule'].get('nctId', 'Unknown')
                briefTitle = study['protocolSection']['identificationModule'].get('briefTitle', 'Unknown')
                officialTitle = study['protocolSection']['identificationModule'].get('OfficialTitle', 'Unknown')
                briefSummary = study['protocolSection']['descriptionModule'].get('briefSummary', 'Unknown')
                overallStatus = study['protocolSection']['statusModule'].get('overallStatus', 'Unknown')
                startDate = study['protocolSection']['statusModule'].get('startDateStruct', {}).get('date', 'Unknown Date')
                conditions = ', '.join(study['protocolSection']['conditionsModule'].get('conditions', ['No conditions listed']))
                acronym = study['protocolSection']['identificationModule'].get('acronym', 'Unknown')
                # nctId = study['protocolSection']['identificationModule'].get('nctId', 'Unknown')

                # Extract interventions safely
                interventions_list = study['protocolSection'].get('armsInterventionsModule', {}).get('interventions', [])
                interventions = ', '.join([intervention.get('name', 'No intervention name listed') for intervention in interventions_list]) if interventions_list else "No interventions listed"
                
                # Extract locations safely
                locations_list = study['protocolSection'].get('contactsLocationsModule', {}).get('locations', [])
                # location_facilities = 
                locations = ', '.join([f"{location.get('city', 'No City')} / {location.get('state', 'No State')} / {location.get('country', 'No Country')}" for location in locations_list]) if locations_list else "No locations listed"
                
                # Extract contact info 
                centralContact = study['protocolSection'].get('contactsLocationsModule', {}).get('centralContacts', [])
                contacts = ', '.join([f"{contact.get('name', 'No Name')} -  {contact.get('role', 'No Role')} - {contact.get('phone', 'No Phone')} - {contact.get('phoneExt', 'No Phone Ext')} - {contact.get('email', 'No email')}" for contact in centralContact]) if centralContact else "No contact listed"

                # Extract dates and phases
                primaryCompletionDate = study['protocolSection']['statusModule'].get('primaryCompletionDateStruct', {}).get('date', 'Unknown Date')
                studyFirstPostDate = study['protocolSection']['statusModule'].get('studyFirstPostDateStruct', {}).get('date', 'Unknown Date')
                lastUpdatePostDate = study['protocolSection']['statusModule'].get('lastUpdatePostDateStruct', {}).get('date', 'Unknown Date')
                studyType = study['protocolSection']['designModule'].get('studyType', 'Unknown')
                phases = ', '.join(study['protocolSection']['designModule'].get('phases', ['Not Available']))

                # Extract eligibility requirements safely 
                eligibilityCriteria = study['protocolSection']['eligibilityModule'].get('eligibilityCriteria', {})
                sex = study['protocolSection']['eligibilityModule'].get('sex', {})
                genderDescription = study['protocolSection']['eligibilityModule'].get('genderDescription', 'Unknown')
                minimumAge = study['protocolSection']['eligibilityModule'].get('minimumAge', 'Unknown')
                maximumAge = study['protocolSection']['eligibilityModule'].get('maximumAge', 'Unknown')
                # phases = ', '.join(study['protocolSection']['designModule'].get('phases', ['Not Available']))

                # Append the data to the list as a dictionary
                data_list.append({
                    "NCT ID": nctId,
                    "Acronym": acronym,
                    "briefTitle": briefTitle, 
                    # "officialTitle": officialTitle, 
                    "briefSummary": briefSummary, 
                    "Overall Status": overallStatus,
                    "Start Date": startDate,
                    "Conditions": conditions,
                    "Interventions": interventions,
                    "Locations": locations,
                    "Contacts": contacts, 
                    "Primary Completion Date": primaryCompletionDate,
                    "Study First Post Date": studyFirstPostDate,
                    "Last Update Post Date": lastUpdatePostDate,
                    "Study Type": studyType,
                    "Phases": phases,
                    
                    # 
                    "Eligibility Criteria": eligibilityCriteria,
                    "Sex": sex,
                    # "Gender": genderDescription,
                    "Min Age": minimumAge,
                    "Max Age": maximumAge,
                })

            # Check for nextPageToken and update the params or break the loop
            nextPageToken = data.get('nextPageToken')
            if nextPageToken:
                params['pageToken'] = nextPageToken  # Set the pageToken for the next request
            else:
                break  # Exit the loop if no nextPageToken is present
        else:
            print("Failed to fetch data. Status code:", response.status_code, response.text)

            ### TODO: return a default dataframe? 
            break

    if len(data_list)>0: 
        df = pd.DataFrame(data_list)
    else: 
        df = pd.read_csv("./data/prev_search_results.csv")
        ## process age to integers 
    
    df['Min Age'].dropna(inplace=True)
    df['Max Age'].dropna(inplace=True)
    df['Min Age'].replace('Unknown', '0 years', inplace=True)
    df['Max Age'][(df['Max Age'] == 'Unknown')] = df['Min Age']
    df['Min Age'] = df['Min Age'].apply(lambda x: [int(i) for i in x.split() if i.isdigit()][0])
    df['Max Age'] = df['Max Age'].apply(lambda x: [int(i) for i in x.split() if i.isdigit()][0])

    df.to_csv('./data/prev_search_results.csv')

    print('got all records', df.shape)
    return df

def get_ctg_by_ids(ids):
    # Initial URL for the first API call
    base_url = "https://clinicaltrials.gov/api/v2/studies"
    # Initialize an empty list to store the data
    data_list = []
    for id in ids: 
        params = {
            # 'filter.ids': '|'.join(ids)
            'filter.ids': id, 
            "pageSize": 1, 
        }
        # Loop until there is no nextPageToken / no ids left 
        n_page = 0
        while n_page<1 and True:
            # Print the current URL (for debugging purposes)
            n_page += 1
            print("Fetching data from:", base_url + '?' + '&'.join([f"{k}={v}" for k, v in params.items()]))
            
            # Send a GET request to the API
            response = requests.get(base_url, params=params)

            # Check if the request was successful
            if response.status_code == 200:
                data = response.json()  # Parse JSON response
                studies = data.get('studies', [])  # Extract the list of studies

                # Loop through each study and extract specific information
                for study in studies:
                    # Safely access nested keys
                    nctId = study['protocolSection']['identificationModule'].get('nctId', 'Unknown')
                    briefTitle = study['protocolSection']['identificationModule'].get('briefTitle', 'Unknown')
                    officialTitle = study['protocolSection']['identificationModule'].get('OfficialTitle', 'Unknown')
                    briefSummary = study['protocolSection']['descriptionModule'].get('briefSummary', 'Unknown')
                    overallStatus = study['protocolSection']['statusModule'].get('overallStatus', 'Unknown')
                    startDate = study['protocolSection']['statusModule'].get('startDateStruct', {}).get('date', 'Unknown Date')
                    conditions = ', '.join(study['protocolSection']['conditionsModule'].get('conditions', ['No conditions listed']))
                    acronym = study['protocolSection']['identificationModule'].get('acronym', 'Unknown')
                    # nctId = study['protocolSection']['identificationModule'].get('nctId', 'Unknown')

                    # Extract interventions safely
                    interventions_list = study['protocolSection'].get('armsInterventionsModule', {}).get('interventions', [])
                    interventions = ', '.join([intervention.get('name', 'No intervention name listed') for intervention in interventions_list]) if interventions_list else "No interventions listed"
                    
                    # Extract locations safely
                    locations_list = study['protocolSection'].get('contactsLocationsModule', {}).get('locations', [])
                    # location_facilities = 
                    locations = ', '.join([f"{location.get('city', 'No City')} / {location.get('state', 'No State')} / {location.get('country', 'No Country')}" for location in locations_list]) if locations_list else "No locations listed"
                    
                    # Extract contact info 
                    centralContact = study['protocolSection'].get('contactsLocationsModule', {}).get('centralContacts', [])
                    contacts = ', '.join([f"{contact.get('name', 'No Name')} -  {contact.get('role', 'No Role')} - {contact.get('phone', 'No Phone')} - {contact.get('phoneExt', 'No Phone Ext')} - {contact.get('email', 'No email')}" for contact in centralContact]) if centralContact else "No contact listed"

                    # Extract dates and phases
                    primaryCompletionDate = study['protocolSection']['statusModule'].get('primaryCompletionDateStruct', {}).get('date', 'Unknown Date')
                    studyFirstPostDate = study['protocolSection']['statusModule'].get('studyFirstPostDateStruct', {}).get('date', 'Unknown Date')
                    lastUpdatePostDate = study['protocolSection']['statusModule'].get('lastUpdatePostDateStruct', {}).get('date', 'Unknown Date')
                    studyType = study['protocolSection']['designModule'].get('studyType', 'Unknown')
                    phases = ', '.join(study['protocolSection']['designModule'].get('phases', ['Not Available']))

                    # Extract eligibility requirements safely 
                    eligibilityCriteria = study['protocolSection']['eligibilityModule'].get('eligibilityCriteria', {})
                    sex = study['protocolSection']['eligibilityModule'].get('sex', {})
                    genderDescription = study['protocolSection']['eligibilityModule'].get('genderDescription', 'Unknown')
                    minimumAge = study['protocolSection']['eligibilityModule'].get('minimumAge', 'Unknown')
                    maximumAge = study['protocolSection']['eligibilityModule'].get('maximumAge', 'Unknown')
                    # phases = ', '.join(study['protocolSection']['designModule'].get('phases', ['Not Available']))

                    # Append the data to the list as a dictionary
                    data_list.append({
                        "NCT ID": nctId,
                        "Acronym": acronym,
                        "briefTitle": briefTitle, 
                        # "officialTitle": officialTitle, 
                        "briefSummary": briefSummary, 
                        "Overall Status": overallStatus,
                        "Start Date": startDate,
                        "Conditions": conditions,
                        "Interventions": interventions,
                        "Locations": locations,
                        "Contacts": contacts, 
                        "Primary Completion Date": primaryCompletionDate,
                        "Study First Post Date": studyFirstPostDate,
                        "Last Update Post Date": lastUpdatePostDate,
                        "Study Type": studyType,
                        "Phases": phases,
                        
                        # 
                        "Eligibility Criteria": eligibilityCriteria,
                        "Sex": sex,
                        # "Gender": genderDescription,
                        "Min Age": minimumAge,
                        "Max Age": maximumAge,
                    })

                # Check for nextPageToken and update the params or break the loop
                nextPageToken = data.get('nextPageToken')
                if nextPageToken:
                    params['pageToken'] = nextPageToken  # Set the pageToken for the next request
                else:
                    break  # Exit the loop if no nextPageToken is present
            else:
                print("Failed to fetch data. Status code:", response.status_code, response.text)

                ### TODO: return a default dataframe? DONE 
                break
    

    if len(data_list)>0: 
        df = pd.DataFrame(data_list)
    else: 
        df = pd.read_csv("./data/prev_search_results_ids.csv")
        ## process age to integers 
    # print(df)
    df['Min Age'].dropna(inplace=True)
    df['Max Age'].dropna(inplace=True)
    df['Min Age'].replace('Unknown', '0 years', inplace=True)
    df['Max Age'][(df['Max Age'] == 'Unknown')] = df['Min Age']
    df['Min Age'] = df['Min Age'].apply(lambda x: [int(i) for i in x.split() if i.isdigit()][0])
    df['Max Age'] = df['Max Age'].apply(lambda x: [int(i) for i in x.split() if i.isdigit()][0])

    df.to_csv('./data/prev_search_results_ids.csv')

    print('got all records', df.shape)
    return df


def get_pie_graph_options(name, data): 
    options = {
        "tooltip": {"trigger": "item"},
        "legend": {"top": "1%", "left": "top"},
        "series": [
            {
                "name": name,
                "type": "pie",
                "radius": ["40%", "70%"],
                "avoidLabelOverlap": True,
                "itemStyle": {
                    "borderRadius": 10,
                    "borderColor": "#fff",
                    "borderWidth": 2,
                },
                "label": {"show": False, "position": "center"},
                "emphasis": {
                    "label": {"show": True, "fontSize": "15", "fontWeight": "bold"}
                },
                "labelLine": {"show": False},
                "data": [{"value": val, "name": n} for n,val in data.items()]
            }
        ],
    }

    return options 

def get_locations_df(df): 
    cities_list = [cities.split(', ') for cities in df['Locations'].values.tolist()]
    cities_list = [city for cities in cities_list for city in cities if '/' in city and len(city.split(' / '))==3]
    cities = [city.split(' / ')[0] for city in cities_list]
    states = [city.split(' / ')[1] for city in cities_list]
    countries = [city.split(' / ')[2] for city in cities_list]
    df_locs = pd.DataFrame(data={'city':cities, 'state':states, 'country':countries})
    df_locs = df_locs.value_counts().reset_index(name='counts')
    df_cities_geo = pd.read_csv('./data/worldcities.csv')
    df_locs_formap = pd.merge(df_locs, df_cities_geo[['city', 'lat', 'lng', 'admin_name', 'country']], left_on=['city', 'state', 'country'], right_on=['city', 'admin_name', 'country'], how='inner')
    df_locs_formap['counts'] = df_locs_formap['counts']*100
    # print(df_locs_formap)
    return df_locs_formap