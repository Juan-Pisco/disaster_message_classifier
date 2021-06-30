# Disaster Response Pipeline Project | Made by Juan David Pisco

### Project Summary

This project is an approach of solving a filter message problem. Via NLP techniques and ML modeling, a distress message can be
detected and sent to the appropiate authorities and optimize response and aid times.  

### Files explanation

Folders with their respective job are:
* app Folder (main python code, HTML code, CSS and resources)
    * run.py file (Executes webpage in an allocated port of your private ip)
    * templates Folder (HTML, CSS and resources)
        * go.html, master.html files (main pages)
    * static, res folders (contain css code and image used)
* data Folder (csv raw data, db treated data and python data wrangling script)
    * disaster_categories.csv (raw categories according to id number)
    * disaster_messages.csv (raw messages with its original version)
    * DisasterResponse.db (treated data sql file with "message" table containing data)
    * process_data (python script that treats the data and creates the db file)
* models Folder (classifier model and model training python script)
    * classifier.pkl (model saved in pickle format)
    * train_classifier.py file (python script that trains the model with the database created previously)
    

### Running Instructions:
1. Run the following commands in the project's root directory to set up your database and model.

    - To install all the dependencies needed
        `pip install -r requirements.txt`
    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Run the following command in the app's directory to run your web app.
    `python run.py`

3. Go to http://0.0.0.0:3001/ or the route that your python interpreter prints for previewing the web app.
