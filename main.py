from flask import Flask, request, render_template
import requests
from tinydb import TinyDB

app = Flask(__name__)
db = TinyDB("obiski.json")

OPENWEATHER_KEY = "TVOJ_API_KLJUC"

# pridobi IP obiskovalca
def get_ip():
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    return request.remote_addr


@app.route("/")
def index():

    ip = get_ip()

    # pridobi lokacijo iz IP
    geo = requests.get(f"https://freeipapi.com/api/json/{ip}").json()

    city = geo.get("cityName")
    country = geo.get("countryName")
    lat = geo.get("latitude")
    lon = geo.get("longitude")

    # pridobi vreme
    weather = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_KEY}&units=metric"
    ).json()

    temp = weather["main"]["temp"]
    desc = weather["weather"][0]["description"]

    visit = {
        "ip": ip,
        "city": city,
        "country": country,
        "temperature": temp,
        "weather": desc
    }

    # shrani obisk
    db.insert(visit)

    return render_template("index.html", visit=visit)


@app.route("/obiskovalci")
def obiskovalci():
    visits = db.all()
    return render_template("obiskovalci.html", visits=visits)


if __name__ == "__main__":
    app.run(debug=True)