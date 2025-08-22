import streamlit as st
from Home import face_rec
import pandas as pd

st.set_page_config(page_title='Reporting', layout='wide')
st.subheader('Reporting')

# Extract data from Redis
name = 'attendance:logs'
def load_logs(name, end=-1):
    logs_list = face_rec.r.lrange(name, start=0,  end=end)
    return logs_list

# tabs to show info
tab1, tab2, tab3 = st.tabs(['Registered Data', 'Logs', 'Attendance Report'])
with tab1:
    if st.button('Refresh Data'):
        with st.spinner('Retrieving data from Redis ...'):
            redis_face_db = face_rec.retrieve_data('academy:register')
            st.dataframe(redis_face_db[['Name', 'Role']])

with tab2:
    if st.button('Refresh Logs'):
        st.write(load_logs(name=name))

with tab3:
    st.subheader('Attendance Report')

    # load logs into logs_list
    logs_list = load_logs(name=name)
    # convert bytes to list
    convert_byte_to_string = lambda x: x.decode('utf-8')
    logs_list_string = list(map(convert_byte_to_string, logs_list))
    # split by @
    split_string = lambda x: x.split('@')
    logs_nested_list = list(map(split_string, logs_list_string))
    # convert nested list into DataFrame
    logs_df = pd.DataFrame(logs_nested_list, columns= ['Name', 'Role','Timestamp'])
    # datetime
    logs_df['Timestamp'] = pd.to_datetime(logs_df['Timestamp'])
    logs_df['Date'] = logs_df['Timestamp'].dt.date
    # Intime and Outtime
    report_df = logs_df.groupby(by=['Date', 'Name', 'Role']).agg(
        In_time = pd.NamedAgg(column='Timestamp', aggfunc='min'),
        Out_time = pd.NamedAgg(column='Timestamp', aggfunc='max')
    ).reset_index()

    report_df['In_time'] = pd.to_datetime(report_df['In_time'])
    report_df['Out_time'] = pd.to_datetime(report_df['Out_time'])
    report_df['Duration'] = report_df['Out_time'] - report_df['In_time']

    # Marking Person absent or present
    all_dates = report_df['Date'].unique()
    name_role = report_df[['Name', 'Role']].drop_duplicates().values.tolist()

    date_name_role_zip = []
    for dt in all_dates:
        for name, role in name_role:
            date_name_role_zip.append([dt, name, role])

    date_name_role_zip_df = pd.DataFrame(date_name_role_zip, columns=['Date', 'Name', 'Role'])
    date_name_role_zip_df = pd.merge(date_name_role_zip_df, report_df, how='left', on=['Date', 'Name','Role'])

    # Durations
    date_name_role_zip_df['Duration_seconds'] = date_name_role_zip_df['Duration'].dt.seconds
    date_name_role_zip_df['Duration_hours'] = date_name_role_zip_df['Duration_seconds'] / (60*60)

    def status_marker(x):
        if pd.Series(x).isnull().all():
            return 'Absent'
        elif x > 0 and x < 1:
            return 'Absent (Less than 1 hour)'
        elif x >= 1 and x < 4:
            return 'Half day (less than 4 hours)'
        elif x >= 4 and x < 6:
            return 'Half day'
        elif x >= 6:
            return 'Present'
    
    date_name_role_zip_df['Status'] = date_name_role_zip_df['Duration_hours'].apply(status_marker)

    st.dataframe(date_name_role_zip_df)