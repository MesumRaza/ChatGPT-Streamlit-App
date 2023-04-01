import openai
import streamlit as st
import json

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
       

def generate_response(prompt,openai_api_key):
    
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

openai_api_key = st.text_input("Enter your OpenAI API Key:", type="password")
openai.api_key = openai_api_key

company_description = st.text_area("Enter your Company's Detailed Outlook here:")

if st.button("Generate"):
    prompt = generate_prompt(company_description)
    api_response = json.loads(generate_response(prompt,openai_api_key))
       
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