from flask import Flask, render_template, jsonify, request
import requests
from datetime import datetime

app = Flask(__name__)

OPENWEATHER_API_KEY = "ffce0c21759d98c85cd9dc44f540c8a4"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/weather')
def api_weather():
    city = request.args.get('city', 'Bangkok')
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric&lang=th"
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({
            "city": city,
            "temp": "N/A",
            "humidity": "N/A",
            "desc": "ไม่พบข้อมูล",
            "advice": "กรุณาลองใหม่",
            "time": datetime.now().strftime("%H:%M:%S")
        })

    data = response.json()
    temp = data['main']['temp']
    humidity = data['main']['humidity']
    desc = data['weather'][0]['description']

    if temp >= 30:
        advice = "อากาศร้อน! ดื่มน้ำเยอะ ๆ"
    elif temp <= 15:
        advice = "อากาศเย็น! ใส่เสื้อหนาว"
    else:
        advice = "อากาศกำลังสบาย"

    return jsonify({
        "city": city,
        "temp": temp,
        "humidity": humidity,
        "desc": desc,
        "advice": advice,
        "time": datetime.now().strftime("%H:%M:%S")
    })

if __name__ == '__main__':
    # สำหรับรันในเครื่องทดสอบ
    app.run(host="0.0.0.0", port=5000)
