from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import mars_scrape


# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to index page to render Mongo data to template
@app.route("/")
def index():

    # Find one record of data from Mongo
    mars = mongo.db.mars.find_one()
    
    # Activate jinja within the website index page
    return render_template("index.html", mars=mars)
    

@app.route("/scrape")
def scrape():

    # Run the scrape function for Mars news and facts
    mars = mongo.db.mars
    mars_data = mars_scrape.scrape()

    # mars.append
    mars.update({}, mars_data, upsert = True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)