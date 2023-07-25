from flask import Flask, jsonify, request
import os
import speech_recognition as sr
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_audio
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def convert_to_wav(mp4_path, wav_path):
    ffmpeg_extract_audio(mp4_path, wav_path)

def speech_to_text(file_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(file_path) as source:
        print("Mengubah suara menjadi teks...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.record(source)

    try:
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
    if 'audio' not in request.files:
        return jsonify({
            "status": "error",
            "message": "Tidak ada file audio yang dikirim."
        })

    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({
            "status": "error",
            "message": "File audio tidak valid."
        })

    if audio_file:
        mp4_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename)
        audio_file.save(mp4_path)

        wav_path = os.path.splitext(mp4_path)[0] + ".wav"
        convert_to_wav(mp4_path, wav_path)

        text = speech_to_text(wav_path)

        os.remove(mp4_path)
        os.remove(wav_path)

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
    else:
        return jsonify({
            "status": "error",
            "message": "Tidak dapat mengakses file audio."
        })

if __name__ == "__main__":
    app.run(debug=True)
