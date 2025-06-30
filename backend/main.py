from backend.agent.planner import run_agent_task

if __name__ == "__main__":
    prompt = "Book a flight from LA to NYC on July 20 and block my calendar at 9 AM for 'Trip to NYC'"
    response = run_agent_task(prompt)
    print("\n--- Final Agent Output ---")
    print(response)
