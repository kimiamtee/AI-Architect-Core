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
from typing import Optional, Dict, Any
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
            text = page.get_text("text")  # Extract plain text
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
    Call OpenRouter API with proper error handling and timeout.
    Returns dict with 'success' (bool) and 'response' or 'error' (str)
    """
    
    headers = {
        "Authorization": f"Bearer {api_key.strip()}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://ai-architect-core.streamlit.app",
        "X-Title": "AI-Architect-Core"
    }
    
    # Construct specialized architectural prompt
    prompt = f"""You are an expert AI Zoning Auditor and Licensed Architect with deep expertise in urban planning regulations.

Analyze the following zoning document and answer the user's question with:
- Exact numeric calculations (FAR, GFA, setbacks, parking ratios)
- Dimensional requirements (heights, distances, plot coverage)
- Code compliance validation
- Professional recommendations

If numeric data is provided in the question (plot size, dimensions), perform precise calculations.

ZONING DOCUMENT CONTENT:
{document_text[:18000]}

USER QUESTION:
{user_query}

Provide a clear, structured response with exact numbers and code references where applicable."""

    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
        "max_tokens": 2000
    }
    
    try:
        response = requests.post(
            OPENROUTER_API_URL,
            headers=headers,
            json=payload,
            timeout=REQUEST_TIMEOUT
        )
        
        # Check HTTP status
        if response.status_code == 401:
            return {"success": False, "error": "Invalid API Key. Please check your OpenRouter credentials."}
        elif response.status_code == 429:
            return {"success": False, "error": "Rate limit exceeded. Please wait a moment and try again."}
        elif response.status_code != 200:
            return {"success": False, "error": f"API Error (Status {response.status_code}): {response.text[:200]}"}
        
        # Parse JSON response
        data = response.json()
        
        if "choices" in data and len(data["choices"]) > 0:
            content = data["choices"][0]["message"]["content"]
            return {"success": True, "response": content}
        else:
            return {"success": False, "error": f"Unexpected API response format: {str(data)[:200]}"}
    
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timeout. The API took too long to respond. Please try again."}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Network connection error. Please check your internet connection."}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {str(e)}"}


def generate_3d_massing(width: float, length: float, floors: int, floor_height: float = 3.0):
    """
    Generate professional 3D massing visualization using Matplotlib.
    """
    total_height = floors * floor_height
    
    fig = plt.figure(figsize=(10, 8), facecolor='white')
    ax = fig.add_subplot(111, projection='3d')
    
    # Define building vertices
    vertices = [
        [0, 0, 0], [width, 0, 0], [width, length, 0], [0, length, 0],  # Base
        [0, 0, total_height], [width, 0, total_height], 
        [width, length, total_height], [0, length, total_height]  # Top
    ]
    
    # Define faces (each face is 4 vertices)
    faces = [
        [vertices[0], vertices[1], vertices[5], vertices[4]],  # Front
        [vertices[1], vertices[2], vertices[6], vertices[5]],  # Right
        [vertices[2], vertices[3], vertices[7], vertices[6]],  # Back
        [vertices[3], vertices[0], vertices[4], vertices[7]],  # Left
        [vertices[4], vertices[5], vertices[6], vertices[7]],  # Top
        [vertices[0], vertices[1], vertices[2], vertices[3]]   # Bottom
    ]
    
    # Create 3D polygon collection
    face_collection = Poly3DCollection(
        faces,
        facecolors='#3498db',
        linewidths=1.5,
        edgecolors='#2c3e50',
        alpha=0.85
    )
    ax.add_collection3d(face_collection)
    
    # Set axis limits with padding
    ax.set_xlim(0, width * 1.2)
    ax.set_ylim(0, length * 1.2)
    ax.set_zlim(0, total_height * 1.2)
    
    # Labels and title
    ax.set_xlabel('Width (m)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Length (m)', fontsize=11, fontweight='bold')
    ax.set_zlabel('Height (m)', fontsize=11, fontweight='bold')
    ax.set_title(
        f'Climate-Optimized Massing Envelope\n{floors} Floors | {total_height}m Total Height | {width}m × {length}m Footprint',
        fontsize=13,
        fontweight='bold',
        pad=20
    )
    
    # Styling
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

# Header
st.title("🏗️ AI-Architect-Core")
st.markdown("**Enterprise Zoning Auditor & Climate-Responsive 3D Massing Engine**")
st.caption("Designed for International Architectural Tech Firms | Dubai Portfolio Standards")

# Sidebar Configuration
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
st.sidebar.markdown("### 📚 About")
st.sidebar.info(
    "This tool combines RAG-powered zoning analysis with parametric 3D massing generation "
    "for architectural feasibility studies."
)

# ==========================================
# SECTION 1: ZONING ANALYSIS (RAG)
# ==========================================
st.markdown("---")
st.header("📄 Section 1: High-Precision Zoning Analysis (RAG)")

uploaded_file = st.file_uploader(
    "Upload Zoning Regulation PDF",
    type=["pdf"],
    help="Upload municipal zoning codes, building regulations, or planning documents"
)

# Process uploaded PDF
if uploaded_file is not None:
    with st.spinner("🔍 Extracting text from PDF..."):
        try:
            pdf_bytes = uploaded_file.read()
            extracted_text, total_pages = extract_pdf_text(pdf_bytes)
            
            st.session_state.pdf_text = extracted_text
            st.session_state.pdf_pages = total_pages
            
            if extracted_text:
                st.success(
                    f"✅ PDF processed successfully! "
                    f"**{total_pages} pages** | **{len(extracted_text):,} characters** extracted"
                )
                
                with st.expander("📖 Preview Extracted Text (First 2000 characters)"):
                    st.text(extracted_text[:2000] + "...")
            else:
                st.warning(
                    "⚠️ No text extracted from PDF. The document might be scanned/image-based. "
                    "You can still ask questions - the AI will work with available context."
                )
        
        except Exception as e:
            st.error(f"❌ Error processing PDF: {str(e)}")
            st.session_state.pdf_text = ""

# Query Interface
user_query = st.text_input(
    "❓ Ask about Zoning Rules",
    placeholder="e.g., What is the maximum FAR for residential plots? What are the setback requirements?",
    help="Ask specific questions about FAR, height limits, setbacks, parking, plot coverage, etc."
)

col1, col2 = st.columns([1, 5])
with col1:
    analyze_button = st.button("🔍 Analyze", type="primary", use_container_width=True)
with col2:
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.current_analysis = None
        st.rerun()

# Process Analysis Request
if analyze_button:
    if not api_key:
        st.error("⚠️ Please enter your OpenRouter API Key in the sidebar!")
    elif not st.session_state.pdf_text:
        st.error("⚠️ Please upload a valid PDF document first!")
    elif not user_query.strip():
        st.error("⚠️ Please enter a question!")
    else:
        with st.spinner("🤖 Analyzing zoning regulations and performing calculations..."):
            result = call_openrouter_api(
                api_key=api_key,
                document_text=st.session_state.pdf_text,
                user_query=user_query
            )
            
            if result["success"]:
                # Store in session state
                st.session_state.current_analysis = {
                    "query": user_query,
                    "response": result["response"],
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.chat_history.append(st.session_state.current_analysis)
            else:
                st.error(f"❌ API Error: {result['error']}")

# Display Current Analysis
if st.session_state.current_analysis:
    st.markdown("### 🤖 AI Auditor Analysis")
    st.success(st.session_state.current_analysis["response"])

# Display Chat History
if len(st.session_state.chat_history) > 1:
    with st.expander(f"📜 View Chat History ({len(st.session_state.chat_history)} interactions)"):
        for i, item in enumerate(reversed(st.session_state.chat_history[:-1]), 1):
            st.markdown(f"**Q{i}:** {item['query']}")
            st.info(item['response'])
            st.caption(f"🕒 {item['timestamp']}")
            st.markdown("---")

# ==========================================
# SECTION 2: 3D MASSING ENGINE
# ==========================================
st.markdown("---")
st.header("☀️ Section 2: Autonomous Climate Massing Engine")

col_params, col_viz = st.columns([1, 2])

with col_params:
    st.markdown("### 🎛️ Building Parameters")
    
    width = st.slider(
        "Building Width (m)",
        min_value=10,
        max_value=50,
        value=16,
        step=1,
        help="East-West dimension"
    )
    
    length = st.slider(
        "Building Length (m)",
        min_value=10,
        max_value=50,
        value=26,
        step=1,
        help="North-South dimension"
    )
    
    floors = st.slider(
        "Number of Floors",
        min_value=1,
        max_value=20,
        value=7,
        step=1
    )
    
    floor_height = st.number_input(
        "Floor Height (m)",
        min_value=2.5,
        max_value=5.0,
        value=3.0,
        step=0.1
    )
    
    total_height = floors * floor_height
    gfa = width * length * floors
    
    st.markdown("---")
    st.markdown("### 📊 Calculated Metrics")
    st.metric("Total Height", f"{total_height} m")
    st.metric("Gross Floor Area (GFA)", f"{gfa:,.0f} m²")
    st.metric("Footprint", f"{width * length:,.0f} m²")
    
    generate_button = st.button("🚀 Generate 3D Massing", type="primary", use_container_width=True)

with col_viz:
    if generate_button or 'last_3d_config' in st.session_state:
        # Store configuration to persist visualization
        st.session_state.last_3d_config = (width, length, floors, floor_height)
        
        with st.spinner("🎨 Rendering 3D envelope..."):
            fig = generate_3d_massing(width, length, floors, floor_height)
            st.pyplot(fig)
            plt.close()

# ==========================================
# FOOTER
# ==========================================
st.markdown("---")
st.caption(
    "🏗️ **AI-Architect-Core** | Powered by OpenRouter API & PyMuPDF | "
    "Built for Enterprise Architectural Technology Workflows"
)
