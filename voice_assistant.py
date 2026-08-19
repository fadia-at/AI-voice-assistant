import asyncio
import os
import string
import arabic_reshaper
from bidi.algorithm import get_display
import cohere
import edge_tts
from faster_whisper import WhisperModel
import pygame
import speech_recognition as sr

co = cohere.Client("حط مفتاحك الخاص فيك من cohere ")


def ar(text):
  reshaped_text = arabic_reshaper.reshape(text)
  return get_display(reshaped_text)


def speak(text):
  async def _tts():
    communicate = edge_tts.Communicate(text, "ar-SA-HamedNeural")
    await communicate.save("reply.mp3")

  asyncio.run(_tts())

  pygame.mixer.init()
  pygame.mixer.music.load("reply.mp3")
  pygame.mixer.music.play()
  while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
  pygame.mixer.music.unload()
  pygame.mixer.quit()

  if os.path.exists("reply.mp3"):
    try:
      os.remove("reply.mp3")
    except:
      pass


model = WhisperModel("small", device="cpu", compute_type="int8")
recognizer = sr.Recognizer()
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True
chat_history = []

print(ar("أهلا ! بدأ مساعدك الذكي... للمغادرة قل 'مع السلامة' أو 'خروج'"))

while True:
  with sr.Microphone() as source:
    print(ar("\n--- خليك مستعد !!---"))
    recognizer.adjust_for_ambient_noise(source, duration=0.3)

    print(ar("يبدا التسجيل الان..."))
    try:
      audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
      print(ar("تم التسجيل"))
    except sr.WaitTimeoutError:
      continue

  print(ar("جاري تحويل الصوت الى نص..."))
  with open("temp.wav", "wb") as f:
    f.write(audio.get_wav_data())

  segments, _ = model.transcribe("temp.wav", language="ar", beam_size=1)
  user_text = "".join([segment.text for segment in segments]).strip()

  if not user_text:
    continue

  print(ar(f"أنت: {user_text}"))

  clean_text = user_text.translate(
      str.maketrans("", "", string.punctuation + "،؟؛.!؟")
  ).strip()
  exit_keywords = [
      "مع السلامه",
      "مع السلامة",
      "خروج",
      "وداعا",
      "وداعاً",
      "باي",
      "مع سلامه",
    
      "انهاء",
  ]

  if any(kw in clean_text for kw in exit_keywords):
    exit_reply = "مع السلامة! أتمنى لك يوماً سعيداً."
    print(ar(f"المساعد: {exit_reply}"))
    speak(exit_reply)
    break

  print(ar("جاري التفكير وتوليد الرد..."))
  response = co.chat(
      chat_history=chat_history,
      message=f"أنت مساعد ذكي ومختصر، أجب باللغة العربية بإيجاز: {user_text}",
  )
  ai_reply = response.text.strip()
  print(ar(f"المساعد: {ai_reply}"))

  chat_history.append({"role": "USER", "message": user_text})
  chat_history.append({"role": "CHATBOT", "message": ai_reply})

  speak(ai_reply)