import os
import re
from flask import Flask, jsonify, render_template, request, url_for
from flask_jsglue import JSGlue

from cs50 import SQL
from helpers import lookup

# configure application
app = Flask(__name__)
JSGlue(app)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///mashup.db")

# configure the API key for the session
API_KEY = os.environ.get("API_KEY") or "AIzaSyAnWslm-G159K5Bej0tJGRcFEDnOHQ5Cds"

@app.route("/")
def index():
    """Render map."""
    
    if not API_KEY:
        raise RuntimeError("API_KEY not set")
    return render_template("index.html", key=API_KEY)

@app.route("/articles")
def articles():
    """Look up articles for geo."""
    # TODO
    
    # created a dictionary of keys and values from the lookup function based on the geo's zip code value
    articles = lookup(request.args.get("geo"))
    
    # make sure that the user entered location can be found in the database
    if not articles:
        raise RuntimeError("Error Occured: Articles could not be fetched")
    return jsonify(articles[:5])

@app.route("/search")
def search():
    """Search for places that match query."""
    # TODO
    
    location = request.args.get("q") + "%"
    
    # ensure user enters something into the search form
    if not location:
        return

    # stores a dictionary of keys and values of all columns matching the user inputted location
    locationData = db.execute("SELECT * FROM places WHERE postal_code LIKE :location OR place_name LIKE :location OR admin_code1 LIKE :location OR admin_name1 LIKE :location", location=location)
    
    return jsonify(locationData[:10])

@app.route("/update")
def update():
    """Find up to 10 places within view."""

    # ensure parameters are present
    if not request.args.get("sw"):
        raise RuntimeError("missing sw")
    if not request.args.get("ne"):
        raise RuntimeError("missing ne")

    # ensure parameters are in lat,lng format
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("sw")):
        raise RuntimeError("invalid sw")
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("ne")):
        raise RuntimeError("invalid ne")

    # explode southwest corner into two variables
    (sw_lat, sw_lng) = [float(s) for s in request.args.get("sw").split(",")]

    # explode northeast corner into two variables
    (ne_lat, ne_lng) = [float(s) for s in request.args.get("ne").split(",")]

    # find 10 cities within view, pseudorandomly chosen if more within view
    if (sw_lng <= ne_lng):

        # doesn't cross the antimeridian
        rows = db.execute("""SELECT * FROM places
            WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude AND longitude <= :ne_lng)
            GROUP BY country_code, place_name, admin_code1
            ORDER BY RANDOM()
            LIMIT 10""",
            sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    else:

        # crosses the antimeridian
        rows = db.execute("""SELECT * FROM places
            WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude OR longitude <= :ne_lng)
            GROUP BY country_code, place_name, admin_code1
            ORDER BY RANDOM()
            LIMIT 10""",
            sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    # output places as JSON
    return jsonify(rows)
