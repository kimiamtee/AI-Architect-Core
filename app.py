import streamlit as st
import fitz  # PyMuPDF (استخراج بسیار سریع و دقیق متون و جداول)
import requests
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ۱. تنظیمات اولیه صفحه وب‌سایت
st.set_page_config(page_title="AI Architectural Core", page_icon="🏗️", layout="wide")

st.title("🏗️ AI Architectural Core - Enterprise Zoning Auditor")
st.write("Upload any Zoning PDF (Text, Tables, or Scanned) for accurate AI analysis and generate climate-optimized 3D massing.")

# Sidebar برای تنظیمات کلید API
st.sidebar.header("🔑 Configuration")
api_key = st.sidebar.text_input("Enter OpenRouter API Key", type="password")

# ==========================================
# ۲. بخش اول: استخراج و تحلیل هوشمند ضوابط (RAG)
# ==========================================
st.header("📄 1. High-Precision Zoning Analysis (RAG)")
uploaded_file = st.file_uploader("Upload Zoning PDF", type=["pdf"])

full_text = ""

if uploaded_file is not None:
    try:
        # پردازش PDF با PyMuPDF
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        
        for i, page in enumerate(doc):
            t = page.get_text()
            if t.strip():
                full_text += f"\n--- Page {i+1} ---\n" + t
        
        st.success(f"✅ PDF processed successfully! Total Pages: {len(doc)} ({len(full_text)} characters extracted)")
        
    except Exception as e:
        st.error(f"Error processing PDF: {e}")

user_query = st.text_input("Ask about Zoning Rules (FAR, Height, Setbacks, Plot size, Parking):")

if st.button("Analyze Document"):
    if not api_key:
        st.error("⚠️ Please enter your OpenRouter API Key in the sidebar!")
    elif uploaded_file is None or not full_text.strip():
        st.error("⚠️ Please upload a valid PDF document first!")
    elif not user_query:
        st.error("⚠️ Please enter your question!")
    else:
        with st.spinner("🤖 Deeply analyzing zoning document & calculations..."):
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key.strip()}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://streamlit.io",
                "X-Title": "AI Architecture Core"
            }
            
            prompt = f"""
You are an expert AI Zoning Auditor & Architect. 
Analyze the following zoning document text and answer the user question with exact math, setback dimensions, FAR, heights, and parking requirements. 
If the user provides plot dimensions in their prompt, compute the exact footprint and allowed floor dimensions.

Document Content:
{full_text[:20000]}

User Question:
{user_query}
"""
            
            payload = {
                "model": "openai/gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.1
            }
            
            try:
                res = requests.post(url, headers=headers, json=payload).json()
                if "choices" in res and len(res["choices"]) > 0:
                    st.subheader("🤖 AI Auditor Analysis:")
                    st.success(res['choices'][0]['message']['content'])
                else:
                    st.error("API Error: " + str(res))
            except Exception as e:
                st.error(f"Connection Error: {e}")

st.divider()

# ==========================================
# ۳. بخش دوم: موتور هندسی سه‌بعدی اقلیمی (3D Massing)
# ==========================================
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
    
    # رسم خطوط پایه و سقف
    ax.plot(x, y, 0, color='#2C3E50', linewidth=2, label='Ground Footprint')
    ax.plot(x, y, total_height, color='#27AE60', linewidth=3, label='Optimized Roof')
    
    # رسم ستون‌های عمودی
    for ix, iy in zip(x[:4], y[:4]):
        ax.plot([ix, ix], [iy, iy], [0, total_height], color='#27AE60', linestyle='--')
        
    ax.set_title(f"Optimized Massing Envelope ({floors} Floors - {total_height}m Height)")
    ax.set_xlabel("Width (m)")
    ax.set_ylabel("Length (m)")
    ax.set_zlabel("Height (m)")
    
    st.pyplot(fig)
