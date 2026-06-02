import config
from ai_client import AIClient
import json

ai = AIClient()
diff = config.DIFFICULTY_SCALES["Chinese"][0] # "HSK 1-2 (Beginner)"
import re
match = re.search(r'\((.*?)\)', diff)
level = match.group(1) if match else "Intermediate"

try:
    reply, success = ai.get_reply("你好", "Chinese", level)
    print("SUCCESS:", success)
    print("REPLY:", reply)
except Exception as e:
    print("EXCEPTION:", e)
