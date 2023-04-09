'''
===================================
  Module: Langchain Functions
  Author: Kenneth Leung
  Last Modified: 07 Apr 2023
===================================
'''
from langchain import LLMChain
from langchain.chains import SimpleSequentialChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
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


def define_main_prompt(context):
    system_template = f"""Use the following pieces of context to answer the question at the end. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    {context}

    Helpful answer:"""

    messages = [
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template('{question}')
    ]

    prompt = ChatPromptTemplate.from_messages(messages)

    return prompt


def define_review_prompt():
    template = """You are an AI reviewer of the following response of a large language model.

    {response}

    If the response above talks about it being unsure of the answer or has no information about the specific topic, 
    return the given response directly without changing any word, but append the string
    '||No Info||' at the end of the response.   

    Do not give any other response that is not in line with the above instructions.

    """
    prompt_template = PromptTemplate(input_variables=["response"], template=template)

    return prompt_template


def run_chain(query):
    llm = define_llm()
    docs = retrieve_vectors(query)
    context = compile_context(docs)
    metadata = get_metadata(docs)
    main_prompt = define_main_prompt(context)
    main_chain = LLMChain(prompt=main_prompt, 
                         llm=llm)
    review_prompt = define_review_prompt()
    review_chain = LLMChain(prompt=review_prompt,
                            llm=llm)
    
    overall_chain = SimpleSequentialChain(chains=[main_chain, review_chain], verbose=True)
    reviewed_response = overall_chain.run(query)

    if '||No Info||' in reviewed_response:
        reviewed_response = reviewed_response.replace('||No Info||', '')
        metadata = ["No Info", "No Info"]

    return reviewed_response, metadata
