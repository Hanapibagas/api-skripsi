from flask import Flask, jsonify

import speech_recognition as sr

app = Flask(__name__)

def speech_to_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Silakan mulai berbicara...")
        recognizer.adjust_for_ambient_noise(source)

        audio = recognizer.listen(source)

    try:
        print("Mengubah suara menjadi teks...")
        text = recognizer.recognize_google(audio, language="id-ID")

        print("Teks hasil pengenalan suara:")
        print(text)
        return text
    except sr.UnknownValueError:
        print("Pengenalan suara gagal: Tidak dapat mengenali suara")
        return None
    except sr.RequestError as e:
        print(f"Pengenalan suara gagal: {e}")
        return None

@app.route("/api/speech-to-text", methods=["POST"])
def api_speech_to_text():
    text = speech_to_text()
    if text:
        response = {
            "status": "success",
            "text": text
        }
    else:
        response = {
            "status": "error",
            "message": "Pengenalan suara gagal. Coba lagi."
        }
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
