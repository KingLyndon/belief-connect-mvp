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

# --- CUSTOM CSS & JS INJECTION (NEURAL ANTIGRAVITY) ---
def inject_neural_interface():
    # CSS: OLED Black, Floating Cards, Neon Accents
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;500;700&display=swap');

        /* APP CONTAINER CLEANUP */
        .stApp {
            background-color: #000000;
            color: #E0E0E0;
            font-family: 'Rajdhani', sans-serif;
        }
        header, footer {
            visibility: hidden;
        }
        
        /* TYPOGRAPHY */
        h1, h2, h3 {
            font-family: 'Orbitron', 'sans-serif';
            color: #FFB6C1; /* Neural Pink */
            text-shadow: 0 0 10px rgba(255, 182, 193, 0.7);
        }
        p, div, label, span {
            color: #CCCCCC;
        }

        /* FLOATING CARDS (ANTIGRAVITY FEEL) */
        .floating-card {
            background: rgba(20, 20, 30, 0.6);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 182, 193, 0.2);
            border-radius: 15px;
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
            animation: float 6s ease-in-out infinite;
        }

        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0px); }
        }

        /* INPUTS & BUTTONS */
        .stTextInput > div > div > input {
            background-color: rgba(0, 0, 0, 0.5);
            color: #FFB6C1;
            border: 1px solid #FF2D55;
            border-radius: 8px;
        }
        .stButton > button {
            background: linear-gradient(135deg, #FF2D55 0%, #000000 100%);
            color: white;
            border: 1px solid #FFB6C1;
            border-radius: 20px;
            padding: 0.5rem 2rem;
            font-family: 'Orbitron', sans-serif;
            text-transform: uppercase;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            box-shadow: 0 0 15px #FF2D55;
            transform: scale(1.05);
            border-color: #FFFFFF;
        }
        
        /* PROGRESS BAR */
        .stProgress > div > div > div > div {
            background-color: #FF2D55;
        }

        </style>
    """, unsafe_allow_html=True)

    # JS: Neural Web Canvas (Particle Network)
    # Using a simple script directly in HTML component for self-containment
    components.html("""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { margin: 0; overflow: hidden; background: transparent; }
            canvas { display: block; }
        </style>
    </head>
    <body>
        <canvas id="neuralCanvas"></canvas>
        <script>
            const canvas = document.getElementById('neuralCanvas');
            const ctx = canvas.getContext('2d');
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;

            let particlesArray;
            const mouse = { x: null, y: null, radius: 150 };

            window.addEventListener('mousemove', function(event) {
                mouse.x = event.x;
                mouse.y = event.y;
            });

            class Particle {
                constructor(x, y, loading) {
                    this.x = x;
                    this.y = y;
                    this.size = Math.random() * 2 + 1;
                    this.baseX = this.x;
                    this.baseY = this.y;
                    let speed = (Math.random() * 0.5) + 0.2; // Slow float
                    
                    // Simulate moving forward tunnel effect simply by spreading from center if needed
                    // For now, gentle drift
                    this.density = (Math.random() * 30) + 1;
                    this.loading = loading; 
                }
                draw() {
                    ctx.fillStyle = '#FFB6C1';
                    ctx.beginPath();
                    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                    ctx.closePath();
                    ctx.fill();
                }
                update() {
                    let dx = mouse.x - this.x;
                    let dy = mouse.y - this.y;
                    let distance = Math.sqrt(dx * dx + dy * dy);
                    let forceDirectionX = dx / distance;
                    let forceDirectionY = dy / distance;
                    let maxDistance = mouse.radius;
                    let force = (maxDistance - distance) / maxDistance;
                    let directionX = forceDirectionX * force * this.density;
                    let directionY = forceDirectionY * force * this.density;

                    if (distance < mouse.radius) {
                        this.x -= directionX;
                        this.y -= directionY;
                    } else {
                        if (this.x !== this.baseX) {
                            let dx = this.x - this.baseX;
                            this.x -= dx/10;
                        }
                        if (this.y !== this.baseY) {
                            let dy = this.y - this.baseY;
                            this.y -= dy/10;
                        }
                    }
                    this.draw();
                }
            }

            function init() {
                particlesArray = [];
                let numberOfParticles = (canvas.height * canvas.width) / 9000;
                for (let i = 0; i < numberOfParticles; i++) {
                    let x = Math.random() * canvas.width;
                    let y = Math.random() * canvas.height;
                    particlesArray.push(new Particle(x, y));
                }
            }

            function connect() {
                let opacityValue = 1;
                for (let a = 0; a < particlesArray.length; a++) {
                    for (let b = a; b < particlesArray.length; b++) {
                        let distance = ((particlesArray[a].x - particlesArray[b].x) * (particlesArray[a].x - particlesArray[b].x)) + 
                                       ((particlesArray[a].y - particlesArray[b].y) * (particlesArray[a].y - particlesArray[b].y));
                        if (distance < (canvas.width/7) * (canvas.height/7)) {
                            opacityValue = 1 - (distance/20000);
                            ctx.strokeStyle = 'rgba(255, 182, 193,' + opacityValue + ')';
                            ctx.lineWidth = 1;
                            ctx.beginPath();
                            ctx.moveTo(particlesArray[a].x, particlesArray[a].y);
                            ctx.lineTo(particlesArray[b].x, particlesArray[b].y);
                            ctx.stroke();
                        }
                    }
                }
            }

            function animate() {
                requestAnimationFrame(animate);
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                for (let i = 0; i < particlesArray.length; i++) {
                    particlesArray[i].update();
                }
                connect();
            }

            init();
            animate();
            
            window.addEventListener('resize',  function() {
                canvas.width = window.innerWidth;
                canvas.height = window.innerHeight;
                init();
            });
        </script>
    </body>
    </html>
    """, height=0, scrolling=False) # Height 0 prevents layout shift, fixed pos handles bg

    # Hack to make the iframe fullscreen background
    st.markdown("""
        <style>
        iframe[title="streamlit.components.v1.html"] {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: -1;
        }
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
            # Fallback for UI testing without creds, though functionality will limit
            # st.error("Supabase credentials not found in .streamlit/secrets.toml")

    def sign_in(self, email, password):
        if not self.connected: 
            # Mock for testing UI if no DB
            if email == "demo@blupr.io": return {"user": {"id": "demo", "email": email}, "error": None}
            return {"user": None, "error": "Database not connected"}
        try:
            res = self.client.auth.sign_in_with_password({"email": email, "password": password})
            return {"user": res.user, "error": None}
        except Exception as e:
            return {"user": None, "error": str(e)}

    def sign_up(self, email, password, name):
        if not self.connected:
             return {"user": None, "error": "Database not connected"}
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
        if not self.connected: return np.random.rand(10).tolist() # Mock
        try:
            res = self.client.table("responses").select("*").eq("user_id", user_id).execute()
            # Convert to list ordered by index
            data = res.data
            # We assume 10 questions for MVP simple vector
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
            # Return some mock vectors
            return [
                {"user_id": "mock1", "vector": np.random.rand(10).tolist()},
                {"user_id": "mock2", "vector": np.random.rand(10).tolist()}
            ]
        try:
            # This is expensive in real prod, but fine for MVP
            # Fetch all responses
            res = self.client.table("responses").select("*").execute()
            data = res.data
            
            # Group by user
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
    st.markdown("<div class='floating-card' style='text-align: center;'><h1>BluPr</h1><p>Belief Blueprint</p></div>", unsafe_allow_html=True)
    
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
        st.markdown(f"<div class='floating-card'><h2>Link Sequence {step+1}/{len(questions)}</h2><h1>{questions[step]}</h1></div>", unsafe_allow_html=True)
        
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
        st.markdown("<div class='floating-card'><h4>Clan: The Void Walkers</h4><p>Seekers of the digital infinite.</p></div>", unsafe_allow_html=True)
        
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
