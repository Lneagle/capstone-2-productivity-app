# TimeTrackr
TimeTrackr provides an easy way for users to track their time on daily tasks as well as keep track of what their team members are working on.  Users simply need to click "start" to begin a time entry and "stop" to end it.  Users with an admin role (such as team leads or managers) can add, edit, and delete tasks, as well as view time sheets for all users.

<img width="1192" height="448" alt="image" src="https://github.com/user-attachments/assets/8a38ec79-07fd-4744-a430-e944cc537638" />

<img width="1206" height="474" alt="image" src="https://github.com/user-attachments/assets/c48cfa7e-7753-417e-9a98-b5874033f4cf" />


## Installation
**Set up your database**  
Ensure that you have a database set up (using sqlite, postgres, or similar).  Store the database URI in a variable named 'SQLALCHEMY_DATABASE_URI' in your .env file.

**Use pipenv to install required packages**  
Enter the server directory and run the following:
```bash
pipenv install
pipenv shell
```

**Configure the `FLASK_APP` and `FLASK_RUN_PORT` environment variables**  
Note: the frontend configuration specifies port 5555 for the backend.  If you are running the server on another port, you will need to update the "API_URL" variable in `frontend/services/fetchData.js`
```bash
export FLASK_APP=app.py
export FLASK_RUN_PORT=5555
```

**Initialize the database**
```bash
flask db upgrade head
```

**Seed the database**  
A `seed.py` file is provided for demo purposes.  It is recommended to modify this file with your data to set up your own clients and projects, as there is not yet a UI available to add those.

**Run `python app.py` from the `server` directory**

**Change into the `frontend` directory and use `npm` to install and run the frontend code:**
```bash
npm install
npm start
```
 
## Future Considerations
Planned upgrades include adding projects, adding clients, editing timestamps, user authentication, time totals by day and by task/project, and charts for the timesheet page.
