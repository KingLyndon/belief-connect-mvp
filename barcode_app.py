import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.figure import Figure
import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Tuple
from supabase import create_client

# ============================================================================
# DATABASE CONNECTION (Supabase)
# ============================================================================
# Updated with your specific project credentials
URL = "https://rinbuwveuurjrzqijiai.supabase.co"
KEY = "sb_publishable_rcamFVqYmdrLgnKtq_Or2Q_ojNXBJTg"
supabase = create_client(URL, KEY)

def save_user_data(name, responses, clan_name):
    """Function to push data to Supabase table 'profiles'"""
    # Convert dictionary responses {1:5, 2:4} into a simple list [5, 4, ...]
    response_list = [responses[i] for i in sorted(responses.keys())]
    
    data = {
        "username": name,
        "responses": response_list,
        "clan_name": clan_name
    }
    try:
        supabase.table("profiles").insert(data).execute()
        return True
    except Exception as e:
        st.error(f"Database Error: {e}")
        return False

# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class Question:
    id: int
    text: str
    trait: str
    color_name: str
    hex_color: str
    intensity: str

@dataclass
class UserProfile:
    name: str
    responses: Dict[int, int]
    barcode_vector: List[float]

# ============================================================================
# CONFIGURATION
# ============================================================================

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
    UserProfile(name="Alex Rivera", responses={1: 4, 2: 5, 3: 4, 4: 4, 5: 2, 6: 2, 7: 5, 8: 4, 9: 2, 10: 4}, barcode_vector=[]),
    UserProfile(name="Sam Chen", responses={1: 5, 2: 4, 3: 5, 4: 3, 5: 2, 6: 2, 7: 4, 8: 5, 9: 3, 10: 5}, barcode_vector=[]),
    UserProfile(name="Jordan Taylor", responses={1: 3, 2: 3, 3: 3, 4: 4, 5: 4, 6: 3, 7: 3, 8: 3, 9: 2, 10: 2}, barcode_vector=[]),
    UserProfile(name="Casey Morgan", responses={1: 2, 2: 2, 3: 2, 4: 5, 5: 5, 6: 4, 7: 2, 8: 2, 9: 1, 10: 1}, barcode_vector=[]),
    UserProfile(name="Riley Park", responses={1: 4, 2: 4, 3: 4, 4: 4, 5: 3, 6: 2, 7: 4, 8: 4, 9: 2, 10: 4}, barcode_vector=[]),
]

ANSWER_OPTIONS = {1: "Strongly Disagree", 2: "Disagree", 3: "Neutral", 4: "Agree", 5: "Strongly Agree"}

# ============================================================================
# CORE FUNCTIONS
# ============================================================================

def calculate_saturation(answer: int, intensity: str) -> float:
    extremity = abs(answer - 3) / 2
    intensity_base = {'high': 0.5, 'medium': 0.6, 'low': 0.7}
    base = intensity_base.get(intensity, 0.6)
    return base + (extremity * (1 - base))

def hex_to_rgb_with_saturation(hex_color: str, saturation: float) -> Tuple[float, float, float]:
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    r, g, b = r/255, g/255, b/255
    gray = (r + g + b) / 3
    r = gray + saturation * (r - gray)
    g = gray + saturation * (g - gray)
    b = gray + saturation * (b - gray)
    return (r, g, b)

def generate_barcode(responses: Dict[int, int]) -> Figure:
    fig = Figure(figsize=(12, 2), facecolor='#0a0a0a')
    ax = fig.add_subplot(111)
    ax.set_xlim(0, len(QUESTIONS))
    ax.set_ylim(0, 1)
    ax.axis('off')
    for i, question in enumerate(QUESTIONS):
        if question.id in responses:
            answer = responses[question.id]
            saturation = calculate_saturation(answer, question.intensity)
            color = hex_to_rgb_with_saturation(question.hex_color, saturation)
            rect = mpatches.Rectangle((i, 0), 1, 1, facecolor=color, edgecolor='none')
            ax.add_patch(rect)
    fig.tight_layout(pad=0)
    return fig

def create_barcode_vector(responses: Dict[int, int]) -> List[float]:
    vector = []
    for question in QUESTIONS:
        if question.id in responses:
            answer = responses[question.id]
            saturation = calculate_saturation(answer, question.intensity)
            value = (answer - 1) / 4 * saturation
            vector.append(value)
        else:
            vector.append(0.5)
    return vector

def calculate_similarity(user1_vector: List[float], user2_vector: List[float]) -> float:
    distance = np.sqrt(sum((a - b) ** 2 for a, b in zip(user1_vector, user2_vector)))
    max_distance = np.sqrt(10)
    return (1 - (distance / max_distance)) * 100

def find_matches(user_responses: Dict[int, int]) -> List[Tuple[UserProfile, float]]:
    user_vector = create_barcode_vector(user_responses)
    matches = []
    for mock_user in MOCK_USERS:
        if not mock_user.barcode_vector:
            mock_user.barcode_vector = create_barcode_vector(mock_user.responses)
        similarity = calculate_similarity(user_vector, mock_user.barcode_vector)
        matches.append((mock_user, similarity))
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches

# ============================================================================
# STREAMLIT UI
# ============================================================================

def apply_dark_mode():
    st.markdown("""
        <style>
        .stApp { background-color: #0a0a0a; color: #ffffff; }
        .stButton>button { background-color: #ffffff; color: #000000; border-radius: 8px; padding: 0.5rem 2rem; }
        .stRadio > label { background-color: #1a1a1a; padding: 1rem; border-radius: 8px; border: 1px solid #333333; margin: 0.5rem 0; cursor: pointer; }
        .match-card { background-color: #1a1a1a; border: 1px solid #333333; border-radius: 12px; padding: 1.5rem; margin: 1rem 0; }
        .clan-badge { background-color: #ffffff; color: #000000; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600; display: inline-block; }
        </style>
    """, unsafe_allow_html=True)

def main():
    apply_dark_mode()
    
    if 'responses' not in st.session_state: st.session_state.responses = {}
    if 'survey_completed' not in st.session_state: st.session_state.survey_completed = False
    if 'current_question' not in st.session_state: st.session_state.current_question = 0
    if 'saved_to_db' not in st.session_state: st.session_state.saved_to_db = False
    
    st.title("🧬 BeliefConnect")
    st.markdown("*Connect with people who think like you*")
    st.markdown("---")
    
    if not st.session_state.survey_completed:
        render_survey()
    else:
        render_results()

def render_survey():
    total_questions = len(QUESTIONS)
    current_idx = st.session_state.current_question
    
    st.progress((len(st.session_state.responses) / total_questions))
    st.caption(f"Question {current_idx + 1} of {total_questions}")
    
    question = QUESTIONS[current_idx]
    st.markdown(f"### {question.text}")
    st.caption(f"*{question.trait}*")
    
    answer = st.radio("Your response:", options=list(ANSWER_OPTIONS.keys()), format_func=lambda x: ANSWER_OPTIONS[x], key=f"q_{question.id}")
    st.session_state.responses[question.id] = answer
    
    col1, _, col3 = st.columns([1, 1, 1])
    with col1:
        if current_idx > 0:
            if st.button("← Previous", use_container_width=True):
                st.session_state.current_question -= 1
                st.rerun()
    with col3:
        if current_idx < total_questions - 1:
            if st.button("Next →", use_container_width=True):
                st.session_state.current_question += 1
                st.rerun()
        else:
            # NEW: Ask for name before finishing
            user_name = st.text_input("Enter your name to join the community:", placeholder="e.g. John Doe")
            if st.button("Finish & See Results", use_container_width=True):
                if user_name:
                    st.session_state.user_name = user_name
                    st.session_state.survey_completed = True
                    st.rerun()
                else:
                    st.warning("Please enter your name to proceed.")

def render_results():
    st.markdown(f"## {st.session_state.user_name}'s Belief Barcode")
    fig = generate_barcode(st.session_state.responses)
    st.pyplot(fig)
    
    # CALCULATE CLAN FOR DATABASE
    matches = find_matches(st.session_state.responses)
    clan_name = "The Vanguard" if matches[0][1] > 85 else "The Hearth"
    
    # NEW: AUTOMATICALLY SAVE TO DATABASE ONCE
    if not st.session_state.saved_to_db:
        with st.spinner("Saving your profile to the cloud..."):
            success = save_user_data(st.session_state.user_name, st.session_state.responses, clan_name)
            if success:
                st.session_state.saved_to_db = True
                st.toast("Profile saved successfully!")

    st.markdown("---")
    clan_matches = [m for m in matches if m[1] >= 90]
    if clan_matches:
        st.markdown("## 🎉 Clan Access Unlocked!")
        st.success(f"You have {len(clan_matches)} high-similarity matches (90%+)")
    
    st.markdown("## Your Matches")
    for user, similarity in matches:
        st.markdown(f"""<div class="match-card"><h3>{user.name}</h3><div style="font-size: 2rem;">{similarity:.1f}%</div></div>""", unsafe_allow_html=True)

    if st.button("Start Over", use_container_width=True):
        st.session_state.responses = {}
        st.session_state.survey_completed = False
        st.session_state.current_question = 0
        st.session_state.saved_to_db = False
        st.rerun()

if __name__ == "__main__":
    st.set_page_config(page_title="BeliefConnect", page_icon="🧬", layout="centered")
    main()
