# BieberGPT - AI Music Recommendation Chatbot
BieberGPT is an AI chatbot designed to recommend music by Justin Bieber and local artists based on the user's mood. It aims to solve the problem of finding music that puts you in the mood you desire. The chatbot utilizes various APIs and frameworks to provide personalized music recommendations and concert plans.

## Getting Started
You can access BieberGPT on Streamlit at this web address:
[https://biebergpt-outsidellms.streamlit.app/]
For the best user experience, open the web page, and click the three dots in the top right corner. Then click Settings. On the dropdown menu that says "Choose app theme, colors and fonts," select Dark. Follow the instructions provided on the web app to generate AI-generated song recommendations and concert plans. 

If you wish to run the project locally, follow the steps below:

1. Clone the GitHub repository for BieberGPT
2. Install the required dependencies: pip install apiclient streamlit dotenv python-http-client sendgrid
3. Set up the necessary environment variables by creating a .env file and add your API keys for OpenAI, YouTube, SendGrid and Jambase.
4. Run the streamlit app: streamlit run app.py

## How It Works
BieberGPT uses several APIs and libraries to provide music recommendations and concert plans:
# 1. **OpenAI GPT-3.5 Turbo**
BieberGPT leverages the power of the OpenAI GPT-3.5 Turbo language model to generate AI-generated Justin Bieber song recommendations based on the user's mood. The language model is integrated into the chatbot using the LangChain library
# 2. **YouTube API**
To provide song recommendations, BieberGPT uses the YouTube API to search for the top related videos for the recommended Justin Bieber song. Users can access the YouTube link to listen to the suggested song.
# 3. **Jambase API**
BieberGPT fetches concert data using the Jambase API. The chatbot recommends concerts of local artists based on the user's mood and location preference (San Francisco or Los Angeles). The concerts are suggested for artists Vnssa, Justin Jay, or Nala.
# 4. **SendGrid API**
BieberGPT utilizes the SendGrid API to send concert plans to the user's email. After selecting a concert, the chatbot sends a reminder email with the details of the recommended concert.

## Contributions
We welcome contributions to BieberGPT! If you have any ideas, bug fixes, or enhancements, feel free to open an issue or submit a pull request on GitHub.

## Credits
BieberGPT is an AI hack for Outside LLMs 2023. Special thanks to developers Boyd Lever and Elizabeth Siegle, and to LangChain, Streamlit, YouTube, Jambase, and SendGrid for their APIs.

Enjoy the music with BieberGPT! 🎶🎤
