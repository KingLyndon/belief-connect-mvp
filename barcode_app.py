import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw
import time
import math
import hashlib
from datetime import datetime
# --- CONFIGURATION ---
st.set_page_config(
    page_title="BluPr | Belief Blueprint",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)
# --- CUSTOM CSS & JS INJECTION (NEURAL ANTIGRAVITY v2.0) ---
def inject_neural_interface():
    # CSS: ANTIGRAVITY AESTHETIC (Space Grotesk + Inter)
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Space+Grotesk:wght@300;500;700&display=swap');
        /* RESET & BASE */
        .stApp {
            background-color: #000000;
            font-family: 'Inter', sans-serif;
            color: #E0E0E0;
        }
        
        /* HIDE STREAMLIT CHROME */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        /* TYPOGRAPHY */
        h1, h2, h3, h4, .big-font {
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            color: #FFFFFF;
            letter-spacing: -0.02em;
        }
        h1 {
            font-size: 3.5rem !important;
            background: linear-gradient(90deg, #FFFFFF, #FFB6C1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 30px rgba(255, 45, 85, 0.3);
        }
        p, div, label {
            color: #AAAAAA;
            font-weight: 300;
        }
        /* GLASS CONTAINERS */
        .glass-panel {
            background: rgba(10, 10, 10, 0.6);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 24px;
            padding: 2.5rem;
            box-shadow: 0 20px 50px rgba(0,0,0, 0.5);
            transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        .glass-panel:hover {
            transform: translateY(-5px);
            border-color: rgba(255, 45, 85, 0.3);
            box-shadow: 0 30px 60px rgba(255, 45, 85, 0.1);
        }
        /* INPUT FIELDS */
        .stTextInput > div > div {
            background-color: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            color: white;
            transition: all 0.3s ease;
        }
        .stTextInput > div > div:focus-within {
            border-color: #FF2D55;
            box-shadow: 0 0 15px rgba(255, 45, 85, 0.2);
            background-color: rgba(255, 255, 255, 0.05);
        }
        .stTextInput input {
            color: white !important;
        }
        /* BUTTONS - NEON PILLS */
        .stButton > button {
            background: #FFFFFF;
            color: #000000;
            border: none;
            border-radius: 100px;
            padding: 0.75rem 2.5rem;
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            font-size: 1rem;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
            box-shadow: 0 0 20px rgba(255, 255, 255, 0.2);
        }
        .stButton > button:hover {
            background: #FF2D55;
            color: #FFFFFF;
            box-shadow: 0 0 40px rgba(255, 45, 85, 0.6);
            transform: scale(1.05);
        }
        .stButton > button:active {
            transform: scale(0.98);
        }
        /* SLIDER */
        .stSlider > div > div > div > div {
            background-color: #FF2D55;
        }
        /* CUSTOM METRICS */
        .stMetric label {
            color: #888;
        }
        .stMetric .css-1wivap2 {
            font-family: 'Space Grotesk';
            color: #FFB6C1;
            text-shadow: 0 0 10px rgba(255, 45, 85, 0.5);
        }
        
        </style>
    """, unsafe_allow_html=True)
    # JS: ADVANCED NEURAL WEB (LIVE WALLPAPER)
    components.html("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <style>
            body { margin: 0; overflow: hidden; background: #000000; }
            canvas { display: block; }
        </style>
    </head>
    <body>
        <canvas id="neural-canvas"></canvas>
        <script>
            /**
             * NEURAL ANTIGRAVITY ENGINE
             * 
             * Simulates a living neural network floating in zero gravity.
             * Reacts to mouse proximity ("Synaptic Excitation").
             */
            
            const canvas = document.getElementById('neural-canvas');
            const ctx = canvas.getContext('2d');
            
            let width, height;
            let particles = [];
            
            // CONFIGURATION (THE BRAIN PARAMETERS)
            const config = {
                particleCount: 130,
                connectionDistance: 140,
                mouseRadius: 200,
                baseColor: { r: 255, g: 45, b: 85 }, // #FF2D55
                secondaryColor: { r: 255, g: 255, b: 255 },
                speed: 0.4
            };
            const mouse = { x: -1000, y: -1000 };
            class Nueron {
                constructor() {
                    this.init();
                }
                init() {
                    this.x = Math.random() * width;
                    this.y = Math.random() * height;
                    this.vx = (Math.random() - 0.5) * config.speed;
                    this.vy = (Math.random() - 0.5) * config.speed;
                    this.size = Math.random() * 2 + 1; // 1-3px
                    this.life = Math.random(); // Phase for pulsing
                }
                update() {
                    // Move
                    this.x += this.vx;
                    this.y += this.vy;
                    // Pulse size
                    this.life += 0.01;
                    const pulse = Math.sin(this.life) * 0.5 + 1;
                    // Mouse Interaction (Antigravity Push/Pull)
                    // We want a "flow" effect. Mouse attracts slightly, then swirls.
                    const dx = mouse.x - this.x;
                    const dy = mouse.y - this.y;
                    const dist = Math.sqrt(dx*dx + dy*dy);
                    
                    if (dist < config.mouseRadius) {
                        const force = (config.mouseRadius - dist) / config.mouseRadius;
                        // Gentle attraction
                        this.vx += (dx / dist) * force * 0.05;
                        this.vy += (dy / dist) * force * 0.05;
                    }
                    // Boundaries (Wrap around for infinite feeling)
                    if (this.x < 0) this.x = width;
                    if (this.x > width) this.x = 0;
                    if (this.y < 0) this.y = height;
                    if (this.y > height) this.y = 0;
                    // Draw Nucleus
                    ctx.beginPath();
                    ctx.arc(this.x, this.y, this.size * pulse, 0, Math.PI*2);
                    ctx.fillStyle = `rgba(${config.baseColor.r}, ${config.baseColor.g}, ${config.baseColor.b}, 0.8)`;
                    ctx.fill();
                }
            }
            function init() {
                width = window.innerWidth;
                height = window.innerHeight;
                canvas.width = width;
                canvas.height = height;
                
                particles = [];
                // Dynamic count based on screen area
                const count = Math.floor((width * height) / 10000); 
                for(let i=0; i<count; i++) {
                    particles.push(new Nueron());
                }
            }
            function drawConnections() {
                for(let i=0; i<particles.length; i++) {
                    for(let j=i+1; j<particles.length; j++) {
                        const p1 = particles[i];
                        const p2 = particles[j];
                        
                        const dx = p1.x - p2.x;
                        const dy = p1.y - p2.y;
                        const dist = Math.sqrt(dx*dx + dy*dy);
                        if (dist < config.connectionDistance) {
                            const opacity = 1 - (dist / config.connectionDistance);
                            
                            ctx.beginPath();
                            ctx.moveTo(p1.x, p1.y);
                            ctx.lineTo(p2.x, p2.y);
                            
                            // Gradient for synapse
                            const grad = ctx.createLinearGradient(p1.x, p1.y, p2.x, p2.y);
                            grad.addColorStop(0, `rgba(${config.baseColor.r}, ${config.baseColor.g}, ${config.baseColor.b}, ${opacity * 0.4})`);
                            grad.addColorStop(1, `rgba(${config.secondaryColor.r}, ${config.secondaryColor.g}, ${config.secondaryColor.b}, ${opacity * 0.2})`);
                            
                            ctx.strokeStyle = grad;
                            ctx.lineWidth = opacity * 1.5;
                            ctx.stroke();
                        }
                    }
                }
            }
            function animate() {
                ctx.clearRect(0, 0, width, height);
                
                particles.forEach(p => p.update());
                drawConnections();
                
                requestAnimationFrame(animate);
            }
            // Events
            window.addEventListener('resize', init);
            window.addEventListener('mousemove', e => {
                mouse.x = e.clientX;
                mouse.y = e.clientY;
            });
            window.addEventListener('touchmove', e => {
                mouse.x = e.touches[0].clientX;
                mouse.y = e.touches[0].clientY;
            });
            // Start
            init();
            animate();
        </script>
    </body>
    </html>
    """, height=0, scrolling=False)
    # Fullscreen Background Iframe Hack
    st.markdown("""
        <style>
        iframe[title="streamlit.components.v1.html"] {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: -1;
            pointer-events: none; /* Let clicks pass through to app, but listener in iframe still works via mousemove if adjusted... actually pointer-events:none kills interaction. We need a different approach. */
        }
        /* To allow canvas interaction, we need pointer-events: auto on the iframe but it might block Streamlit UI. 
           Solution: Send mouse events from Streamlit to iframe? Hard.
           Better: Make iframe fullscreen with z-index -1. 
           In Streamlit, iframes swallow events. 
           We will set pointer-events: none on the iframe container, ensuring visual only.
           But user wanted "follow user". 
           Actually, if z-index is -1, the body (Streamlit) is on top. 
           The iframe won't get mouse events. 
           We can TRY to use a specialized Component or just accept visual ambience for now.
           OR: We can use 'mix-blend-mode' hacks.
           
           Reverting to visual-only dynamic background (it has internal drift).
        */
        </style>
    """, unsafe_allow_html=True)
# --- SUPABASE MANAGER ---
from supabase import create_client, Client
class SupabaseManager:
    def __init__(self):
        try:
            url = st.secrets["SUPABASE_URL"]
            key = st.secrets["SUPABASE_KEY"]
            self.client: Client = create_client(url, key)
            self.connected = True
        except Exception as e:
            self.connected = False
            # Demo Mode active
    def sign_in(self, email, password):
        if not self.connected: 
            # DEMO MODE
            return {"user": {"id": "demo_user", "email": email}, "error": None}
        try:
            res = self.client.auth.sign_in_with_password({"email": email, "password": password})
            return {"user": res.user, "error": None}
        except Exception as e:
            return {"user": None, "error": str(e)}
    def sign_up(self, email, password, name):
        if not self.connected:
             # DEMO MODE
             return {"user": {"id": "demo_user", "email": email}, "error": None}
        try:
            res = self.client.auth.sign_up({"email": email, "password": password, "options": {"data": {"name": name}}})
            return {"user": res.user, "error": None}
        except Exception as e:
            return {"user": None, "error": str(e)}
    def save_response(self, user_id, question_index, value):
        if not self.connected: return
        # Table: responses (user_id, question_index, value, created_at)
        # Using upsert to handle updates if re-answered
        data = {
            "user_id": user_id,
            "question_index": question_index,
            "value": value,
            "updated_at": datetime.now().isoformat()
        }
        try:
            self.client.table("responses").upsert(data).execute()
        except Exception as e:
            st.error(f"Error saving: {e}")
    def get_user_responses(self, user_id):
        if not self.connected: 
            # Return demo vector or random if empty
            return np.random.rand(10).tolist()
        try:
            res = self.client.table("responses").select("*").eq("user_id", user_id).execute()
            data = res.data
            vector = [0.5] * 10
            for item in data:
                idx = item.get('question_index')
                if idx < 10:
                    vector[idx] = item.get('value')
            return vector
        except Exception as e:
            return [0.5] * 10
    def get_all_vectors(self):
        if not self.connected: 
            # Demo Pool
            return [
                {"user_id": "demo1", "vector": np.random.rand(10).tolist()},
                {"user_id": "demo2", "vector": np.random.rand(10).tolist()},
                {"user_id": "demo3", "vector": np.random.rand(10).tolist()}
            ]
        try:
            res = self.client.table("responses").select("*").execute()
            data = res.data
            users = {}
            for item in data:
                uid = item['user_id']
                if uid not in users: users[uid] = [0.5]*10
                idx = item['question_index']
                if idx < 10: users[uid][idx] = item['value']
            return [{"user_id": k, "vector": v} for k,v in users.items()]
        except Exception as e:
            return []
# --- APP STATE & LOGIC ---
if 'app_state' not in st.session_state:
    st.session_state.app_state = 'LOGIN' 
if 'user' not in st.session_state:
    st.session_state.user = None
if 'user_vector' not in st.session_state:
    st.session_state.user_vector = []
if 'onboarding_step' not in st.session_state:
    st.session_state.onboarding_step = 0
# --- PAGES ---
def login_page(db):
    st.markdown("<div class='glass-panel' style='text-align: center;'><h1>BluPr</h1><p>Belief Blueprint</p></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Sign In")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Enter the Void"):
            res = db.sign_in(email, password)
            if res['user']:
                st.session_state.user = res['user']
                # Load profile/vector
                uid = res['user'].id if hasattr(res['user'], 'id') else res['user']['id']
                st.session_state.user_vector = db.get_user_responses(uid)
                # Check if onboarding done (simple check: if vector has variance or stored flag)
                # For MVP, if vector is default (all 0.5 presumably) we might show onboarding, 
                # but let's assume if they log in they might see dashboard. 
                # Better: Check if they have responses.
                if sum(st.session_state.user_vector) == 5.0 and st.session_state.user_vector[0] == 0.5: # Naive check for "clean" slate
                     st.session_state.app_state = 'ONBOARDING'
                else:
                    st.session_state.app_state = 'DASHBOARD'
                st.rerun()
            else:
                st.error(f"Access Denied: {res['error']}")
    with col2:
        st.markdown("### Join the Neural Web")
        new_email = st.text_input("Email", key="new_email")
        new_name = st.text_input("Codename", key="new_name")
        new_pass = st.text_input("Password", type="password", key="new_pass")
        if st.button("Initiate Link"):
            res = db.sign_up(new_email, new_pass, new_name)
            if res['user']:
                st.session_state.user = res['user']
                st.session_state.user_vector = [0.5]*10
                st.session_state.app_state = 'ONBOARDING'
                st.rerun()
            else:
                st.error(f"Link Failed: {res['error']}")
def onboarding_page(db):
    questions = [
        "Do you believe chaos is essential for order?",
        "Is technology a liberator or a cage?",
        "Does fate exist, or is it all random?",
        "Is true altruism possible?",
        "Should art disturb or comfort?",
        "Is the past more important than the future?",
        "Is solitude strength or weakness?",
        "Do you trust intuition over logic?",
        "Is competition necessary for progress?",
        "Are we alone in the universe?"
    ]
    
    step = st.session_state.onboarding_step
    
    if step < len(questions):
        st.markdown(f"<div class='glass-panel'><h2>Link Sequence {step+1}/{len(questions)}</h2><h1>{questions[step]}</h1></div>", unsafe_allow_html=True)
        
        # Intensity Slider
        val = st.slider("Resonance Intensity", 0.0, 1.0, 0.5, 0.01)
        
        if st.button("Transmit"):
            # Save to local state
            if len(st.session_state.user_vector) <= step:
                st.session_state.user_vector.append(val)
            else:
                 st.session_state.user_vector[step] = val
            
            # Save to DB immediately (progressive)
            user = st.session_state.user
            uid = user.id if hasattr(user, 'id') else user['id']
            db.save_response(uid, step, val)
            
            st.session_state.onboarding_step += 1
            st.rerun()
    else:
        # Done
        st.session_state.app_state = 'DASHBOARD'
        st.rerun()
def generate_barcode_img(vector):
    width = 300
    height = 533 # 9:16
    img = Image.new('RGB', (width, height), color='black')
    draw = ImageDraw.Draw(img)
    
    num_bars = len(vector)
    if num_bars == 0: return img
    bar_height = height / num_bars
    
    for i, val in enumerate(vector):
        r, g, b = 255, 182, 193
        factor = 0.3 + (val * 0.7) 
        color = (int(r*factor), int(g*factor), int(b*factor))
        
        y0 = i * bar_height
        y1 = y0 + bar_height - 4 # spacing
        draw.rectangle([0, y0, width, y1], fill=color)
        
    return img
def calculate_similarity(v1, v2):
    # Euclidean Distance-based similarity
    # Formula: (1 - (dist / sqrt(n))) * 100
    # where vectors are 0-1 normalized
    a = np.array(v1)
    b = np.array(v2)
    n = len(v1)
    dist = np.linalg.norm(a - b)
    max_dist = np.sqrt(n) # max dist if one is all 0s and other all 1s
    similarity = (1 - (dist / max_dist)) * 100
    return max(0, min(100, similarity))
def dashboard_page(db):
    user_vector = st.session_state.user_vector
    
    col_l, col_m, col_r = st.columns([1, 1, 1])
    
    with col_l:
        st.markdown("### Your Barcode")
        st.caption("The visual manifestation of your belief system.")
        img = generate_barcode_img(user_vector)
        st.image(img, use_column_width=True)
        if st.button("Download for Story"):
            st.info("Barcode Image Generated. Long-press or right click to save.")
    with col_m:
        st.markdown("### Twin Chamber")
        
        # Find matches
        others = db.get_all_vectors()
        best_match = None
        best_score = 0
        user = st.session_state.user
        my_uid = user.id if hasattr(user, 'id') else user['id']
        
        for other in others:
            if other['user_id'] != my_uid:
                score = calculate_similarity(user_vector, other['vector'])
                if score > best_score:
                    best_score = score
                    best_match = other
        
        st.metric("Highest Resonance", f"{best_score:.1f}%")
        
        # Visualizing the match or lack thereof
        st.markdown(f"""
        <div style='background:rgba(255,182,193,0.1); padding:1rem; border-radius:10px; border:1px solid #FF2D55;'>
            <h3 style='margin:0'>Status: {'CONNECTED' if best_score >= 90 else 'SEARCHING'}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if best_score >= 90:
            st.success("Twin Connection Active")
            st.balloons()
            if st.button("Enter Twin Sync Portal"):
                st.write("Portal Opening... (Chat Feature v2)")
        else:
            st.warning("Signal Weak. No >90% matches found.")
            # Countdown logic mock
            t = st.empty()
            st.markdown("Resonance fading in:")
            now = datetime.now()
            end_of_day = now.replace(hour=23, minute=59, second=59)
            remaining = end_of_day - now
            st.markdown(f"<h2 style='color:#FF2D55'>{str(remaining).split('.')[0]}</h2>", unsafe_allow_html=True)
    with col_r:
        st.markdown("### Clan Hub")
        st.markdown("<div class='glass-panel'><h4>Clan: The Void Walkers</h4><p>Seekers of the digital infinite.</p></div>", unsafe_allow_html=True)
        
        st.markdown("#### The Wall")
        st.info("Poll: Is consciousness a bug or a feature?")
        c1, c2 = st.columns(2)
        c1.button("Bug (40%)")
        c2.button("Feature (60%)")
        
        st.markdown("#### Recommendations")
        st.markdown("- 📖 *Neuromancer*")
        st.markdown("- 🎬 *Ex Machina*")
        st.markdown("- 🥘 *Ramen (Synthesized)*")
# --- MAIN ---
def main():
    inject_neural_interface()
    db = SupabaseManager()
    
    if st.session_state.app_state == 'LOGIN':
        login_page(db)
    elif st.session_state.app_state == 'ONBOARDING':
        onboarding_page(db)
    elif st.session_state.app_state == 'DASHBOARD':
        dashboard_page(db)
if __name__ == "__main__":
    main()
