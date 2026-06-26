DROP TABLE IF EXISTS applications;
DROP TABLE IF EXISTS candidates;
DROP TABLE IF EXISTS jobs;

CREATE TABLE candidates (
    candidate_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    phone VARCHAR(20),
    education VARCHAR(150),
    experience_years INT DEFAULT 0,
    skills TEXT NOT NULL,
    resume_summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE jobs (
    job_id SERIAL PRIMARY KEY,
    title VARCHAR(120) NOT NULL,
    department VARCHAR(100),
    required_skills TEXT NOT NULL,
    minimum_experience INT DEFAULT 0,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE applications (
    application_id SERIAL PRIMARY KEY,
    job_id INT NOT NULL REFERENCES jobs(job_id) ON DELETE CASCADE,
    candidate_id INT NOT NULL REFERENCES candidates(candidate_id) ON DELETE CASCADE,
    match_score INT NOT NULL,
    matched_skills TEXT,
    screened_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO candidates
    (full_name, email, phone, education, experience_years, skills, resume_summary)
VALUES
    ('Fatimah A', 'fatimah@example.com', '9876543210', 'B.Tech Computer Science', 1, 'Python, SQL, Flask, HTML, CSS', 'Worked on database and web application mini-projects.'),
    ('Riya Mathew', 'riya@example.com', '9876501234', 'B.Tech IT', 2, 'Python, Data Analysis, Excel, SQL', 'Interested in data analysis and reporting.'),
    ('Adil Khan', 'adil@example.com', '9876512345', 'BCA', 1, 'Java, HTML, CSS, MySQL', 'Built small web applications and academic projects.'),
    ('Meera Nair', 'meera@example.com', '9876523456', 'B.Tech ECE', 0, 'Python, Machine Learning, SQL', 'Completed coursework in machine learning and databases.');

INSERT INTO jobs
    (title, department, required_skills, minimum_experience, description)
VALUES
    ('Python Flask Developer', 'Software Development', 'Python, SQL, Flask, HTML, CSS', 1, 'Build and maintain database-backed web applications.'),
    ('Data Analyst Intern', 'Analytics', 'Python, SQL, Excel, Data Analysis', 0, 'Prepare reports and analyze recruitment data.');
