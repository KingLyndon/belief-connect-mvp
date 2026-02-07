import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.figure import Figure
import numpy as np
import bcrypt
import pandas as pd
from datetime import datetime, timedelta
from supabase import create_client
import io
import urllib.parse

# ============================================================================
# 1. CORE CONFIGURATION & STYLING
# ============================================================================
URL = "https://rinbuwveuurjrzqijiai.supabase.co"
KEY = "sb_publishable_rcamFVqYmdrLgnKtq_Or2Q_ojNXBJTg"
supabase = create_client(URL, KEY)

def apply_futuristic_theme():
    st.markdown(f"""
        <style>
        /* Base Theme */
        .stApp {{
            background-color: #000000;
            color: #FFFFFF;
            font-family: 'Inter', sans-serif;
        }}
        
        /* Branding Section */
        .logo-text {{
            font-family: 'Orbitron', sans-serif;
            font-size: 80px;
            font-weight: 900;
            background: -webkit-linear-gradient(#FFFFFF, #FF2D55);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: 15px;
            text-align: center;
            margin-bottom: 0px;
        }}
        
        .tagline {{
            color: #FF2D55;
            text-align: center;
            letter-spacing: 3px;
            font-size: 12px;
            text-transform: uppercase;
            margin-top: -20px;
            margin-bottom: 40px;
        }}

        /* Futuristic Cards */
        .glass-card {{
            background: rgba(255, 45, 85, 0.05);
            border: 1px solid rgba(255, 45, 85, 0.2);
            border-radius: 20px;
            padding: 25px;
            margin-bottom: 20px;
        }}

        /* Inputs and Buttons */
        .stTextInput>div>div>input {{
            background-color: #000000;
            color: white;
            border: 1px solid #333;
            border-radius: 10px;
        }}
        
        .stButton>button {{
            background-color: transparent;
            color: #FF2D55;
            border: 1px solid #FF2D55;
            border-radius: 50px;
            height: 3.5em;
            transition: all 0.3s ease;
            width: 100%;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-size: 14px;
        }}
        
        .stButton>button:hover {{
            background-color: #FF2D55;
            color: white;
            box-shadow: 0 0 20px rgba(255, 45, 85, 0.4);
        }}
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {{
            background-color: #050505;
            border-right: 1px solid #222;
        }}
        
        .share-btn {{
            text-decoration: none;
            color: white;
            background: #FF2D55;
            padding: 12px;
            border-radius: 10px;
            display: block;
            text-align: center;
            margin-bottom: 10px;
            font-weight: bold;
        }}
        </style>
    """, unsafe_allow_html=True)

# ============================================================================
# 2. SECURITY & DATA UTILS
# ============================================================================
def hash_pw(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_pw(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# 40 Questions Engine
QUESTIONS = [
    {"id": 1, "text": "Absolute freedom is more valuable than communal harmony.", "trait": "Liberty", "color": "#FF2D55"},
    {"id": 2, "text": "I value high-stakes leadership over comfortable cooperation.", "trait": "Ambition", "color": "#FF79C6"},
    {"id": 3, "text": "The unknown is a playground, not a threat.", "trait": "Change", "color": "#BD93F9"},
    {"id": 4, "text": "Logic must prevail even when it hurts.", "trait": "Rationality", "color": "#8BE9FD"},
    {"id": 5, "text": "Stability is a cage, not a foundation.", "trait": "Stability", "color": "#50FA7B"},
    # ... Imagine 35 more questions here following this traits/color logic
]
# Fill remaining 35 questions programmatically for MVP
for i in range(6, 41):
    QUESTIONS.append({"id": i, "text": f"Deeper psychometric insight regarding {QUESTIONS[i%5]['trait']} #{i}", "trait": QUESTIONS[i%5]['trait'], "color": QUESTIONS[i%5]['color']})

# ============================================================================
# 3. VISUALIZATION: THE VERTICAL BLUPR
# ============================================================================
def generate_vertical_blupr(responses_df):
    # Fixed vertical aspect ratio for Story sharing (9:16)
    fig = Figure(figsize=(5, 8.8), facecolor='#000000')
    ax = fig.add_subplot(111)
    ax.set_ylim(0, len(responses_df))
    ax.set_xlim(0, 1)
    ax.axis('off')
    
    for i, row in responses_df.iterrows():
        q_data = next((q for q in QUESTIONS if q["id"] == row['question_id']), {"color": "#FF2D55"})
        # Intensity logic for Peaceful/Futuristic Pink tones
        sat = 0.4 + (abs(row['score'] - 3) / 2) * 0.6
        hex_c = q_data['color'].lstrip('#')
        r, g, b = [int(hex_c[j:j+2], 16)/255 for j in (0, 2, 4)]
        gray = (r + g + b) / 3
        color = (gray + sat * (r - gray), gray + sat * (g - gray), gray + sat * (b - gray))
        
        ax.add_patch(mpatches.Rectangle((0, i), 1, 1, facecolor=color))
    return fig

# ============================================================================
# 4. APP STAGES
# ============================================================================
def main():
    apply_futuristic_theme()
    
    if 'user' not in st.session_state:
        show_auth()
    else:
        # Check if onboarding (initial 10) is complete
        ans = supabase.table("daily_responses").select("*").eq("user_email", st.session_state.user['email']).execute()
        ans_df = pd.DataFrame(ans.data)
        
        if len(ans_df) < 10:
            show_onboarding(ans_df)
        else:
            show_dashboard(ans_df)

def show_auth():
    st.markdown('<p class="logo-text">BluPr</p>', unsafe_allow_html=True)
    st.markdown('<p class="tagline">The Blueprint of your Mind</p>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["EXISTING USER", "NEW IDENTITY"])
    
    with tab1:
        email = st.text_input("Email", key="l_email")
        pw = st.text_input("Password", type="password", key="l_pw")
        if st.button("Access BluPr"):
            user = supabase.table("users").select("*").eq("email", email).execute()
            if user.data and check_pw(pw, user.data[0]['password_hash']):
                st.session_state.user = user.data[0]
                st.rerun()
            else: st.error("Blueprint match failed.")

    with tab2:
        name = st.text_input("Display Name", key="s_name")
        email = st.text_input("Email ID", key="s_email")
        pw = st.text_input("Secret Password", type="password", key="s_pw")
        if st.button("Commence"):
            h_pw = hash_pw(pw)
            try:
                supabase.table("users").insert({"email": email, "password_hash": h_pw, "display_name": name, "clan_name": "Neutral"}).execute()
                st.success("Identity established. Please Login.")
            except: st.error("Identity already exists.")

def show_onboarding(ans_df):
    q_idx = len(ans_df)
    q = QUESTIONS[q_idx]
    st.markdown(f"### INITIALIZATION PHASE {q_idx + 1}")
    st.progress((q_idx + 1) / 10)
    
    st.markdown(f"## {q['text']}")
    score = st.select_slider("Intensity", options=[1,2,3,4,5], value=3)
    
    if st.button("SYNC"):
        supabase.table("daily_responses").insert({"user_email": st.session_state.user['email'], "question_id": q['id'], "score": score}).execute()
        st.rerun()

def show_dashboard(ans_df):
    user = st.session_state.user
    st.sidebar.markdown(f"<h1 style='color:#FF2D55;'>BluPr</h1>", unsafe_allow_html=True)
    nav = st.sidebar.radio("CHAMBER", ["Identity", "Clan Hub", "Twin Chamber"])

    if nav == "Identity":
        st.markdown(f"### Welcome back, {user['display_name']}")
        
        # Check for Daily Pulse (3 Qs)
        today = datetime.now().date()
        todays_ans = ans_df[pd.to_datetime(ans_df['answered_at']).dt.date == today]
        
        if len(todays_ans) < 3:
            st.markdown('<div class="glass-card"><h4>DAILY PULSE</h4>', unsafe_allow_html=True)
            q_idx = len(ans_df)
            q = QUESTIONS[q_idx]
            st.write(q['text'])
            score = st.slider("Response", 1, 5, 3)
            if st.button("PULSE CHECK"):
                supabase.table("daily_responses").insert({"user_email": user['email'], "question_id": q['id'], "score": score}).execute()
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Display Vertical Barcode
        fig = generate_vertical_blupr(ans_df)
        st.pyplot(fig)
        
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches='tight', pad_inches=0, transparent=False)
        st.download_button("DOWNLOAD STORY IMAGE", buf.getvalue(), "my_blupr.png", "image/png")

    elif nav == "Clan Hub":
        st.header(f"CLAN: VANGUARD")
        tab1, tab2 = st.tabs(["The Wall", "Shared Recs"])
        
        with tab1:
            st.markdown('<div class="glass-card"><b>Wall Poll:</b> Should the Clan move toward a decentralised leadership?</div>', unsafe_allow_html=True)
            st.button("AGREE")
            st.button("DISAGREE")
            
        with tab2:
            st.write("Top Affinity for your Clan:")
            col1, col2 = st.columns(2)
            with col1: st.button("👍 Movie: Ex Machina")
            with col2: st.button("👍 Book: Zero to One")

    elif nav == "Twin Chamber":
        st.header("TWIN SYNC")
        # Similarity Math (Euclidean Distance on last 10)
        st.markdown('<div class="glass-card">Searching for 90%+ Blueprint similarities...</div>', unsafe_allow_html=True)
        
        # Simulated Twin
        st.markdown(f"""
            <div style="padding:15px; border-left: 2px solid #FF2D55; background: #111;">
                <b>Twin: Riley</b> | 92.4% Match<br>
                <span style="color:#FF2D55;">⚠️ Losing connection in 2d 14h 32m</span>
            </div>
        """, unsafe_allow_html=True)
        st.text_input("Send Sync Message...")

if __name__ == "__main__":
    main()
