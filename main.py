import os
from apiclient.discovery import build #youtube api
import http.client
from langchain import LLMMathChain, OpenAI
from langchain.agents import initialize_agent, load_tools
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain
import re

#sendgrid send email plan
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail)

#python web app deployed: https://biebergpt-outsidellms.streamlit.app/
import streamlit as st

#run locally 
from dotenv import dotenv_values
import json 

st.title('BieberGPT🤖🎶')
st.image('https://s.france24.com/media/display/ba80de5a-c06a-11eb-9594-005056bf87d6/w:1280/p:1x1/000_1OG6IB.jpg',width=100)
st.subheader('Enter details below to get an AI-recommended Bieber song and a song from a select Outside Lands performer🎤 according to your desired mood! You will also get emailed📧 a concert of an OSL performer from the JamBase API')
st.write('Miss out on Outside Lands tickets? Catch some Outside Lands performers at other concerts! Data received from the JamBase API, songs/performers recommended by gpt-3.5-turbo-0613, app input received via Streamlit')
st.image('https://storage.tally.so/d9947039-48cb-4392-8636-1cacdf028a21/Frame-2-4-.png',width=100 )
st.write("Made with ❤️ at Outside🎶 LLMs⛓️ 2023")
st.write("[Code on GitHub](https://github.com/elizabethsiegle/biebergpt-streamlit)")
config = dotenv_values(".env")
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"] #config.get('OPENAI_API_KEY')
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
#validate email
email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
def validate_email(email):
    # pass the regular expression and the string into the fullmatch() method
    if(re.fullmatch(email_regex, email)):
        return True
    else:
        return False
tools = load_tools(["llm-math"], llm=llm)
agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)
with st.form('my_form'):
    email = st.text_input('Email to send concert plan to')
    mood = st.selectbox(
        'What mood would you like to feel by listening to music?',
        ("upbeat", "pensive","sad")
    )
    location = st.selectbox('What location would you like to see concerts in?',
                            ("San Francisco", "Los Angeles"))
    submitted = st.form_submit_button('Submit')
    if submitted:
        if(validate_email(email)):
            songFromJBLLM = agent.run(f"What is a Justin Bieber song relating to {mood}")
            # songFromEmpire = list of artists ??
            # check out upcoming concerts from JamBase
            DEVELOPER_KEY = st.secrets["YOUTUBE_API_KEY"] # REPLACE IF RUNNING LOCALLY: config.get('YOUTUBE_API_KEY')
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
            prompt_template = PromptTemplate.from_template(
                  "Pick a song by Vnssa, Justin Jay, or Nala to listen to when I want to feel {mood}"
            )
            prompt = PromptTemplate(
                input_variables=["mood"],
                template="Pick a song by Vnssa, Justin Jay, or Nala to listen to when I want to feel {mood}",
            )
            chain = LLMChain(llm=llm, prompt=prompt)
            artistByMoodTxt = chain.run(mood)
            st.success(artistByMoodTxt)
            artistByMood = ''
            if "Justin Jay" in artistByMoodTxt:
                artistByMood = "justin+jay"
            elif "Vnssa" in artistByMoodTxt:
                artistByMood = "Vnssa"
            elif "Nala" in artistByMoodTxt:
                artistByMood = "Nala"
            print(f"artistByMood {artistByMood}")
            conn = http.client.HTTPSConnection("www.jambase.com") 
            jambaseapikey = st.secrets["JAMBASE_API_KEY"]
            conn.request("GET", f"/jb-api/v1/events?eventType=concerts&geoMetroId=jambase:4&artistName={artistByMood}&apikey={jambaseapikey}", headers=headers)
            jamurl = f"/jb-api/v1/events?eventType=concerts&artistName={artistByMood}&apikey={jambaseapikey}"
            res = conn.getresponse()
            data = res.read()
            json_data = json.loads(data)
            print(f"jamurl {jamurl}")
            first_event_name = json_data["events"][0]["name"]
            first_event_startdate = json_data["events"][0]["startDate"]
            first_event_startdate = first_event_startdate.split('T')[0]
            first_event_ticket_url = json_data["events"][0]["offers"][0]["url"]
            st.success(f"You should go to {artistByMood}'s concert on {first_event_startdate} at {first_event_ticket_url}")
            #email reminder for show
            #hardcoded bc Jambase API does not include SF concerts for Nala or Justin Jay when it should and whem 
            message = Mail(
                from_email='music_mood@osllms.com',
                to_emails=email,
                subject=f'Concert plan based on your mood',
                html_content=f'<strong>Have fun at the concert!</strong>!\n\n{artistByMood} on {first_event_startdate} at {first_event_ticket_url} or in SF on Friday, August 11: https://www.eventbrite.com/e/outside-lands-night-show-vnssa-nala-martyn-bootyspoon-tickets-660769749107')
            if artistByMood == "Nala":
                message = Mail(
                    from_email='music_mood@osllms.com',
                    to_emails=email,
                    subject=f'Concert plan based on your mood',
                    html_content=f'<strong>Have fun at the concert!</strong>!\n\n{artistByMood} on {first_event_startdate} at {first_event_ticket_url} or in SF on Friday, August 11: https://www.eventbrite.com/e/outside-lands-night-show-vnssa-nala-martyn-bootyspoon-tickets-660769749107')
            elif artistByMood == "justin+jay":
                message = Mail(
                    from_email='music_mood@osllms.com',
                    to_emails=email,
                    subject=f'Concert plan based on your mood',
                    html_content=f'<strong>Have fun at the concert!</strong>!\n\n{artistByMood} on {first_event_startdate} at {first_event_ticket_url} or in SF on Friday, August 11: https://www.ticketmaster.com/event/1C005ED0CEF55C87')
            else:
                Mail(
                    from_email='music_mood@osllms.com',
                    to_emails=email,
                    subject=f'Concert plan based on your mood',
                    html_content=f'<strong>Have fun at the concert!</strong>!\n\nFor some reason, an OSL performer was not found for you')
            os.environ["SENDGRID_API_KEY"] = st.secrets["SENDGRID_API_KEY"] #config.get('SENDGRID_API_KEY')
            sg = SendGridAPIClient()
            response = sg.send(message)
            print("Message Sent!")
        else:
            st.warning("Check email validity")
st.write("This uses the JamBase API to get concert data, LangChain PromptTemplates (and a chain and agent), Twilio SendGrid, YouTube API, and Streamlit in Python")

