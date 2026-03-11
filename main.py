from flask import Flask, request
import requests
app = Flask(__name__)

@app.route("/")
def hello_world():
    #ip = request.remote_addr
    #return f"Vaš IP naslov je: {ip}"
# Pridobi IP naslov obiskovalca 
    if request.headers.get('X-Forwarded-For'): 
        ip = request.headers.get('X-Forwarded-For').split(',')[0] 
    else:
        ip = request.remote_addr  

    #API klic za lokacijo IP naslova    
    url = "https://free.freeipapi.com/api/json/95.87.148.60"
    klic = requests.get(url)
    data = klic.json()
    
    mesto = data.get("cityName")   
    drzava = data.get("countryName")

    return f"Vaš IP naslov je: {ip}, Mesto: {mesto}, Država: {drzava}"  # Za debugging return  f"Vaš IP je: {ip}"`

app.run(debug = True)