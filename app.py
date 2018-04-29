from flask import Flask, render_template, request, redirect, url_for
from bs4 import BeautifulSoup as BS
import requests
from flask_pymongo import PyMongo
import urllib.parse
from scraping import scrape
from searchurl import search_url
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger

app = Flask(__name__)

# DB config
app.config['MONGO_DBNAME'] = 'connect_to_mongo'
app.config['MONGO_URI'] = 'mongodb://{username}:' + urllib.parse.quote({password}) + '{db_url}/connect_to_mongo'
mongo = PyMongo(app)

@app.route('/', methods = ['GET','POST'])
def main():
    if request.method == 'POST':
        company_name = request.form ['cname']
        frequency = request.form ['freq']
        start_time = request.form ['stime']
        end_time = request.form ['etime']
        
        app.config['frequency'] = frequency
        app.config['start_time'] = start_time
        app.config['end_time'] = end_time

        # Job scheduling
        if app.config.get('frequency'):
            trigger = OrTrigger([
                CronTrigger(hour= app.config.get('start_time')+ '-' + app.config.get('end_time'), minute=app.config.get('frequency'))
             ])
            scheduler.add_job(main, trigger)

        company_url = search_url(company_name)
        if company_url:
            c_url = requests.get(company_url)
            soup = BS(c_url.text, "html.parser")

            # Returns bse and nse contents if present
            b,n = scrape(soup)

            # Adding info to Database  
            bse_db = mongo.db.bse
            nse_db = mongo.db.nse

            if b:
                bse_entry = bse_db.insert({'BSE Date': b['bse_date'], 'BSE Time':b['bse_time'], 'BSE Current Price':b['bse_current_price'], 'BSE absolute price':b['bse_abs_price'], 'BSE percentage':
                           b['bse_per'], 'BSE Volume': b['bse_volume'], 'BSE Prev close':b['bse_prev_close'], 'BSE Open price':b['bse_open_price'], 'BSE bid price': b['bse_bid_price'],
                           'BSE offer price': b['bse_offer_price']})
            if n:
                nse_entry = nse_db.insert({'NSE Date': n['nse_date'], 'NSE Time':n['nse_time'], 'NSE Current Price': n['nse_current_price'], 'NSE absolute price':n['nse_abs_price'], 'NSE percentage':
                           n['nse_per'], 'NSE Volume': n['nse_volume'], 'NSE Prev close':n['nse_prev_close'], 'NSE Open price':n['nse_open_price'], 'NSE bid price': n['nse_bid_price'],
                          'NSE offer price': n['nse_offer_price']})

            if bse_db or nse_db:
                return redirect(url_for('info'))

        else: 
            error = "Sorry! Company not found."
            return render_template('index.html', error = error)
       
    return render_template('index.html')

@app.route("/info")
def info():
     bse_entries = mongo.db.bse.find()
     nse_entries = mongo.db.nse.find()
     if bse_entries or nse_entries:
         return render_template('scraped_data.html', bse_entries=bse_entries, nse_entries=nse_entries)
     return render_template('index.html')

if __name__ == "__main__":

    # Initializing scheduler
    scheduler = BackgroundScheduler()
    scheduler.start()
    
    app.run(debug=True)

