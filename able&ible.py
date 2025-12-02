import streamlit as st
import google.generativeai as genai
import random
import time
import os

# --- Configuration & Styles ---
st.set_page_config(
    page_title="Trident Word Wizards",
    page_icon="🧙‍♂️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Trident Academy Branding and Activity Specifics
st.markdown("""
<style>
    /* Global Styles & Castle Background */
    .stApp {
        background: linear-gradient(to bottom, #0b1026, #2b32b2); /* Night Sky */
        background-attachment: fixed;
        color: #fff; /* Default text white for contrast */
    }
    
    /* Starry Background Animation (Simple) */
    .stApp:before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 4px),
            radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 3px),
            radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 4px);
        background-size: 550px 550px, 350px 350px, 250px 250px; 
        background-position: 0 0, 40px 60px, 130px 270px;
        z-index: -1;
        opacity: 0.6;
    }

    .main-header {
        font-family: 'Comic Sans MS', 'Comic Sans', cursive;
        color: #FFD700; /* Gold */
        text-align: center;
        font-size: 3.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 3px 3px 0 #000;
    }
    .sub-header {
        color: #E0E0E0;
        text-align: center;
        font-size: 1.3rem;
        margin-bottom: 2rem;
        text-shadow: 1px 1px 2px #000;
    }
    
    /* Default Button Styling (Reset for inner activities) */
    .stButton button {
        background-color: #003366;
        color: white;
        border-radius: 20px;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border: 2px solid #003366;
        transition: transform 0.1s;
    }
    .stButton button:hover {
        background-color: #004080;
        color: #FFCC00;
        transform: scale(1.05);
    }

    /* Primary Button Styling (Check Answer / Next) - Green & Big */
    div.stButton > button[kind="primary"] {
        background-color: #28a745;
        border-color: #28a745;
        color: white;
        font-size: 1.3rem;
        padding: 0.75rem 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #218838;
        border-color: #1e7e34;
        color: white;
        transform: scale(1.05);
        box-shadow: 0 0 15px rgba(40, 167, 69, 0.6);
    }

    /* --- LOGIN SCROLL STYLING --- */
    .scroll-container {
        background-color: #fdfbf7;
        background-image: url("https://www.transparenttextures.com/patterns/aged-paper.png");
        border: 10px solid #d4af37;
        border-radius: 10px 10px 50px 50px; /* Scroll shape approx */
        padding: 3rem;
        text-align: center;
        color: #333;
        box-shadow: 0 0 50px rgba(255, 215, 0, 0.3);
        margin: 2rem auto;
        max-width: 600px;
        position: relative;
    }
    .scroll-container:before, .scroll-container:after {
        content: "";
        position: absolute;
        top: -20px; height: 20px; width: 110%; left: -5%;
        background: #d4af37;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.3);
    }
    .scroll-container:after {
        top: auto; bottom: -20px;
    }

    /* --- Activity 1: Syllable Detective --- */
    [data-testid="stForm"] {
        background-color: #e3f2fd;
        border: 3px dashed #003366;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        color: #333;
    }

    /* --- Activity 2: Word Construction (Updated Design) --- */
    .blueprint-container {
        border: 3px solid #003366;
        background-color: #E3F2FD;
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        position: relative;
        margin-bottom: 2rem;
        box-shadow: 0 4px 0 rgba(0,0,0,0.1);
        color: #333;
    }
    .blueprint-label {
        background-color: #003366;
        color: #FFCC00;
        padding: 5px 15px;
        border-radius: 10px;
        font-weight: bold;
        text-transform: uppercase;
        margin-bottom: 10px;
        display: inline-block;
    }
    .thought-bubble {
        background-color: white;
        border-radius: 30px;
        padding: 15px 30px;
        border: 2px solid #333;
        display: inline-block;
        font-family: 'Comic Sans MS', cursive;
        font-size: 1.5rem;
        position: relative;
        margin-left: 20px;
        color: #333;
    }
    .thought-bubble:before {
        content: "";
        position: absolute;
        top: 50%; left: -12px; margin-top: -6px;
        border-width: 6px 12px 6px 0;
        border-style: solid;
        border-color: transparent #333 transparent transparent;
    }
    .brick-btn-style button {
        background-color: #D2691E !important; 
        color: white !important;
        border: 2px solid #8B4513 !important;
        border-radius: 5px !important;
        font-family: monospace;
        font-size: 1.5rem !important;
        box-shadow: 0px 6px 0px #8B4513 !important;
        margin-bottom: 10px;
        transition: all 0.1s;
    }
    .brick-btn-style button:active {
        box-shadow: 0px 2px 0px #8B4513 !important;
        transform: translateY(4px) !important;
    }
    .assembling-zone {
        border: 4px dashed #555;
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        margin-top: 2rem;
        min-height: 120px;
        color: #333;
    }
    .zone-label { color: #555; font-weight: bold; text-transform: uppercase; margin-bottom: 10px; display: block; letter-spacing: 2px; }
    .built-text { font-family: monospace; font-size: 3rem; color: #003366; letter-spacing: 5px; }
    .construct-btn-container button {
        background-color: #8B4513 !important; color: #FFCC00 !important; font-size: 1.5rem !important;
        border: 3px solid #5A2D0C !important; box-shadow: 0 4px 0 #5A2D0C !important;
    }
    .back-btn-container button {
        background-color: rgba(255,255,255,0.1) !important; color: #fff !important; border: 1px solid #fff !important;
    }

    /* --- Activity 3: Sentence Master --- */
    .sentence-display {
        font-size: 2.5rem !important; font-weight: bold; color: #333; line-height: 1.5; padding: 20px;
        background: white; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;
    }
    .filled-word { color: #28a745; text-decoration: underline; font-weight: 800; }
    .blank-space { color: #FFCC00; text-decoration: underline; font-weight: 800; }
    
    /* --- Activity 4: Antonym Bubbles --- */
    .antonym-clue { font-size: 3rem; font-weight: bold; color: #FFD700; text-align: center; text-shadow: 2px 2px 0 #000; }
    .antonym-answer-box {
        font-size: 3rem; font-weight: bold; color: #28a745; text-align: center; border: 3px solid #28a745;
        border-radius: 15px; padding: 10px; background-color: white; display: inline-block; min-width: 300px;
    }
    .antonym-placeholder {
        font-size: 3rem; color: #ccc; border-bottom: 3px solid #fff; display: inline-block; min-width: 150px; text-align: center;
    }
    
    /* --- Activity 6: Reading --- */
    .story-box {
        background-color: #fff; padding: 2rem; border-radius: 10px; border-left: 10px solid #003366;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1); color: #333;
    }
    .quiz-box {
        background-color: #FFCC00; padding: 2rem; border-radius: 10px; color: #003366;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }

</style>
""", unsafe_allow_html=True)

# --- Gemini Setup ---
api_key = st.secrets.get("API_KEY") or os.environ.get("API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

# --- Constants & Data ---
SYLLABLE_DATA = [
    {"id": 1, "word": "presentable", "correctSyllables": ["pre", "sent", "able"]},
    {"id": 2, "word": "miserable", "correctSyllables": ["mis", "er", "able"]},
    {"id": 3, "word": "valuable", "correctSyllables": ["val", "u", "able"]},
    {"id": 4, "word": "impossible", "correctSyllables": ["im", "poss", "ible"]},
    {"id": 5, "word": "dependable", "correctSyllables": ["de", "pend", "able"]},
    {"id": 6, "word": "reversible", "correctSyllables": ["re", "vers", "ible"]},
    {"id": 7, "word": "favorable", "correctSyllables": ["fa", "vor", "able"]},
]

WORD_BUILDER_DATA = [
    {"id": 1, "parts": ["val", "u", "able"], "meaning": "worth a lot", "targetWord": "valuable"},
    {"id": 2, "parts": ["re", "li", "able"], "meaning": "dependable", "targetWord": "reliable"},
    {"id": 3, "parts": ["in", "cred", "ible"], "meaning": "fantastic", "targetWord": "incredible"},
    {"id": 4, "parts": ["in", "vis", "ible"], "meaning": "not able to be seen", "targetWord": "invisible"},
    {"id": 5, "parts": ["re", "vers", "ible"], "meaning": "able to be turned inside out", "targetWord": "reversible"},
    {"id": 6, "parts": ["re", "mark", "able"], "meaning": "astonishing", "targetWord": "remarkable"},
    {"id": 7, "parts": ["div", "is", "ible"], "meaning": "able to be divided", "targetWord": "divisible"},
]

SENTENCE_DATA = [
    {"id": 1, "sentencePart1": "My grandmother's gold ring cost a lot of money. It is very", "sentencePart2": ".", "options": ["valueless", "valuable"], "correctOption": "valuable"},
    {"id": 2, "sentencePart1": "The sunny weather was", "sentencePart2": "for our picnic, so we had a great time!", "options": ["favored", "favorable"], "correctOption": "favorable"},
    {"id": 3, "sentencePart1": "Dry wood is highly", "sentencePart2": ", so keep it away from the campfire flames.", "options": ["combust", "combustible"], "correctOption": "combustible"},
    {"id": 4, "sentencePart1": "My old car starts every single morning. It is very", "sentencePart2": ".", "options": ["depend", "dependable"], "correctOption": "dependable"},
    {"id": 5, "sentencePart1": "Please comb your hair and tuck in your shirt so you look", "sentencePart2": "for the photo.", "options": ["presented", "presentable"], "correctOption": "presentable"},
    {"id": 6, "sentencePart1": "The number ten is evenly", "sentencePart2": "by the number two.", "options": ["divide", "divisible"], "correctOption": "divisible"},
    {"id": 7, "sentencePart1": "Don't worry about the mess! This marker is", "sentencePart2": "and comes off with soap.", "options": ["wash", "washable"], "correctOption": "washable"},
]

ANTONYM_DATA = [
    {"id": 1, "clue": "Calm and quiet", "answer": "excitable"},
    {"id": 2, "clue": "Crazy", "answer": "sensible"},
    {"id": 3, "clue": "Worthless", "answer": "valuable"},
    {"id": 4, "clue": "Happy", "answer": "miserable"},
    {"id": 5, "clue": "Impossible", "answer": "possible"},
    {"id": 6, "clue": "Cozy", "answer": "uncomfortable"},
    {"id": 7, "clue": "Useless", "answer": "usable"},
]

YES_NO_DATA = [
    {"id": 1, "question": "Can a raincoat be reversible?", "answer": True},
    {"id": 2, "question": "Are most glasses nonbreakable?", "answer": False},
    {"id": 3, "question": "Is fried liver horrible?", "answer": True},
    {"id": 4, "question": "Can a dry forest be combustible?", "answer": True},
    {"id": 5, "question": "Are your grades in school improvable?", "answer": True},
    {"id": 6, "question": "Is your handsome face washable?", "answer": True},
    {"id": 7, "question": "Is a fresh quart of milk returnable?", "answer": False},
]

READING_STORIES = [
    {
        "id": 1,
        "title": "An Unforgettable Cruise",
        "paragraphs": [
            "One hazy day Nancy and her dad were cruising on their 36-foot sailboat on Lake Michigan. The weather report that morning was favorable so they headed for Muskegon.",
            "About noontime the sun disappeared, waves began to roll, and dense fog set in. Three miles offshore, land was suddenly invisible. It was incredible that the weather could be so changeable.",
            "Dad got out his compass and charts and began to take bearings. How far to Muskegon? It was possible that they were fairly close.",
            "Groping their way slowly through the dense fog was miserable. The fog was so thick now you could barely see the bow of the boat. Presently the channel light became visible, and they set their course toward it.",
            "Suddenly a terrible, thunderous sound startled them. Nancy looked up and there, looming behind them in the fog, was the unmistakable shape of a huge steamship. Would the ship see Nancy and her dad in this fog?"
        ],
        "questions": [
            {"question": "What was the weather like when they started?", "options": ["Horrible", "Favorable", "Invisible", "Miserable"], "correctAnswer": "Favorable"},
            {"question": "The land became _______ when the fog set in.", "options": ["Visible", "Invisible", "Changeable", "Unmistakable"], "correctAnswer": "Invisible"},
            {"question": "The sound of the steamship was:", "options": ["Quiet", "Terrible and Thunderous", "Combustible", "Playful"], "correctAnswer": "Terrible and Thunderous"}
        ]
    },
    {
        "id": 2,
        "title": "The Incredible Robot",
        "paragraphs": [
            "Tim decided to build a robot for the school science fair. His friends said it was impossible to build one in just a week, but Tim was a sensible boy who planned ahead.",
            "He used flexible plastic parts so the robot would not be breakable if it fell. The electronic sensors were very valuable, so he handled them with care.",
            "On the day of the fair, the robot worked perfectly! The judges said Tim's invention was remarkable. It could even do the dishes.",
            "Tim felt very capable. Winning the first prize trophy was tangible proof of his hard work."
        ],
        "questions": [
            {"question": "What did Tim's friends think about his plan?", "options": ["It was sensible", "It was impossible", "It was favorable", "It was invisible"], "correctAnswer": "It was impossible"},
            {"question": "Why did Tim use flexible plastic?", "options": ["So it was not breakable", "So it was edible", "So it was miserable", "So it was combustible"], "correctAnswer": "So it was not breakable"},
            {"question": "The judges thought the invention was:", "options": ["Terrible", "Remarkable", "Changeable", "Valueless"], "correctAnswer": "Remarkable"}
        ]
    },
    {
        "id": 3,
        "title": "The Enjoyable Picnic",
        "paragraphs": [
            "The Smith family planned an enjoyable picnic in the park. Mom made sure all the food was edible and tasty.",
            "They brought a big, soft blanket that was very comfortable to sit on. Dad told some terrible jokes that made everyone groan, but they laughed anyway.",
            "Suddenly, it started to rain! They had to be flexible and move the picnic into the car.",
            "Even with the rain, it was a memorable day."
        ],
        "questions": [
            {"question": "The blanket they brought was:", "options": ["Terrible", "Comfortable", "Breakable", "Invisible"], "correctAnswer": "Comfortable"},
            {"question": "How did the family feel about the picnic?", "options": ["It was enjoyable", "It was miserable", "It was horrible", "It was impossible"], "correctAnswer": "It was enjoyable"},
            {"question": "When it rained, the family had to be:", "options": ["Rigid", "Flexible", "Combustible", "Valuable"], "correctAnswer": "Flexible"}
        ]
    }
]

# --- State Management ---
if 'student_name' not in st.session_state:
    st.session_state.student_name = ""
if 'current_activity' not in st.session_state:
    st.session_state.current_activity = None
if 'completed_syllables' not in st.session_state:
    st.session_state.completed_syllables = []
if 'completed_words' not in st.session_state:
    st.session_state.completed_words = []
# Index trackers
if 'sent_index' not in st.session_state:
    st.session_state.sent_index = 0
if 'ant_index' not in st.session_state:
    st.session_state.ant_index = 0
if 'yn_index' not in st.session_state:
    st.session_state.yn_index = 0
if 'reading_story_index' not in st.session_state:
    st.session_state.reading_story_index = 0
if 'reading_quiz_index' not in st.session_state:
    st.session_state.reading_quiz_index = 0
if 'story_is_read' not in st.session_state:
    st.session_state.story_is_read = False
if 'wb_difficulty' not in st.session_state:
    st.session_state.wb_difficulty = 'normal'

# New Activity "Done" States for manual next button
if 'syl_correct_state' not in st.session_state:
    st.session_state.syl_correct_state = False
if 'wb_correct_state' not in st.session_state:
    st.session_state.wb_correct_state = False

# --- WELCOME SCREEN LOGIC ---
def login_screen():
    # Styled like a magical scroll on top of the castle background
    st.markdown("""
    <div class="scroll-container">
        <h1 style='color: #8B4513; font-family: "Comic Sans MS", cursive;'>📜 Welcome, Young Wizard!</h1>
        <p style='font-size: 1.2rem; color: #555;'>I am the Guardian of the Words.<br>Please declare your name to enter the castle.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            name_input = st.text_input("My name is:", placeholder="Type your name...")
            # Use a primary button for style
            submit = st.form_submit_button("🏰 Enter the Castle 🏰", use_container_width=True, type="primary")
            
            if submit:
                if name_input.strip():
                    st.session_state.student_name = name_input.strip()
                    st.rerun()
                else:
                    st.warning("The castle gates remain closed. Please tell me your name!")

if not st.session_state.student_name:
    login_screen()
    st.stop()

# --- Helper Functions ---
def go_home():
    st.session_state.current_activity = None

def celebrate_success():
    """Randomized visual reward system with personalization"""
    name = st.session_state.student_name
    
    # Mix of generic and personalized messages
    messages = [
        "Awesome Job! 🎉",
        f"Way to go, {name}! 🌟",
        "You are a Word Wizard! 🧙‍♂️",
        f"Spectacular work, {name}! ✨",
        "Brilliant! 💡",
        f"{name}, you are on fire! 🔥",
        "Correct! 🎯"
    ]
    
    msg = random.choice(messages)
    effect = random.choice(["balloons", "snow", "magic"])
    
    if effect == "balloons":
        st.balloons()
    elif effect == "snow":
        st.snow()
    else:
        pass
        
    st.toast(msg, icon="⭐")

def play_error():
    st.toast("Not quite! Try again.", icon="❌")

def reset_progress():
    st.session_state.completed_syllables = []
    st.session_state.completed_words = []
    st.session_state.sent_index = 0
    st.session_state.ant_index = 0
    st.session_state.yn_index = 0
    st.session_state.reading_quiz_index = 0
    st.session_state.story_is_read = False
    
    keys_to_remove = [k for k in st.session_state.keys() if k.startswith("antonym_") or k.startswith("yn_answered_") or k.startswith("sent_answered_") or k.startswith("read_answered_") or k.endswith("_correct_state")]
    for k in keys_to_remove:
        del st.session_state[k]
        
    st.session_state.syl_correct_state = False
    st.session_state.wb_correct_state = False
        
    st.success("Progress Reset!")
    time.sleep(1)
    st.rerun()

# --- Gemini Functions ---
def ask_gemini_explanation(word):
    if not api_key:
        return None
    try:
        prompt = f"Explain to a 4th grade student why the word '{word}' is spelled with its specific suffix (-able or -ible). Keep it encouraging and brief (under 30 words)."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return None

# --- Activities ---

def activity_menu():
    # Inject Custom CSS for Door Buttons ONLY on this menu
    st.markdown("""
    <style>
    /* Activity Menu Grid Layout - Door Styling */
    div.door-container button {
        background: linear-gradient(to bottom, #8B4513, #5A2D0C) !important;
        color: #FFD700 !important;
        border: 4px solid #FFD700 !important;
        border-radius: 50% 50% 5px 5px !important; /* Arched top */
        height: 180px !important;
        width: 100% !important;
        font-size: 1.5rem !important;
        font-family: 'Comic Sans MS', cursive !important;
        text-shadow: 2px 2px 4px #000;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5), inset 0 0 30px rgba(0,0,0,0.5) !important;
        transition: transform 0.2s !important;
        white-space: normal !important;
        margin-bottom: 20px !important;
    }
    div.door-container button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 0 30px #FFD700 !important; /* Glowing effect */
        border-color: #fff !important;
    }
    div.door-container p {
        font-size: 1.5rem !important; /* Make button text bigger */
    }
    </style>
    """, unsafe_allow_html=True)

    # Personalized Header
    st.markdown(f"<h1 class='main-header'>Welcome, {st.session_state.student_name}! 🧙‍♂️</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Choose a door to begin your adventure!</p>", unsafe_allow_html=True)

    # 2 Rows of 3 Columns
    r1c1, r1c2, r1c3 = st.columns(3)
    r2c1, r2c2, r2c3 = st.columns(3)
    
    # Row 1
    with r1c1:
        st.markdown('<div class="door-container">', unsafe_allow_html=True)
        if st.button("✂️\nSyllable\nDetective"):
            st.session_state.current_activity = "SYLLABLES"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    with r1c2:
        st.markdown('<div class="door-container">', unsafe_allow_html=True)
        if st.button("🔨\nWord\nBuilder"):
            st.session_state.current_activity = "WORD_BUILDER"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    with r1c3:
        st.markdown('<div class="door-container">', unsafe_allow_html=True)
        if st.button("✍️\nSentence\nMaster"):
            st.session_state.current_activity = "SENTENCE_FILL"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Row 2
    with r2c1:
        st.markdown('<div class="door-container">', unsafe_allow_html=True)
        if st.button("🔄\nOpposites"):
            st.session_state.current_activity = "ANTONYMS"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    with r2c2:
        st.markdown('<div class="door-container">', unsafe_allow_html=True)
        if st.button("👍\nYes or No?"):
            st.session_state.current_activity = "YES_NO"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    with r2c3:
        st.markdown('<div class="door-container">', unsafe_allow_html=True)
        if st.button("📖\nReading\nComp"):
            st.session_state.current_activity = "READING"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    if st.button("🗑️ Reset All Progress"):
        reset_progress()

def syllable_splitter():
    # ... (code for syllable_splitter remains same, just ensuring indent)
    # Split header into two columns: Title (Left), Next Button (Right)
    c_header, c_next = st.columns([3, 1])
    
    with c_header:
        st.header("✂️ Syllable Detective")
    
    # Progress
    total = len(SYLLABLE_DATA)
    completed = len(st.session_state.completed_syllables)
    st.progress(completed / total if total > 0 else 0)
    
    # Get Task
    incomplete = [t for t in SYLLABLE_DATA if t['id'] not in st.session_state.completed_syllables]
    
    if not incomplete:
        st.success("You've mastered all words! 🎉")
        if st.button("Start Over"):
            st.session_state.completed_syllables = []
            st.rerun()
        return

    task = incomplete[0]
    
    # If already correctly answered, show Next button at top
    if st.session_state.syl_correct_state:
        with c_next:
            if st.button("Next Word ➡", type="primary"):
                st.session_state.completed_syllables.append(task['id'])
                st.session_state.syl_correct_state = False
                st.rerun()
    
    # Layout Separation: Word & Instructions vs Input Box
    st.markdown(f"<div style='text-align:center; font-size:3rem; color:#003366; font-weight:bold; margin-bottom:1rem; text-shadow:none;'>{task['word']}</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#333;'>Break the word into parts below. Keep the suffix (-able/-ible) together!</p>", unsafe_allow_html=True)
    
    # Distinct Input Container
    
    cols = st.columns(len(task['correctSyllables']))
    user_inputs = []
    
    with st.form(key=f"syllable_form_{task['id']}"):
        for i, col in enumerate(cols):
            val = col.text_input(f"Syllable {i+1}", key=f"syl_{task['id']}_{i}", label_visibility="visible").strip().lower()
            user_inputs.append(val)
        
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Check Answer")

    if submitted:
        if user_inputs == task['correctSyllables']:
            celebrate_success()
            st.session_state.syl_correct_state = True
            
            with st.spinner("Asking the AI Wizard for a tip..."):
                expl = ask_gemini_explanation(task['word'])
                if expl:
                    st.success(f"Wizard says: {expl}")
            st.rerun()
        else:
            play_error()
            st.error("Not quite! Check your splits. Is the suffix in one box?")
            
    if st.session_state.syl_correct_state:
        st.success("Correct! Great job!")

def word_builder():
    # --- Top Row: Back Button (Left), Title (Center) ---
    c_back, c_title = st.columns([1, 4])
    with c_back:
        st.markdown('<div class="back-btn-container">', unsafe_allow_html=True)
        if st.button("⬅ Back", key="wb_back_btn"):
            st.session_state.current_activity = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c_title:
        st.markdown("<h1 style='text-align:center; color:#FFD700; margin-top:0; text-shadow: 2px 2px #000;'>WORD CONSTRUCTION</h1>", unsafe_allow_html=True)
    
    incomplete = [t for t in WORD_BUILDER_DATA if t['id'] not in st.session_state.completed_words]
    if not incomplete:
        st.success("All words built! 🏗️")
        if st.button("Reset Construction"):
            st.session_state.completed_words = []
            st.rerun()
        return

    task = incomplete[0]
    
    if st.session_state.wb_correct_state:
        if st.button("Next Word ➡", type="primary", key="wb_next_top"):
            st.session_state.completed_words.append(task['id'])
            st.session_state.wb_correct_state = False
            st.session_state.wb_current_build = []
            st.rerun()
    
    if 'wb_current_build' not in st.session_state:
        st.session_state.wb_current_build = []
    
    current_word = "".join(st.session_state.wb_current_build)
    
    # --- BLUEPRINT SECTION ---
    st.markdown(f"""
    <div class="blueprint-container">
        <div class="blueprint-label">BLUEPRINT</div><br>
        <span style='font-size: 3rem;'>📜</span>
        <div class="thought-bubble">{task['meaning']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # --- SCATTERED PARTS (Bricks) ---
    parts = task['parts'].copy()
    if st.session_state.wb_difficulty == 'challenge':
        all_parts = [p for t in WORD_BUILDER_DATA for p in t['parts']]
        distractors = random.sample(all_parts, 3)
        parts.extend(distractors)
    random.seed(task['id'] + len(parts)) 
    random.shuffle(parts)

    st.markdown('<div class="brick-btn-style">', unsafe_allow_html=True)
    b_cols = st.columns(len(parts))
    for i, part in enumerate(parts):
        if b_cols[i].button(part, key=f"btn_{task['id']}_{i}_{len(st.session_state.wb_current_build)}", use_container_width=True, disabled=st.session_state.wb_correct_state):
            st.session_state.wb_current_build.append(part)
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # --- ASSEMBLING ZONE ---
    st.markdown(f"""
    <div class="assembling-zone">
        <span class="zone-label">ASSEMBLING ZONE</span>
        <div class="built-text">{current_word}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c_reset, c_spacer, c_construct = st.columns([1, 2, 1])
    
    with c_reset:
        if st.button("↺ Reset", use_container_width=True, disabled=st.session_state.wb_correct_state):
            st.session_state.wb_current_build = []
            st.rerun()
            
    with c_construct:
        st.markdown('<div class="construct-btn-container">', unsafe_allow_html=True)
        if st.button("CONSTRUCT!", key="wb_construct_btn", use_container_width=True, disabled=st.session_state.wb_correct_state):
            built_word = "".join(st.session_state.wb_current_build)
            if built_word == task['targetWord']:
                celebrate_success()
                st.session_state.wb_correct_state = True
                st.rerun()
            else:
                play_error()
                st.error(f"Try again! You built '{built_word}'")
                time.sleep(1)
                st.session_state.wb_current_build = []
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state.wb_correct_state:
        st.success(f"Correct! The word is {task['targetWord']}.")

def sentence_fill():
    c_header, c_next = st.columns([3, 1])
    with c_header:
        st.header("✍️ Sentence Master")
    
    st.markdown("""
    <style>
    div.stButton > button {
        font-size: 2.5rem !important;
        font-weight: bold !important;
        line-height: 1.5 !important;
        padding: 1.5rem !important;
        min-height: 120px;
        width: 100%;
        white-space: normal; word-wrap: break-word;
    }
    </style>
    """, unsafe_allow_html=True)
    
    if st.session_state.sent_index >= len(SENTENCE_DATA):
        st.success("You have completed all sentences! 🎓")
        if st.button("Start Over"):
            st.session_state.sent_index = 0
            st.rerun()
        return

    task = SENTENCE_DATA[st.session_state.sent_index]
    st.markdown(f"**Sentence {st.session_state.sent_index + 1} of {len(SENTENCE_DATA)}**")
    
    answered_key = f"sent_answered_{task['id']}"
    if answered_key not in st.session_state:
        st.session_state[answered_key] = None
        
    if st.session_state[answered_key] == "correct":
        with c_next:
            if st.button("Next Sentence ➡", key="next_sent_top", type="primary"):
                 st.session_state.sent_index += 1
                 st.rerun()
    
    blank_content = f"<span class='blank-space'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>"
    display_style = ""
    
    if st.session_state[answered_key] == "correct":
        blank_content = f"<span class='filled-word'>{task['correctOption']}</span>"
        display_style = "border: 3px solid #28a745;"
    
    st.markdown(f"""
    <div class="sentence-display" style="{display_style}">
        {task['sentencePart1']} {blank_content} {task['sentencePart2']}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align:center; margin-top:2rem;'>Choose the missing word:</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    is_disabled = (st.session_state[answered_key] == "correct")
    
    with col1:
        opt1 = task['options'][0]
        if st.button(opt1, key=f"btn_opt1_{task['id']}", use_container_width=True, disabled=is_disabled):
            if opt1 == task['correctOption']:
                celebrate_success()
                st.session_state[answered_key] = "correct"
                st.rerun()
            else:
                play_error()
                st.toast(f"'{opt1}' is not correct. Try the other one!", icon="❌")

    with col2:
        opt2 = task['options'][1]
        if st.button(opt2, key=f"btn_opt2_{task['id']}", use_container_width=True, disabled=is_disabled):
            if opt2 == task['correctOption']:
                celebrate_success()
                st.session_state[answered_key] = "correct"
                st.rerun()
            else:
                play_error()
                st.toast(f"'{opt2}' is not correct. Try the other one!", icon="❌")

def antonym_activity():
    c_header, c_next = st.columns([3, 1])
    with c_header:
        st.header("🔄 Opposites (Tap to Fill)")
    
    st.markdown("""
    <style>
    div[data-testid="column"] button {
        font-size: 1.5rem !important; padding: 1rem 2rem !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    if st.session_state.ant_index >= len(ANTONYM_DATA):
        st.success("All opposites found! ☯️")
        if st.button("Play Again"):
            st.session_state.ant_index = 0
            st.rerun()
        return

    task = ANTONYM_DATA[st.session_state.ant_index]
    options_key = f"antonym_options_{task['id']}"
    state_key = f"antonym_state_{task['id']}"
    
    if options_key not in st.session_state:
        options = [task['answer']]
        others = [t['answer'] for t in ANTONYM_DATA if t['answer'] != task['answer']]
        options.extend(random.sample(others, min(3, len(others))))
        random.shuffle(options)
        st.session_state[options_key] = options

    if state_key not in st.session_state:
        st.session_state[state_key] = "unanswered"

    options = st.session_state[options_key]
    current_state = st.session_state[state_key]
    
    if current_state == "correct":
        with c_next:
            if st.button("Next Word ➡", type="primary", key="ant_next_top"):
                st.session_state.ant_index += 1
                st.rerun()

    st.markdown(f"**Word {st.session_state.ant_index + 1} of {len(ANTONYM_DATA)}**")
    st.markdown(f"<div class='antonym-clue'>{task['clue']}</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; font-size: 2.5rem; margin: 10px 0;'>⇄</div>", unsafe_allow_html=True)
    
    answer_html = "<div style='text-align:center; margin-bottom: 2rem;'>"
    if current_state == "correct":
         answer_html += f"<div class='antonym-answer-box'>{task['answer']}</div>"
    else:
         answer_html += "<div class='antonym-placeholder'>?</div>"
    answer_html += "</div>"
    
    st.markdown(answer_html, unsafe_allow_html=True)
    
    if current_state == "unanswered":
        st.info("Tap the bubble that means the opposite!")
        cols = st.columns(len(options))
        for i, opt in enumerate(options):
            if cols[i].button(opt, key=f"ant_btn_{task['id']}_{i}", use_container_width=True):
                if opt == task['answer']:
                    celebrate_success()
                    st.session_state[state_key] = "correct"
                    st.rerun()
                else:
                    play_error()
    else:
        st.success("Correct!")

def yes_no_activity():
    c_header, c_next = st.columns([3, 1])
    with c_header:
        st.header("👍 Yes or No?")
    
    if st.session_state.yn_index >= len(YES_NO_DATA):
        st.success("You finished the questions! ✅")
        if st.button("Restart"):
            st.session_state.yn_index = 0
            st.rerun()
        return

    task = YES_NO_DATA[st.session_state.yn_index]
    answered_key = f"yn_answered_{task['id']}"
    if answered_key not in st.session_state:
        st.session_state[answered_key] = None
        
    if st.session_state[answered_key] is not None:
        with c_next:
            if st.button("Next Question ➡", key="next_q_top", type="primary"):
                 st.session_state.yn_index += 1
                 st.rerun()
    
    st.markdown(f"""
    <div style="background:white; padding:3rem; border-radius:15px; text-align:center; box-shadow:0 4px 6px rgba(0,0,0,0.1); margin-bottom:2rem;">
        <h2 style="color:#003366;">{task['question']}</h2>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state[answered_key] is None:
        st.markdown("""
        <style>
        div[data-testid="column"] .stButton button {
            font-size: 3rem !important;
            padding: 2rem !important;
            min-height: 150px;
            margin-top: 20px;
        }
        </style>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        if c1.button("YES 👍", use_container_width=True):
            if task['answer'] == True:
                celebrate_success()
                st.session_state[answered_key] = "correct"
            else:
                play_error()
                st.session_state[answered_key] = "wrong"
            st.rerun()
            
        if c2.button("NO 👎", use_container_width=True):
            if task['answer'] == False:
                celebrate_success()
                st.session_state[answered_key] = "correct"
            else:
                play_error()
                st.session_state[answered_key] = "wrong"
            st.rerun()
    else:
        if st.session_state[answered_key] == "correct":
            name = st.session_state.student_name
            fun_messages = [
                "🎉 SPECTACULAR! 🎉",
                f"🌟 YOU GOT IT, {name.upper()}! 🌟",
                "🚀 WAY TO GO! 🚀",
                "🧙‍♂️ PURE MAGIC! 🧙‍♂️",
                f"✨ EXCELLENT WORK, {name.upper()}! ✨"
            ]
            msg = random.choice(fun_messages)
            st.markdown(f"""
            <div style="
                background-color: #d4edda; padding: 3rem; border-radius: 20px; border: 5px solid #28a745; 
                text-align: center; margin-bottom: 2rem; animation: pulse 2s infinite; box-shadow: 0 10px 20px rgba(0,0,0,0.1);">
                <h1 style="color: #155724; font-size: 4rem; margin:0; font-family: 'Comic Sans MS', cursive;">{msg}</h1>
                <p style="font-size: 2rem; color: #155724; margin-top: 1rem;">That answer was correct!</p>
            </div>
            <style>
            @keyframes pulse {{
                0% {{ transform: scale(1); box-shadow: 0 0 0 0 rgba(40, 167, 69, 0.7); }}
                70% {{ transform: scale(1.02); box-shadow: 0 0 0 15px rgba(40, 167, 69, 0); }}
                100% {{ transform: scale(1); box-shadow: 0 0 0 0 rgba(40, 167, 69, 0); }}
            }}
            </style>
            """, unsafe_allow_html=True)
        else:
            st.error("Oops! That was incorrect.")

def reading_activity():
    c1, c2 = st.columns([3, 1])
    with c1:
        st.header("📖 Reading Comprehension")
    with c2:
        if st.button("🔄 New Story"):
            st.session_state.reading_story_index = (st.session_state.reading_story_index + 1) % len(READING_STORIES)
            st.session_state.reading_quiz_index = 0
            st.session_state.story_is_read = False
            st.rerun()
    
    story = READING_STORIES[st.session_state.reading_story_index]
    font_size = st.slider("Adjust Text Size:", min_value=16, max_value=32, value=20)
    col_story, col_quiz = st.columns([2, 1])
    
    with col_story:
        story_html = f"""
        <div class='story-box' style='font-size:{font_size}px; line-height: 1.6;'>
            <h3 style='color:#003366; margin-bottom:1rem;'>{story['title']}</h3>
        """
        for p in story['paragraphs']:
            story_html += f"<p style='margin-bottom:1rem;'>{p}</p>"
        story_html += "</div>"
        
        st.markdown(story_html, unsafe_allow_html=True)
        if not st.session_state.story_is_read:
            st.write("---")
            if st.button("✅ I have read the story"):
                st.session_state.story_is_read = True
                st.rerun()

    with col_quiz:
        if not st.session_state.story_is_read:
            st.info("Please read the story and click the confirmation button to start the quiz.")
        else:
            st.markdown("<div class='quiz-box'>", unsafe_allow_html=True)
            st.markdown("### Quiz Time!")
            q_idx = st.session_state.reading_quiz_index
            
            if q_idx < len(story['questions']):
                q = story['questions'][q_idx]
                read_answered_key = f"read_answered_{story['id']}_{q_idx}"
                if read_answered_key not in st.session_state:
                    st.session_state[read_answered_key] = False
                
                if st.session_state[read_answered_key]:
                    if st.button("Next Question ➡", key="read_next_q", type="primary"):
                        st.session_state.reading_quiz_index += 1
                        st.rerun()
                
                st.write(f"**Q{q_idx+1}: {q['question']}**")
                ans_key = f"read_q_{story['id']}_{q_idx}"
                ans = st.radio("Choose:", q['options'], key=ans_key, disabled=st.session_state[read_answered_key])
                
                if st.button("Check Answer", key=f"chk_{ans_key}", disabled=st.session_state[read_answered_key]):
                    if ans == q['correctAnswer']:
                        celebrate_success()
                        st.success("Correct!")
                        st.session_state[read_answered_key] = True
                        st.rerun()
                    else:
                        play_error()
                        
                if st.session_state[read_answered_key]:
                    st.success("Correct Answer!")
            else:
                st.balloons()
                st.success("Story Completed! 📚")
                if st.button("Read Next Story"):
                    st.session_state.reading_story_index = (st.session_state.reading_story_index + 1) % len(READING_STORIES)
                    st.session_state.reading_quiz_index = 0
                    st.session_state.story_is_read = False
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

# --- Main App Logic ---

if st.session_state.current_activity:
    if st.session_state.current_activity != "WORD_BUILDER":
        if st.button("← Back to Menu"):
            go_home()
            st.rerun()

if st.session_state.current_activity == "SYLLABLES":
    syllable_splitter()
elif st.session_state.current_activity == "WORD_BUILDER":
    word_builder()
elif st.session_state.current_activity == "SENTENCE_FILL":
    sentence_fill()
elif st.session_state.current_activity == "ANTONYMS":
    antonym_activity()
elif st.session_state.current_activity == "YES_NO":
    yes_no_activity()
elif st.session_state.current_activity == "READING":
    reading_activity()
else:
    activity_menu()
