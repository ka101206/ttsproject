# Polyglot AI Tutor

A fully containerized, multi-lingual AI language tutor running inside a virtual Linux desktop. It uses Kokoro-ONNX, Piper-TTS, and Microsoft Edge-TTS engines to provide ultra-realistic speech synthesis in Japanese, Chinese, Korean, Spanish, French, and Italian — with AI-powered conversation, grammar tutoring, and vocabulary tracking.

## Features

- **AI Conversation** — Chat with an AI tutor in your target language with automatic text-to-speech responses
- **Multi-Language TTS** — Natural speech synthesis powered by Kokoro (Japanese), Piper (European), and Edge-TTS (Chinese/Korean)
- **Browser Audio Playback** — All TTS audio plays through your browser speakers with adjustable volume
- **Native IME Input** — Type in Japanese, Chinese, Korean, etc. using your Mac's built-in input method directly in the app
- **Grammar Tutor** — Double-click any AI response to get a detailed grammar breakdown, or ask follow-up questions
- **Vocabulary Notebook** — Automatically saves new words with definitions; hover to review
- **Conversation Mode** — Hands-free voice-to-voice practice with speech recognition
- **Replay Controls** — Full and partial replay at adjustable speeds

## Getting Started

### 1. Download the AI Models

The AI language models are large (300MB+) and not included in this repository. Download them using the provided script:

```bash
chmod +x download_models.sh
./download_models.sh
```

Or manually download and place these files:
- `kokoro-v1.0.onnx` (project root)
- `voices.bin` (project root)
- `models/es_ES-sharvard-medium.onnx`
- `models/fr_FR-tom-medium.onnx`
- `models/it_IT-riccardo-x_low.onnx`

### 2. Run the Application

```bash
docker compose up -d
```

### 3. Open in Browser

Navigate to: **http://localhost:8080/vnc.html**

The app auto-connects and scales to fit your browser window. No need to click "Connect".

### 4. Remote Access (Share with others)

Because the app routes all traffic (VNC, Audio, IME) through a single port (`8080`) via an internal Nginx proxy, you can easily share it over the internet using a tunneling service.

The easiest way is using `localtunnel` (requires Node.js):
```bash
npx localtunnel --port 8080
```
This will generate a public URL (e.g., `https://random-words.loca.lt`) that anyone can open in their browser to use the application remotely.

### 5. Typing in Other Languages

To type in Japanese, Chinese, Korean, etc.:
1. Switch your Mac's input source (e.g., via the menu bar or keyboard shortcut)
2. Click the input field in the app
3. Type normally — the IME composition preview appears in real-time
4. Press Enter to finalize the composed text, then Enter again to send

### Stopping the Application

```bash
docker compose down
```

## Architecture

The app runs in a Docker container with a virtual desktop (Xvfb + Fluxbox + x11vnc), served to your browser via noVNC. A custom HTML wrapper (`polyglot_vnc.html`) adds:

- **IME Support** — Transparent textarea overlay intercepts keyboard input for IME composition while forwarding regular keys to VNC
- **Browser Audio Bridge** — HTTP server on port 8081 queues TTS audio files; browser JS polls and plays them via HTML5 Audio API
- **Grammar/IME Controls** — HTTP endpoints for toggling the grammar tutor and handling text composition

## Key Files

| File | Purpose |
|------|---------|
| `gui.py` | Main Tkinter application with all UI and logic |
| `tts_engine.py` | Japanese TTS (Kokoro-ONNX) |
| `european_tts.py` | Spanish/French/Italian TTS (Piper) |
| `chinese_tts.py` | Chinese TTS (Edge-TTS) |
| `korean_tts.py` | Korean TTS (Edge-TTS) |
| `ai_client.py` | AI conversation backend |
| `stt_engine.py` | Speech-to-text engine |
| `polyglot_vnc.html` | Custom noVNC page with IME + audio |
| `start.sh` | Container startup script |
