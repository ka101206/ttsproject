# config.py
import os

# --- API Settings ---
AI_MODEL = "qwen2.5" 
AI_API_URL = "http://host.docker.internal:11434/v1" 
API_KEY = "ollama" 

# --- Language Definitions ---
SUPPORTED_LANGUAGES = ["Japanese", "Spanish", "French", "Italian", "Chinese", "Korean"]
JAPANESE_MODES = ["なし", "ふりがな", "かなのみ"]

# --- Audio Settings ---
DEFAULT_SILENCE_TIMEOUT = 2.5  
DEFAULT_SENSITIVITY = 50.0
DEFAULT_TTS_SPEED = 1.2        

# --- UI Bounds ---
TIMEOUT_RANGE = (1.0, 10.0)
SPEED_RANGE = (1.0, 2.0)
SENSITIVITY_RANGE = (0.0, 100.0)

# --- Immersion Mode ---
IMMERSION_MODE = False

# --- Difficulty Settings ---
DIFFICULTY_SCALES = {
    "Japanese": ["N5 (Beginner)", "N4 (Elementary)", "N3 (Intermediate)", "N2 (Pre-Advanced)", "N1 (Advanced)"],
    "Chinese": ["HSK 1-2 (Beginner)", "HSK 3 (Elementary)", "HSK 4 (Intermediate)", "HSK 5 (Pre-Advanced)", "HSK 6 (Advanced)"],
    "Korean": ["TOPIK 1 (Beginner)", "TOPIK 2 (Elementary)", "TOPIK 3 (Intermediate)", "TOPIK 4 (Pre-Advanced)", "TOPIK 5-6 (Advanced)"],
    "Spanish": ["A1 (Beginner)", "A2 (Elementary)", "B1 (Intermediate)", "B2 (Upper Intermediate)", "C1-C2 (Advanced)"],
    "French": ["A1 (Beginner)", "A2 (Elementary)", "B1 (Intermediate)", "B2 (Upper Intermediate)", "C1-C2 (Advanced)"],
    "Italian": ["A1 (Beginner)", "A2 (Elementary)", "B1 (Intermediate)", "B2 (Upper Intermediate)", "C1-C2 (Advanced)"]
}

DIFFICULTY_PROMPT_MODIFIERS = {
    "Beginner": "VOCABULARY: Very simple, high-frequency words. SENTENCES: Short, simple syntax. GRAMMAR: Strictly basic tenses and structures. Avoid complex conjugation.",
    "Elementary": "VOCABULARY: Common everyday words. SENTENCES: Simple to compound sentences. GRAMMAR: Foundational grammar structures.",
    "Intermediate": "VOCABULARY: Varied everyday and situational vocabulary. SENTENCES: Compound and basic complex sentences. GRAMMAR: Moderate complexity.",
    "Pre-Advanced": "VOCABULARY: Broad range of vocabulary, including some idioms. SENTENCES: Complex syntax. GRAMMAR: Advanced structures allowed.",
    "Advanced": "VOCABULARY: Native-level, unrestricted. Use idioms and nuanced words. SENTENCES: Highly complex and completely natural. GRAMMAR: Full, unrestricted grammatical range."
}

DIFFICULTY_SPEEDS = {
    "Beginner": 0.8,
    "Elementary": 0.9,
    "Intermediate": 1.0,
    "Pre-Advanced": 1.1,
    "Advanced": 1.2
}

# --- Scenarios ---
SCENARIOS = {
    "Restaurant": {
        "title": "Ordering at a Restaurant",
        "user_role": "Customer",
        "ai_role": "Waiter",
        "user_goal": "Order a random dish.",
        "goal": "The user must order a specific dish. (Asking for recommendations or asking what is on the menu is NOT ordering. They must explicitly place an order).",
        "start_instruction": "Welcome the customer and politely ask if they have decided on their order. If the target language is Japanese, you MUST say exactly: 'いらっしゃいませ。ご注文はお決まりですか？'",
        "persona_instruction": "You are a professional waiter. Speak ONLY in natural, polite customer service language appropriate for the target language (e.g. Keigo in Japanese, formal 'usted' in Spanish). Do NOT use casual language. Keep your responses short."
    },
    "Classroom": {
        "title": "New Class Introduction",
        "user_role": "New Student",
        "ai_role": "Teacher",
        "user_goal": "Introduce your name, age, hobby, and end with a greeting.",
        "goal": "The user must introduce their name, age, AND hobby, and end with a greeting. (They must provide ALL 4 pieces of information).",
        "start_instruction": "Warmly introduce the new student to the class and ask them to introduce themselves. If the target language is Japanese, you MUST say exactly: '新しい生徒を紹介します。自己紹介をお願いします。'",
        "persona_instruction": "You are a friendly teacher. Speak politely but warmly and naturally to your students. Keep your responses short."
    },
    "Shopping": {
        "title": "Buying Clothes",
        "user_role": "Customer",
        "ai_role": "Shop Clerk",
        "user_goal": "Ask for a different size of clothing and buy it.",
        "goal": "The user must ask if a different size is available. You must say yes and offer it. Then, the user must explicitly say they will buy it. Do NOT append [GOAL_REACHED] until they explicitly declare they are buying it.",
        "start_instruction": "Welcome the customer and ask if they are looking for anything specific. If the target language is Japanese, you MUST say exactly: 'いらっしゃいませ。何かお探しですか？'",
        "persona_instruction": "You are a polite retail shop clerk. Speak ONLY in natural, polite customer service language appropriate for the target language (e.g. Keigo in Japanese). Keep your responses short."
    },
    "Directions": {
        "title": "Asking for Directions",
        "user_role": "Tourist",
        "ai_role": "Local",
        "user_goal": "Ask how to get to the train station and thank them.",
        "goal": "The user must ask for directions to the train station. You must give them directions. Then, the user must explicitly thank you. Do NOT append [GOAL_REACHED] until they explicitly thank you for the directions.",
        "start_instruction": "Notice the tourist looking lost and politely ask if they need help. If the target language is Japanese, you MUST say exactly: 'どうかしましたか？道に迷いましたか？'",
        "persona_instruction": "You are a helpful local citizen. Speak politely and naturally to a stranger. Keep your responses short."
    },
    "Convenience Store": {
        "title": "Convenience Store Checkout",
        "user_role": "Customer",
        "ai_role": "Cashier",
        "user_goal": "State whether you need a plastic bag, then pay.",
        "goal": "The user must state if they need a plastic bag. You must then ask for payment. Finally, the user must explicitly say they are paying (e.g. 'I will pay by card' or 'Here is the cash'). Do NOT append [GOAL_REACHED] until they explicitly pay.",
        "start_instruction": "Welcome the customer and ask if they need a plastic bag for their items. If the target language is Japanese, you MUST say exactly: 'いらっしゃいませ。レジ袋はご利用ですか？'",
        "persona_instruction": "You are a fast-paced convenience store cashier. Speak ONLY in standard customer service language appropriate for the target language (e.g. Keigo in Japanese). Keep your responses short."
    }
}