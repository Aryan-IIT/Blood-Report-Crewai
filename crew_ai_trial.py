from crewai import Agent, Task, Crew, Process
# from langchain.llms import Ollama 
import os
from dotenv import load_dotenv

load_dotenv()


# Set the API key (replace with a valid key)
open_api_key=os.environ["OPENAI_API_KEY"]
# #
# #Define the research agent
# research = Agent(
#     role='Researcher',
#     goal='Research new AI insights',
#     backstory='You work in AI research',
#     verbose=True,
#     allow_delegation=False,
#     llm=ollama_model
# )

# # Define the task with an expected output
# task1 = Task(
#     description='Investigate the latest AI trends',
#     agent=research,
#     expected_output='A report summarizing the latest trends in AI'
# )

# # Initialize the crew with the agent and task
# crew = Crew(
#     agents=[research],
#     tasks = [task1],
#     process=Process.sequential
# )

# # Kick off the process
# try:
#     result = crew.kickoff()
#     print(result)
# except Exception as e:
#     print(f"Error during execution: {e}")

# from crewai_tools import SerperDevTool

# tool = SerperDevTool(
#     search_url="https://google.serper.dev/scholar",
#     n_results=2,
# )

# print(tool.run(search_query="ChatGPT"))

# Using Tool: Search the internet

# Search results: Title: Role of chat gpt in public health
# Link: https://link.springer.com/article/10.1007/s10439-023-03172-7
# Snippet: … ChatGPT in public health. In this overview, we will examine the potential uses of ChatGPT in
# ---
# Title: Potential use of chat gpt in global warming
# Link: https://link.springer.com/article/10.1007/s10439-023-03171-8
# Snippet: … as ChatGPT, have the potential to play a critical role in advancing our understanding of climate
# ---

from crewai_tools import FileWriterTool

# Initialize the tool
file_writer_tool = FileWriterTool()

# Write content to a file in a specified directory
result = file_writer_tool._run('example.txt', 'This is a test content.', 'test_directory')
print(result)
