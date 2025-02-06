import streamlit as st
import openai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Initialize the OpenAI client
client = openai.Client(
    api_key="YOUR API KEY",
)

# Function to summarize and chunk the book
def openapi_reply(text, chunk_size):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a book librarian and a good summarizer and analyzer of books. Your job is to summarize and chunk the book content in equal parts."},
            {"role": "user", "content": f"Summarize and chunk the book '{text}' into chunks of size {chunk_size} words."},
        ],
    )

    return response.choices[0].message.content.strip().split('\n\n')  # Assuming chunks are separated by double newlines

# Function to send email
def send_email(chunks, receiver_email):
    sender_email = "mohammadabbas21000@gmail.com"
    password = "abbas3Kay"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Book Summary and Chunks"
    message["From"] = sender_email
    message["To"] = receiver_email

    full_content = "\n\n".join(chunks)
    part = MIMEText(full_content, "plain")
    message.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

# Streamlit UI
st.set_page_config(page_title="SUMMARIFY", page_icon=":books:", layout="wide")

st.title("📚 SUMMARIFY")
st.markdown("Welcome to the SUMMARIFY!")
st.markdown("Enter the name of the book you want to summarize and choose how you want to receive the summary.")

book_name = st.text_input("Enter the book name:", "")
chunk_size = 120  # Define the chunk size

col1, col2 = st.columns(2)

with col1:
    if st.button("Submit and Read Now"):
        if book_name:
            chunks = openapi_reply(book_name, chunk_size)
            st.subheader("Book Summary")
            for chunk in chunks:
                st.write(chunk)
        else:
            st.error("Please enter a book name.")

with col2:
    if st.button("Submit and Read via Email"):
        email = st.text_input("Enter your email address:")
        if st.button("Confirm"):
            if email:
                with st.spinner("Sending email..."):
                    chunks = openapi_reply(book_name, chunk_size)
                    send_email(chunks, email)
                st.success("You will receive the summary and chunks on your email.")
            else:
                st.error("Please enter a valid email address.")