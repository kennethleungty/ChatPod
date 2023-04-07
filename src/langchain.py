from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate)
import streamlit as st


def define_llm():
    llm = ChatOpenAI(
                model_name='gpt-3.5-turbo',
                temperature=0,
                openai_api_key=st.session_state.OPENAI_API_KEY
               )
    return llm


def retrieve_vectors(query):
    docsearch = st.session_state.vectorstore
    docs = docsearch.similarity_search_with_score(query, k=2)
    return docs


def compile_context(docs):
    texts = [doc[0].page_content for doc in docs]
    context = " ".join(texts)

    return context


def get_metadata(docs):
    metadata_list = []
    for doc in docs:
        text = doc[0].page_content
        score = doc[1]
        start_time = round(doc[0].metadata['start'])
        url_raw = doc[0].metadata['url']
        url_embed = url_raw.replace('.com/episode/', '.com/embed/episode/') + \
                    f'?utm_source=generator&t={start_time}'

        metadata_i = {'text': text,
                      'score': score,
                      'url_embed': url_embed}
        
        metadata_list.append(metadata_i)

    return metadata_list


def define_prompt(context):
    system_template = f"""Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

    {context}

    Helpful answer:"""

    messages = [
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template('{question}')
    ]

    prompt = ChatPromptTemplate.from_messages(messages)

    return prompt


def run_chain(query):
    llm = define_llm()
    docs = retrieve_vectors(query)
    context = compile_context(docs)
    metadata = get_metadata(docs)
    prompt = define_prompt(context)
    llm_chain = LLMChain(prompt=prompt, 
                         llm=llm, 
                         verbose=False)
    
    response = llm_chain.predict(question=query)
    
    return response, metadata
