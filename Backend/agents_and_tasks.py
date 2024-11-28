'''
- AGENT 1 - take pdf and perform RAG on it for certain keywords -> Crewai pdf rag search
- AGENT 2 - use those keywords and provide summary with it -> Normal agent, File write (save in txt)
- AGENT 3 - help generate a prompt for google search engine -> Normal agent
- Task - take those keywords and perform google searches of relevant articles, based on agent 3's output. -> Crewai Google serper search, Selenium scraper
- Task - write the googled contents in a txt -> crewai File write
'''

from crewai import Agent, Crew, Process, Task
from crewai_tools import PDFSearchTool, FileWriterTool, SerperDevTool
from mailing import clean_markdown
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.environ["OPENAI_API_KEY"]


def save_outputs_to_files(report: str, email: str, output_folder: str = "Output"):
    """
    Saves the agent's report and email content into two Markdown files in the specified output folder.

    Args:
        report (str): The content of the agent's report.
        email (str): The content of the email.
        output_folder (str): The folder where the text files will be saved. Defaults to 'Output'.

    Returns:
        dict: A dictionary containing the status and relative paths of the written files.
    """
    from pathlib import Path
    from crewai_tools import FileWriterTool

    # Initialize the FileWriterTool
    file_writer_tool = FileWriterTool()

    # Ensure the output folder exists
    output_path = Path(output_folder).resolve()
    output_path.mkdir(parents=True, exist_ok=True)

    # Define filenames
    report_filename = "agent_report.md"
    email_filename = "email_content.md"

    # Create file paths
    report_path = output_path / report_filename
    email_path = output_path / email_filename

    # Write files using the FileWriterTool
    try:
        report_status = file_writer_tool._run(
            filename=report_filename,
            content=report,
            directory=str(output_path),
            overwrite=True  # Explicitly set overwrite to True
        )
    except Exception as e:
        report_status = f"An error occurred while accessing report file: {e}"

    try:
        email_status = file_writer_tool._run(
            filename=email_filename,
            content=email,
            directory=str(output_path),
            overwrite=True  # Explicitly set overwrite to True
        )
    except Exception as e:
        email_status = f"An error occurred while accessing email file: {e}"

    # Calculate relative paths if possible
    try:
        report_relative_path = str(report_path.relative_to(Path.cwd()))
    except ValueError:
        report_relative_path = str(report_path)

    try:
        email_relative_path = str(email_path.relative_to(Path.cwd()))
    except ValueError:
        email_relative_path = str(email_path)

    return {
        "report_status": report_status,
        "email_status": email_status,
        "report_path": report_relative_path,  # Relative or absolute path
        "email_path": email_relative_path,  # Relative or absolute path
    }


def pdf_rag(path: str):
    pdf_search_tool = PDFSearchTool(
        pdf=path,
    )

    # --- Agents ---
    # Research Agent
    research_agent = Agent(
        role="Healthcare practitioner, blood report analyst",
        goal="Search through the Blood Report PDF to interpret and provide diagnosis",
        allow_delegation=False,
        verbose=False,
        backstory=(
            """
            The research agent is a medical practitioner who is fluent in reading through a blood report.
            The agent's job is to:
            1. Diagnose and communicate potential health risks in an understandable way.
            2. Diagnose and communicate other statistics. 
            3. Provide a summary of the patient's metadata (Name, Date, Address, and more).
            """
        ),
        tools=[pdf_search_tool],
    )

    # Professional Writer Agent
    professional_writer_agent = Agent(
        role="Professional healthcare content writer",
        goal="Draft a well-structured and personalized email to the patient based on the research agent's findings.",
        allow_delegation=False,
        verbose=False,
        backstory=(
            """
            The professional writer agent is skilled in composing formal and empathetic health-related correspondence.
            The agent's job is to:
            1. Summarize the research findings into a personalized email.
            2. Use simple, non-technical language to explain medical terms.
            3. Encourage follow-up consultations if necessary.
            """
        ),
        tools=[],
    )

    # --- Tasks ---
    # Task 1: Detailed Blood Test Report Analysis
    detailed_report_blood_test = Task(
        description=(
            """
            Analyze the blood test PDF for the following:
            1. Summarize key patient metadata, such as Name, Age, Gender, and Test Date.
            2. Identify any abnormal values or health risks based on the reference intervals provided in the report.
            3. Summarize overall health indicators, including liver, kidney, thyroid, and glucose levels.
            """
        ),
        expected_output="Generated detailed blood test analysis report.",
        tools=[pdf_search_tool],
        agent=research_agent,
    )

    # Task 2: Write Email
    write_email_task = Task(
        description=(
            """
            Compose a personalized email to the patient based on the findings from the detailed blood test analysis.
            The email should:
            1. Thank the patient for their trust in the lab.
            2. Summarize the findings clearly and concisely.
            3. Include actionable recommendations, such as consulting a healthcare provider.
            4. Offer support and contact information for any queries. Contact Number: 022-25232834
            5. Use this, [Your Name] = Dr. Sam (Head of Hematology)  
            6. DO NOT Have a subject. 
            """
        ),
        expected_output="Generated personalized email for the patient.",
        tools=[],
        agent=professional_writer_agent,
    )

    task_result_report = research_agent.execute_task(detailed_report_blood_test) #detailed report content
    # print("\n\n the task result is:\n")
    # print(task_result)

    # --- Crew ---
    crew = Crew(
        agents=[research_agent, professional_writer_agent],
        tasks=[detailed_report_blood_test, write_email_task],
        process=Process.sequential,
    )

    # Execute the tasks
    crew_output = crew.kickoff()

    #email content
    # print(f"Raw Output: {crew_output.raw}")  
    
    # Extract the generated report and email content
    agent_report = task_result_report  # Output of the first task (detailed report)
    email_content = crew_output.raw  # Output of the second task (email)

    # # Save outputs to text files
    # returned_dict = save_outputs_to_files(agent_report, email_content)
    # print(f"Report status: {returned_dict['report_status']}")
    # print(f"Email status: {returned_dict['email_status']}")

    return agent_report, email_content

def web_articles_extract(agent_report):
    """
    Extracts relevant web articles based on the summarized blood report (agent_report).

    Args:
        agent_report (str): The summarized blood report generated by the research agent.

    Returns:
        str: The agent report concatenated with relevant web articles on the identified illnesses, separated by a blank line.
    """

    # Initialize the search tool for Google Scholar
    search_tool = SerperDevTool(
        search_url="https://google.serper.dev/scholar",
        n_results=2,  # Number of results to retrieve
    )

    # Agent to generate the Google search query
    diagnose_extracter = Agent(
        role="Reader of summarized blood report",
        goal="Analyze the blood report and identify health concerns to formulate a Google search query.",
        allow_delegation=False,
        verbose=False,
        backstory=(
            f"""
            The agent is responsible for reading the blood report summary and generating relevant search queries 
            to find articles and research papers that provide insights into the identified health conditions. 
            For example, if the blood report indicates elevated glucose levels, the agent might generate a query like 
            "causes of elevated glucose levels and treatments".
            Blood Report Summary:
            {agent_report}
            """
        ),
    )

    # Task to generate the search query
    article_extractor = Task(
        description=(
            """
            Based on the blood report summary, generate a search query to find relevant articles or research papers 
            on potential health concerns identified in the report.

            Please reply with concise and simple search queries (string) for Google Scholar. 
            Keep them comma separeted for particular diagnosis. 
            
            """
        ),
        expected_output="elevated ALT causes and treatment,high HbA1c levels causes and treatments,elevated creatinine levels",
        agent=diagnose_extracter,
    )

    # Crew to execute the query generation
    crew = Crew(
        agents=[diagnose_extracter],
        tasks=[article_extractor],
        process=Process.sequential,
    )

    
    # Execute the task and get the output
    crew_output = crew.kickoff()
    search_query = crew_output.raw
    google_prompts = crew_output.raw.split(",")

    # print(google_prompts)
    # print("\n\n")
    # Run the search tool with the generated query
    final_str = ""
    for prompt in google_prompts:
        articles_str = search_tool.run(search_query=prompt)
        final_str+=articles_str

    cleaned_attachment_content = clean_markdown(f"{agent_report}\n\nRelevant Web Articles:\n{final_str}")
    # # Return the agent report concatenated with relevant web articles
    return cleaned_attachment_content
