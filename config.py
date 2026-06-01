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