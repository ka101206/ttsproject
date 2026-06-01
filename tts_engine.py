import os
import glob
import soundfile as sf
import threading
import re 

from kokoro_onnx import Kokoro
from misaki import ja 

class TTSEngine:
    def __init__(self, audio_player=None):
        self.engine = None
        self.ja_g2p = ja.JAG2P()
        self.lock = threading.Lock()
        self.cache = {}
        self.current_ja_voice = "jf_alpha"
        self.audio_player = audio_player  # callback: play_audio(filepath) -> blocks until done
        threading.Thread(target=self._init_engine, daemon=True).start()

    def _init_engine(self):
        with self.lock:
            if self.engine: return self.engine
            target_model = "kokoro-v1.0.onnx"
            if not os.path.exists(target_model):
                found = glob.glob("*.onnx")
                target_model = found[0] if found else None
            if not target_model:
                print("❌ TTS Error: No .onnx file found!")
                return None
            try:
                self.engine = Kokoro(target_model, "voices.bin")
                print("✅ Japanese TTS Engine (Kokoro) loaded successfully!")
                return self.engine
            except Exception as e:
                print(f"❌ TTS Init Error: {e}")
                return None

    def set_voice(self, ja_voice):
        self.current_ja_voice = ja_voice

    def speak(self, text, speed=1.0, is_japanese=True, on_start=None, on_done=None):
        threading.Thread(target=self._run_speak, args=(text, speed, on_start, on_done)).start()
        
    def _run_speak(self, text, speed, on_start, on_done):
        engine = self._init_engine()
        if not engine: return

        with self.lock:
            try:
                if on_start: on_start()
                
                # Split text strictly by Japanese punctuation
                chunks = re.split(r'(?<=[。！？])', text)

                for chunk in chunks:
                    clean_chunk = chunk.strip()
                    if not clean_chunk:
                        continue 
                        
                    cache_key = (clean_chunk, self.current_ja_voice, speed)
                    if cache_key in self.cache:
                        samples, sample_rate = self.cache[cache_key]
                        print(f"🔊 Using cached audio for: {clean_chunk}")
                    else:
                        print(f"🔊 Generating audio for chunk: {clean_chunk}")
                        phonemes, _ = self.ja_g2p(clean_chunk)
                        samples, sample_rate = engine.create(
                            phonemes, voice=self.current_ja_voice, speed=speed, lang="j", is_phonemes=True
                        )
                        self.cache[cache_key] = (samples, sample_rate)

                    import uuid
                    filename = f'temp_audio_{uuid.uuid4().hex}.mp3'
                    sf.write(filename, samples, sample_rate)

                    # Play audio via browser callback
                    if self.audio_player:
                        self.audio_player(filename)
                    else:
                        print("⚠️ No audio player configured, skipping playback")

            except Exception as e:
                print(f"❌ Audio Error: {e}")
            finally:
                if on_done: on_done()
