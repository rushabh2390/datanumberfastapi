# FAVM Application (TO-DO application have backend in FASTAPI and store in MongoDB and frontend in Vue CLi)
---
## Required  npm(version: 8.1.2) and python(version >3.7) mongoDB(version 4.4.0)
---
### Run locally
1. Clone this repo.
2. Go to project in terminal   
``` cd datafastapi ```
3. Go to backend   
``` cd backend ```
4. Create virtual environment by running following command ( Note: if pipenv is not there the install it using ```pip install pipenv```)   
``` pipenv shell ```   
5. Run the followiing command to active virtual environment   
``` pipenv install ```
6. Execute the following command to run uvicorn
``` uvicorn main:app --reload ```
7. You can visit fastapi docs from [backend](http://127.0.0.1:8000/docs)  
---
### Run in Docker
1. clone this repo
2. Go to project in terminal   
``` cd datafastapi ```
3. Run follwing command to start docker with application
``` docker-compose up ``` Or ``` docker-compose up -d ```
4. You can visit fastapi docs from [backend](http://127.0.0.1:8000/docs)
