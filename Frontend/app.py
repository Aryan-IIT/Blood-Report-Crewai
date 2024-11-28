# Streamlit App for Health Diagnosis
import streamlit as st
from pathlib import Path
import os
from dotenv import load_dotenv
import sys
import tempfile
from datetime import date

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "Backend"))
import agents_and_tasks as wm  # Import work module
from mailing import send_diagnosis_email  # Function to send email

# Load environment variables for API keys and email credentials
load_dotenv()

# Set Streamlit page title and layout
st.set_page_config(page_title="Blood Report Analyzer App", layout="wide")

# Initialize Session State for inputs and report generation
if 'report_generated' not in st.session_state:
    st.session_state.report_generated = False
if 'report_content' not in st.session_state:
    st.session_state.report_content = None
if 'email_content' not in st.session_state:
    st.session_state.email_content = None
if 'report_with_article' not in st.session_state:
    st.session_state.report_with_article = None

# PDF Path
sample_pdf_path = Path(__file__).resolve().parent.parent / "PDF" / "sample_pdf.pdf"

# Check if the sample PDF exists
if not sample_pdf_path.exists():
    st.error(f"The sample PDF file at {sample_pdf_path} does not exist.")
    st.stop()

# App Header
st.title("Blood Report Diagnosis Report Generator")
st.write("This app processes blood reports (PDFs) for diagnosis, extracts insights, and sends reports via email.")

st.sidebar.header("Input Options")
use_sample = st.sidebar.checkbox("Use Sample PDF", value=True)

uploaded_file = None
if not use_sample:
    uploaded_file = st.sidebar.file_uploader("Upload your PDF", type=["pdf"])

if not use_sample and not uploaded_file:
    st.warning("Please upload a PDF file or use the sample PDF.")
    st.stop()

# Process PDF and Generate Reports
def generate_report(pdf_path):
    """
    Generate report from PDF and cache results in session state
    """
    try:
        report_content, email_content = wm.pdf_rag(str(pdf_path))
        report_with_article = wm.web_articles_extract(report_content)
        
        st.session_state.report_generated = True
        st.session_state.report_content = report_content
        st.session_state.email_content = email_content
        st.session_state.report_with_article = report_with_article
        
        st.success("Report generated successfully!")
        return True
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return False

# Generate Report Button
if st.sidebar.button("Generate Report"):
    # Determine PDF path
    if use_sample:
        pdf_path = sample_pdf_path
    else:
        # Use temporary file to handle uploaded PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.read())
            pdf_path = temp_file.name
    
    # Generate report
    generate_report(pdf_path)

# Display Report if Generated
if st.session_state.report_generated:
    st.subheader("Report with Web Articles")
    st.text_area("Generated Report", 
                 value=st.session_state.report_with_article, 
                 height=300)

    # Email Input Section
    st.subheader("Email the Report")
    with st.form(key="email_form", clear_on_submit=True):
        username = st.text_input("Enter your name:")
        recipient_email = st.text_input("Recipient Email:")
        submit_email = st.form_submit_button("Send Email")
        
        if submit_email:
            if username and recipient_email:
                try:
                    subject = f"Health Diagnosis Report of {username} ({date.today()}), LPL Rohini"
                    body = st.session_state.email_content
                    attachment_filename = f"Blood Diagnosis Report {username}.txt"
                    attachment_content = st.session_state.report_with_article

                    # Send Email
                    send_diagnosis_email(
                        os.environ["SENDER_EMAIL"],
                        os.environ["SENDER_PASSWORD"],
                        recipient_email,
                        subject,
                        body,
                        attachment_filename,
                        attachment_content,
                    )
                    st.success(f"Email sent to {recipient_email} successfully!")
                except Exception as e:
                    st.error(f"Email sending failed: {e}")
            else:
                st.error("Please provide both name and recipient email.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Built by Aryan")