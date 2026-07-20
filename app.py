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
    try:
        reader = pypdf.PdfReader(uploaded_file)
        # خواندن تمام صفحات PDF
        for i, page in enumerate(reader.pages):
            extracted = page.extract_text()
            if extracted:
                pdf_text += f"\n--- Page {i+1} ---\n" + extracted
        st.success(f"✅ PDF Uploaded and Parsed Successfully! ({len(reader.pages)} pages extracted)")
    except Exception as e:
        st.error(f"Error reading PDF: {e}")

# ۳. بخش پرسش و پاسخ چت از فایل
user_query = st.text_input("Ask a question about zoning laws (e.g., FAR, Height, Setbacks, Parking):")

if st.button("Analyze & Answer"):
    if not api_key:
        st.error("⚠️ Please enter your OpenRouter API Key in the sidebar on the left!")
    elif not pdf_text:
        st.error("⚠️ Please upload a valid PDF file first!")
    elif not user_query:
        st.error("⚠️ Please type a question in the box above!")
    else:
        with st.spinner("🤖 AI is searching the whole zoning document..."):
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key.strip()}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://streamlit.io",
                "X-Title": "AI Architecture RAG"
            }
            
            # ارسال تا ۱۵,۰۰۰ کاراکتر برای پوشش دادن کل دفترچه
            prompt = f"""
You are an expert AI Zoning Auditor. Read the whole provided document text carefully. 
Extract exact numerical facts for FAR, Maximum Height, Setbacks, and Parking requirements if available. 
If specific numbers are in tables, summarize them accurately.

Document Text:
{pdf_text[:15000]}

User Question:
{user_query}
"""
            
            payload = {
                "model": "openai/gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.1
            }
            
            try:
                response = requests.post(url, headers=headers, json=payload)
                res_json = response.json()
                
                if "choices" in res_json and len(res_json["choices"]) > 0:
                    answer = res_json['choices'][0]['message']['content']
                    st.subheader("🤖 AI Auditor Response:")
                    st.success(answer)
                elif "error" in res_json:
                    st.error(f"❌ OpenRouter API Error: {res_json['error'].get('message', res_json['error'])}")
                else:
                    st.warning("⚠️ Received an unrecognized response from AI server.")
                    st.json(res_json)
                    
            except Exception as e:
                st.error(f"❌ Connection Error: {e}")

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
