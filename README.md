## TimeVault (name)

 Backend (FastAPI)

mkdir my-calendar-app
cd my-calendar-app
mkdir backend
cd backend

pip install -r requirements.txt
uvicorn main:app --reload
notepad requirements.txt
***
fastapi
uvicorn
python-dotenv
requests
mysql-connector-python
google-auth
google-auth-oauthlib
google-auth-httplib2
***

pip install -r requirements.txt
pip install -r requirements.txt --user
pip show uvicorn
pip install uvicorn --user

cd D:\GitHUB\Calendar_GoogleAPI\my-calendar-app\backend
python -m uvicorn main:app --reload

python -m venv env
.\env\Scripts\activate
env\Scripts\activate

Get-ExecutionPolicy
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\env\Scripts\Activate

(env) PS D:\GitHUB\Calendar_GoogleAPI\my-calendar-app\backend>

pip install -r requirements.txt
python -m uvicorn main:app --reload

## 

cd D:\GitHUB\Calendar_GoogleAPI\my-calendar-app

mkdir frontend
cd frontend
npx create-react-app .

npm install react-router-dom axios
npm start

--------------------

my-calendar-app/
   ├─ backend/
   │   ├─ main.py
   │   ├─ requirements.txt
   │   └─ .env           (optional for secrets)
   └─ frontend/
       ├─ package.json
       ├─ public/
       │   └─ index.html
       └─ src/
           ├─ App.js
           ├─ index.js
           ├─ pages/
           │   ├─ LoginPage.js
           │   └─ CalendarPage.js
           └─ components/
               ├─ CalendarGrid.js
               └─ Sidebar.js