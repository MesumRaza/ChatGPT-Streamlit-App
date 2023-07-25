import openai
import json
import streamlit as st

# Set up OpenAI API credentials


def generate_prompt(company_description):
    prompt = ("Generate a SWOT analysis for a company based on the following description:\n\n" +

    f"{company_description} \n\n"

    """ Provide a Pretty JSON Format Output with No Additional Text other than JSON And output in the following format: 
        
    {"Strengths": Business Strengths in Comma Seperated Python List Format
    , "Weakness": Business Weakness in Comma Seperated Python List Format
    , "Opportunity": Business Opportunities  in Comma Seperated Python List Format
    , "Threat": Business Threats in Comma Seperated Python List Format}""")
    
    return prompt

def generate_response_openrouter(prompt):
    openai.api_base = "https://openrouter.ai/api/v1"
    openai.api_key = st.secrets['open_router_key']

    response = openai.ChatCompletion.create(
    model="google/palm-2-chat-bison", # Optional (user controls the default),
    messages=[{"role": "system", "content": "You are a Management Consultant",'role': 'user','content': prompt}],
    headers={ 'Authorization': 'Bearer {key}'.format(key=openai.api_key)
              ,"HTTP-Referer": 'https://mesumraza-chatgpt-strea-swot-generator-streamlit-chatgpt-jdwyhz.streamlit.app/' # To identify your app
              ,"X-Title": 'SWOT_Generator_StreamLit_ChatGPT' },
    )
    reply = response.choices[0].message.content.strip()
    
    return reply


def generate_response_chatgpt(prompt,openai_api_key):
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.5,
    )
    api_response = response.choices[0].text.strip()
    return api_response

# Define the layout of the Streamlit app
st.title("SWOT Analysis Generator")

model_choice = st.selectbox('Select your Model Mode',['Free','ChatGPT'])

if model_choice=='ChatGPT':
    openai_api_key = st.text_input("Enter your OpenAI API Key:", type="password")

company_description = st.text_area("Enter your Company's Detailed Outlook here:")

if st.button("Generate"):
    
    prompt = generate_prompt(company_description)
    
    
    with st.spinner(text="Loading Wisdom..."):
        if model_choice=='Free':
            api_response = json.loads(generate_response_openrouter(prompt))
        elif model_choice=='ChatGPT':
            api_response = json.loads(generate_response_chatgpt(prompt,openai_api_key))        
        
        
    st.divider()
    
    format_output_tab,prompt_input_tab,api_response_tab = st.tabs(["Formatted Output","Prompt Input","API Response"])

    with format_output_tab:
        for section, items in api_response.items():
            with st.expander(section):
                for points in items:
                    st.write(points)
    
    with prompt_input_tab:
        st.write(prompt)
        
    with api_response_tab:
        st.write(api_response)
