from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
import os
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from prompt import *
from utils import *

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


# Function to generate Content using LLM
def generate_content(topic,description,keywords,length,language,career_focus,tone,job_function,industry,target_audience,cta):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-8b", temperature=1, api_key=GOOGLE_API_KEY)
    PROMPT_TEMPLATE = PROMPT # imported from prompt.py
    prompt = PromptTemplate(
        input_variables=["topic","description","keywords","length","language","career_focus","tone","job_function","industry","target_audience","cta"],
        template=PROMPT_TEMPLATE,
    )
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    response = llm_chain.run({
        "topic": topic,
        "description": description,
        "keywords": keywords,
        "length": length,
        "language": language,
        "career_focus": career_focus,
        "tone": tone,
        "job_function": job_function,
        "industry": industry,
        "target_audience": target_audience,
        "cta": cta,


    })
    return response

# Define the streamlit 

st.set_page_config(page_title="LinkedIn Content Generation", layout="wide")
st.header("LinkedIn Content Generation")

topic = st.text_input("Topic", placeholder="Specify the subject of the post")


with st.sidebar:
    st.title("Parameters")
    
    description = st.text_area("Description", placeholder="Provide a brief overview of the topic")
    keywords = st.text_input("Keywords", placeholder="Include up to 5 relevant keywords (comma-separated)")    
    length = st.selectbox("Length", ["Short (1-2 paragraphs)", "Medium (2-3 paragraphs)", "Long (3-5 paragraphs)"])
    
    language = st.selectbox("Language", ["English", "Other (please specify)"])
    if language == "Other (please specify)":
            other_language = st.text_input("Other Language", placeholder="Specify the language")
    else:
        other_language = ""

    career_focus = st.text_input("Career Focus", placeholder="Define the specific career or profession")
    tone = st.selectbox("Tone", ["Formal", "Informal", "Inspiring", "Humorous", "Conversational"])
    job_function = st.text_input("Job Function", placeholder="Specify a job title or functional area")
    industry = st.text_input("Industry", placeholder="Identify the industry or sector")
    target_audience = st.text_area("Target Audience", placeholder="Outline specific job roles, industries, or companies")
    
    cta = st.selectbox("Call-to-Action (CTA)", ["Engage", "Visit", "Sign Up", "Other (please specify)"])
    if cta == "Other (please specify)":
        other_cta = st.text_input("Other CTA", placeholder="Specify the CTA")
    else:
        other_cta = ""
    

# Generate the content 
if st.button("Generate Content"):
    response=generate_content(topic,description,keywords,length,language,career_focus,tone,job_function,industry,target_audience,cta)
    st.subheader("Generated Content :")
    st.write(response)

    # Download options
    st.download_button(
            label="Download as TXT",
            data=convert_to_txt(response),
            file_name="content.txt",
            mime="text/plain",
        )
    st.download_button(
            label="Download as DOCX",
            data=convert_to_docx(response),
            file_name="content.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
        