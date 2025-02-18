
import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Streamlit Page Config
st.set_page_config(page_title='Data Sweeper', layout='wide')
st.title('Data Sweeper')
st.write('Transform your files between CSV or Excel Format with built-in data cleaning and visualization!')

# File Uploader
uploaded_files = st.file_uploader('Upload Your (CSV or Excel files):', type=['csv', 'xlsx'], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        # ✅ Corrected file extension extraction
        file_ext = os.path.splitext(file.name)[1].lower()

        if file_ext == '.csv':
            df = pd.read_csv(file)
        elif file_ext == '.xlsx':
            df = pd.read_excel(file, engine='openpyxl')  # ✅ Ensure openpyxl is used
        else:
            st.error(f'Unsupported file type: {file_ext}')
            continue

        # ✅ Display file info
        st.write(f'**File Name:** {file.name}')
        st.write(f'**File Size:** {file.size / 1024:.2f} KB')
        st.dataframe(df.head())

        # ✅ File Conversion (CSV <-> Excel)
        st.subheader('Convert File Type')
        conversion_type = st.radio(f'Convert {file.name} to:', ['CSV', 'Excel'], key=file.name)

        if st.button(f'Convert {file.name}'):
            buffer = BytesIO()
            new_file_name = file.name.rsplit('.', 1)[0]  # Remove original extension

            if conversion_type == 'CSV':
                df.to_csv(buffer, index=False)
                new_file_name += '.csv'
                mime_type = 'text/csv'
            elif conversion_type == 'Excel':
                df.to_excel(buffer, index=False, engine='openpyxl')
                new_file_name += '.xlsx'
                mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            
            buffer.seek(0)  # ✅ Ensure buffer is at the beginning
            file_data = buffer.getvalue()  # ✅ Convert buffer to bytes

            # ✅ Fixed Download Button
            st.download_button(
                label=f'Download {new_file_name}',
                data=file_data,  # ✅ Ensure correct data format
                file_name=new_file_name,
                mime=mime_type
            )

st.success('✅ All files processed successfully!')
