import streamlit as st
import pypdf
import requests
import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ۱. تنظیمات صفحه وب‌سایت
st.set_page_config(page_title="AI Architectural Core", page_icon="🏗️", layout="wide")

st.title("🏗️ AI Architectural Core & Zoning RAG Engine")
st.write("Upload municipal zoning documents, query zoning laws, and generate autonomous architectural envelopes.")

# sidebar برای تنظیمات و کلید API
st.sidebar.header("🔑 Configuration")
api_key = st.sidebar.text_input("Enter OpenRouter API Key", type="password")

# ۲. بخش آپلود فایل PDF ضوابط
st.header("📄 1. Document Zoning Analysis (RAG)")
uploaded_file = st.file_uploader("Upload Zoning PDF", type=["pdf"])

pdf_text = ""
if uploaded_file is not None:
    reader = pypdf.PdfReader(uploaded_file)
    for page in reader.pages:
        pdf_text += page.extract_text()
    st.success("✅ PDF Uploaded and Parsed Successfully!")

# ۳. بخش پرسش و پاسخ چت از فایل
user_query = st.text_input("Ask a question about zoning laws (e.g., FAR, Height, Setbacks, Parking):")

if st.button("Analyze & Answer"):
    if not api_key:
        st.error("Please enter your OpenRouter API Key in the sidebar!")
    elif not pdf_text:
        st.error("Please upload a PDF file first!")
    else:
        with st.spinner("AI is analyzing the document..."):
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://streamlit.io"
            }
            prompt = f"You are an AI Zoning Auditor. Read this document text and answer strictly based on facts:\n\n{pdf_text}\n\nQuestion: {user_query}"
            payload = {
                "model": "openai/gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.1
            }
            try:
                res = requests.post(url, headers=headers, json=payload).json()
                answer = res['choices'][0]['message']['content']
                st.subheader("🤖 AI Auditor Response:")
                st.write(answer)
            except Exception as e:
                st.error(f"Error connecting to AI API: {e}")

st.divider()

# ۴. بخش تولید رندر سه‌بعدی بهینه‌شده اقلیمی
st.header("☀️ 2. Autonomous Climate Massing Engine")
col1, col2 = st.columns(2)

with col1:
    width = st.slider("Building Width (m)", 10, 50, 16)
    length = st.slider("Building Length (m)", 10, 50, 26)
    floors = st.slider("Number of Floors", 1, 20, 7)
    floor_height = 3.0
    total_height = floors * floor_height

if st.button("Generate 3D Solar Envelope"):
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    
    x = [0, width, width, 0, 0]
    y = [0, 0, length, length, 0]
    
    ax.plot(x, y, 0, color='#2C3E50', linewidth=2)
    ax.plot(x, y, total_height, color='#27AE60', linewidth=3, label='Optimized Roof')
    
    for ix, iy in zip(x[:4], y[:4]):
        ax.plot([ix, ix], [iy, iy], [0, total_height], color='#27AE60', linestyle='--')
        
    ax.set_title(f"Optimized Massing Envelope ({floors} Floors - {total_height}m)")
    st.pyplot(fig)
