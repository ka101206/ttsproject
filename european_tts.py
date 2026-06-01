import wave
import threading
import os
import re
from piper.voice import PiperVoice

class EuropeanTTSEngine:
    def __init__(self, audio_player=None):
        self.model_files = {
            "Spanish": "models/es_ES-sharvard-medium.onnx",
            "French": "models/fr_FR-tom-medium.onnx",
            "Italian": "models/it_IT-riccardo-x_low.onnx"
        }
        self.voice = None
        self.current_lang = None
        self.lock = threading.Lock()
        self.audio_player = audio_player  # callback: play_audio(filepath) -> blocks until done

    def load_voice(self, language):
        if language != self.current_lang:
            path = self.model_files.get(language)
            if path and os.path.exists(path):
                self.voice = PiperVoice.load(path)
                self.current_lang = language
                print(f"✅ Successfully loaded {language} neural model.")
            else:
                print(f"❌ Error: Model file not found for {language} at {path}")

    def speak(self, text, language, speed=1.0, on_start=None, on_done=None):
        threading.Thread(target=self._run_speak, args=(text, language, speed, on_start, on_done), daemon=True).start()

    def _run_speak(self, text, language, speed, on_start, on_done):
        with self.lock: 
            self.load_voice(language)
            if not self.voice:
                return

            if on_start:
                on_start()
            
            # Get the NATIVE sample rate from the model itself
            native_rate = self.voice.config.sample_rate
            
            chunks = re.split(r'(?<=[.!?])', text)
            output_file = "output_euro.wav"
            
            # Neural Speed (Preserves Pitch)
            l_scale = 1.0 / max(0.1, float(speed))
            
            # Inject length_scale directly into the config to avoid wrapper errors
            if hasattr(self.voice, 'config'):
                self.voice.config.length_scale = l_scale

            print(f"⏩ {language} | Rate: {native_rate}Hz | Speed: {speed}x")

            for chunk in chunks:
                clean_chunk = chunk.strip()
                if not clean_chunk:
                    continue
                
                import uuid
                output_file = f"output_euro_{uuid.uuid4().hex}.wav"
                    
                try:
                    with wave.open(output_file, "wb") as wav_file:
                        wav_file.setnchannels(1)
                        wav_file.setsampwidth(2)
                        wav_file.setframerate(native_rate)
                        
                        for result in self.voice.synthesize(clean_chunk):
                            wav_file.writeframes(result.audio_int16_bytes)
                            
                except Exception as e:
                    print(f"❌ Piper Synthesis Error: {e}")
                    continue
                
                if os.path.exists(output_file) and os.path.getsize(output_file) > 44:
                    # Play audio via browser callback
                    if self.audio_player:
                        self.audio_player(output_file)
                    else:
                        print("⚠️ No audio player configured, skipping playback")
            
            if on_done:
                on_done()