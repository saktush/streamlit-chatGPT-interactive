import openai
import streamlit as st
from decouple import config


def make_request(question_input: str):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"{question_input}"},
        ]
    )
    return response


def main():
    # set basics
    response = False
    prompt_tokens = 0
    completion_tokes = 0
    total_tokens_used = 0
    cost_of_response = 0
    st.session_state.triggered_enter = False
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

    # set header
    st.header("OpenAI ChatGPT API interface")

    # Display response in scrollable area

    # st.markdown("""---""")
    with st.form(key='request_form'):
        response_area = st.empty()
        question_input = st.text_area("Enter question and push Submit", height=150)
        submit_button = st.form_submit_button(label='Submit',
                                              help="Press CMD/Ctrl + Enter to send a request",
                                              )
        if submit_button or st.session_state.triggered_enter:
            response = make_request(question_input)
        else:
            pass

        # show response
        if response:
            response_text = response["choices"][0]["message"]["content"]
            response_area.text_area(label="Response", value=response_text, height=150)
            st.markdown("""---""")

            prompt_tokens = response["usage"]["prompt_tokens"]
            completion_tokes = response["usage"]["completion_tokens"]
            total_tokens_used = response["usage"]["total_tokens"]
            cost_of_response = total_tokens_used * 0.000002

    with st.sidebar:
        st.title("Usage Stats:")
        st.markdown("""---""")
        st.write("Promt tokens used :", prompt_tokens)
        st.write("Completion tokens used :", completion_tokes)
        st.write("Total tokens used :", total_tokens_used)
        st.write("Total cost of request: ${:.8f}".format(cost_of_response))


if __name__ == '__main__':
    API_KEY = config('OPENAI_API_KEY')
    openai.api_key = API_KEY
    # TODO: think about running code with shell file
    main()
    pass
