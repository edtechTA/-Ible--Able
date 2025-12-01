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

# Custom CSS for Trident Academy Branding
st.markdown("""
<style>
    /* Trident Colors: Blue #003366, Gold #FFCC00 */
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
    .activity-card {
        background-color: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        border: 2px solid transparent;
        transition: all 0.3s ease;
        height: 100%;
    }
    .activity-card:hover {
        border-color: #003366;
        transform: translateY(-5px);
    }
    .stButton button {
        background-color: #003366;
        color: white;
        border-radius: 20px;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton button:hover {
        background-color: #004080;
        color: #FFCC00;
    }
    .success-text {
        color: #28a745;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .error-text {
        color: #dc3545;
        font-weight: bold;
    }
    .word-display {
        font-size: 3rem;
        font-weight: bold;
        color: #003366;
        text-align: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# --- Gemini Setup ---
# Tries to get API key from Streamlit secrets first, then environment variable
api_key = st.secrets.get("API_KEY") or os.environ.get("API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

# --- Constants & Data ---
# Ported directly from constants.ts

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
    },
    {
        "id": 3,
        "title": "The Adorable Puppy",
        "paragraphs": [
            "Sarah wanted a dog for a long time. Her parents said she had to be responsible before she could get one. Finally, they agreed.",
            "They visited the shelter and found a small, adorable puppy. He was very excitable and jumped all over Sarah.",
            "At first, the puppy's behavior was terrible. He chewed shoes and barked all night. Sarah wondered if he would ever be manageable.",
            "With patience and treats, the puppy learned to sit. He became a lovable member of the family."
        ],
        "questions": [
            {"question": "What did Sarah need to be before getting a dog?", "options": ["Excitable", "Responsible", "Invisible", "Possible"], "correctAnswer": "Responsible"},
            {"question": "The puppy was described as:", "options": ["Miserable", "Combustible", "Adorable", "Available"], "correctAnswer": "Adorable"},
            {"question": "Eventually, the puppy became:", "options": ["Unmanageable", "Lovable", "Horrible", "Breakable"], "correctAnswer": "Lovable"}
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
if 'sentence_scores' not in st.session_state:
    st.session_state.sentence_scores = set()
if 'antonym_scores' not in st.session_state:
    st.session_state.antonym_scores = set()
if 'wb_difficulty' not in st.session_state:
    st.session_state.wb_difficulty = 'normal'

# --- Helper Functions ---
def go_home():
    st.session_state.current_activity = None

def play_success():
    st.toast("Awesome Job! 🎉", icon="⭐")
    st.balloons()

def play_error():
    st.toast("Try Again!", icon="❌")

def reset_progress():
    st.session_state.completed_syllables = []
    st.session_state.completed_words = []
    st.session_state.sentence_scores = set()
    st.session_state.antonym_scores = set()
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

def generate_new_words():
    if not api_key:
        return []
    try:
        prompt = """Generate 3 new words ending in -able or -ible suitable for a Lesson 6 Orton-Gillingham reading exercise. 
        Return them exactly in this format: word|part1-part2-part3
        Example: incredible|in-cred-ible
        Ensure they are distinct from: presentable, miserable, valuable, impossible."""
        response = model.generate_content(prompt)
        lines = response.text.split('\n')
        new_tasks = []
        for line in lines:
            if '|' in line:
                word, parts = line.split('|')
                new_tasks.append({
                    "id": random.randint(1000,9999),
                    "word": word.strip(),
                    "correctSyllables": parts.strip().split('-')
                })
        return new_tasks
    except:
        return []

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
    
    # Progress Bar
    total = len(SYLLABLE_DATA)
    completed = len(st.session_state.completed_syllables)
    st.progress(completed / total if total > 0 else 0)
    st.caption(f"Progress: {completed}/{total} words")

    # Select Task (find first incomplete or random)
    incomplete = [t for t in SYLLABLE_DATA if t['id'] not in st.session_state.completed_syllables]
    
    if not incomplete:
        st.success("You've mastered all words! 🎉")
        if st.button("Start Over"):
            st.session_state.completed_syllables = []
            st.rerun()
        return

    task = incomplete[0]
    
    st.markdown(f"<div class='word-display'>{task['word']}</div>", unsafe_allow_html=True)
    st.info("Break the word into parts. Remember: keep the suffix (-able/-ible) together in the last box!")

    # Dynamic Columns for Inputs
    cols = st.columns(len(task['correctSyllables']))
    user_inputs = []
    
    with st.form(key=f"syllable_form_{task['id']}"):
        for i, col in enumerate(cols):
            val = col.text_input(f"Part {i+1}", key=f"syl_{task['id']}_{i}").strip().lower()
            user_inputs.append(val)
        
        submitted = st.form_submit_button("Check Answer")
        
        if submitted:
            if user_inputs == task['correctSyllables']:
                play_success()
                st.session_state.completed_syllables.append(task['id'])
                
                # AI Explanation
                with st.spinner("Asking the AI Wizard for a tip..."):
                    expl = ask_gemini_explanation(task['word'])
                    if expl:
                        st.markdown(f"> *Wizard says:* {expl}")
                
                time.sleep(2)
                st.rerun()
            else:
                play_error()
                st.error("Not quite! Check your splits. Is the suffix in one box?")

def word_builder():
    st.header("🔨 Word Construction Site")
    
    # Difficulty Toggle
    diff = st.radio("Difficulty:", ["normal", "challenge"], index=0 if st.session_state.wb_difficulty == 'normal' else 1, horizontal=True)
    if diff != st.session_state.wb_difficulty:
        st.session_state.wb_difficulty = diff
        st.rerun()

    # Get Incomplete Task
    incomplete = [t for t in WORD_BUILDER_DATA if t['id'] not in st.session_state.completed_words]
    
    if not incomplete:
        st.success("All words built! 🏗️")
        if st.button("Reset Construction"):
            st.session_state.completed_words = []
            st.rerun()
        return

    task = incomplete[0]
    
    st.markdown(f"### Meaning: *{task['meaning']}*")
    
    # Setup Parts
    parts = task['parts'].copy()
    if st.session_state.wb_difficulty == 'challenge':
        # Add distractors
        all_parts = [p for t in WORD_BUILDER_DATA for p in t['parts']]
        distractors = random.sample(all_parts, 3)
        parts.extend(distractors)
    
    # Shuffle parts (seed by task id to keep stable during interaction)
    random.seed(task['id'] + len(parts)) 
    random.shuffle(parts)

    # State for current building attempt
    if 'wb_current_build' not in st.session_state:
        st.session_state.wb_current_build = []
    
    # Display Built Word So Far
    st.markdown(f"<div style='font-size:2rem; font-family:monospace; background:#e9ecef; padding:1rem; border-radius:10px; text-align:center; letter-spacing: 5px;'>{''.join(st.session_state.wb_current_build)}</div>", unsafe_allow_html=True)
    
    st.write("---")
    st.write("Click parts to add them:")
    
    # Buttons for parts
    # To avoid rerun issues wiping state instantly, we use callbacks or check click state
    cols = st.columns(4)
    for i, part in enumerate(parts):
        if cols[i % 4].button(part, key=f"btn_{task['id']}_{i}"):
            st.session_state.wb_current_build.append(part)
            st.rerun()

    col_act1, col_act2 = st.columns(2)
    if col_act1.button("Checking Answer..."):
        # Dummy button, logic is below
        pass
    
    if col_act1.button("✅ Check Word"):
        built_word = "".join(st.session_state.wb_current_build)
        if built_word == task['targetWord']:
            play_success()
            st.session_state.completed_words.append(task['id'])
            st.session_state.wb_current_build = [] # Reset for next
            time.sleep(1)
            st.rerun()
        else:
            play_error()
            st.error(f"Try again! You built '{built_word}'")
            time.sleep(1)
            st.session_state.wb_current_build = []
            st.rerun()
            
    if col_act2.button("↺ Reset"):
        st.session_state.wb_current_build = []
        st.rerun()

def sentence_fill():
    st.header("✍️ Sentence Master")
    
    score = len(st.session_state.sentence_scores)
    st.caption(f"Score: {score}/{len(SENTENCE_DATA)}")
    
    for task in SENTENCE_DATA:
        container = st.container()
        container.markdown(f"**{task['sentencePart1']} _____ {task['sentencePart2']}**")
        
        # Unique key for each radio
        choice = container.radio("Choose:", task['options'], key=f"sent_{task['id']}", horizontal=True)
        
        if container.button("Check", key=f"btn_sent_{task['id']}"):
            if choice == task['correctOption']:
                play_success()
                st.session_state.sentence_scores.add(task['id'])
                container.success(f"Correct! The sentence is: {task['sentencePart1']} {choice} {task['sentencePart2']}")
            else:
                play_error()
                container.error("Try again.")
        st.divider()

def antonym_activity():
    st.header("🔄 Opposites Attract")
    
    score = len(st.session_state.antonym_scores)
    st.caption(f"Score: {score}/{len(ANTONYM_DATA)}")
    
    # Word Bank
    st.info(f"Word Bank: {', '.join([t['answer'] for t in ANTONYM_DATA])}")
    
    for task in ANTONYM_DATA:
        col1, col2 = st.columns([1, 2])
        col1.markdown(f"**{task['clue']}**")
        ans = col2.text_input("Opposite:", key=f"ant_{task['id']}").strip().lower()
        
        if ans:
            if ans == task['answer']:
                if task['id'] not in st.session_state.antonym_scores:
                    play_success()
                    st.session_state.antonym_scores.add(task['id'])
                col2.success("Correct!")
            else:
                col2.warning("Keep trying...")

def yes_no_activity():
    st.header("👍 Yes or No?")
    
    for task in YES_NO_DATA:
        st.subheader(task['question'])
        col1, col2 = st.columns(2)
        
        yes = col1.button("YES", key=f"yes_{task['id']}", use_container_width=True)
        no = col2.button("NO", key=f"no_{task['id']}", use_container_width=True)
        
        if yes:
            if task['answer'] == True:
                play_success()
                st.success("Correct!")
            else:
                play_error()
                st.error("Incorrect.")
        
        if no:
            if task['answer'] == False:
                play_success()
                st.success("Correct!")
            else:
                play_error()
                st.error("Incorrect.")
        st.divider()

def reading_activity():
    st.header("📖 Reading Comprehension")
    
    if 'current_story_idx' not in st.session_state:
        st.session_state.current_story_idx = 0
        
    story = READING_STORIES[st.session_state.current_story_idx]
    
    col_s1, col_s2 = st.columns([2, 1])
    
    with col_s1:
        st.subheader(story['title'])
        for p in story['paragraphs']:
            st.write(p)
            st.write("") # spacing
            
    with col_s2:
        if st.button("🔄 Read Another Story"):
            # Cycle story
            st.session_state.current_story_idx = (st.session_state.current_story_idx + 1) % len(READING_STORIES)
            st.rerun()
            
        st.markdown("### Quiz")
        for i, q in enumerate(story['questions']):
            st.write(f"**{i+1}. {q['question']}**")
            ans = st.radio("Answer:", q['options'], key=f"read_q_{story['id']}_{i}")
            
            if st.button(f"Check Q{i+1}", key=f"chk_read_{story['id']}_{i}"):
                if ans == q['correctAnswer']:
                    play_success()
                else:
                    play_error()

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