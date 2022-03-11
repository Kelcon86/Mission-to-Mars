

from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
def index():
    # Uses PyMongo to find the "mars" collection in our Mongo DB
    mars = mongo.db.mars.find_one()
    # Tells Flask to return an HTML template using an index.html file; will be created after we build the Flask routes
    return render_template("index.html", mars=mars)

# This scraping route will be the "button" of our web application


@app.route("/scrape")  # This will run the function that we create beneath it
def scrape():
    mars = mongo.db.mars  # Variable that points to our Mongo DB
    # Variable to hold the newly scraped data (references scrape_all function from the scraping.py file exported from Jupyter Notebook)
    mars_data = scraping.scrape_all()
    # Update the database with the new data using update_one
    mars.update_one({}, {"$set": mars_data}, upsert=True)
    # Empty {} above means first matching document in the collection will be updated, as opposed to specifying
    # $set means "modified"
    # Upsert indicates to Mongo to create a new document if one doesn't already exist; new data will always be saved
    return redirect('/', code=302)
    # Navigates away from scraping page and back to homepage to see the updated content


if __name__ == "__main__":
    app.run()
