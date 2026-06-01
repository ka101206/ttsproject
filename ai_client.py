# ai_client.py
import openai
import re
import config

class AIClient:
    def __init__(self):
        base_url = config.AI_API_URL.split("/chat/completions")[0]
        self.client = openai.OpenAI(api_key=config.API_KEY, base_url=base_url)
        self.model = config.AI_MODEL
        self.conversation_history = [] 

    def clear_history(self):
        self.conversation_history = []
        
    def get_reply(self, user_text, target_language, difficulty="Intermediate"):
        system_prompt = f"""[ROLE]
You are a human language exchange partner chatting via text message. You are NOT an AI assistant. You are brief, natural, and highly conversational.

[CORE RULES - ALL LANGUAGES]
1. LENGTH LIMIT: Maximum 30 words. 1-2 sentences.
2. NO ESSAYS: Never use lists, bullet points, or multiple pieces of advice. ONE brief thought, ONE question.
3. THE TWO-WAY MIRROR (DYNAMIC FORMALITY):
   - You MUST match the user's exact level of formality based on their latest message.
   - If the user speaks formally, YOU MUST SPEAK FORMALLY.
   - If the user speaks casually/informally, YOU MUST SPEAK CASUALLY.
   - Do not mix formal and casual grammar in the same response.
4. SAFETY FILTER: Do not discuss or generate content that is violent, explicit, R-18, or inappropriate for a school environment. Graciously decline if prompted.

[LANGUAGE RULES: {target_language}]
1. EXCLUSIVE LANGUAGE: Speak ONLY in {target_language}.
"""

        if target_language == "Japanese":
            system_prompt += """2. JAPANESE FORMALITY DETECTION:
   - FORMAL MODE TRIGGER: If the user uses です, ます, でしょうか, or polite phrasing, you MUST reply using standard polite Japanese (丁寧語 - です/ます).
   - CASUAL MODE TRIGGER: If the user uses だ, 俺, さ, よ, or dictionary-form verbs, you MUST reply using casual Japanese (タメ口 - だ/ね/よ). In this mode, ZERO polite tokens (です/ます) are allowed.
3. VOCABULARY: No English words allowed except universally recognized Romaji (e.g., AI, OK, USB). No Hanzi.

[CORRECT EXAMPLES OF MIRRORING]
User (Formal): 相談があるんですが、いいでしょうか？
You (Formal): もちろんです！どのようなご相談ですか？

User (Casual): 相談があるんだけど、いいかな？
You (Casual): もちろん！何でも聞いてね。"""
        else:
            system_prompt += f"""2. FORMALITY DETECTION: Strictly obey the 'Two-Way Mirror' rule for {target_language} grammar."""

        # Inject difficulty rules
        diff_rules = config.DIFFICULTY_PROMPT_MODIFIERS.get(difficulty, config.DIFFICULTY_PROMPT_MODIFIERS["Intermediate"])
        system_prompt += f"""\n\n[DIFFICULTY LEVEL: {difficulty}]
You must strictly constrain your language to match the requested difficulty tier:
{diff_rules}"""

        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(self.conversation_history)
        messages.append({"role": "user", "content": user_text})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.2, 
                max_tokens=60
            )
            ai_reply = self._cleanup_text(response.choices[0].message.content)
            self.conversation_history.append({"role": "user", "content": user_text})
            self.conversation_history.append({"role": "assistant", "content": ai_reply})
            if len(self.conversation_history) > 12: self.conversation_history = self.conversation_history[-12:]
            return ai_reply, True
        except Exception as e:
            return f"Error: {str(e)}", False
        
    def get_stateless_reply(self, prompt):
        """Used for the Grammar Tutor. Does not read from or save to conversation history."""
        
        system_prompt = """[ROLE]
You are an expert language grammar tutor. 
Your job is to explain grammar, sentence structure, and vocabulary clearly and concisely in English. 
Break down the components of the sentences provided to you so a learner can easily understand them.
Feel free to use formatting like bullet points or newlines if it helps clarify the grammar."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.2, 
                max_tokens=300 # Explanations need more tokens than the 60 used in standard chat
            )
            # We don't use self._cleanup_text here because we WANT to allow 
            # newlines and bullet points for grammar explanations.
            ai_reply = response.choices[0].message.content.strip()
            return ai_reply, True
            
        except Exception as e:
            return f"Error: {str(e)}", False

    def _cleanup_text(self, text):
        lines = text.split('\n')
        cleaned_lines = [line.strip() for line in lines if any(c.isalnum() for c in line)]
        reply = " ".join(cleaned_lines)
        reply = re.sub(r'^[。・•\-\*]\s*', '', reply)
        return reply.strip()