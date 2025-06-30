import os 
import sys
from io import StringIO
from dotenv import load_dotenv
# Get me the LangChain function to create an agent, and the enum to specify what kind of agent I want.
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from backend.agent.tools import book_flight, book_hotel, block_calendar

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Define tools as LangChain Tool objects
tools = [
    Tool(
        name="book_flight",
        func=book_flight,
        description="Book a flight using input like 'DEL to JFK on 2025-07-20'."
    ),
    Tool(
        name="book_hotel",
        func=book_hotel,
        description="Find and book hotels with input like 'Paris on 2025-07-20 for 2 nights'."
    ),
    Tool(
        name="block_calendar",
        func=block_calendar,
        description="Block 9 AM on July 20 for meeting."
    )
]

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo") # temperature(randomness) - most deterministic (ideal for planning, factual queries).

agent = initialize_agent(
    tools=tools,
    llm=llm,
    # The agent chooses tools using the zero-shot ReAct pattern — based only on the tool descriptions, without training examples.
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    # You’ll see the agent's thought process
    verbose=True,
    handle_parsing_errors=True
    # max_iterations=1 
)

# Now returns trace and resutl so two str's
def run_agent_task(user_input: str) -> tuple[str, str]:
    """Run agent and return both reasoning trace and final answer."""
    buffer = StringIO()
    sys_stdout = sys.stdout
    sys.stdout = buffer
    
    try:
        result = agent.run(user_input)
    finally:
        sys.stdout = sys_stdout
    
    trace = buffer.getvalue()
    return trace, result