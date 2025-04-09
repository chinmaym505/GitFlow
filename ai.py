from langchain.llms import OpenAI

llm = OpenAI(model_name="gpt-neo")
response = llm.generate("What is the capital of France?")
print(response)