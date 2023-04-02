'''
===================================
  Module: Frontend (Streamlit)
  Author: Kenneth Leung
  Last Modified: 15 Mar 2023
===================================
'''
from datetime import datetime as dt
from streamlit_extras.app_logo import add_logo

import box
import streamlit as st
import time
import yaml
import base64

st.set_page_config(page_icon='assets/favicon-32x32.png',
                   page_title='Chat Podcast',
                   initial_sidebar_state="auto")

add_logo('assets/Banner_1.png', height=100)

# Import config vars
# with open('config.yml', 'r', encoding='utf8') as ymlfile:
#     cfg = box.Box(yaml.safe_load(ymlfile))

# Import CSS styles
with open('assets/styles.css', encoding='utf8') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# if 'example_query' not in st.session_state:
#     st.session_state.example_query = ''

# ===============================
#            Layout
# ===============================
st.sidebar.subheader("Your clients today (3)")

selected_date = st.sidebar.date_input(
                "Selected date",
                value=dt.today(),
                label_visibility='visible')
st.text(" ")

st.image('assets/Banner_3.png')

chat_placeholder = st.empty()

with chat_placeholder:
    user_query = st.text_input('Label',
                               'testing 223',
                               placeholder='Placeholder',
                               label_visibility='collapsed')

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        db_transcripts = st.checkbox(label='Call Transcripts', value=True)
    with col2:
        db_recsys = st.checkbox(label='Personalized Recommendations', value=False)

# =============================================
#                 Query Section
# =============================================
# if user_query != cfg.PLACEHOLDER_TEXT and user_query != '':
#     # Pass the query to ChatGPT
#     if st.session_state.client_name == '':
#         st.error('Please first select a client in the left sidebar',
#                  icon='🚨')

#         with st.container():
#             tab1, tab2 = st.tabs(["Response", "Sources"])
#             with tab1:
#                 st.write(f"{response['answer']}")
#             with tab2:
#                 # st.subheader('Source Documents')
#                 for i, doc in enumerate(response['source_documents']):
#                     st.caption(f'Relevant Text Chunk {i+1}:')
#                     # PDF has different metadata structure
#                     if db_factsheets:
#                         st.caption(f'Retrieved from: `{doc.metadata["file_path"]}`')
#                         st.caption(f'Page number {doc.metadata["page_number"]}')
#                     else:
#                         st.caption(f'Retrieved from: `{doc.metadata["source"]}`')
#                     st.write(doc.page_content)
#                     st.markdown("""---""")
#             st.text(" ")

st.text(" ")
st.caption('Footer')