import streamlit as st
import openai

API_KEY = "{text=''}"

with open("API_KEY.txt", "r") as key:
    _key = key.read()[0]
    API_KEY.format(_key)


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

    # set header
    st.header("Streamlit + OpenAI ChatGPT API")
    st.markdown("""---""")

    with st.form(key='my_form'):
        question_input = st.text_area("Enter question and push Enter to send", height=200)
        submit_button = st.form_submit_button(label='Submit',
                                              help="Press CMD/Ctrl + Enter to send the message")
        if submit_button or st.session_state.triggered_enter:
            response = make_request(question_input)
        else:
            pass

    st.markdown("""---""")

    if response:
        st.write("Response:")
        st.write(response["choices"][0]["message"]["content"])

        prompt_tokens = response["usage"]["prompt_tokens"]
        completion_tokes = response["usage"]["completion_tokens"]
        total_tokens_used = response["usage"]["total_tokens"]

        cost_of_response = total_tokens_used * 0.000002
    else:
        pass

    with st.sidebar:
        st.title("Usage Stats:")
        st.markdown("""---""")
        st.write("Promt tokens used :", prompt_tokens)
        st.write("Completion tokens used :", completion_tokes)
        st.write("Total tokens used :", total_tokens_used)
        st.write("Total cost of request: ${:.8f}".format(cost_of_response))


if __name__ == '__main__':
    main()
    # print("To run this script type:\nstreamlit run src/main.py")
    pass
