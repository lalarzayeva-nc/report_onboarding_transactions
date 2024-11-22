import streamlit as st
import pandas as pd
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# Set Streamlit to wide mode
st.set_page_config(layout="wide")

# Setting up Google Drive API credentials
service_account_info = st.secrets["gcp_service_account"]
credentials = service_account.Credentials.from_service_account_info(service_account_info)
service = build('drive', 'v3', credentials=credentials)

# Function to read data from Google Drive
def read_data(name, file_id):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    fh.seek(0)
    globals()[name] = pd.read_csv(fh)

# Reading data from Google Drive
read_data('df', '1NLmx2WhjyDuupfUc88DgHPRY-vJt5jg8')  # Replace with your file ID for `df`
read_data('df_verifications', '1TxgH3FNX3-DJ97XGEjxtYU5ykLNkcYz5')  # Replace with your file ID for `df_verifications`

df_verifications['created_at'] = pd.to_datetime(df_verifications['created_at'])
df_verifications['created_at'] = df_verifications['created_at'].dt.strftime('%d-%m-%Y')
df_verifications['attempted_at'] = pd.to_datetime(df_verifications['attempted_at'])
df_verifications['attempted_at'] = df_verifications['attempted_at'].dt.strftime('%d-%m-%Y')

df['created_datetime_dubai'] = pd.to_datetime(df['created_datetime_dubai'])
df['created_datetime_dubai'] = df['created_datetime_dubai'].dt.strftime('%d-%m-%Y')

# Preprocessing the data
df_verifications = df_verifications[['user_id', 'email', 'verification_status', 'created_at', 'attempted_at', 'which_month']]
df_verifications.rename(columns = {'user_id':'consumer_id','created_at':'user_onboarded_at'}, inplace =True)

df_verifications['user_onboarded_at'] = pd.to_datetime(df_verifications['user_onboarded_at'], errors='coerce')
df_verifications = df_verifications.sort_values(by='user_onboarded_at', ascending=False)
df_verifications = df_verifications.reset_index()
del(df_verifications['index'])

df = df[['created_datetime_dubai', 'consumer_id', 'email', 'order_id', 'reference', 'order_amount', 'plan_name', 'order_status', 'merchant_name', 'which_month']]
df.rename(columns={'created_datetime_dubai': 'transaction date','order_amount':'order_amount_qar'}, inplace = True)
df['order_amount_usd'] = df['order_amount_qar'] * 0.27
df = df[['transaction date', 'consumer_id', 'email', 'order_id', 'reference', 'order_amount_qar', 'order_amount_usd','plan_name', 'order_status', 'merchant_name', 'which_month']]

df['transaction date'] = pd.to_datetime(df['transaction date'], errors='coerce')
df = df.sort_values(by='transaction date', ascending=False)
df = df.reset_index()
del(df['index'])

######################PL
#https://drive.google.com/file/d/1ydq4pdNkRH-oiKaJ_hcKAEZ2bjlDdry_/view?usp=drive_link
read_data('df_pl', '1hhKTlbfOY4t7Xn1l9FKmyvxT1SaNaQQz')  # Replace with your file ID for `df`
read_data('df_verifications_pl', '1ydq4pdNkRH-oiKaJ_hcKAEZ2bjlDdry_')  # Replace with your file ID for `df_verifications`

df_verifications_pl['created_at'] = pd.to_datetime(df_verifications_pl['created_at'])
df_verifications_pl['created_at'] = df_verifications_pl['created_at'].dt.strftime('%d-%m-%Y')
df_verifications_pl['attempted_at'] = pd.to_datetime(df_verifications_pl['attempted_at'])
df_verifications_pl['attempted_at'] = df_verifications_pl['attempted_at'].dt.strftime('%d-%m-%Y')

df_pl['created_datetime_dubai'] = pd.to_datetime(df_pl['created_datetime_dubai'])
df_pl['created_datetime_dubai'] = df_pl['created_datetime_dubai'].dt.strftime('%d-%m-%Y')

# Preprocessing the data
df_verifications_pl = df_verifications_pl[['user_id', 'email', 'verification_status', 'created_at', 'attempted_at', 'which_month']]
df_verifications_pl.rename(columns = {'user_id':'consumer_id','created_at':'user_onboarded_at'}, inplace =True)

df_verifications_pl['user_onboarded_at'] = pd.to_datetime(df_verifications_pl['user_onboarded_at'], errors='coerce')
df_verifications_pl= df_verifications_pl.sort_values(by='user_onboarded_at', ascending=False)
df_verifications_pl = df_verifications_pl.reset_index()
del(df_verifications_pl['index'])

df_pl = df_pl[['created_datetime_dubai', 'consumer_id', 'email', 'order_id', 'reference', 'order_amount', 'plan_name', 'order_status', 'merchant_name', 'which_month']]
df_pl.rename(columns={'created_datetime_dubai': 'transaction date','order_amount':'order_amount_qar'}, inplace = True)
df_pl['order_amount_usd'] = df_pl['order_amount_qar'] * 0.27
df_pl = df_pl[['transaction date', 'consumer_id', 'email', 'order_id', 'reference', 'order_amount_qar', 'order_amount_usd','plan_name', 'order_status', 'merchant_name', 'which_month']]

df_pl['transaction date'] = pd.to_datetime(df_pl['transaction date'], errors='coerce')
df_pl = df_pl.sort_values(by='transaction date', ascending=False)
df_pl = df_pl.reset_index()
del(df_pl['index'])




# Streamlit app layout
st.title("REPORT")

# Creating tabs for dataframes
tab1, tab2, tab3, tab4 = st.tabs(["Transactions - SW", "User Onboarding - SW", "Transactions - PL", "User Onboarding - PL"])

################################################################################################################################################
with tab1:
    st.header("Transactions SW Data")

    # Add title for checkboxes
    st.subheader("Which Month")
    unique_months = df['which_month'].dropna().unique()

    # Add a "Select All" checkbox (default to True)
    select_all_sw = st.checkbox("Select All", key="select_all_sw", value=True)

    # Create checkboxes for each month, controlled by "Select All"
    selected_months = []
    for i, month in enumerate(unique_months):
        checked = st.checkbox(f"{month}", key=f"transactions_sw_month_{month}_{i}", value=select_all_sw)
        if checked:
            selected_months.append(month)

    # Apply filters if any are selected
    if selected_months:
        filtered_df = df[df['which_month'].isin(selected_months)]
    else:
        filtered_df = pd.DataFrame(columns=df.columns)  # Empty DataFrame if no month is selected

    # Display the full table with wide mode
    st.dataframe(filtered_df, use_container_width=True, height=1650)

####################################################################################################################################################
with tab2:
    st.header("User Onboarding SW Data")

    # Add title for checkboxes
    st.subheader("Which Month")
    unique_months_verifications = df_verifications['which_month'].dropna().unique()

    # Add a "Select All" checkbox (default to True)
    select_all_sw_verifications = st.checkbox("Select All", key="select_all_sw_verifications", value=True)

    # Create checkboxes for each month, controlled by "Select All"
    selected_months_verifications = []
    for i, month in enumerate(unique_months_verifications):
        checked = st.checkbox(f"{month}", key=f"verifications_sw_month_{month}_{i}", value=select_all_sw_verifications)
        if checked:
            selected_months_verifications.append(month)

    # Apply filters if any are selected
    if selected_months_verifications:
        filtered_verifications_df = df_verifications[df_verifications['which_month'].isin(selected_months_verifications)]
    else:
        filtered_verifications_df = pd.DataFrame(columns=df_verifications.columns)  # Empty DataFrame if no month is selected

    # Display the full table with wide mode
    st.dataframe(filtered_verifications_df, use_container_width=True, height=1650)

##################################################################################################################################################
with tab3:
    st.header("Transactions PL Data")

    # Add title for checkboxes
    st.subheader("Which Month")
    unique_months = df_pl['which_month'].dropna().unique()

    # Add a "Select All" checkbox (default to True)
    select_all_pl = st.checkbox("Select All", key="select_all_pl", value=True)

    # Create checkboxes for each month, controlled by "Select All"
    selected_months = []
    for i, month in enumerate(unique_months):
        checked = st.checkbox(f"{month}", key=f"transactions_pl_month_{month}_{i}", value=select_all_pl)
        if checked:
            selected_months.append(month)

    # Apply filters if any are selected
    if selected_months:
        filtered_df = df_pl[df_pl['which_month'].isin(selected_months)]
    else:
        filtered_df = pd.DataFrame(columns=df_pl.columns)  # Empty DataFrame if no month is selected

    # Display the full table with wide mode
    st.dataframe(filtered_df, use_container_width=True,  height=1650)

######################################################################################################################################################
with tab4:
    st.header("User Onboarding PL Data")

    # Add title for checkboxes
    st.subheader("Which Month")
    unique_months_verifications_pl = df_verifications_pl['which_month'].dropna().unique()

    # Add a "Select All" checkbox (default to True)
    select_all_pl_verifications = st.checkbox("Select All", key="select_all_pl_verifications", value=True)

    # Create checkboxes for each month, controlled by "Select All"
    selected_months_verifications_pl = []
    for i, month in enumerate(unique_months_verifications_pl):
        checked = st.checkbox(f"{month}", key=f"verifications_pl_month_{month}_{i}", value=select_all_pl_verifications)
        if checked:
            selected_months_verifications_pl.append(month)

    # Apply filters if any are selected
    if selected_months_verifications_pl:
        filtered_verifications_df_pl = df_verifications_pl[df_verifications_pl['which_month'].isin(selected_months_verifications_pl)]
    else:
        filtered_verifications_df_pl = pd.DataFrame(columns=df_verifications_pl.columns)  # Empty DataFrame if no month is selected

    # Display the full table with wide mode
    st.dataframe(filtered_verifications_df_pl, use_container_width=True, height=1650)
