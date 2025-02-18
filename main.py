import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set up the Streamlit page
st.set_page_config(page_title='Data Sweeper', layout='wide')
st.title('Data Sweeper')
st.write('Transform your files between CSV or Excel Format with built-in data cleaning and visualization!')

# Upload files
uploaded_files = st.file_uploader('Upload Your (CSV or Excel files):', type=['csv', 'xlsx'], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        # ✅ Corrected file extension extraction
        file_ext = os.path.splitext(file.name)[1].lower()

        if file_ext == '.csv':
            df = pd.read_csv(file)
        elif file_ext == '.xlsx':  # ✅ Fixed typo
            df = pd.read_excel(file, engine='openpyxl')  # ✅ Ensure openpyxl is used
        else:
            st.error(f'Unsupported file type: {file_ext}')
            continue

        # ✅ Display file info
        st.write(f'**File Name:** {file.name}')
        st.write(f'**File Size:** {file.size / 1024:.2f} KB')
        st.write('Preview of the DataFrame:')
        st.dataframe(df.head())

        # ✅ Data Cleaning Options
        st.subheader('Data Cleaning Options:')
        if st.checkbox(f'Clean data for {file.name}'):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f'Remove Duplicates from {file.name}'):
                    df.drop_duplicates(inplace=True)
                    st.write('✅ Duplicates Removed!')

            with col2:
                if st.button(f'Fill Missing Values for {file.name}'):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write('✅ Missing Values have been Filled!')

        # ✅ Column Selection for Conversion
        st.subheader('Select Columns to Keep')
        selected_columns = st.multiselect(f'Choose Columns for {file.name}', df.columns, default=df.columns)
        df = df[selected_columns]

        # ✅ Data Visualization
        if st.checkbox(f'Show Visualization for {file.name}'):
            st.subheader('Bar Chart')
            numeric_df = df.select_dtypes(include='number')  # Select numeric columns only
            if not numeric_df.empty:
                st.bar_chart(numeric_df.iloc[:, :2])  # ✅ Fixed selection of first 2 numeric columns
            else:
                st.warning('No numeric columns available for visualization.')

        # ✅ File Conversion (CSV <-> Excel)
        st.subheader('Convert File Type')
        conversion_type = st.radio(f'Convert {file.name} to:', ['CSV', 'Excel'], key=file.name)

        if st.button(f'Convert {file.name}'):
            buffer = BytesIO()
            if conversion_type == 'CSV':
                df.to_csv(buffer, index=False)
                new_file_name = file.name.rsplit('.', 1)[0] + '.csv'
                mime_type = 'text/csv'
            elif conversion_type == 'Excel':
                df.to_excel(buffer, index=False, engine='openpyxl')  # ✅ Fixed Excel export
                new_file_name = file.name.rsplit('.', 1)[0] + '.xlsx'
                mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            buffer.seek(0)

            # ✅ Download button
            st.download_button(
                label=f'Download {file.name} as {conversion_type}',
                data=buffer,
                filename=new_file_name,
                mime=mime_type
            )

st.success('✅ All files processed successfully!')

# import streamlit as st
# import pandas as pd
# import os

# st.set_page_config(page_title='Data Sweeper', layout='wide')
# st.title('Data Sweeper')
# st.write('Transform your files between CSV or Excel Format with built-in data cleaning and visualization!')

# uploaded_files = st.file_uploader('Upload Your (CSV or Excel files):', type=['csv', 'xlsx'], accept_multiple_files=True)

# if uploaded_files:
#     for file in uploaded_files:
#         file_ext = os.path.splitext(file.name)[1].lower()

#         if file_ext == '.csv':
#             df = pd.read_csv(file)
#         elif file_ext == '.xlsx':  # Corrected from 'xlex' to 'xlsx'
#             df = pd.read_excel(file)
#         else:
#             st.error(f'Unsupported file type: {file_ext}')
#             continue
        
#         st.write(df.head())  # Display first few rows

