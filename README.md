# GuitAR-scrapping
GuitAR is an web app which projects the chords for any song from our wide selection on to user's guitar on their screen so that all they have to do is press the highlighted strings to play the song.
This is GuitAr's database builder
## Setup

### Install Python Dependencies
Note: Install Python >= 3.8
1. Install beautifulsoup
```bash
  pip install beautifulsoup4
```
2. Install Selenium
```bash
  pip install selenium
```
3. Install pymongo
```bash
  pip install pymongo
```
### Download Chrome Webdriver
Download Chrome driver with version matching your chrome app from ![here](https://chromedriver.chromium.org/downloads)

### Setup .env file
1. Add .env file at src/ using mkdir .env
2. Add your mongoDB Atlas Password and webdriver location
```bash
MONGODB_PASSWORD = "<YOUR_MONGODB_PASSSWORD_HERE>"
WEBDRIVER_LOCATION = "<YOUR_WEBDRIVER_LOCATION_HERE>"
```
### Run Script
Run main.py
