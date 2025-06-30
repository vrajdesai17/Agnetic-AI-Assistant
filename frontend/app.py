import sys
import os
import streamlit as st
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.agent.planner import run_agent_task
import re

st.markdown("""
<style>
    .element-container { padding: 0rem 0rem 0.5rem 0rem; }
    code { font-size: 0.9rem !important; }
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Agentic AI Assistant", page_icon="🤖")

st.title("🧠 Agentic AI Workflow Assistant")
st.markdown("Ask me to plan tasks like booking flights, hotels, or blocking your calendar.")

st.info("""
✈️ **Flight Booking Instructions**
To book a flight, type in the following format:  
`<ORIGIN> to <DESTINATION> on <YYYY-MM-DD>`  
Example: `MAD to LON on 2025-07-20`

---

📅 **Google Calendar Blocking**  
To block a calendar time, say something like:  
`Block my calendar at 3 PM tomorrow` or `Add event at 9 AM on Friday`

---

🏨 **Hotel Booking**  
Say: `Book a hotel in Paris on 2025-07-20 for 2 nights`
""")


def render_trace(trace_text):
    # 🧼 Step 1: Remove ANSI escape codes like [32;1m
    trace_text = re.sub(r"\[\d+(?:;\d+)*m", "", trace_text)

    # 🧩 Step 2: Split and render each block
    blocks = re.split(r"(?=Thought:|Action:|Action Input:|Observation:|Final Answer:)", trace_text)
    for block in blocks:
        block = block.strip()
        if block.startswith("Thought:"):
            st.markdown(f"🧠 **{block}**")
        elif block.startswith("Action:"):
            st.markdown(f"🛠️ **{block}**")
        elif block.startswith("Action Input:"):
            st.markdown(f"📥 **{block}**")
        elif block.startswith("Observation:"):
            st.markdown(f"👀 **{block}**")
        elif block.startswith("Final Answer:"):
            st.markdown(f"✅ **{block}**")
        elif block.startswith("> Entering") or block.startswith("> Finished"):
            with st.expander("🔁 System Info"):
                st.code(block)
        elif block:
            st.markdown(f"📝 {block}")


# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    
# Show past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
prompt = st.chat_input("What can I help you with today?")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        with st.spinner("Thinking..."):
            try:
                trace, response = run_agent_task(prompt)
                with st.expander("🧠 Agent Reasoning Trace", expanded=False):
                    render_trace(trace)
                st.markdown(response)
            except Exception as e:
                st.error(f"❌ Error: {e}")
                response = "There was an error processing your request."
                
    st.session_state.messages.append({"role": "assistant", "content": response})
