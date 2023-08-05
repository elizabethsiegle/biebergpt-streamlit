import os
# from langchain.chat_models import ChatOpenAI
from googleapiclient.discovery import build
import http.client
from langchain import LLMMathChain, OpenAI, SerpAPIWrapper
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
import re
import requests

import streamlit as st

from dotenv import dotenv_values

st.title('Bieberbot')
st.subheader('enter details below')

config = dotenv_values(".env")
os.environ["OPENAI_API_KEY"] = config.get('OPENAI_API_KEY')
os.environ["SERPAPI_API_KEY"] = config.get('SERPAPI_API_KEY')
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
search = SerpAPIWrapper()
llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
tools = [
    Tool(
        name = "Search",
        func=search.run,
        description="useful for when you need to answer questions about current events. You should ask targeted questions"
    ),
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="useful for when you need to answer questions about math"
    )
]
#validate email
email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
def validate_email(email):
    # pass the regular expression and the string into the fullmatch() method
    if(re.fullmatch(email_regex, email)):
        return True
    else:
        return False
    
agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)
with st.form('my_form'):
    email = st.text_input('Email to send plan to')
    mood = st.selectbox(
        'What mood would you like to feel by listening to music?',
        ("upbeat", "somber", "pensive", "optimistic", "sad")
    )
    # mood = st.text_input('What kind of mood would you like to be in?')
    location = st.selectbox(
    'In what city would you like to attend a concert?',
    ('San Francisco', 'Los Angeles'))
    submitted = st.form_submit_button('Submit')
    if submitted:
        if(validate_email(email)):
            songFromJBLLM = agent.run(f"What is a Justin Bieber song relating to {mood}")
            # songFromEmpire = list of artists
            # check out upcoming concerts from Jambase
            DEVELOPER_KEY = "AIzaSyBIA3XG7cpwCIm4P6LyZYGRUaocvB6k9P0" 
            YOUTUBE_API_SERVICE_NAME = "youtube"
            YOUTUBE_API_VERSION = "v3"
            youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, 
                                       developerKey = DEVELOPER_KEY)
            search_keyword = youtube.search().list(q=songFromJBLLM, part="id,snippet", maxResults = 6).execute()
            URLS = f"https://www.youtube.com/watch?v={search_keyword['items'][0]['id']['videoId']}"
            st.success(f"{songFromJBLLM} and it's here on YouTube {URLS}")

            #Jambase concert location
            headers = { 'Accept': "application/json" }
            metroIDDict = { "San Francisco": "jambase:4",
                           "Los Angeles": "jambase:3"
            }
            genreDict = { "bluegrass": "upbeat",
                         "blues": "upbeat",
                         "classical": "pensive",
                         "jazz": "optimistic",
            }
            
            geoMetroID = metroIDDict[location]
            conn = http.client.HTTPSConnection("www.jambase.com")
            conn.request("GET", f"/jb-api/v1/events?artistName=Vnssa&geoMetroId={geoMetroID}&apikey=fc96baa4-a173-419e-aece-55224a9205dc", headers=headers)
            res = conn.getresponse()
            data = res.read()
            print(data.decode("utf-8"))
            st.success(f"You should go to this concert in {location}: ")
            #email reminder for show
        else:
            st.warning("Check email validity")

