from flask import Flask, jsonify, request
import os
import speech_recognition as sr
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_audio
from flask_cors import CORS
import base64

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
            "message": "Mohon maaf pelaporan anda tidak dapat kami proses, mohon coba lagi."
        })

    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({
            "status": "error",
            "message": "Mohon maaf pelaporan anda tidak dapat kami proses, mohon coba lagi."
        })

    data = request.form.to_dict()
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if audio_file:
        mp4_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename)
        audio_file.save(mp4_path)

        wav_path = os.path.splitext(mp4_path)[0] + ".wav"
        convert_to_wav(mp4_path, wav_path)

        text = speech_to_text(wav_path)

        os.remove(mp4_path)
        os.remove(wav_path)

        if text:
            maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"
            encoded_text = base64.b64encode(text.encode()).decode()

            response = {
                "status": "Selamat pelaporan anda telah kami teruskan, mohon untuk menunggu bantuan yang akan datang.",
                "encoded_text": encoded_text,
                "text": text,  # Teks hasil pengenalan suara
                "latitude": latitude,
                "longitude": longitude,
                "mapsLink": maps_link
            }
        else:
            response = {
                "status": "Mohon maaf pelaporan anda tidak dapat kami proses, mohon coba lagi.",
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
