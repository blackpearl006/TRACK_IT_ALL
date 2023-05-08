# TRACK_IT_ALL

## Day to day activities tracking app at your fingertip

### Project Report

**Author:** Ninad Aithal  
**ID:** 21f1006030  
**Email:** 21f1006030@student.onlinedegree.iitm.ac.in  

### Description

A day-to-day life activity tracking app where a user can register and add trackers and log values in it and be provided with a graphical representation of the log. Also, can manipulate the trackers and log like updating it or deleting it.

### Technologies used

- flask: framework used to create the web app using python
- flask-sqlalchemy: tools and methods to interact with the database from flask application
- flask_wtf: validations are easy and good interface
- email-validator: validating input email
- flask_bcrypt: enables hashing and related utilities
- flask_login: access control and session management
- flask_restful: construct API’s

### DB Schema Design

- 3 Tables: user, tracker, log
- 3 One-to-Many Relationships:
  - user.id < tracker.owner
  - user.id < log.user_id
  - tracker.id < log.tracker_id
- First 2 relationships are necessary, and the 3rd relationship makes querying easier (redundant relationship).
- tracker.last_modified has the number of the year so it's an integer.
- user.username is unique - login using the username.
- If we delete a tracker, all the associated logs get deleted.

### API Design

3 API classes: UserAPI, TrackerAPI, LogAPI have been implemented all having 4 methods GET,POST,PUT,DELETE and having custom validations. YAML file not created.

### Architecture and Features

- my_app folder and main.py file are inside the zip folder.
- To start the web app run the main.py file (refer ReadMe.md).
- my_app contains:
  - ReadMe.md: how to run the web application.
  - Static folder: containing images in images, CSS in CSS, and JavaScript in the JS folder.
  - Template folder: containing all the templates and also templates for modals in a folder.
  - track_it_all.db: database.
  - int.py: all the code which will run by default when the app is started.
  - api.py: all the APIs are defined here.
  - command.txt: all the required libraries to install.
  - forms.py: forms used in the app are defined here.
  - models.py: the database is initialized here.
  - routes.py: routes used in the application are written here.
  - validation.py: custom validations for APIs are defined here.
  - debug.log: log file.
- Default features like CRUD operations on trackers and logs have been implemented, along with that we can update user profile, and a graphical representation of the tracker and log is being displayed on the dashboard.
- For creating a new tracker & log, a new page is being rendered, whereas for updating and deleting modals are being used.
- For the rendering of graphs, Chart.js is being used.

### Replit Link

https://replit.com/@blackpearl006/21f1006030#main.py

### Video

https://drive.google.com/file/d/1QPdOSxyOLwaPLgDWXR2K6LGGqtZzsytd/view?usp=sharing


## How to run the program

1. Open file browser and locate the code file / download it (.zip format available in replit.com)
2. If the file is in .zip format unzip it to find main.py and a folder my_app
3. Open the code on your choice of editor or in the terminal
4. Create a virtual environment and activate it
5. Take the main.py file outside of the folder my_app
6. Your editor must have open unzipped folder having my_app folder, main.py, virtualenv
7. Install all the packages written in my_app/command.txt
8. After the installation is completed you can run the application make sure you are in the file with main.py and my_app folder

Code for creating the virtual environment:
<br>
  `python3 -m venev project_env`
  <br>
  `source project_env/bin/activate`

Code for install all the dependencies:

  `pip install -r my_app/command.txt`

Code for running the application:

`python main.py`


Author

NINAD AITHAL

