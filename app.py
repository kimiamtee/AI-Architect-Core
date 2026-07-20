import streamlit as st
import fitz  # PyMuPDF (بسیار سریع و دقیق)
import requests
import base64

st.set_page_config(page_title="AI Architectural Core", page_icon="🏗️", layout="wide")

st.title("🏗️ AI Architectural Core - Enterprise Zoning Auditor")
st.write("Upload any Zoning PDF (Text, Tables, or Scanned) for accurate AI analysis.")

# Sidebar API Key
st.sidebar.header("🔑 Configuration")
api_key = st.sidebar.text_input("Enter OpenRouter API Key", type="password")

st.header("📄 1. High-Precision Zoning Analysis")
uploaded_file = st.file_uploader("Upload Zoning PDF", type=["pdf"])

pdf_pages_text = []

if uploaded_file is not None:
    try:
        # خواندن فایل با PyMuPDF (سریع‌ترین و دقیق‌ترین موتور پایتون)
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        
        full_text = ""
        for i, page in enumerate(doc):
            t = page.get_text()
            if t.strip():
                full_text += f"\n--- Page {i+1} ---\n" + t
        
        st.success(f"✅ PDF processed successfully! Total Pages: {len(doc)}")
        
    except Exception as e:
        st.error(f"Error processing PDF: {e}")

user_query = st.text_input("Ask about Zoning Rules (FAR, Height, Setbacks, Plot size, Parking):")

if st.button("Analyze Document"):
    if not api_key:
        st.error("⚠️ Please enter your OpenRouter API Key in the sidebar!")
    elif uploaded_file is None:
        st.error("⚠️ Please upload a PDF document first!")
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
                if "choices" in res:
                    st.subheader("🤖 AI Auditor Analysis:")
                    st.success(res['choices'][0]['message']['content'])
                else:
                    st.error("API Error: " + str(res))
            except Exception as e:
                st.error(f"Connection Error: {e}")
