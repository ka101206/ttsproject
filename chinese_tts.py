import asyncio
import threading
import edge_tts
import os

class ChineseTTSEngine:
    def __init__(self, audio_player=None):
        print("Loading Edge-TTS Engine (Chinese)...")
        # "Xiaoxiao" is the world-renowned 'gold standard' for natural Chinese TTS
        self.voice = "zh-CN-XiaoxiaoNeural" 
        self.audio_player = audio_player  # callback: play_audio(filepath) -> blocks until done

    def speak(self, text, speed=1.0, on_start=None, on_done=None):
        """Threaded wrapper to keep the GUI responsive."""
        threading.Thread(target=self._run_speak, args=(text, speed, on_start, on_done), daemon=True).start()

    def _run_speak(self, text, speed, on_start, on_done):
        if on_start:
            on_start()
            
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self._generate_and_play(text, speed))
            loop.close()
        except Exception as e:
            print(f"Chinese TTS Error: {e}")
        finally:
            if on_done:
                on_done()

    async def _generate_and_play(self, text, speed):
        import uuid
        temp_file = f"temp_zh_{uuid.uuid4().hex}.mp3"
        
        # Convert float speed to Edge-TTS string rate
        rate_percent = int((speed - 1.0) * 100)
        rate_str = f"{rate_percent:+d}%"
        
        # 1. Generate the audio from Microsoft's Neural servers
        communicate = edge_tts.Communicate(text, self.voice, rate=rate_str)
        await communicate.save(temp_file)
        
        # 2. Play audio via browser callback
        if self.audio_player:
            self.audio_player(temp_file)
        else:
            print("⚠️ No audio player configured, skipping playback")
            
        # 3. Clean up the temp file
