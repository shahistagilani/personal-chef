from uuid import uuid4
from langchain.messages import HumanMessage
from chef_agent.chef import build_agent
import streamlit as st
import logging

logger = logging.getLogger(__name__)

st.set_page_config(page_title="Personal Chef", page_icon="🍳")
st.title("Personal Chef")
st.caption("Tell me what ingredients you have, and I’ll help you find something to cook.")


@st.cache_resource
def get_agent():
    return build_agent()


if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid4())
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

if st.button("New conversation"):
    st.session_state.thread_id = str(uuid4())
    st.session_state.chat_messages = []
    st.rerun()

for message in st.session_state.chat_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What ingredients do you have?"):
    st.session_state.chat_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking of something delicious..."):
            try:
                response = get_agent().invoke(
                    {"messages": [HumanMessage(content=prompt)]},
                    config={"configurable": {"thread_id": st.session_state.thread_id}},
                )
                answer = response["messages"][-1].text
                st.markdown(answer)
                st.session_state.chat_messages.append(
                    {"role": "assistant", "content": answer}
                )
            except Exception as error:
                logger.exception("Agent request failed")
                st.error(f"I couldn't get a response. Check your API keys and try again.\n\n{error}")
