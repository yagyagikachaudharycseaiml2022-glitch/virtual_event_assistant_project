try:
    import pyttsx3
except Exception:
    pyttsx3 = None

def speak_text(text: str, out_file: str = None):
    if pyttsx3 is None:
        raise RuntimeError("pyttsx3 not installed or not available in this environment")
    engine = pyttsx3.init()
    if out_file:
        engine.save_to_file(text, out_file)
        engine.runAndWait()
        return out_file
    engine.say(text)
    engine.runAndWait()
    return None
