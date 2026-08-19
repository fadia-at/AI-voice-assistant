# AI-voice-assistant
# Arabic AI Voice Assistant

An interactive, end-to-end Arabic voice assistant that captures spoken input, transcribes it locally, generates context-aware intelligent responses via a Large Language Model (LLM), and speaks the answers back using natural Text-to-Speech in a continuous conversation loop.

---
System Architecture

The project operates through a complete 3-stage pipeline:
1. Speech-to-Text (STT): Captures microphone input and transcribes Arabic speech locally using faster-whisper.
2. Large Language Model (LLM): Processes user prompts, maintains multi-turn conversation memory (`chat_history`), and generates concise responses using the Cohere API.
3. Text-to-Speech (TTS): Converts generated text into natural Arabic audio using edge-tts (`ar-SA-HamedNeural`) and plays it seamlessly.

---

Detailed Code Explanation

 1. Library Imports & Initialization
* `speech_recognition` & `faster_whisper`: Handles dynamic microphone input calibration and runs the quantized small Whisper model locally on CPU for high Arabic transcription accuracy.
* `cohere`: Authenticates client requests and manages context-aware multi-turn conversational chat sessions.
* `edge_tts` & `pygame`: Synthesizes natural Saudi/Arabic speech (`ar-SA-HamedNeural`), plays back the generated audio stream, and properly frees file locks via pygame.mixer.music.unload().
* `arabic_reshaper` & `bidi.algorithm`: Reshapes and reverses Arabic bidirectional text strings to render correctly in standard CLI/Terminal environments.

2. Audio Processing & Speech Recognition
* Dynamically adjusts for background room noise using adjust_for_ambient_noise prior to listening.
* Captures voice frames into a temporary WAV buffer.
* Employs initial_prompt prompting within Whisper transcription to boost recognition rates for Arabic and regional Saudi dialect phrasing while minimizing hallucination.

3. Conversational Loop & Context Management
* Wrapped inside a persistent loop (`while True`) to enable hands-free continuous dialogue.
* Appends alternating user and chatbot turns to chat_history, enabling context retention across queries.
* Implements robust exit keyword filtering (e.g., "مع السلامة", "خروج", "وداعاً") while explicitly excluding common greeting overlaps (e.g., "السلام عليكم") to prevent accidental terminations.

---
Here very important notes !!!!
I put video when i run the code here https://drive.google.com/file/d/1wHdUtkVs9a7gqkMwzJqWkrYDmYeQRwBK/view?usp=drivesdk
Also to run the code you need to add your API key from cohere at line 12!!!
