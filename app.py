"""
AI-Architect-Core: Enterprise Zoning Auditor & Climate-Responsive 3D Massing Engine
Designed for high-end architectural firms (Dubai/International Portfolio Standards)
"""

import streamlit as st
import fitz  # PyMuPDF
import requests
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from typing import Dict, Any
import time

# ==========================================
# CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="AI-Architect-Core | Enterprise Zoning Auditor",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "openai/gpt-4o-mini"
REQUEST_TIMEOUT = 30  # seconds

# Custom CSS for polished metric cards
st.markdown("""
    <style>
    .stMetric { background-color: #ffffff; padding: 12px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# HELPER FUNCTIONS
# ==========================================

@st.cache_data(show_spinner=False)
def extract_pdf_text(pdf_bytes: bytes) -> tuple[str, int]:
    """
    Extract text from PDF using PyMuPDF with robust error handling.
    Returns (extracted_text, total_pages)
    """
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        full_text = ""
        
        for page_num, page in enumerate(doc, start=1):
            text = page.get_text("text")
            if text.strip():
                full_text += f"\n--- Page {page_num} ---\n{text}"
        
        total_pages = len(doc)
        doc.close()
        return full_text.strip(), total_pages
    
    except Exception as e:
        raise Exception(f"PDF parsing failed: {str(e)}")


def call_openrouter_api(
    api_key: str,
    document_text: str,
    user_query: str
) -> Dict[str, Any]:
    """
    Call OpenRouter API with structured output formatting and error handling.
    """
    headers = {
        "Authorization": f"Bearer {api_key.strip()}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://ai-architect-core.streamlit.app",
        "X-Title": "AI-Architect-Core"
    }
    
    # Strictly formatted prompt to ensure concise and organized response for ANY query
    prompt = f"""You are an expert Executive AI Zoning Auditor and Licensed Architect.

Analyze the zoning document and answer the user query in a STRICTLY STRUCTURED, CONCISE EXECUTIVE FORMAT.
Avoid long conversational introductions or fluffy explanations.

Format your response EXACTLY as follows:

### 🎯 EXECUTIVE AUDIT SUMMARY:
- **Primary Finding:** [Direct one-sentence answer to user query]
- **Numeric Limits / Metrics:** [List exact values like FAR, Setbacks, Heights, Coverage, or Parking]
- **Net Footprint / Dimensions (if applicable):** [Width x Length or Area calculations]

### 📋 CODE COMPLIANCE BULLETS:
- [Key rule 1 from document]
- [Key rule 2 from document]
- [Key rule 3 from document]

ZONING DOCUMENT CONTENT:
{document_text[:18000]}

USER QUESTION:
{user_query}"""

    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
        "max_tokens": 1500
    }
    
    try:
        response = requests.post(
            OPENROUTER_API_URL,
            headers=headers,
            json=payload,
            timeout=REQUEST_TIMEOUT
        )
        
        if response.status_code == 401:
            return {"success": False, "error": "Invalid API Key. Please check your OpenRouter credentials."}
        elif response.status_code == 429:
            return {"success": False, "error": "Rate limit exceeded. Please wait a moment and try again."}
        elif response.status_code != 200:
            return {"success": False, "error": f"API Error (Status {response.status_code}): {response.text[:200]}"}
        
        data = response.json()
        if "choices" in data and len(data["choices"]) > 0:
            content = data["choices"][0]["message"]["content"]
            return {"success": True, "response": content}
        else:
            return {"success": False, "error": f"Unexpected API response format: {str(data)[:200]}"}
    
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timeout. Please try again."}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Network connection error. Check internet connection."}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {str(e)}"}


def generate_3d_massing(width: float, length: float, floors: int, floor_height: float = 3.5):
    """
    Generate professional 3D massing visualization using Matplotlib Poly3DCollection.
    """
    total_height = floors * floor_height
    
    fig = plt.figure(figsize=(9, 7), facecolor='white')
    ax = fig.add_subplot(111, projection='3d')
    
    vertices = [
        [0, 0, 0], [width, 0, 0], [width, length, 0], [0, length, 0],
        [0, 0, total_height], [width, 0, total_height], 
        [width, length, total_height], [0, length, total_height]
    ]
    
    faces = [
        [vertices[0], vertices[1], vertices[5], vertices[4]],
        [vertices[1], vertices[2], vertices[6], vertices[5]],
        [vertices[2], vertices[3], vertices[7], vertices[6]],
        [vertices[3], vertices[0], vertices[4], vertices[7]],
        [vertices[4], vertices[5], vertices[6], vertices[7]],
        [vertices[0], vertices[1], vertices[2], vertices[3]]
    ]
    
    face_collection = Poly3DCollection(
        faces,
        facecolors='#27ae60',
        linewidths=1.5,
        edgecolors='#2c3e50',
        alpha=0.75
    )
    ax.add_collection3d(face_collection)
    
    ax.set_xlim(0, width * 1.3)
    ax.set_ylim(0, length * 1.3)
    ax.set_zlim(0, total_height * 1.3)
    
    ax.set_xlabel('Width (m)', fontsize=10, fontweight='bold')
    ax.set_ylabel('Length (m)', fontsize=10, fontweight='bold')
    ax.set_zlabel('Height (m)', fontsize=10, fontweight='bold')
    ax.set_title(
        f'3D Envelope Massing\n{floors} Floors | {total_height:.1f}m Height | Footprint: {width:.1f}m × {length:.1f}m',
        fontsize=12,
        fontweight='bold',
        pad=15
    )
    
    ax.view_init(elev=25, azim=45)
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    
    return fig


# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================
if 'pdf_text' not in st.session_state:
    st.session_state.pdf_text = ""
if 'pdf_pages' not in st.session_state:
    st.session_state.pdf_pages = 0
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_analysis' not in st.session_state:
    st.session_state.current_analysis = None

# ==========================================
# MAIN UI LAYOUT
# ==========================================

st.title("🏗️ AI-Architect-Core")
st.caption("Enterprise Zoning Auditor & Climate-Responsive 3D Massing Engine")

st.sidebar.header("🔑 API Configuration")
api_key = st.sidebar.text_input(
    "OpenRouter API Key",
    type="password",
    help="Get your API key from https://openrouter.ai/keys"
)

if api_key:
    st.sidebar.success("✅ API Key Configured")
else:
    st.sidebar.warning("⚠️ API Key Required")

st.sidebar.markdown("---")
st.sidebar.info("Combine RAG zoning analysis with interactive 3D massing feasibility.")

# Organize layout into 3 crisp tabs
tab1, tab2, tab3 = st.tabs(["📄 1. Zoning RAG Auditor", "📊 2. Feasibility Calculator", "☀️ 3. 3D Massing Engine"])

# ------------------------------------------
# TAB 1: RAG ZONING AUDITOR
# ------------------------------------------
with tab1:
    st.header("📄 Section 1: Zoning Regulation Audit")
    
    uploaded_file = st.file_uploader(
        "Upload Zoning PDF Document",
        type=["pdf"],
        help="Upload municipal zoning code"
    )

    if uploaded_file is not None:
        with st.spinner("🔍 Extracting text from PDF..."):
            try:
                pdf_bytes = uploaded_file.read()
                extracted_text, total_pages = extract_pdf_text(pdf_bytes)
                st.session_state.pdf_text = extracted_text
                st.session_state.pdf_pages = total_pages
                
                if extracted_text:
                    st.success(f"✅ PDF processed! **{total_pages} pages** | **{len(extracted_text):,} characters**")
                else:
                    st.warning("⚠️ No plain text found. Document might be scanned.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

    user_query = st.text_area(
        "❓ Ask about Zoning Rules / Plot Info:",
        height=140,
        placeholder="e.g., I am evaluating a residential plot measuring 20m x 35m..."
    )

    c_btn1, c_btn2 = st.columns([1, 5])
    with c_btn1:
        analyze_button = st.button("🔍 Run Audit", type="primary", use_container_width=True)
    with c_btn2:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.current_analysis = None
            st.rerun()

    if analyze_button:
        if not api_key:
            st.error("⚠️ Enter your OpenRouter API Key in the sidebar!")
        elif not st.session_state.pdf_text:
            st.error("⚠️ Upload a valid PDF document first!")
        elif not user_query.strip():
            st.error("⚠️ Enter a question!")
        else:
            with st.spinner("🤖 Analyzing zoning rules and calculating metrics..."):
                result = call_openrouter_api(
                    api_key=api_key,
                    document_text=st.session_state.pdf_text,
                    user_query=user_query
                )
                if result["success"]:
                    st.session_state.current_analysis = {
                        "query": user_query,
                        "response": result["response"],
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    st.session_state.chat_history.append(st.session_state.current_analysis)
                else:
                    st.error(f"❌ API Error: {result['error']}")

    if st.session_state.current_analysis:
        st.markdown("### 🤖 AI Auditor Brief")
        st.info(st.session_state.current_analysis["response"])

# ------------------------------------------
# TAB 2: FEASIBILITY CALCULATOR
# ------------------------------------------
with tab2:
    st.header("📊 Interactive Footprint & Feasibility Calculator")
    st.write("Enter plot dimensions & setbacks extracted from Tab 1 to calculate net footprint metrics.")
    
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        plot_w = st.number_input("Plot Width (m)", value=15.0, step=1.0)
        front_sb = st.number_input("Front Setback (m)", value=3.0, step=0.5)
    with col_p2:
        plot_l = st.number_input("Plot Length (m)", value=20.0, step=1.0)
        rear_sb = st.number_input("Rear Setback (m)", value=3.0, step=0.5)
    with col_p3:
        target_floors = st.number_input("Floors Count", value=3, min_value=1, max_value=20)
        side_sb = st.number_input("Side Setbacks (m each)", value=1.5, step=0.5)

    net_w = max(0.0, plot_w - (2 * side_sb))
    net_l = max(0.0, plot_l - front_sb - rear_sb)
    plot_area = plot_w * plot_l
    footprint_area = net_w * net_l
    coverage_pct = (footprint_area / plot_area * 100) if plot_area > 0 else 0
    total_gfa = footprint_area * target_floors

    st.markdown("---")
    st.subheader("💡 Calculated Feasibility Metrics:")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Plot Area", f"{plot_area:.0f} m²")
    m2.metric("Net Footprint Size", f"{net_w:.1f}m × {net_l:.1f}m")
    m3.metric("Ground Coverage", f"{footprint_area:.0f} m²", f"{coverage_pct:.1f}% Coverage")
    m4.metric("Total Buildable GFA", f"{total_gfa:.0f} m²", f"{target_floors} Floors")

# ------------------------------------------
# TAB 3: 3D MASSING ENGINE
# ------------------------------------------
with tab3:
    st.header("☀️ Climate 3D Massing Visualization")
    
    col_params, col_viz = st.columns([1, 2])
    
    with col_params:
        st.markdown("### 🎛️ Building Parameters")
        
        width = st.slider("Building Width (m)", 5.0, 50.0, float(net_w if net_w > 0 else 12.0))
        length = st.slider("Building Length (m)", 5.0, 50.0, float(net_l if net_l > 0 else 14.0))
        floors = st.slider("Floors Count", 1, 20, int(target_floors))
        floor_height = st.number_input("Floor Height (m)", 2.5, 5.0, 3.5, 0.1)
        
        total_height = floors * floor_height
        gfa = width * length * floors
        
        st.markdown("---")
        st.metric("Total Height", f"{total_height:.1f} m")
        st.metric("Footprint Area", f"{width * length:.1f} m²")
        st.metric("Total GFA", f"{gfa:,.0f} m²")

    with col_viz:
        with st.spinner("🎨 Rendering 3D envelope..."):
            fig = generate_3d_massing(width, length, floors, floor_height)
            st.pyplot(fig)
            plt.close()

# Footer
st.markdown("---")
st.caption("🏗️ **AI-Architect-Core** | Powered by OpenRouter API & PyMuPDF")

import json

# ==========================================
# بخش خروجی‌های حرفه‌ای (در انتهای Tab 2 یا Tab 3 اضافه می‌شود)
# ==========================================
st.markdown("---")
st.subheader("📥 Export & Rhino/Grasshopper Integration")

col_exp1, col_exp2 = st.columns(2)

# ۱. ساخت فایل JSON اختصاصی برای گراس‌هاپر
grasshopper_data = {
    "project_name": "Villa Feasibility Analysis",
    "site_parameters": {
        "plot_width": plot_w,
        "plot_length": plot_l,
        "plot_area": plot_area
    },
    "building_envelope": {
        "net_width": net_w,
        "net_length": net_l,
        "floors_count": target_floors,
        "floor_height": 3.5,
        "total_height": target_floors * 3.5,
        "ground_footprint": footprint_area,
        "total_gfa": total_gfa
    },
    "setbacks": {
        "front": front_sb,
        "rear": rear_sb,
        "sides": side_sb
    }
}

# تبدیل به رشته JSON
json_string = json.dumps(grasshopper_data, indent=4)

with col_exp1:
    st.download_button(
        label="🦏 Download Grasshopper JSON Parameter File",
        file_name="zoning_params.json",
        mime="application/json",
        data=json_string,
        help="Import this JSON directly into Grasshopper to generate 3D geometry in Rhino!"
    )

# ۲. دانلود گزارش متنی آنالیز
if st.session_state.current_analysis:
    report_text = f"""==================================================
AI-ARCHITECT-CORE: EXECUTIVE FEASIBILITY REPORT
Timestamp: {st.session_state.current_analysis['timestamp']}
==================================================

[1] ZONING AUDIT ANALYSIS:
{st.session_state.current_analysis['response']}

==================================================
[2] CALCULATED METRICS:
- Total Plot Area: {plot_area:.0f} sqm
- Net Building Dimensions: {net_w:.1f}m x {net_l:.1f}m
- Footprint Area: {footprint_area:.0f} sqm ({coverage_pct:.1f}% coverage)
- Total GFA: {total_gfa:.0f} sqm ({target_floors} Floors)
==================================================
"""
    with col_exp2:
        st.download_button(
            label="📄 Download Executive Audit Report (.txt)",
            file_name="Zoning_Feasibility_Report.txt",
            mime="text/plain",
            data=report_text
        )
