from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import mars_scrape

app = Flask(__name__)

# Set up mongo connection with PyMongo
app.config["MONGO_URI"] = "mongodb://localhost:27017"

mongo = PyMongo(app)

### Scrape route for mars_scrape()
@app.route("/scrape")
def scrape_urls():

    print("We are in scrape")

    #####mars_news_data = mongo.db.mars_data
    mars_news_data = mars_scrape.scrape_urls()

    # Insert mars_news_data into database collection mars_data
    mongo.db.mars_data.update({}, mars_news_data, upsert=True)
    #for MongoClient # db.mars_data.update({}, mars_news_data, upsert=True)
    
    # Redirect back to Landing Page
    return redirect("/", code=302)
    
    ###return "Scraping was successful."


### Main - Landing Page - index.html
@app.route("/")
def index():
    
    # Get mars_news_data documents from database mars_db ( or heroku_8mh5bx8l ), collection mars_data
    mars_news_data = mongo.db.mars_data.find_one()
    #for MongoClient# mars_news_data = db.mars_data.find_one()
    
    return render_template("index.html", mars_news_data=mars_news_data)

if __name__ == "__main__":
    ##print (mars_scrape.scrape_urls())
    app.run(debug=True)