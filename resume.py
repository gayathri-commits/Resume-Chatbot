import streamlit as st
import PyPDF2
from openai import OpenAI

# 👇 Groq uses the OpenAI-compatible client but different base URL
client = OpenAI(
    api_key="YOUR-GROQ-API-KEY",
    base_url="https://api.groq.com/openai/v1"
)

st.set_page_config(page_title="⚡ Resume Q&A Chatbot (Groq Powered!)")
st.title("💬 Resume Q&A using LLaMA 3")
st.caption("Upload your resume and ask smart questions, powered by Groq + LLaMA3 💡")

# Resume upload
uploaded_file = st.file_uploader("📄 Upload your Resume (PDF)", type=["pdf"])
resume_text = ""

if uploaded_file:
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    for page in pdf_reader.pages:
        resume_text += page.extract_text() + "\n"
    st.success("✅ Resume uploaded!")

# Question input
if resume_text:
    question = st.text_input("Ask a question about your resume 👇")
    if question:
        prompt = f"""
        Here's my resume:

        {resume_text}

        Now answer this question based only on the content of the resume:
        "{question}"

        Be short, helpful, and only use relevant information from the resume.
        """

        with st.spinner("Thinking really fast... ⚡"):
            response = client.chat.completions.create(
                model="llama3-8b-8192",  # 🔥 Use Groq's blazing LLaMA3 model
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )

        answer = response.choices[0].message.content
        st.markdown("### 🧠 Answer")
        st.write(answer)
