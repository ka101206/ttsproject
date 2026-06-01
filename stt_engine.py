# stt_engine.py
import speech_recognition as sr
import numpy as np
import io
import wave
import queue
import time

class STTEngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.sample_rate = 16000
        self.audio_queue = queue.Queue()

    def get_rms(self, block):
        return np.sqrt(np.mean(np.square(block.astype(float))))

    def listen_and_transcribe(self, target_language, timeout=2.5, sensitivity=50.0, status_check=None):
        # Clear any stale audio from the queue before starting
        while not self.audio_queue.empty():
            try:
                self.audio_queue.get_nowait()
            except queue.Empty:
                break

        try:
            # We don't have a reliable ambient noise calibration because we can't block
            # the browser from sending, and the browser mic has its own AGC.
            # We'll use a fixed conservative threshold modified by sensitivity.
            ambient_rms = 100.0
            sens_factor = max(0.01, 2.0 - (sensitivity / 50.0))
            threshold = max(ambient_rms * 1.5 * sens_factor, 300 * sens_factor)
                
            audio_data = []
            pre_speech_buffer = []
            silence_timer = 0.0
            has_spoken = False
            
            # This loop reads chunks pushed by the browser over HTTP
            while True:
                # Kill switch if the user turns off conversation mode mid-listen
                if status_check and not status_check():
                    return "ERROR: Cancelled"
                    
                try:
                    # Browser sends chunks every ~0.25s (4096 frames at 16kHz)
                    chunk_bytes = self.audio_queue.get(timeout=0.5)
                    chunk = np.frombuffer(chunk_bytes, dtype=np.int16)
                    # Reshape for RMS calculation if needed, or just leave flat
                    chunk = chunk.reshape(-1, 1)
                except queue.Empty:
                    if status_check and not status_check():
                        return "ERROR: Cancelled"
                    continue
                    
                rms = self.get_rms(chunk)
                if has_spoken:
                    print(f"DEBUG - RMS: {rms:.2f} (Threshold: {threshold:.2f})", flush=True)
                    
                # If sound is louder than background noise (User is speaking)
                if rms > threshold:
                    if not has_spoken:
                        print(f"Speech detected! RMS: {rms:.2f} > Threshold: {threshold:.2f}", flush=True)
                        has_spoken = True
                        # Keep 0.5s of audio from *before* the threshold was crossed so we don't clip the first letter
                        audio_data.extend(pre_speech_buffer)
                        
                    audio_data.append(chunk)
                    silence_timer = 0.0 # Reset silence timer while speaking
                    
                # If sound is quiet (User is silent)
                else:
                    if has_spoken:
                        audio_data.append(chunk)
                        silence_timer += 0.1 # chunk size is ~0.1s
                        
                        # If we hit the timeout limit, break the loop and send to Google
                        if silence_timer >= timeout:
                            break
                    else:
                        # Maintain a rolling 1-second buffer (4 chunks of 0.25s) of background noise
                        pre_speech_buffer.append(chunk)
                        if len(pre_speech_buffer) > 4:
                            pre_speech_buffer.pop(0)
            
            # Send the collected audio to speech recognition
            if not audio_data or not has_spoken:
                return "ERROR: No speech"
                
            recording = np.concatenate(audio_data, axis=0)
            byte_io = io.BytesIO()
            with wave.open(byte_io, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(self.sample_rate)
                wf.writeframes(recording.tobytes())
            
            byte_io.seek(0)
            print(f"Sending {len(audio_data)} chunks to Google STT...", flush=True)
            with sr.AudioFile(byte_io) as source:
                audio = self.recognizer.record(source)
                try:
                    text = self.recognizer.recognize_google(audio, language=target_language)
                    print(f"Google STT recognized: {text}", flush=True)
                    if text and text.strip():
                        return text.strip()
                    return "ERROR: Empty result"
                except sr.UnknownValueError:
                    print("Google STT: Unrecognized", flush=True)
                    return "ERROR: Unrecognized"
                except sr.RequestError as e:
                    print(f"Google STT Error: {e}", flush=True)
                    return "ERROR: API Unavailable"

        except Exception as e:
            print(f"STT Exception: {type(e).__name__} - {str(e)}", flush=True)
            import traceback
            traceback.print_exc()
            return f"ERROR: {str(e)}"