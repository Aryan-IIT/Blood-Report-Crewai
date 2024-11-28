# Blood Report Diagnosis and Recommendation System

This project is a comprehensive solution that processes blood test reports, analyzes the data, and provides personalized health recommendations to users. It utilizes the CrewAI framework, OpenAI API, and Google Serper Search to achieve these goals.

## Features

1. **Blood Report Processing**: The system can handle both sample and user-uploaded PDF blood test reports.
2. **Report Understanding**: The CrewAI agents analyze the report and extract relevant insights and information.
3. **Internet Search**: The agents search the internet for articles and resources that are relevant to the user's health profile.
4. **Recommendation Generation**: Based on the report analysis and internet search, the agents provide personalized health recommendations.
5. **Secure Email Delivery**: The system securely sends the analysis and recommendations to the user via email.

## Project Structure

The project has the following file structure:

```
.
├── .gitignore
├── .env
├── Backend
│   ├── __init__.py
│   ├── agents_and_tasks.py
│   └── mailing.py
├── Frontend
│   └── app.py
├── PDF
│   ├── sample_pdf.pdf
│   └── user_uploaded_pdf.pdf
├── README.md
└── requirements.txt
```

- `Backend` directory:
  - `agents_and_tasks.py`: Contains the implementation of the CrewAI agents and their tasks.
  - `mailing.py`: Handles the email sending functionality.
- `Frontend` directory:
  - `app.py`: The Streamlit application that serves as the user interface.
- `PDF` directory:
  - Contains sample and user-uploaded PDF files for the blood test reports.

## Getting Started

To run the Blood Report Diagnosis and Recommendation System, follow these steps:

1. **Set up the environment**:
   - Create a virtual environment and activate it.
   - Install the required dependencies by running `pip install -r requirements.txt`.
   - Set the necessary environment variables (e.g., OpenAI API key, Google Serper API key) in a `.env` file.

2. **Run the Streamlit app**:
   - Navigate to the `Frontend` directory.
   - Run the Streamlit app using the command `streamlit run app.py`.
   - The app will start running, and you can access it in your web browser.

3. **Interact with the app**:
   - The Streamlit app will provide an interface for you to either use the sample PDF or upload your own blood test report.
   - Click the "Generate Report" button to initiate the report analysis and recommendation generation process.
   - Once the process is complete, the app will display the generated report and provide an option to email the results.

4. **Customize and extend**:
   - Modify the `agents_and_tasks.py` file to customize the agent behavior and task logic.
   - Update the `mailing.py` file to enhance the email sending functionality or integrate with other communication channels.
   - Explore the Streamlit app (`app.py`) to improve the user interface and experience.

## Dependencies

The project relies on the following key dependencies:

- CrewAI: A framework for building AI agent-based systems.
- OpenAI API: Used for natural language processing and understanding.
- Google Serper Search: Utilized for web article retrieval and information aggregation.
- Streamlit: A Python library for building interactive web applications.
- smtplib: Python's built-in library for sending emails.

Please ensure that you have the necessary API keys and credentials set up before running the application.

## Conclusion

The Blood Report Diagnosis and Recommendation System is a powerful tool that helps users understand their health better by analyzing their blood test reports and providing personalized recommendations. The combination of CrewAI, OpenAI, and Google Serper Search enables a comprehensive and secure solution for delivering valuable health insights to users. Feel free to explore, customize, and extend this project to meet your specific requirements.
