from orchestrator.executor import Executor

executor = Executor()

while True:
    text = input("You: ")
    print("Agent:", executor.handle(text))
