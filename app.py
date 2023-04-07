'''
===================================
  Module: Main Page UI (Streamlit)
  Author: Kenneth Leung
  Last Modified: 08 Apr 2023
===================================
'''
# from streamlit_extras.app_logo import add_logo
from src.utils import *
from src.langchain import *
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

import box
import streamlit as st
import yaml

# Import config vars
with open('config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))

st.set_page_config(page_icon='assets/favicon-32x32.png',
                   page_title='ChatPod - Q&A over your Podcasts',
                   initial_sidebar_state="auto")

# add_logo('assets/Banner_1.png', height=100)

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
st.image('assets/main_banner_with_text.png')

st.sidebar.title('Welcome to ChatPod')
st.sidebar.selectbox('Step 1: Select Podcast', ['Me, Myself, and AI'])
st.sidebar.image('assets/Banner_3.png')

with st.sidebar.expander("Step 2: Enter your OpenAI API Key"):
    st.session_state.OPENAI_API_KEY = st.text_input(label='*We do NOT store and cannot view your API key*',
                                                    placeholder='sk-p999HAfj6Cm1bO00SXgJc7kFxvFPtQ1KBBWrqSOU',
                                                    type="password",
                                                    help='You can find your Secret API key at \
                                                          https://platform.openai.com/account/api-keys')
st.sidebar.text(" ")
st.sidebar.text(" ")
st.sidebar.text(" ")
st.sidebar.caption('Brought to you by **[Kenneth Leung](https://github.com/kennethleungty)**')

query_tab, episodes_tab, podcast_tab = st.tabs(["Ask Podcast", "Select Episodes", "Podcast Info"])

# ===============================
#           Episodes Tab
# ===============================
with episodes_tab:
    if st.session_state.OPENAI_API_KEY in [None, '']:
        st.success('👈Please first enter your OpenAI API key in the left sidebar. Thank you!')
    if st.session_state.podcast == 'Me, Myself, and AI':
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
#       Podcast Info Tab
# ===============================
with podcast_tab:
    if st.session_state.podcast == 'Me, Myself, and AI':
        st.image('assets/Banner_3.png')
        st.text(" ")
        st.caption("""Why do only 10 percent of companies succeed with AI? In this series by MIT SMR and BCG, \
            we talk to the leaders who've achieved big wins with AI in their companies and learn how they did it.\
            Hear what gets experts from companies like Microsoft, Delta Air Lines, and others excited to do their \
            jobs every day and what they consider the keys to their success. **Hosted by Sam Ransbotham (Boston College) and Shervin Khodabandeh (BCG)**.
            """)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.caption('[Open Spotify](https://open.spotify.com/show/7ysPBcYtOPVgI6W5an6lup)')
        with col2:
            st.caption('[Open Apple Podcasts](https://podcasts.apple.com/us/podcast/me-myself-and-ai/id1533115958)')
        with col3:
            st.caption('[Open BCG page](https://www.bcg.com/capabilities/digital-technology-data/artificial-intelligence/mit-podcast-series)')

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
        st.success('👈Please first enter your OpenAI API key in the left sidebar. Thank you!')
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
            st.text(' ')
            with st.container():
                tab1, tab2 = st.tabs(["Snippet 1", "Snippet 2"])
                with tab1:
                    display_snippet(metadata[1])    

                with tab2:
                    display_snippet(metadata[0])    

# Edit Streamlit CSS (including hide footer and remove top padding)
edit_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .block-container {
                    padding-top: 2rem;
                    padding-bottom: 0rem;
                    padding-left: 0rem;
                    padding-right: 0rem;
                }
            </style>
            """
st.markdown(edit_streamlit_style, unsafe_allow_html=True)
