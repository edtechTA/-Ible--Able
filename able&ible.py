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
    /* Global Styles */
    .stApp {
        background-color: #f8f9fa;
    }
    .main-header {
        font-family: 'Comic Sans MS', 'Comic Sans', cursive;
        color: #003366;
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sub-header {
        color: #555;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    /* Button Styling - Default Blue */
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

    /* Primary Button Styling (Check Answer) - Green & Big */
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

    /* Activity 1: Syllable Detective */
    [data-testid="stForm"] {
        background-color: #e3f2fd;
        border: 3px dashed #003366;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
    }

    /* Activity 2: Word Builder Zones */
    .wb-workshop {
        background-color: #003366; /* Trident Blue */
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .wb-parts-bin {
        background-color: #FFF3CD; /* Light Gold */
        border: 2px solid #FFCC00;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .built-word-display {
        background-color: white;
        border: 2px solid #003366;
        border-radius: 10px;
        padding: 1rem;
        font-size: 2.5rem;
        font-family: monospace;
        letter-spacing: 5px;
        color: #003366;
        margin-bottom: 2rem;
        display: inline-block;
        min-width: 300px;
    }
    .wb-controls {
        padding: 1rem;
        border-top: 1px solid #ccc;
        margin-top: 2rem;
    }

    /* Activity 3: Sentence Master */
    .sentence-display {
        font-size: 2.5rem !important;
        font-weight: bold;
        color: #333;
        line-height: 1.5;
        padding: 20px;
        background: white;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .filled-word {
        color: #28a745;
        text-decoration: underline;
        font-weight: 800;
    }
    .blank-space {
        color: #FFCC00;
        text-decoration: underline;
        font-weight: 800;
    }
    
    /* Activity 4: Antonym Bubbles */
    .antonym-clue {
        font-size: 3rem;
        font-weight: bold;
        color: #003366;
        text-align: center;
    }
    .antonym-answer-box {
        font-size: 3rem; 
        font-weight: bold; 
        color: #28a745; /* Green for correct */
        text-align: center;
        border: 3px solid #28a745;
        border-radius: 15px;
        padding: 10px;
        background-color: white;
        display: inline-block;
        min-width: 300px;
    }
    .antonym-placeholder {
        font-size: 3rem;
        color: #ccc;
        border-bottom: 3px solid #003366;
        display: inline-block;
        min-width: 150px;
        text-align: center;
    }
    
    /* Activity 6: Reading */
    .story-box {
        background-color: #fff;
        padding: 2rem;
        border-radius: 10px;
        border-left: 10px solid #003366;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .quiz-box {
        background-color: #FFCC00;
        padding: 2rem;
        border-radius: 10px;
        color: #003366;
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
    {"id": 1, "sentencePart1": "The thief did not steal my", "sentencePart2": "ring because he thought it was cheap.", "options": ["valueless", "valuable"], "correctOption": "valueless"},
    {"id": 2, "sentencePart1": "Dad favored going to the beach today, but the weather was", "sentencePart2": "for swimming.", "options": ["favored", "unfavorable"], "correctOption": "unfavorable"},
    {"id": 3, "sentencePart1": "Gas and kerosene will burn easily. They are", "sentencePart2": "liquids.", "options": ["combust", "combustible"], "correctOption": "combustible"},
    {"id": 4, "sentencePart1": "Janet is very dependable. You can always", "sentencePart2": "on her when you need her help.", "options": ["depend", "dependable"], "correctOption": "depend"},
    {"id": 5, "sentencePart1": "My report looked neat and presentable. I", "sentencePart2": "it orally to the class yesterday.", "options": ["presented", "presentable"], "correctOption": "presented"},
    {"id": 6, "sentencePart1": "You can divide twelve by six evenly. However, six is not evenly", "sentencePart2": "by twenty.", "options": ["divide", "divisible"], "correctOption": "divisible"},
    {"id": 7, "sentencePart1": "Can you wash that shirt? I do not think that silk is", "sentencePart2": ".", "options": ["wash", "washable"], "correctOption": "washable"},
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
    }
]

# --- State Management ---
if 'current_activity' not in st.session_state:
    st.session_state.current_activity = None
if 'completed_syllables' not in st.session_state:
    st.session_state.completed_syllables = []
if 'completed_words' not in st.session_state:
    st.session_state.completed_words = []
# Index trackers for one-at-a-time activities
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

# --- Helper Functions ---
def go_home():
    st.session_state.current_activity = None

def celebrate_success():
    """Randomized visual reward system"""
    effect = random.choice(["balloons", "snow", "magic"])
    if effect == "balloons":
        st.balloons()
    elif effect == "snow":
        st.snow()
    else:
        st.toast("✨ Magical! Outstanding Work! ✨", icon="🧙‍♂️")
        time.sleep(0.5)
        st.toast("🌟 You are a Word Wizard! 🌟", icon="⭐")

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
    
    # Reset activity specific session states
    keys_to_remove = [k for k in st.session_state.keys() if k.startswith("antonym_") or k.startswith("yn_answered_")]
    for k in keys_to_remove:
        del st.session_state[k]
        
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
    st.markdown("<h1 class='main-header'>Trident Word Wizards 🧙‍♂️</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Lesson 6: <span style='background:#FFCC00; padding:2px 5px; border-radius:4px'>-able</span> & <span style='background:#FFCC00; padding:2px 5px; border-radius:4px'>-ible</span></p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("✂️ Syllable Split", use_container_width=True):
            st.session_state.current_activity = "SYLLABLES"
            st.rerun()
        if st.button("🔄 Opposites", use_container_width=True):
            st.session_state.current_activity = "ANTONYMS"
            st.rerun()

    with col2:
        if st.button("🔨 Word Builder", use_container_width=True):
            st.session_state.current_activity = "WORD_BUILDER"
            st.rerun()
        if st.button("👍 Yes or No?", use_container_width=True):
            st.session_state.current_activity = "YES_NO"
            st.rerun()

    with col3:
        if st.button("✍️ Sentence Master", use_container_width=True):
            st.session_state.current_activity = "SENTENCE_FILL"
            st.rerun()
        if st.button("📖 Reading Comp", use_container_width=True):
            st.session_state.current_activity = "READING"
            st.rerun()
    
    st.divider()
    if st.button("🗑️ Reset All Progress"):
        reset_progress()

def syllable_splitter():
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
    
    # Layout Separation: Word & Instructions vs Input Box
    st.markdown(f"<div style='text-align:center; font-size:3rem; color:#003366; font-weight:bold; margin-bottom:1rem;'>{task['word']}</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Break the word into parts below. Keep the suffix (-able/-ible) together!</p>", unsafe_allow_html=True)
    
    # Distinct Input Container
    
    cols = st.columns(len(task['correctSyllables']))
    user_inputs = []
    
    with st.form(key=f"syllable_form_{task['id']}"):
        for i, col in enumerate(cols):
            # Using label_visibility="collapsed" to make it cleaner, visual instructions above
            val = col.text_input(f"Syllable {i+1}", key=f"syl_{task['id']}_{i}", label_visibility="visible").strip().lower()
            user_inputs.append(val)
        
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Check Answer")

    if submitted:
        if user_inputs == task['correctSyllables']:
            celebrate_success()
            st.session_state.completed_syllables.append(task['id'])
            
            # AI Explanation
            with st.spinner("Asking the AI Wizard for a tip..."):
                expl = ask_gemini_explanation(task['word'])
                if expl:
                    st.success(f"Wizard says: {expl}")
            
            time.sleep(3)
            st.rerun()
        else:
            play_error()
            st.error("Not quite! Check your splits. Is the suffix in one box?")

def word_builder():
    st.header("🔨 Word Construction Site")
    
    # Difficulty
    col_d1, col_d2 = st.columns([3,1])
    with col_d2:
        diff = st.radio("Mode:", ["normal", "challenge"], index=0 if st.session_state.wb_difficulty == 'normal' else 1, horizontal=True)
    if diff != st.session_state.wb_difficulty:
        st.session_state.wb_difficulty = diff
        st.rerun()

    incomplete = [t for t in WORD_BUILDER_DATA if t['id'] not in st.session_state.completed_words]
    
    if not incomplete:
        st.success("All words built! 🏗️")
        if st.button("Reset Construction"):
            st.session_state.completed_words = []
            st.rerun()
        return

    task = incomplete[0]
    
    # ZONE 1: The Workshop (Meaning only)
    st.markdown("### 1. The Blueprint")
    st.markdown(f"<div class='wb-workshop'><h3>Meaning: {task['meaning']}</h3></div>", unsafe_allow_html=True)
    
    # ZONE 2: Parts Bin AND Build Display
    st.markdown("### 2. Construction Zone")
    
    # State Build
    if 'wb_current_build' not in st.session_state:
        st.session_state.wb_current_build = []
    
    current_word = "".join(st.session_state.wb_current_build) if st.session_state.wb_current_build else "?"
    
    # Shuffle parts
    parts = task['parts'].copy()
    if st.session_state.wb_difficulty == 'challenge':
        all_parts = [p for t in WORD_BUILDER_DATA for p in t['parts']]
        distractors = random.sample(all_parts, 3)
        parts.extend(distractors)
    random.seed(task['id'] + len(parts)) 
    random.shuffle(parts)

    # Start Yellow Box
    st.markdown('<div class="wb-parts-bin">', unsafe_allow_html=True)
    
    # The Word Being Built (Inside Yellow Box)
    st.markdown(f"<div class='built-word-display'>{current_word}</div>", unsafe_allow_html=True)
    st.markdown("<p><b>Click parts to add them:</b></p>", unsafe_allow_html=True)
    
    # Buttons
    b_cols = st.columns(len(parts))
    for i, part in enumerate(parts):
        if b_cols[i].button(part, key=f"btn_{task['id']}_{i}_{len(st.session_state.wb_current_build)}", use_container_width=True):
            st.session_state.wb_current_build.append(part)
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)

    # ZONE 3: Control Panel
    st.markdown('<div class="wb-controls">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    
    with c1:
        if st.button("↺ Reset Word", use_container_width=True):
            st.session_state.wb_current_build = []
            st.rerun()
            
    with c3:
        # Green Primary Button for Check Answer
        if st.button("✅ Check Answer", key="wb_check_btn", type="primary", use_container_width=True):
            built_word = "".join(st.session_state.wb_current_build)
            if built_word == task['targetWord']:
                celebrate_success()
                st.session_state.completed_words.append(task['id'])
                st.session_state.wb_current_build = []
                time.sleep(2)
                st.rerun()
            else:
                play_error()
                st.error(f"Try again! You built '{built_word}'")
                time.sleep(2)
                st.session_state.wb_current_build = []
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def sentence_fill():
    st.header("✍️ Sentence Master")
    
    # Temporary styles to make THESE specific buttons huge
    st.markdown("""
    <style>
    div.stButton > button {
        font-size: 1.5rem !important;
        padding: 1.5rem !important;
        min-height: 100px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    if st.session_state.sent_index >= len(SENTENCE_DATA):
        st.success("You have completed all sentences! 🎓")
        if st.button("Start Over"):
            st.session_state.sent_index = 0
            st.rerun()
        return

    # One sentence at a time
    task = SENTENCE_DATA[st.session_state.sent_index]
    
    st.markdown(f"**Sentence {st.session_state.sent_index + 1} of {len(SENTENCE_DATA)}**")
    
    # Check if a choice was just made (stored in session state for this frame)
    # We use a unique key for the activity state logic
    
    # Display logic: 
    # If correct choice was made: Show filled sentence GREEN
    # If default: Show blank sentence
    
    # Placeholder for the blank
    blank_visual = f"<span class='blank-space'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>"
    
    st.markdown(f"""
    <div class="sentence-display">
        {task['sentencePart1']} {blank_visual} {task['sentencePart2']}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align:center; margin-top:2rem;'>Choose the missing word:</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    # Left Option
    with col1:
        opt1 = task['options'][0]
        if st.button(opt1, key=f"btn_opt1_{task['id']}", use_container_width=True):
            if opt1 == task['correctOption']:
                celebrate_success()
                st.markdown(f"""
                <div class="sentence-display" style="border: 3px solid #28a745;">
                    {task['sentencePart1']} <span class='filled-word'>{opt1}</span> {task['sentencePart2']}
                </div>
                """, unsafe_allow_html=True)
                time.sleep(2)
                st.session_state.sent_index += 1
                st.rerun()
            else:
                play_error()
                st.toast(f"'{opt1}' is not correct. Try the other one!", icon="❌")

    # Right Option
    with col2:
        opt2 = task['options'][1]
        if st.button(opt2, key=f"btn_opt2_{task['id']}", use_container_width=True):
            if opt2 == task['correctOption']:
                celebrate_success()
                st.markdown(f"""
                <div class="sentence-display" style="border: 3px solid #28a745;">
                    {task['sentencePart1']} <span class='filled-word'>{opt2}</span> {task['sentencePart2']}
                </div>
                """, unsafe_allow_html=True)
                time.sleep(2)
                st.session_state.sent_index += 1
                st.rerun()
            else:
                play_error()
                st.toast(f"'{opt2}' is not correct. Try the other one!", icon="❌")

def antonym_activity():
    st.header("🔄 Opposites (Tap to Fill)")
    
    # CSS for larger buttons specific to this activity
    st.markdown("""
    <style>
    div[data-testid="column"] button {
        font-size: 1.5rem !important; 
        padding: 1rem 2rem !important;
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
    
    # State Key for randomness stability
    options_key = f"antonym_options_{task['id']}"
    state_key = f"antonym_state_{task['id']}" # 'unanswered', 'correct'
    
    # Initialize State
    if options_key not in st.session_state:
        # Bubble Bank Generation (Stable per question)
        options = [task['answer']]
        others = [t['answer'] for t in ANTONYM_DATA if t['answer'] != task['answer']]
        options.extend(random.sample(others, min(3, len(others))))
        random.shuffle(options)
        st.session_state[options_key] = options

    if state_key not in st.session_state:
        st.session_state[state_key] = "unanswered"

    options = st.session_state[options_key]
    current_state = st.session_state[state_key]

    st.markdown(f"**Word {st.session_state.ant_index + 1} of {len(ANTONYM_DATA)}**")
    
    # -- UI LAYOUT --
    
    # 1. Clue Word (Top)
    st.markdown(f"<div class='antonym-clue'>{task['clue']}</div>", unsafe_allow_html=True)
    
    # 2. Swap Icon (Middle)
    st.markdown("<div style='text-align:center; font-size: 2.5rem; margin: 10px 0;'>⇄</div>", unsafe_allow_html=True)
    
    # 3. Answer/Placeholder Area (Bottom)
    # Construct HTML first to ensure proper nesting for centering
    answer_html = "<div style='text-align:center; margin-bottom: 2rem;'>"
    if current_state == "correct":
         answer_html += f"<div class='antonym-answer-box'>{task['answer']}</div>"
    else:
         answer_html += "<div class='antonym-placeholder'>?</div>"
    answer_html += "</div>"
    
    st.markdown(answer_html, unsafe_allow_html=True)
    
    # -- LOGIC & BUTTONS --
    
    if current_state == "unanswered":
        st.info("Tap the bubble that means the opposite!")
        cols = st.columns(len(options))
        for i, opt in enumerate(options):
            # Key uses index 'i' but options list is now STABLE in session state
            if cols[i].button(opt, key=f"ant_btn_{task['id']}_{i}", use_container_width=True):
                if opt == task['answer']:
                    celebrate_success()
                    st.session_state[state_key] = "correct"
                    st.rerun()
                else:
                    play_error()
    else:
        # Correct State - Show Next Button
        if st.button("Next Word ➡", type="primary"):
            st.session_state.ant_index += 1
            st.rerun()

def yes_no_activity():
    st.header("👍 Yes or No?")

    # Inject specific styles for MASSIVE buttons in this activity
    st.markdown("""
    <style>
    div.stButton > button {
        font-size: 3rem !important;
        padding: 2rem !important;
        min-height: 150px;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    if st.session_state.yn_index >= len(YES_NO_DATA):
        st.success("You finished the questions! ✅")
        if st.button("Restart"):
            st.session_state.yn_index = 0
            st.rerun()
        return

    task = YES_NO_DATA[st.session_state.yn_index]
    
    # Card View
    st.markdown(f"""
    <div style="background:white; padding:3rem; border-radius:15px; text-align:center; box-shadow:0 4px 6px rgba(0,0,0,0.1); margin-bottom:2rem;">
        <h2 style="color:#003366;">{task['question']}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # State to show result
    if f"yn_answered_{task['id']}" not in st.session_state:
        st.session_state[f"yn_answered_{task['id']}"] = None

    if st.session_state[f"yn_answered_{task['id']}"] is None:
        c1, c2 = st.columns(2)
        if c1.button("YES 👍", use_container_width=True):
            if task['answer'] == True:
                celebrate_success()
                st.session_state[f"yn_answered_{task['id']}"] = "correct"
            else:
                play_error()
                st.session_state[f"yn_answered_{task['id']}"] = "wrong"
            st.rerun()
            
        if c2.button("NO 👎", use_container_width=True):
            if task['answer'] == False:
                celebrate_success()
                st.session_state[f"yn_answered_{task['id']}"] = "correct"
            else:
                play_error()
                st.session_state[f"yn_answered_{task['id']}"] = "wrong"
            st.rerun()
            
    else:
        # Show Feedback and Next Button
        if st.session_state[f"yn_answered_{task['id']}"] == "correct":
            st.success("Correct Answer!")
        else:
            st.error("Oops! That was incorrect.")
            
        if st.button("Next Question ➡"):
            st.session_state.yn_index += 1
            st.rerun()

def reading_activity():
    st.header("📖 Reading Comprehension")
    
    story = READING_STORIES[st.session_state.reading_story_index]
    
    # Font Size Slider
    font_size = st.slider("Adjust Text Size:", min_value=16, max_value=32, value=20)
    
    col_story, col_quiz = st.columns([2, 1])
    
    with col_story:
        # Construct the HTML content manually so the style wrapper applies to all text
        story_html = f"""
        <div class='story-box' style='font-size:{font_size}px; line-height: 1.6;'>
            <h3 style='color:#003366; margin-bottom:1rem;'>{story['title']}</h3>
        """
        
        for p in story['paragraphs']:
            story_html += f"<p style='margin-bottom:1rem;'>{p}</p>"
            
        story_html += "</div>"
        
        st.markdown(story_html, unsafe_allow_html=True)
        
        # Read Confirmation
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
                st.write(f"**Q{q_idx+1}: {q['question']}**")
                
                # Use a placeholder for the answer key to reset on new questions
                ans_key = f"read_q_{story['id']}_{q_idx}"
                ans = st.radio("Choose:", q['options'], key=ans_key)
                
                if st.button("Check Answer", key=f"chk_{ans_key}"):
                    if ans == q['correctAnswer']:
                        celebrate_success()
                        st.success("Correct!")
                        time.sleep(1.5)
                        st.session_state.reading_quiz_index += 1
                        st.rerun()
                    else:
                        play_error()
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
