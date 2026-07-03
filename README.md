# Job Portal Backend

Hi there! Welcome to the backend code for the Job Portal project. This is built using **Python** and **FastAPI**. I designed it to be simple, clean, and easy to understand.

## What Does It Do?
This backend powers a job portal where two types of users can interact:
1. **Candidates:** Can create an account, log in, browse available jobs, update their profile, upload a resume, and apply to jobs.
2. **Recruiters:** Can create an account, log in, post new jobs, edit or delete their postings, and review the applications they receive.

## How the Code is Organized
I kept the folder structure as flat and readable as possible so you can find things quickly:

```text
backend/
├── app/
│   ├── main.py        # The starting point of the app
│   ├── database.py    # Sets up the database connection
│   ├── models.py      # Describes what our database tables look like
│   ├── schemas.py     # Checks that the data sent to the API is correct
│   ├── crud.py        # Handles saving and reading data from the database
│   ├── auth.py        # Manages secure logins and passwords
│   └── routers.py     # Contains all the URLs (endpoints) for the API
├── uploads/           # Where candidate resumes get saved
├── requirements.txt   # The list of Python packages needed
└── .env               # Secret settings like the database URL
```

## How the Database Works
There are just three simple tables:
1. **Users:** Stores everyone's info (name, email, secure password, role, etc.).
2. **Jobs:** Stores job postings and links back to the Recruiter who posted it.
3. **Applications:** Links a Candidate to a Job they applied for, along with their application status.

## How to Run the Project Locally

### 1. What You Need
Make sure you have Python (version 3.8 or newer) installed on your computer.

### 2. Set Up a Virtual Environment
It's best to run Python projects in their own little bubble. Open your terminal in the `backend` folder and run:
```bash
python -m venv venv
```

### 3. Turn on the Virtual Environment
- **If you're on Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **If you're on Mac or Linux:**
  ```bash
  source venv/bin/activate
  ```

### 4. Install the Required Packages
```bash
pip install -r requirements.txt
```

### 5. Set Up Your Secrets
Create a file named `.env` in the `backend` folder and paste this inside:
```env
SECRET_KEY=my-super-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL="mysql+pymysql://root:root@localhost:3306/job_portal"
```
*(Make sure your local MySQL server is running and you have created the `job_portal` database!)*

### 6. Start the Server
Make sure you're still in the `backend` folder with your virtual environment turned on, then run:
```bash
uvicorn app.main:app --reload
```

## How to Test the API
The coolest part about FastAPI is that it automatically builds a testing page for you! 

Once the server is running, open your web browser and go to:
👉 **[http://localhost:8000/docs](http://localhost:8000/docs)**

You'll see a clean, interactive dashboard (Swagger UI) where you can easily test logging in, creating jobs, and applying to them—no extra tools needed.
