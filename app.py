'''
===================================
  Module: Landing Page
  Author: Kenneth Leung
  Last Modified: 15 Mar 2023
===================================
'''
from streamlit_extras.app_logo import add_logo
from src.utils import *
from src.langchain import *
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

import box
import os
import streamlit as st
import time
import yaml
import base64

# Import config vars
with open('config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))

st.set_page_config(page_icon='assets/favicon-32x32.png',
                   page_title='PodChat',
                   initial_sidebar_state="auto")

add_logo('assets/Banner_1.png', height=100)

# Import CSS styles
with open('assets/styles.css', encoding='utf8') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

if 'OPENAI_API_KEY' not in st.session_state:
    st.session_state.OPENAI_API_KEY = ''

if 'podcast' not in st.session_state:
    st.session_state.podcast = 'Me, Myself, and AI'

if 'episode_list' not in st.session_state:
    st.session_state.episode_list = ''

# ===============================
#            Layout
# ===============================
st.sidebar.title('Welcome to PodChat')
# st.image('assets/7435432.jpg')
st.image('assets/main_banner_with_text.png')
st.text(' ')

st.sidebar.selectbox('Step 1: Select Podcast', ['Me, Myself, and AI'])
st.sidebar.image('assets/Banner_3.png')


with st.sidebar.expander("Step 2: Type your OpenAI API Key and press Enter"):
    st.session_state.OPENAI_API_KEY = st.text_input(label='*Note: We do NOT store your OpenAPI key*',
                                                    placeholder='sk-p999HAfj6Cm1bO00SXgJc7kFxvFPtQ1KBBWrqSOU',
                                                    type="password",
                                                    help='You can find your Secret API key at \
                                                          https://platform.openai.com/account/api-keys')
st.sidebar.text(" ")
st.sidebar.text(" ")
st.sidebar.text(" ")
st.sidebar.text(" ")
st.sidebar.caption('Developed by [Kenneth Leung](https://github.com/kennethleungty)')

query_tab, episodes_tab = st.tabs(["Ask Podcast", "Select Episodes"])


# ===============================
#           Episodes Tab
# ===============================
with episodes_tab:
    st.caption("Select episodes to include for querying and then press the \
                `Update Episode Selection` button at the bottom of page")
    st.text(" ")
    full_episode_list = get_episode_list()
    checkboxes = [st.checkbox(episode, value=True) \
                  for episode in full_episode_list]

    st.text(" ")
    if st.button('➡️ Update Episode Selection', on_click=update_vectorstore, kwargs={'checkboxes':checkboxes}):
        st.success(f'Updated! New vectorstore size = {len(st.session_state.vectorstore.docstore._dict)}')
    

# ===============================
#           Query Tab
# ===============================
with query_tab:
    chat_placeholder = st.empty()
    with chat_placeholder:
        user_query = st.text_input('Label',
                                '',
                                placeholder=cfg.PLACEHOLDER_TEXT,
                                label_visibility='collapsed')
        
    if st.session_state.OPENAI_API_KEY in [None, '']:
        st.success('👈❗Please first enter your OpenAI API key in the left sidebar. Thank you!')
    else:
        embeddings = OpenAIEmbeddings(openai_api_key=st.session_state.OPENAI_API_KEY)

        # Load vectorstore containing all episodes first
        if 'vectorstore' not in st.session_state:
            st.session_state.vectorstore = FAISS.load_local(f'{cfg.VECTORSTORE_PATH}/all_podcasts', embeddings)


        # =============================================
        #                 Query Section
        # =============================================
        if user_query not in [cfg.PLACEHOLDER_TEXT, '']:
            # Pass the query to ChatGPT
            response, metadata = run_chain(user_query)

            st.write(response)


        # with st.container():
        #     tab1, tab2 = st.tabs(["Response", "Sources"])
        #     with tab1:
        #         st.write(f"{response['answer']}")
        #     with tab2:
        #         # st.subheader('Source Documents')
        #         for i, doc in enumerate(response['source_documents']):
        #             st.caption(f'Relevant Text Chunk {i+1}:')
        #             # PDF has different metadata structure
        #             if db_factsheets:
        #                 st.caption(f'Retrieved from: `{doc.metadata["file_path"]}`')
        #                 st.caption(f'Page number {doc.metadata["page_number"]}')
        #             else:
        #                 st.caption(f'Retrieved from: `{doc.metadata["source"]}`')
        #             st.write(doc.page_content)
        #             st.markdown("""---""")
        #     st.text(" ")

