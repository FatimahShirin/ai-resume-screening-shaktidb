# AI-Based Resume Screening System

This is a ShaktiDB mini-project built with Python, Flask, HTML, and CSS.

The system stores candidate profiles and job requirements in ShaktiDB, compares candidate skills with required job skills, calculates a matching score, ranks candidates, and saves screening results for reports.

## Project Features

- Add candidate details, education, experience, skills, and resume summary.
- Add job roles with required skills and minimum experience.
- Rank candidates for a selected job using simple skill matching.
- Save ranking results in ShaktiDB.
- View reports for popular skills and saved screening results.

## Technologies Used

- Python
- Flask
- ShaktiDB
- HTML
- CSS
- Ubuntu Linux
- GitHub
- VS Code

## Folder Structure

```text
ai_resume_screening_shaktidb/
├── app.py
├── db.py
├── requirements.txt
├── .env.example
├── sql/
│   └── schema.sql
├── static/
│   └── style.css
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── candidates.html
│   ├── jobs.html
│   ├── rankings.html
│   └── reports.html
└── screenshots/
```

## How to Run on Your Lenovo Ubuntu Device

Use these steps on the laptop where ShaktiDB is installed and running.

### 1. Start ShaktiDB

```bash
sudo su - postgres
/usr/lib/postgresql/17.7.1.1/bin/pg_ctl -D /data/shaktidb -l /data/shaktidb/logfile start
exit
```

If it already says the server is running, that is fine.

### 2. Create the Database

```bash
sudo su - postgres
/usr/lib/postgresql/17.7.1.1/bin/createdb resume_screening
exit
```

### 3. Open the Project Folder

Copy this project folder to your Lenovo Ubuntu system. Then open a terminal inside the folder:

```bash
cd ai_resume_screening_shaktidb
```

### 4. Create a Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5. Create the Settings File

```bash
cp .env.example .env
```

If your ShaktiDB user has no password, keep `DB_PASSWORD=` empty.

### 6. Create Tables and Sample Data

```bash
/usr/lib/postgresql/17.7.1.1/bin/psql -d resume_screening -f sql/schema.sql
```

If you need to connect as postgres explicitly:

```bash
/usr/lib/postgresql/17.7.1.1/bin/psql -U postgres -d resume_screening -f sql/schema.sql
```

### 7. Run the Web App

```bash
python app.py
```

Open this in your browser:

```text
http://127.0.0.1:5000
```

## Suggested Screenshots for GitHub

Take screenshots of:

- Dashboard page
- Candidate list page
- Job list page
- Candidate ranking page
- Reports page

Save them in the `screenshots` folder before uploading the project to GitHub.

## Mini-Project Details for Submission Form

**Mini-Project Title:**  
AI-Based Resume Screening System

**Mini-Project Details:**  
An intelligent recruitment platform that stores candidate resumes, skills, qualifications, and experience details in ShaktiDB. The system compares candidate profiles with job requirements and ranks applicants based on skill matching and suitability scores. It provides a structured way to manage recruitment data and generates basic reports on applicant skills and recruitment trends.

**Languages/Platform/OS/Tools:**  
Python, ShaktiDB, Flask, HTML, CSS, Ubuntu Linux, GitHub, VS Code
