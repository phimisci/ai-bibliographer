from dotenv import load_dotenv
import os
import streamlit as st

import anthropic
from anthropic_query import return_claude_response

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
website_title = os.getenv("WEBSITE_TITLE")
llm = anthropic.Anthropic(api_key=api_key)
successful_response = False

if "input_disabled" not in st.session_state:
    st.session_state.input_disabled = False

def disable_user_interaction():
    st.session_state.input_disabled = True

def enable_user_interaction():
    st.session_state.input_disabled = False


claude_response_data = str()
st.set_page_config(
    page_title=website_title, 
    page_icon=":books:", 
    layout="wide", 
    initial_sidebar_state="auto", 
    menu_items=None
    )
st.title(website_title)

@st.cache_data
def list_claude_models():
    modellist = llm.models.list(limit=20)
    return {m["display_name"]: m["id"] for m in modellist.to_dict()["data"]}

available_models = {"Claude 3.7 Sonnet (latest)": "claude-3-7-sonnet-latest"}

st.sidebar.header("About PhiMiSci")
st.sidebar.info(
    """
    Philosophy and the Mind Sciences is an open-access journal at the 
    intersection of Philosophy and the empirical mind sciences.
    """
)

st.sidebar.header("How does this work?")
st.sidebar.info(
    "Your input data is sent to Anthropic's servers and processed in their LLMs."
)
st.sidebar.header("Use with care")
st.sidebar.warning(
    """
    Never input personal and/or sensitive information using this form.\n\n
    Always double check the results returned from a LLM."""
)

with st.form("claude-form", border=False):
    chosen_model = st.selectbox(
        "Select a model:",
        available_models.keys(),
        disabled=st.session_state.input_disabled
    )
    ai_input = st.text_area(
        "I'll accept your typed list of references below:", 
        height=450, 
        key="user_input",
        disabled=st.session_state.input_disabled
        )
    
    submit_button = st.form_submit_button(
        "Convert bibliography", 
        use_container_width = True, 
        type = "primary",
        disabled = st.session_state.input_disabled,
        on_click = disable_user_interaction)
    
    if submit_button:
        input_length = len(st.session_state.user_input.strip())

        if input_length > 75000:
            processing_complete = True
            st.error(
                f"""Your input is likely to be too large for LLM processing.
                    From your input I estimate that it needs to be processed in
                    {input_length//25000+1} batches. I suggest you chop your 
                    input, process the batches individually, and merge the 
                    output files.
                """)
        else: 

            if input_length > 10:
                with st.spinner(text="Processing your references using " + \
                                str(available_models[chosen_model]),
                                show_time=True):
                    claude_response = return_claude_response(
                        client=llm, 
                        model=available_models[chosen_model],
                        references=st.session_state.user_input
                    )
                    claude_response_data = claude_response.content[0].text

                    if claude_response.stop_reason != "end_turn":
                        st.error(f"""
                                 LLM terminated unsucessfully. The stopping
                                 reason was {claude_response.stop_reason}.
                                 """)

                    if claude_response_data[0] != "@":
                        st.error("""
                                Faulty LLM response: Your input does not seem to 
                                have been a list of references
                                """)
                        processing_complete = True
                    else:
                        successful_response = True
                        st.success("Operation successful")
                        processing_complete = True

                    with st.expander("Diagnostic LLM response"):
                        st.code(
                            claude_response_data, 
                            language=None, 
                            wrap_lines=True,
                            height=150
                        )
            else:
                processing_complete = True
                st.error("Your input does not seem to contain anything.")
        

if submit_button and successful_response:
        st.download_button(
            label="Download .bib",
            data=claude_response_data,
            file_name="data.bib",
            mime="text/plain",
            icon=":material/download:",
            use_container_width=True,
            type="primary",
            on_click="ignore"
        )
if submit_button and processing_complete:
    st.button("Start over", on_click = enable_user_interaction, use_container_width=True)