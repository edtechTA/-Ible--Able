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

# --- USER CUSTOMIZATION ---
# Updated Castle Background Link
CASTLE_BACKGROUND_URL = "https://i.ibb.co/JRRCkyZL/game-castle-background.png"

# --- Gemini Setup ---
api_key = st.secrets.get("API_KEY") or os.environ.get("API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

# --- MASTER DATA LISTS (Pool of ~15 words each) ---

MASTER_SYLLABLE_DATA = [
    {"id": 1, "word": "presentable", "correctSyllables": ["pre", "sent", "able"]},
    {"id": 2, "word": "miserable", "correctSyllables": ["mis", "er", "able"]},
    {"id": 3, "word": "valuable", "correctSyllables": ["val", "u", "able"]},
    {"id": 4, "word": "impossible", "correctSyllables": ["im", "poss", "ible"]},
    {"id": 5, "word": "dependable", "correctSyllables": ["de", "pend", "able"]},
    {"id": 6, "word": "reversible", "correctSyllables": ["re", "vers", "ible"]},
    {"id": 7, "word": "favorable", "correctSyllables": ["fa", "vor", "able"]},
    {"id": 8, "word": "comfortable", "correctSyllables": ["com", "fort", "able"]},
    {"id": 9, "word": "incredible", "correctSyllables": ["in", "cred", "ible"]},
    {"id": 10, "word": "visible", "correctSyllables": ["vis", "ible"]},
    {"id": 11, "word": "flexible", "correctSyllables": ["flex", "ible"]},
    {"id": 12, "word": "edible", "correctSyllables": ["ed", "ible"]},
    {"id": 13, "word": "adorable", "correctSyllables": ["a", "dor", "able"]},
    {"id": 14, "word": "responsible", "correctSyllables": ["re", "spons", "ible"]},
    {"id": 15, "word": "breakable", "correctSyllables": ["break", "able"]},
]

MASTER_WORD_BUILDER_DATA = [
    {"id": 1, "parts": ["val", "u", "able"], "meaning": "worth a lot", "targetWord": "valuable"},
    {"id": 2, "parts": ["re", "li", "able"], "meaning": "dependable", "targetWord": "reliable"},
    {"id": 3, "parts": ["in", "cred", "ible"], "meaning": "fantastic / hard to believe", "targetWord": "incredible"},
    {"id": 4, "parts": ["in", "vis", "ible"], "meaning": "not able to be seen", "targetWord": "invisible"},
    {"id": 5, "parts": ["re", "vers", "ible"], "meaning": "able to be turned inside out", "targetWord": "reversible"},
    {"id": 6, "parts": ["re", "mark", "able"], "meaning": "astonishing / worthy of attention", "targetWord": "remarkable"},
    {"id": 7, "parts": ["div", "is", "ible"], "meaning": "able to be divided", "targetWord": "divisible"},
    {"id": 8, "parts": ["com", "fort", "able"], "meaning": "cozy and relaxed", "targetWord": "comfortable"},
    {"id": 9, "parts": ["flex", "ible"], "meaning": "able to bend easily", "targetWord": "flexible"},
    {"id": 10, "parts": ["sens", "ible"], "meaning": "smart and practical", "targetWord": "sensible"},
    {"id": 11, "parts": ["horr", "ible"], "meaning": "very unpleasant", "targetWord": "horrible"},
    {"id": 12, "parts": ["a", "dor", "able"], "meaning": "very cute", "targetWord": "adorable"},
    {"id": 13, "parts": ["vis", "ible"], "meaning": "able to be seen", "targetWord": "visible"},
    {"id": 14, "parts": ["ed", "ible"], "meaning": "safe to eat", "targetWord": "edible"},
    {"id": 15, "parts": ["us", "able"], "meaning": "fit to be used", "targetWord": "usable"},
]

MASTER_SENTENCE_DATA = [
    {"id": 1, "sentencePart1": "My grandmother's gold ring cost a lot. It is very", "sentencePart2": ".", "options": ["valueless", "valuable"], "correctOption": "valuable"},
    {"id": 2, "sentencePart1": "The sunny weather was", "sentencePart2": "for our picnic.", "options": ["favored", "favorable"], "correctOption": "favorable"},
    {"id": 3, "sentencePart1": "Dry wood is highly", "sentencePart2": ", so keep it away from fire.", "options": ["combust", "combustible"], "correctOption": "combustible"},
    {"id": 4, "sentencePart1": "My old car starts every morning. It is very", "sentencePart2": ".", "options": ["depend", "dependable"], "correctOption": "dependable"},
    {"id": 5, "sentencePart1": "Please tuck in your shirt so you look", "sentencePart2": ".", "options": ["presented", "presentable"], "correctOption": "presentable"},
    {"id": 6, "sentencePart1": "The number ten is evenly", "sentencePart2": "by two.", "options": ["divide", "divisible"], "correctOption": "divisible"},
    {"id": 7, "sentencePart1": "Don't worry! This marker is", "sentencePart2": "and comes off.", "options": ["wash", "washable"], "correctOption": "washable"},
    {"id": 8, "sentencePart1": "The gymnast was very", "sentencePart2": "and could do the splits.", "options": ["rigid", "flexible"], "correctOption": "flexible"},
    {"id": 9, "sentencePart1": "That mushroom is poisonous, it is not", "sentencePart2": ".", "options": ["eaten", "edible"], "correctOption": "edible"},
    {"id": 10, "sentencePart1": "The stars are not", "sentencePart2": "during the day.", "options": ["vision", "visible"], "correctOption": "visible"},
    {"id": 11, "sentencePart1": "The puppy was so", "sentencePart2": "that everyone wanted to pet it.", "options": ["adore", "adorable"], "correctOption": "adorable"},
    {"id": 12, "sentencePart1": "It is", "sentencePart2": "for a human to fly without a plane.", "options": ["possible", "impossible"], "correctOption": "impossible"},
    {"id": 13, "sentencePart1": "A good raincoat is", "sentencePart2": "so you can wear it two ways.", "options": ["reverse", "reversible"], "correctOption": "reversible"},
    {"id": 14, "sentencePart1": "The loud music was barely", "sentencePart2": "through the thick walls.", "options": ["audio", "audible"], "correctOption": "audible"},
    {"id": 15, "sentencePart1": "It was a", "sentencePart2": "movie; I hid my eyes the whole time!", "options": ["horror", "horrible"], "correctOption": "horrible"},
]

MASTER_ANTONYM_DATA = [
    {"id": 1, "clue": "Calm", "answer": "excitable"},
    {"id": 2, "clue": "Crazy", "answer": "sensible"},
    {"id": 3, "clue": "Worthless", "answer": "valuable"},
    {"id": 4, "clue": "Happy", "answer": "miserable"},
    {"id": 5, "clue": "Impossible", "answer": "possible"},
    {"id": 6, "clue": "Cozy", "answer": "uncomfortable"},
    {"id": 7, "clue": "Useless", "answer": "usable"},
    {"id": 8, "clue": "Hidden", "answer": "visible"},
    {"id": 9, "clue": "Rigid / Stiff", "answer": "flexible"},
    {"id": 10, "clue": "Poisonous", "answer": "edible"},
    {"id": 11, "clue": "Silent", "answer": "audible"},
    {"id": 12, "clue": "Hateful", "answer": "lovable"},
    {"id": 13, "clue": "Permanent", "answer": "reversible"},
    {"id": 14, "clue": "Careless", "answer": "responsible"},
    {"id": 15, "clue": "Ordinary", "answer": "incredible"},
]

MASTER_YES_NO_DATA = [
    {"id": 1, "question": "Can a raincoat be reversible?", "answer": True},
    {"id": 2, "question": "Are most glasses nonbreakable?", "answer": False},
    {"id": 3, "question": "Is a monster usually horrible?", "answer": True},
    {"id": 4, "question": "Can a dry forest be combustible?", "answer": True},
    {"id": 5, "question": "Are your grades in school improvable?", "answer": True},
    {"id": 6, "question": "Is your face washable?", "answer": True},
    {"id": 7, "question": "Is spilled milk returnable?", "answer": False},
    {"id": 8, "question": "Is a brick edible?", "answer": False},
    {"id": 9, "question": "Is an invisible man easy to see?", "answer": False},
    {"id": 10, "question": "Is a soft bed comfortable?", "answer": True},
    {"id": 11, "question": "Is a rubber band flexible?", "answer": True},
    {"id": 12, "question": "Is a superhero incredible?", "answer": True},
    {"id": 13, "question": "Is the sun visible at night?", "answer": False},
    {"id": 14, "question": "Is a puppy adorable?", "answer": True},
    {"id": 15, "question": "Is a whisper audible in a storm?", "answer": False},
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

# New Activity "Done" States
if 'syl_correct_state' not in st.session_state:
    st.session_state.syl_correct_state = False
if 'wb_correct_state' not in st.session_state:
    st.session_state.wb_correct_state = False

# --- RANDOMIZED SESSION DATA INIT ---
def init_random_data():
    if 'session_syllables' not in st.session_state:
        st.session_state.session_syllables = random.sample(MASTER_SYLLABLE_DATA, min(len(MASTER_SYLLABLE_DATA), 7))
    if 'session_word_builder' not in st.session_state:
        st.session_state.session_word_builder = random.sample(MASTER_WORD_BUILDER_DATA, min(len(MASTER_WORD_BUILDER_DATA), 7))
    if 'session_sentences' not in st.session_state:
        st.session_state.session_sentences = random.sample(MASTER_SENTENCE_DATA, min(len(MASTER_SENTENCE_DATA), 7))
    if 'session_antonyms' not in st.session_state:
        st.session_state.session_antonyms = random.sample(MASTER_ANTONYM_DATA, min(len(MASTER_ANTONYM_DATA), 7))
    if 'session_yes_no' not in st.session_state:
        st.session_state.session_yes_no = random.sample(MASTER_YES_NO_DATA, min(len(MASTER_YES_NO_DATA), 7))

init_random_data()

# --- Background CSS Logic ---
if CASTLE_BACKGROUND_URL:
    background_style = f"""
        [data-testid="stAppViewContainer"] {{
            background-image: url("{CASTLE_BACKGROUND_URL}");
            background-size: 100% auto; /* Forces image to fit width, natural height */
            background-repeat: no-repeat;
            background-position: center bottom; /* Anchor to bottom of screen */
            background-attachment: fixed;
            color: #fff;
        }}
    """
else:
    background_style = """
        [data-testid="stAppViewContainer"] {
            background-color: #2c2c2c;
            color: #fff;
        }
    """

# --- GLOBAL STYLES (Castle Background & Defaults) ---
st.markdown(f"""
<style>
    /* GLOBAL: Background */
    {background_style}
    
    /* Ensure content sits above background - ADDING WHITE OVERLAY HERE */
    [data-testid="block-container"] {{
        z-index: 1;
        position: relative;
        /* Updated: White semi-transparent overlay for readability */
        background-color: rgba(255, 255, 255, 0.9); 
        padding: 3rem;
        border-radius: 20px;
        margin-top: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }}
    
    /* Default text color inside the container should now be dark */
    [data-testid="block-container"] p, 
    [data-testid="block-container"] li, 
    [data-testid="block-container"] h1, 
    [data-testid="block-container"] h2, 
    [data-testid="block-container"] h3 {{
        color: #333;
    }}

    .main-header {{
        font-family: 'Comic Sans MS', 'Comic Sans', cursive;
        color: #003366; /* Changed to dark blue for contrast on white */
        text-align: center;
        font-size: 3.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: none; /* Removed shadow for cleaner look on white */
    }}
    .sub-header {{
        color: #555; /* Dark grey for contrast */
        text-align: center;
        font-size: 1.3rem;
        margin-bottom: 2rem;
        text-shadow: none;
    }}
    
    /* LOGIN SCROLL STYLING */
    .scroll-container {{
        background-color: #fdfbf7;
        background-image: url("https://www.transparenttextures.com/patterns/aged-paper.png");
        border: 10px solid #d4af37;
        border-radius: 10px 10px 50px 50px;
        padding: 3rem;
        text-align: center;
        color: #333;
        box-shadow: 0 0 50px rgba(255, 215, 0, 0.5);
        margin: 2rem auto;
        max-width: 600px;
        position: relative;
    }}
    
    /* DEFAULT BUTTON (Reset for generic buttons) */
    .stButton button {{
        background-color: #003366;
        color: white;
        border-radius: 20px;
        border: 2px solid #003366;
    }}
    
</style>
""", unsafe_allow_html=True)

# --- WELCOME SCREEN LOGIC ---
def login_screen():
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
    name = st.session_state.student_name
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
    
    keys_to_remove = [k for k in st.session_state.keys() if k.startswith("antonym_") or k.startswith("yn_answered_") or k.startswith("sent_answered_") or k.startswith("read_answered_") or k.endswith("_correct_state") or k.startswith("session_")]
    for k in keys_to_remove:
        del st.session_state[k]
        
    st.session_state.syl_correct_state = False
    st.session_state.wb_correct_state = False
    
    # Re-init random data
    init_random_data()
        
    st.success("Progress Reset! New words have been summoned!")
    time.sleep(1)
    st.rerun()

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
    # Make container transparent to show castle, buttons act as "hit zones" over doors
    st.markdown("""
    <style>
    /* Hide the default semi-transparent block container ONLY on the menu so we see the castle */
    [data-testid="block-container"] {
        background-color: transparent !important;
        box-shadow: none !important;
        border: none !important;
    }
    
    /* Transparent Door Buttons */
    div[data-testid="column"] button {
        background-color: rgba(255, 255, 255, 0.15) !important; /* Slight glass effect to see hit zone */
        border: 2px solid rgba(255, 215, 0, 0.5) !important; /* Golden glowing border */
        color: transparent !important; /* HIDE TEXT */
        border-radius: 100px 100px 5px 5px !important; /* Arched Door Shape */
        height: 250px !important; /* Increased height for bigger hit box */
        width: 100% !important;
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.3) !important;
        margin-bottom: 20px !important;
        transition: all 0.3s !important;
    }
    div[data-testid="column"] button:hover {
        background-color: rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 0 40px rgba(255, 215, 0, 0.8) !important;
        transform: scale(1.05) !important;
        cursor: pointer;
    }
    /* Hide the paragraph text inside the button too just in case */
    div[data-testid="column"] button p {
        display: none !important;
    }
    
    /* Revert headers to gold/white for the menu page only */
    .main-header { color: #FFD700 !important; text-shadow: 3px 3px 5px #000 !important; }
    .sub-header { color: #FFF !important; text-shadow: 2px 2px 4px #000 !important; }
    </style>
    """, unsafe_allow_html=True)

    # Simplified Header to not distract from image
    st.markdown(f"<h1 class='main-header'>Welcome, {st.session_state.student_name}!</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Click a door to begin!</p>", unsafe_allow_html=True)

    # PUSH BUTTONS DOWN TO BOTTOM 
    # Use a large spacer. Adjust '45vh' if needed based on the image aspect ratio
    st.markdown("<div style='height: 45vh;'></div>", unsafe_allow_html=True)

    # SINGLE ROW OF 6 COLUMNS for the 6 doors
    c1, c2, c3, c4, c5, c6 = st.columns(6, gap="small")
    
    # We pass text for accessibility/debugging, but CSS hides it visually
    with c1:
        if st.button("Syllable", key="btn_syl"):
            st.session_state.current_activity = "SYLLABLES"
            st.rerun()
    with c2:
        if st.button("Word", key="btn_wb"):
            st.session_state.current_activity = "WORD_BUILDER"
            st.rerun()
    with c3:
        if st.button("Sentence", key="btn_sent"):
            st.session_state.current_activity = "SENTENCE_FILL"
            st.rerun()
    with c4:
        if st.button("Opposites", key="btn_ant"):
            st.session_state.current_activity = "ANTONYMS"
            st.rerun()
    with c5:
        if st.button("YesNo", key="btn_yn"):
            st.session_state.current_activity = "YES_NO"
            st.rerun()
    with c6:
        if st.button("Read", key="btn_read"):
            st.session_state.current_activity = "READING"
            st.rerun()
    
    st.divider()
    if st.button("🗑️ Reset All Progress"):
        reset_progress()

def syllable_splitter():
    # Inject specific styles for this activity to override defaults/doors
    st.markdown("""
    <style>
    /* Reset Button Style for inner activity */
    div.stButton > button {
        background-color: #003366 !important;
        color: white !important;
        border-radius: 20px !important;
        height: auto !important;
        font-size: 1rem !important;
        box-shadow: none !important;
        border: 2px solid #003366 !important;
    }
    /* Syllable Container */
    [data-testid="stForm"] {
        background-color: #e3f2fd;
        border: 3px dashed #003366;
        padding: 2rem;
        border-radius: 15px;
        color: #333;
    }
    div.stButton > button[kind="primary"] {
        background-color: #28a745 !important;
        border-color: #28a745 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    c_header, c_next = st.columns([3, 1])
    with c_header:
        st.header("✂️ Syllable Detective")
    
    # USE SESSION DATA INSTEAD OF MASTER
    data = st.session_state.session_syllables
    
    total = len(data)
    completed = len(st.session_state.completed_syllables)
    st.progress(completed / total if total > 0 else 0)
    
    incomplete = [t for t in data if t['id'] not in st.session_state.completed_syllables]
    
    if not incomplete:
        st.success("You've mastered all words for this session! 🎉")
        if st.button("Start Over (New Words)"):
            reset_progress() # This reshuffles
        return

    task = incomplete[0]
    
    if st.session_state.syl_correct_state:
        with c_next:
            if st.button("Next Word ➡", type="primary"):
                st.session_state.completed_syllables.append(task['id'])
                st.session_state.syl_correct_state = False
                st.rerun()
    
    st.markdown(f"<div style='text-align:center; font-size:3rem; color:#003366; font-weight:bold; margin-bottom:1rem;'>{task['word']}</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#333;'>Break the word into parts below. Keep the suffix (-able/-ible) together!</p>", unsafe_allow_html=True)
    
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
    # Inject WB Specific CSS
    st.markdown("""
    <style>
    /* Reset Button Style */
    div.stButton > button {
        height: auto !important; box-shadow: none !important; border-radius: 5px !important;
    }
    
    /* Blueprint Section */
    .blueprint-container {
        border: 3px solid #003366; background-color: #E3F2FD; border-radius: 15px; padding: 1rem;
        text-align: center; position: relative; margin-bottom: 2rem; box-shadow: 0 4px 0 rgba(0,0,0,0.1); color: #333;
    }
    .blueprint-label {
        background-color: #003366; color: #FFCC00; padding: 5px 15px; border-radius: 10px;
        font-weight: bold; text-transform: uppercase; margin-bottom: 10px; display: inline-block;
    }
    .thought-bubble {
        background-color: white; border-radius: 30px; padding: 15px 30px; border: 2px solid #333;
        display: inline-block; font-family: 'Comic Sans MS', cursive; font-size: 1.5rem; position: relative;
        margin-left: 20px; color: #333;
    }
    .thought-bubble:before {
        content: ""; position: absolute; top: 50%; left: -12px; margin-top: -6px;
        border-width: 6px 12px 6px 0; border-style: solid; border-color: transparent #333 transparent transparent;
    }
    
    /* Bricks */
    .brick-btn-style button {
        background-color: #D2691E !important; color: white !important;
        border: 2px solid #8B4513 !important; border-radius: 5px !important;
        font-family: monospace; font-size: 1.5rem !important;
        box-shadow: 0px 6px 0px #8B4513 !important; margin-bottom: 10px; transition: all 0.1s;
    }
    .brick-btn-style button:active {
        box-shadow: 0px 2px 0px #8B4513 !important; transform: translateY(4px) !important;
    }
    
    .assembling-zone {
        border: 4px dashed #555; background-color: #f8f9fa; border-radius: 10px; padding: 2rem;
        text-align: center; margin-top: 2rem; min-height: 120px; color: #333;
    }
    .zone-label { color: #555; font-weight: bold; text-transform: uppercase; margin-bottom: 10px; display: block; letter-spacing: 2px; }
    .built-text { font-family: monospace; font-size: 3rem; color: #003366; letter-spacing: 5px; }
    
    .construct-btn-container button {
        background-color: #8B4513 !important; color: #FFCC00 !important; font-size: 1.5rem !important;
        border: 3px solid #5A2D0C !important; box-shadow: 0 4px 0 #5A2D0C !important; height: auto !important;
    }
    .back-btn-container button {
        background-color: rgba(0,0,0,0.1) !important; color: #333 !important; border: 1px solid #ccc !important;
    }
    div.stButton > button[kind="primary"] {
        background-color: #28a745 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    c_back, c_title = st.columns([1, 4])
    with c_back:
        st.markdown('<div class="back-btn-container">', unsafe_allow_html=True)
        if st.button("⬅ Back", key="wb_back_btn"):
            st.session_state.current_activity = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c_title:
        st.markdown("<h1 style='text-align:center; color:#003366; margin-top:0;'>WORD CONSTRUCTION</h1>", unsafe_allow_html=True)
    
    # USE SESSION DATA
    data = st.session_state.session_word_builder
    
    incomplete = [t for t in data if t['id'] not in st.session_state.completed_words]
    if not incomplete:
        st.success("All words built for this session! 🏗️")
        if st.button("Start Over (New Words)"):
            reset_progress()
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
    
    st.markdown(f"""
    <div class="blueprint-container">
        <div class="blueprint-label">BLUEPRINT</div><br>
        <span style='font-size: 3rem;'>📜</span>
        <div class="thought-bubble">{task['meaning']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    parts = task['parts'].copy()
    if st.session_state.wb_difficulty == 'challenge':
        all_parts = [p for t in MASTER_WORD_BUILDER_DATA for p in t['parts']] # Use master for distractors
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
        background-color: white !important;
        color: #333 !important;
        border-radius: 10px !important;
        border: 2px solid #ccc !important;
    }
    .sentence-display {
        font-size: 2.5rem !important; font-weight: bold; color: #333; line-height: 1.5; padding: 20px;
        background: white; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;
    }
    .filled-word { color: #28a745; text-decoration: underline; font-weight: 800; }
    .blank-space { color: #FFCC00; text-decoration: underline; font-weight: 800; }
    div.stButton > button[kind="primary"] {
        background-color: #28a745 !important;
        color: white !important;
        min-height: auto !important;
        padding: 0.5rem !important;
        font-size: 1.2rem !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # USE SESSION DATA
    data = st.session_state.session_sentences
    
    if st.session_state.sent_index >= len(data):
        st.success("You have completed all sentences for this session! 🎓")
        if st.button("Start Over (New Sentences)"):
            reset_progress()
        return

    task = data[st.session_state.sent_index]
    st.markdown(f"**Sentence {st.session_state.sent_index + 1} of {len(data)}**")
    
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
    
    st.markdown("<h3 style='text-align:center; margin-top:2rem; color:#333;'>Choose the missing word:</h3>", unsafe_allow_html=True)
    
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
    
    # Activity Specific CSS
    st.markdown("""
    <style>
    div[data-testid="column"] button {
        font-size: 1.5rem !important; padding: 1rem 2rem !important;
        background-color: white !important; color: #333 !important; border-radius: 30px !important;
        border: 2px solid #003366 !important; height: auto !important;
    }
    div.stButton > button[kind="primary"] {
        background-color: #28a745 !important;
        color: white !important;
    }
    .antonym-clue { font-size: 3rem; font-weight: bold; color: #003366; text-align: center; }
    .antonym-answer-box {
        font-size: 3rem; font-weight: bold; color: #28a745; text-align: center; border: 3px solid #28a745;
        border-radius: 15px; padding: 10px; background-color: white; display: inline-block; min-width: 300px;
    }
    .antonym-placeholder {
        font-size: 3rem; color: #ccc; border-bottom: 3px solid #333; display: inline-block; min-width: 150px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # USE SESSION DATA
    data = st.session_state.session_antonyms
    
    if st.session_state.ant_index >= len(data):
        st.success("All opposites found for this session! ☯️")
        if st.button("Play Again (New Words)"):
            reset_progress()
        return

    task = data[st.session_state.ant_index]
    options_key = f"antonym_options_{task['id']}"
    state_key = f"antonym_state_{task['id']}"
    
    if options_key not in st.session_state:
        options = [task['answer']]
        # Use Master list for distractors
        others = [t['answer'] for t in MASTER_ANTONYM_DATA if t['answer'] != task['answer']]
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

    st.markdown(f"**Word {st.session_state.ant_index + 1} of {len(data)}**")
    st.markdown(f"<div class='antonym-clue'>{task['clue']}</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; font-size: 2.5rem; margin: 10px 0; color:#333;'>⇄</div>", unsafe_allow_html=True)
    
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
    
    # USE SESSION DATA
    data = st.session_state.session_yes_no
    
    if st.session_state.yn_index >= len(data):
        st.success("You finished the questions for this session! ✅")
        if st.button("Restart (New Questions)"):
            reset_progress()
        return

    task = data[st.session_state.yn_index]
    answered_key = f"yn_answered_{task['id']}"
    if answered_key not in st.session_state:
        st.session_state[answered_key] = None
        
    if st.session_state[answered_key] is not None:
        with c_next:
            if st.button("Next Question ➡", key="next_q_top", type="primary"):
                 st.session_state.yn_index += 1
                 st.rerun()
    
    st.markdown(f"""
    <div style="background:white; padding:3rem; border-radius:15px; text-align:center; box-shadow:0 4px 6px rgba(0,0,0,0.1); margin-bottom:2rem; color: #333;">
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
            background-color: white !important;
            color: #333 !important;
            border-radius: 15px !important;
        }
        div.stButton > button[kind="primary"] {
            background-color: #28a745 !important;
            color: white !important;
            min-height: auto !important;
            font-size: 1.2rem !important;
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
    st.markdown("""
    <style>
    .story-box { background-color: #fff; padding: 2rem; border-radius: 10px; border-left: 10px solid #003366; box-shadow: 0 2px 5px rgba(0,0,0,0.1); color: #333; }
    .quiz-box { background-color: #FFCC00; padding: 2rem; border-radius: 10px; color: #003366; box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
    div.stButton > button { background-color: #003366; color: white; border-radius: 5px; height: auto !important; font-size: 1rem !important; }
    div.stButton > button[kind="primary"] { background-color: #28a745 !important; }
    </style>
    """, unsafe_allow_html=True)

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
