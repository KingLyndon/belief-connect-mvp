import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.figure import Figure
import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Tuple
from supabase import create_client
import urllib.parse

# ============================================================================
# DATABASE CONNECTION (Supabase)
# ============================================================================
URL = "https://rinbuwveuurjrzqijiai.supabase.co"
KEY = "sb_publishable_rcamFVqYmdrLgnKtq_Or2Q_ojNXBJTg"
supabase = create_client(URL, KEY)

def save_user_data(name, responses, clan_name):
    response_list = [responses[i] for i in sorted(responses.keys())]
    data = {"username": name, "responses": response_list, "clan_name": clan_name}
    try:
        supabase.table("profiles").insert(data).execute()
        return True
    except Exception as e:
        st.error(f"Database Error: {e}")
        return False

# ============================================================================
# DATA MODELS & CONFIG
# ============================================================================

@dataclass
class Question:
    id: int; text: str; trait: str; color_name: str; hex_color: str; intensity: str

QUESTIONS = [
    Question(id=1, text="Individual freedom should always take precedence over collective security.", trait="Liberty vs Security", color_name="Purple", hex_color="#9333EA", intensity="high"),
    Question(id=2, text="I would rather be the leader of a small, struggling team than a member of a large, successful one.", trait="Ambition", color_name="Red", hex_color="#DC2626", intensity="high"),
    Question(id=3, text="I find more comfort in the unknown than in the familiar.", trait="Openness to Change", color_name="Green", hex_color="#16A34A", intensity="medium"),
    Question(id=4, text="In a crisis, the most practical solution is always better than the one that preserves people's feelings.", trait="Rationality", color_name="Blue", hex_color="#2563EB", intensity="medium"),
    Question(id=5, text="I would prefer a guaranteed $50k/year over a 50% chance at $500k/year.", trait="Stability vs Risk", color_name="Orange", hex_color="#EA580C", intensity="high"),
    Question(id=6, text="Tradition provides a necessary roadmap that modern society should follow more closely.", trait="Altruism/Community", color_name="Purple", hex_color="#9333EA", intensity="medium"),
    Question(id=7, text="A successful life is defined by the tangible legacy or work one leaves behind.", trait="Ambition", color_name="Red", hex_color="#DC2626", intensity="medium"),
    Question(id=8, text="I enjoy discussing abstract theories even if they have no practical application.", trait="Openness to Ideas", color_name="Green", hex_color="#16A34A", intensity="low"),
    Question(id=9, text="When making big life decisions, I trust my 'gut feeling' more than a list of pros and cons.", trait="Rationality", color_name="Blue", hex_color="#2563EB", intensity="low"),
    Question(id=10, text="I find a strict daily routine suffocating rather than helpful.", trait="Stability", color_name="Orange", hex_color="#EA580C", intensity="medium"),
]

MOCK_USERS = [
    {"name": "Alex Rivera", "res": {1:4, 2:5, 3:4, 4:4, 5:2, 6:2, 7:5, 8:4, 9:2, 10:4}},
    {"name": "Sam Chen", "res": {1:5, 2:4, 3:5, 4:3, 5:2, 6:2, 7:4, 8:5, 9:3, 10:5}},
    {"name": "Jordan Taylor", "res": {1:3, 2:3, 3:3, 4:4, 5:4, 6:3, 7:3, 8:3, 9:2, 10:2}},
]

ANSWER_OPTIONS = {1: "Strongly Disagree", 2: "Disagree", 3: "Neutral", 4: "Agree", 5: "Strongly Agree"}

# ============================================================================
# CORE LOGIC
# ============================================================================

def calculate_saturation(answer, intensity):
    ext = abs(answer - 3) / 2
    base = {'high': 0.5, 'medium': 0.6, 'low': 0.7}.get(intensity, 0.6)
    return base + (ext * (1 - base))

def hex_to_rgb(hex_c, sat):
    hex_c = hex_c.lstrip('#')
    r, g, b = [int(hex_c[i:i+2], 16)/255 for i in (0, 2, 4)]
    gray = (r + g + b) / 3
    return (gray + sat * (r - gray), gray + sat * (g - gray), gray + sat * (b - gray))

def generate_barcode(responses):
    fig = Figure(figsize=(12, 2), facecolor='#0a0a0a')
    ax = fig.add_subplot(111); ax.set_xlim(0, 10); ax.set_ylim(0, 1); ax.axis('off')
    for i, q in enumerate(QUESTIONS):
        if q.id in responses:
            color = hex_to_rgb(q.hex_color, calculate_saturation(responses[q.id], q.intensity))
            ax.add_patch(mpatches.Rectangle((i, 0), 1, 1, facecolor=color))
    return fig

def get_similarity(v1, v2):
    return (1 - (np.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2))) / np.sqrt(10))) * 100

# ============================================================================
# UI COMPONENTS
# ============================================================================

def main():
    st.set_page_config(page_title="BluPr", page_icon="🧬", layout="centered")
    st.markdown("<style>.stApp { background-color: #0a0a0a; color: #ffffff; } .stButton>button { width: 100%; border-radius: 8px; font-weight: 600; }</style>", unsafe_allow_html=True)
    
    if 'responses' not in st.session_state: st.session_state.responses = {}
    if 'survey_completed' not in st.session_state: st.session_state.survey_completed = False
    if 'current_question' not in st.session_state: st.session_state.current_question = 0
    if 'saved' not in st.session_state: st.session_state.saved = False

    st.title("🧬 BluPr")
    st.markdown("*Your Belief Blueprint.*")
    
    if not st.session_state.survey_completed:
        render_survey()
    else:
        render_results()

def render_survey():
    q = QUESTIONS[st.session_state.current_question]
    st.progress((len(st.session_state.responses) / 10))
    st.markdown(f"### {q.text}")
    ans = st.radio("Response:", list(ANSWER_OPTIONS.keys()), format_func=lambda x: ANSWER_OPTIONS[x], key=f"q_{q.id}")
    st.session_state.responses[q.id] = ans
    
    c1, _, c3 = st.columns([1,1,1])
    if st.session_state.current_question > 0:
        if c1.button("← Back"): st.session_state.current_question -= 1; st.rerun()
    if st.session_state.current_question < 9:
        if c3.button("Next →"): st.session_state.current_question += 1; st.rerun()
    else:
        name = st.text_input("Name for your BluPr:")
        if c3.button("Generate") and name:
            st.session_state.user_name = name; st.session_state.survey_completed = True; st.rerun()

def render_results():
    st.markdown(f"## {st.session_state.user_name}'s BluPr")
    st.pyplot(generate_barcode(st.session_state.responses))
    
    if not st.session_state.saved:
        save_user_data(st.session_state.user_name, st.session_state.responses, "The Vanguard")
        st.session_state.saved = True
        st.toast("BluPr saved! 🚀")

    st.divider()
    
    # --- NEW: SHARE SECTION ---
    st.markdown("### 📢 Share your BluPr")
    share_text = f"I just generated my belief blueprint on BluPr! My thinking is unique. Generate yours here: {st.query_params.get('app_url', 'https://blupr.streamlit.app')}"
    encoded_text = urllib.parse.quote(share_text)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'''<a href="https://wa.me/?text={encoded_text}" target="_blank"><button style="width:100%; border-radius:8px; padding:10px; background-color:#25D366; color:white; border:none; cursor:pointer; font-weight:bold;">Share on WhatsApp</button></a>''', unsafe_allow_html=True)
    with col2:
        st.markdown(f'''<a href="https://twitter.com/intent/tweet?text={encoded_text}" target="_blank"><button style="width:100%; border-radius:8px; padding:10px; background-color:#1DA1F2; color:white; border:none; cursor:pointer; font-weight:bold;">Share on X</button></a>''', unsafe_allow_html=True)
    
    st.divider()
    if st.button("Start New BluPr"):
        st.session_state.responses = {}; st.session_state.survey_completed = False; st.session_state.current_question = 0; st.session_state.saved = False; st.rerun()

if __name__ == "__main__":
    main()
