import openai
import streamlit as st
from decouple import config


# define function to make request to OpenAI API
def make_request(prompt: str) -> str:
    """
    This function makes a request to OpenAI ChatCompletion API and returns the response received

    Parameters:
    question_input (str) : The question input by user

    Returns: response str
    response : Response received from OpenAI ChatCompletion API
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"{prompt}"},
        ]
    )
    return response


# main function to display the form and handle the response
def main():
    # set initial values for variables
    response = False
    prompt_tokens = 0
    completion_tokes = 0
    total_tokens_used = 0
    cost_of_response = 0
    st.session_state.triggered_enter = False
    # set page configuration for Streamlit
    st.set_page_config(
        page_title="GPT 3.5 Local",
        page_icon="🧊",
        layout="centered",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://www.extremelycoolapp.com/help',
            'Report a bug': "https://www.extremelycoolapp.com/bug",
            'About': "# This is a header. This is an *extremely* cool app!"
        }
    )

    # set header for the page
    st.header("OpenAI ChatGPT API interface")

    # create form to take input from user
    with st.form(key='request_form'):
        response_area = st.empty()  # used to show response from OpenAI API
        question_input = st.text_area("Enter question and push Submit", height=150)
        submit_button = st.form_submit_button(label='Submit', help="Push the button!")
        if submit_button or st.session_state.triggered_enter:
            response = make_request(question_input)
        else:
            pass

        # display response from OpenAI API
        if response:
            response_text = response["choices"][0]["message"]["content"]
            response_area.text_area(label="Response", value=response_text, height=150)
            st.markdown("""---""")

            prompt_tokens = response["usage"]["prompt_tokens"]
            completion_tokes = response["usage"]["completion_tokens"]
            total_tokens_used = response["usage"]["total_tokens"]
            cost_of_response = total_tokens_used * 0.000002
        else:
            response_area.text_area(label="Response", value="...", height=150, disabled=True)

    # create sidebar to show usage statistics
    with st.sidebar:
        st.title("Usage Stats:")
        st.markdown("""---""")
        st.write("Promt tokens used :", prompt_tokens)
        st.write("Completion tokens used :", completion_tokes)
        st.write("Total tokens used :", total_tokens_used)
        st.write("Total cost of request: ${:.8f}".format(cost_of_response))


# run the main function
if __name__ == '__main__':
    # set OpenAI API key
    API_KEY = config('OPENAI_API_KEY')
    openai.api_key = API_KEY
    main()
