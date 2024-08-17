import streamlit as st
from openai import OpenAI

st.markdown("""
    <style>
    .main {
        background-color: #ff5400;
        color: #ffffff;
        text-align: center;
        padding: 0rem 0rem 0rem;
        margin-top: 5px;
    }
    .main h1 {
        font-size: 4em;
        padding: 0rem 0px 0rem;
    }
    .main h2 {
        font-size: 3.75em;
        color: #002430; 
        padding: 0rem 0px 0rem;
        margin-bottom: 15px;
    }
    .main p {
        font-size: 1em;
    }
    .main .button {
        background-color: #002430;
        border: none;
        color: white;
        padding: 10px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 1em;
        margin-top: 20px;
        cursor: pointer;
        border-radius: 50px;
    }
    .st-emotion-cache-13ln4jf {
    width: 100%;
    padding: 3rem 1rem 10rem;
    max-width: 46rem;
}
    
    </style>
    """, unsafe_allow_html=True)

# HTML content
st.markdown("""
    <div class="main">
        <h1>KNOW YOURSELF</h1>
        <h2>personify yourself</h2>
        <p>A place to know who you are, what you can become and what you can achieve.</p>
       
    </div>

# Show title and description.
st.title("Jarvis - OO1")
st.write(
    "Hi I am Jarvis, your AI assistant. You can ask me anything.Just Enter your OpenAI API key (my open sesame) to initiate a converstion with me!"
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("How can I help you today?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
