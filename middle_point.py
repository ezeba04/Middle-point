from flask import Flask, render_template, request
from geopy.geocoders import Nominatim


app = Flask(__name__)

addresses = {
    "Iara": "Hipólito Yrigoyen 3450, ciudad autónoma de Buenos Aires",
    "Geri": "Martín de Gainza 59, ciudad autónoma de Buenos Aires",
    "Daiu": "Gavilan y Juan B justo, ciudad autónoma de Buenos Aires",
    "Naza": "Pringles 722, ciudad autónoma de Buenos Aires",
    "Bacher": "Hidalgo 1221, ciudad autónoma de Buenos Aires",
    "Arcu": "Valentín Gómez 3871, ciudad autónoma de Buenos Aires",
    "Mica": "Jose hernandez 2040, ciudad autónoma de Buenos Aires",
    "Katz": "Gascon 657, ciudad autónoma de Buenos Aires",
    "Martin": "Sarmiento 3969, ciudad autónoma de Buenos Aires",
    "Eric": "Camacuá 92, ciudad autónoma de Buenos Aires",
    "Anita": "Scalabrini Ortíz 1834, ciudad autónoma de Buenos Aires",
    "Sol wainer": "Aguero 45, ciudad autónoma de Buenos Aires",
    "Sol Fiterman": "Av Santa Fe 3980, ciudad autónoma de Buenos Aires",
    "Valen": "Hortiguera 172, ciudad autónoma de Buenos Aires",
    "Juli": "soldado de la independencia 580, ciudad autónoma de Buenos Aires"
}
def calculate_midpoint(selected_people):
    selected_addresses = [addresses[name] for name in selected_people]
    
    latitudes = []
    longitudes = []
    for address in selected_addresses:
        coordinates = geocode(address)
        if coordinates:
            latitudes.append(coordinates[0])
            longitudes.append(coordinates[1])
    
    if latitudes and longitudes:
        avg_lat = sum(latitudes) / len(latitudes)
        avg_lng = sum(longitudes) / len(longitudes)
        return avg_lat, avg_lng
    else:
        return None


def geocode(address):
    geolocator = Nominatim(user_agent="midpoint_calculator")
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    else:
        print(f"Geocoding failed for address: {address}")
        return None



@app.route("/")
def index():
    return render_template("index.html", addresses=addresses)

@app.route("/calculate_midpoint", methods=["POST"])
def midpoint():
    selected_people = request.form.getlist("selected_people")
    midpoint = calculate_midpoint(selected_people)
    if midpoint:
        avg_lat, avg_lng = midpoint
        google_maps_link = f"https://www.google.com/maps/search/?api=1&query={avg_lat},{avg_lng}"
        return f"Midpoint coordinates: {midpoint}<br><a href='{google_maps_link}' target='_blank'>Google Maps Link</a>"
    else:
        return "Failed to calculate midpoint."

if __name__ == "__main__":
    app.run(debug=True)