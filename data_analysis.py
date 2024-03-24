import openai
import streamlit as st
from langchain_openai import OpenAI
from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def perform_data_analysis(dataframes, uploaded_file_names):
    
    llm = OpenAI(temperature=0)

    if dataframes:
        uploaded_file_names_options = [""] + uploaded_file_names
        selected_file_name = st.selectbox("Select file for chatting:", options=uploaded_file_names_options)

        if selected_file_name:
            idx = uploaded_file_names.index(selected_file_name)
            pandas_agent = create_pandas_dataframe_agent(llm, dataframes[idx], verbose=True,
                                                          agent_executor_kwargs={"handle_parsing_errors": True})

            st.header('Exploratory data analysis')
            st.subheader('General information about the dataset')

            function_agent(pandas_agent, dataframes[idx])

def function_agent(pandas_agent, df):
    st.write("**Data Overview**")

    # Perform all necessary API calls in one go
    responses = pandas_agent.run([
        "List the columns present, column names along with the data type",
        "How many rows and columns in dataframe",
        "What is the meaning of every column in dataframe and the data in dataframe is about?",
        "How many missing values does this dataframe have? Start the answer with 'There are'",
        "Calculate the correlations between numerical variables to identify potential relationships.",
        "Are there any duplicate values and if so how many?",
        "What new features would be interesting to create?"
    ])

    # Display the responses
    st.write("1. " + responses[0])
    st.write("2. " + responses[1])
    st.write("3. " + responses[2])
    st.write("4. " + responses[3])
    st.write("5. " + responses[4])
    st.write("6. " + responses[5])
    st.write("7. " + responses[6])

    return
