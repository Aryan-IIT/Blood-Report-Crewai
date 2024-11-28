import smtplib
from email.message import EmailMessage
import re

def clean_markdown(text):
            # Remove bold markers
            text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
            # Remove any remaining asterisks
            text = re.sub(r'\*', '', text)
            return text


def send_diagnosis_email(sender_email, sender_password, recipient_email, subject, body, attachment_filename, attachment_content):
    try:
        # Convert Markdown bold to HTML bold while preserving line breaks and spacing
        def convert_markdown_to_html(text):
            # Escape HTML special characters
            text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            
            # Replace **bold** with <b>bold</b>
            text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
            
            # Preserve original formatting by converting to HTML paragraphs
            paragraphs = text.split('\n\n')
            html_paragraphs = []
            for para in paragraphs:
                # Trim leading and trailing whitespace
                para = para.strip()
                if para:
                    # Convert inline line breaks within paragraph
                    para_lines = para.split('\n')
                    formatted_para = ' '.join(para_lines)
                    html_paragraphs.append(f'<p>{formatted_para}</p>')
            
            return '\n'.join(html_paragraphs)

        # Convert Markdown to plain text for attachment
        
        # Create the email message with HTML content
        msg = EmailMessage()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Set HTML content
        html_body = convert_markdown_to_html(body)
        msg.add_alternative(f"""\
        <html>
          <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            {html_body}
          </body>
        </html>
        """, subtype='html')

        # Clean the attachment content
        cleaned_attachment_content = clean_markdown(attachment_content)

        # Attach the cleaned text file
        msg.add_attachment(
            cleaned_attachment_content.encode('utf-8'), 
            maintype='text', 
            subtype='plain', 
            filename=attachment_filename
        )

        # Send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

        print(f"Email sent successfully to {recipient_email}.")

    except Exception as e:
        print(f"Failed to send email: {e}")
        raise