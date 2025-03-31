import time
import os
import json
import joblib
import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import pandas as pd
import io

load_dotenv()
GOOGLE_API_KEY=os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
URLS = [
    'https://coe.gatech.edu/academics/ai-for-engineering/ai-makerspace',
    'https://coe.gatech.edu/news/2024/04/georgia-tech-unveils-new-ai-makerspace-collaboration-nvidia',
    'https://www.atlantanewsfirst.com/2024/05/14/georgia-techs-ai-makerspace-preparing-students-new-world/',

]
new_chat_id = f'{time.time()}'
MODEL_ROLE = 'ai'
AI_AVATAR_ICON = '🤖'
@st.cache_data(show_spinner=False)
def fetch_context(urls):
    soup_text = ''
    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            text = soup.get_text(separator=' ', strip=True)
            soup_text += text + ' '
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching {url}: {e}")
    return soup_text

try:
    os.mkdir('data/')
except:

    pass

try:
    past_chats: dict = joblib.load('data/past_chats_list')
except:
    past_chats = {}

with st.spinner('Fetching and processing information...'):
    context = fetch_context(URLS)
    try:
        with open('pacekb.json', 'r') as f:
            pace_kb = json.load(f)
    except FileNotFoundError:
        st.error("PACE KB data file not found")
        pace_kb = {}

def readfile(filename):
    if filename is not None:
        filecontent = filename.read()
        filetype = filename.name.split('.')[-1]

        try:
            if filetype == 'json':
                return pd.read_json(io.StringIO(filecontent.decode('utf-8')))
            elif filetype == 'csv':
                return pd.read_csv(io.StringIO(filecontent.decode('utf-8')))
            elif filetype in ['xlsx', 'xls']:
                return pd.read_excel(io.BytesIO(filecontent))
            else:
                st.error(f"Unsupported file type: {filetype}. Please upload a JSON, CSV, or Excel file.")
                return None
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return None
    else:
        st.info("Please upload a file.")
        return None

file = None

with st.sidebar:
    st.title("File Upload")
    st.markdown("Upload a file to view its contents")
    filename = st.file_uploader("Choose a file")

    file = readfile(filename)

    st.write('# Past Chats')
    if st.session_state.get('chat_id') is None:
        st.session_state.chat_id = st.selectbox(
            label='Pick a past chat',
            options=[new_chat_id] + list(past_chats.keys()),
            format_func=lambda x: past_chats.get(x, 'New Chat'),
            placeholder='_',
        )
    else:
        st.session_state.chat_id = st.selectbox(
            label='Pick a past chat',
            options=[new_chat_id, st.session_state.chat_id] + list(past_chats.keys()),
            index=1,
            format_func=lambda x: past_chats.get(x, 'New Chat' if x != st.session_state.chat_id else st.session_state.chat_title),
            placeholder='_',
        )
    st.session_state.chat_title = f'ChatSession-{st.session_state.chat_id}'

st.write('# Ask Me Anything AI')

try:
    st.session_state.messages = joblib.load(
        f'data/{st.session_state.chat_id}-st_messages'
    )
    st.session_state.gemini_history = joblib.load(
        f'data/{st.session_state.chat_id}-gemini_messages'
    )
    print('old cache')
except:
    st.session_state.messages = []
    st.session_state.gemini_history = []
    print('new_cache made')

if file is not None:
  if file.to_string() == json.dumps(pace_kb):
      st.session_state.model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                                                     system_instruction=(
                                                             "You are a chatbot made to help students understand what the AIMakerSpace at Georgia Tech is and provide information about PACE resources. "
                                                             "You will receive context on all information currently present through HTML. Use that to answer student queries who are interested in the AIMakerSpace. "
                                                             f"Here is additional knowledge about PACE resources: {json.dumps(pace_kb)} " + context ))
  else:
      st.session_state.model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                                                     system_instruction=(
                                                             "You are a chatbot made to help students understand what the AIMakerSpace at Georgia Tech is. "
                                                             "You will receive context on all information currently present through HTML. Use that to answer student queries who are interested in the AIMakerSpace.\n" + file.to_string()))
else:
  st.session_state.model = genai.GenerativeModel(model_name="gemini-1.5-flash",
    system_instruction=(
        "You are a chatbot made to help students understand what the AIMakerSpace at Georgia Tech is and provide information about PACE resources. "
        "You will receive context on all information currently present through HTML. Use that to answer student queries who are interested in the AIMakerSpace. "
        f"Here is additional knowledge about PACE resources: {json.dumps(pace_kb)} " + context ))

st.session_state.chat = st.session_state.model.start_chat(
    history=st.session_state.gemini_history,
)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(
        name=message['role'],
        avatar=message.get('avatar'),
    ):
        st.markdown(message['content'])

if prompt := st.chat_input('Your message here...'):
    if st.session_state.chat_id not in past_chats.keys():
        past_chats[st.session_state.chat_id] = st.session_state.chat_title
        joblib.dump(past_chats, 'data/past_chats_list')
    with st.chat_message('user'):
        st.markdown(prompt)
    st.session_state.messages.append(
        dict(
            role='user',
            content=prompt,
        )
    )
    response = st.session_state.chat.send_message(
        prompt,
        stream=True,
    )
    with st.chat_message(
        name=MODEL_ROLE,
        avatar=AI_AVATAR_ICON,
    ):
        message_placeholder = st.empty()
        full_response = ''
        assistant_response = response
        for chunk in response:
            for ch in chunk.text.split(' '):
                full_response += ch + ' '
                time.sleep(0.05)
                message_placeholder.write(full_response + '▌')
        message_placeholder.write(full_response)

    st.session_state.messages.append(
        dict(
            role=MODEL_ROLE,
            content=st.session_state.chat.history[-1].parts[0].text,
            avatar=AI_AVATAR_ICON,
        )
    )
    st.session_state.gemini_history = st.session_state.chat.history
    joblib.dump(
        st.session_state.messages,
        f'data/{st.session_state.chat_id}-st_messages',
    )
    joblib.dump(
        st.session_state.gemini_history,
        f'data/{st.session_state.chat_id}-gemini_messages',
    )