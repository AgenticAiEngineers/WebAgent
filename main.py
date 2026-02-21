from agent.agent_core import SimpleAgent

agent = SimpleAgent()

print("\n Smart Agent Ready (type 'exit' to quit)\n")

while True:
    user = input("You: ")

    if user.lower() == "exit":
        break

    response = agent.run(user)
    print("\nAgent:", response)
    print("\n" + "="*50 + "\n")
