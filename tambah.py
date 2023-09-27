from flask import Flask, request, jsonify
import mysql.connector
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_DATABASE")
)


@app.route('/api/laporan', methods=['POST'])
def tambah_laporan():
    data = request.get_json()
    cursor = db.cursor()

    nama_laporan = data['nama_laporan']
    isi_laporan = data['isi_laporan']
    tanggal = datetime.now().strftime("%Y-%m-%d")
    waktu = datetime.now().strftime("%H:%M:%S")
    latitude = data['latitude']
    longitude = data['longitude']
    kelas = data['kelas']

    sql = "INSERT INTO laporan (nama_laporan, isi_laporan, tanggal, latitude, longitude, kelas, waktu) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (nama_laporan, isi_laporan, tanggal,
              latitude, longitude, kelas, waktu)

    try:
        cursor.execute(sql, values)
        db.commit()
        return jsonify({"message": "Data berhasil ditambahkan"}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"message": "Gagal menambahkan data", "error": str(e)}), 500
    finally:
        cursor.close()


@app.route('/api/laporan', methods=['GET'])
def semua_laporan():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM laporan")

    results = cursor.fetchall()
    return jsonify(results), 200


if __name__ == '__main__':
    app.run(debug=True)
