import os
import streamlit as st
from itertools import compress
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

if 'OPENAI_API_KEY' not in st.session_state:
    st.session_state.OPENAI_API_KEY = ''

def get_episode_list():
    episode_list = os.listdir('vectorstore')
    episode_list = [x for x in episode_list if x != 'all_podcasts']

    return episode_list


def update_vectorstore(checkboxes):
    full_episode_list = get_episode_list()
    # Get selected checkboxes in a list (based on boolean filter)
    st.session_state.episode_list = list(compress(full_episode_list, checkboxes))
    embeddings = OpenAIEmbeddings(openai_api_key=st.session_state.OPENAI_API_KEY)

    for i, episode in enumerate(st.session_state.episode_list):
            if i == 0:
                db1 = FAISS.load_local(f"vectorstore/{episode}", embeddings)
            else:
                db2 = FAISS.load_local(f"vectorstore/{episode}", embeddings)
                db1.merge_from(db2)
                
    st.session_state.vectorstore = db1

    print(len(db1.docstore._dict))


