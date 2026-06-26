import os
import re

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

from db import execute, fetch_all, fetch_one

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "resume-screening-secret")


def split_skills(text):
    if not text:
        return []
    values = re.split(r"[,;\n]+", text.lower())
    cleaned = []
    for value in values:
        skill = re.sub(r"[^a-z0-9+#. ]", "", value).strip()
        if skill and skill not in cleaned:
            cleaned.append(skill)
    return cleaned


def calculate_match(candidate_skills, required_skills):
    candidate_set = set(split_skills(candidate_skills))
    required = split_skills(required_skills)
    if not required:
        return 0, []
    matched = [skill for skill in required if skill in candidate_set]
    score = round((len(matched) / len(required)) * 100)
    return score, matched


@app.route("/")
def dashboard():
    stats = {
        "candidates": fetch_one("SELECT COUNT(*) AS count FROM candidates")["count"],
        "jobs": fetch_one("SELECT COUNT(*) AS count FROM jobs")["count"],
        "applications": fetch_one("SELECT COUNT(*) AS count FROM applications")["count"],
    }
    recent_candidates = fetch_all(
        """
        SELECT candidate_id, full_name, email, skills, created_at
        FROM candidates
        ORDER BY candidate_id DESC
        LIMIT 5
        """
    )
    recent_jobs = fetch_all(
        """
        SELECT job_id, title, required_skills, created_at
        FROM jobs
        ORDER BY job_id DESC
        LIMIT 5
        """
    )
    return render_template(
        "dashboard.html",
        stats=stats,
        recent_candidates=recent_candidates,
        recent_jobs=recent_jobs,
    )


@app.route("/candidates", methods=["GET", "POST"])
def candidates():
    if request.method == "POST":
        execute(
            """
            INSERT INTO candidates
                (full_name, email, phone, education, experience_years, skills, resume_summary)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                request.form["full_name"],
                request.form["email"],
                request.form.get("phone"),
                request.form.get("education"),
                request.form.get("experience_years") or 0,
                request.form.get("skills"),
                request.form.get("resume_summary"),
            ),
        )
        flash("Candidate added successfully.")
        return redirect(url_for("candidates"))

    rows = fetch_all(
        """
        SELECT candidate_id, full_name, email, phone, education, experience_years, skills
        FROM candidates
        ORDER BY candidate_id DESC
        """
    )
    return render_template("candidates.html", candidates=rows)


@app.route("/jobs", methods=["GET", "POST"])
def jobs():
    if request.method == "POST":
        execute(
            """
            INSERT INTO jobs (title, department, required_skills, minimum_experience, description)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                request.form["title"],
                request.form.get("department"),
                request.form["required_skills"],
                request.form.get("minimum_experience") or 0,
                request.form.get("description"),
            ),
        )
        flash("Job added successfully.")
        return redirect(url_for("jobs"))

    rows = fetch_all(
        """
        SELECT job_id, title, department, required_skills, minimum_experience, description
        FROM jobs
        ORDER BY job_id DESC
        """
    )
    return render_template("jobs.html", jobs=rows)


@app.route("/rankings", methods=["GET", "POST"])
def rankings():
    jobs = fetch_all("SELECT job_id, title, required_skills FROM jobs ORDER BY title")
    selected_job = None
    ranked_candidates = []

    job_id = request.values.get("job_id")
    if job_id:
        selected_job = fetch_one("SELECT * FROM jobs WHERE job_id = %s", (job_id,))
        candidates = fetch_all(
            """
            SELECT candidate_id, full_name, email, education, experience_years, skills
            FROM candidates
            ORDER BY full_name
            """
        )
        for candidate in candidates:
            score, matched = calculate_match(candidate["skills"], selected_job["required_skills"])
            candidate["score"] = score
            candidate["matched_skills"] = ", ".join(matched) if matched else "No direct match"
            ranked_candidates.append(candidate)

        ranked_candidates.sort(key=lambda row: row["score"], reverse=True)

        if request.method == "POST":
            execute("DELETE FROM applications WHERE job_id = %s", (job_id,))
            for candidate in ranked_candidates:
                execute(
                    """
                    INSERT INTO applications
                        (job_id, candidate_id, match_score, matched_skills)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        selected_job["job_id"],
                        candidate["candidate_id"],
                        candidate["score"],
                        candidate["matched_skills"],
                    ),
                )
            flash("Ranking saved in ShaktiDB.")
            return redirect(url_for("rankings", job_id=job_id))

    return render_template(
        "rankings.html",
        jobs=jobs,
        selected_job=selected_job,
        ranked_candidates=ranked_candidates,
    )


@app.route("/reports")
def reports():
    top_applications = fetch_all(
        """
        SELECT
            j.title AS job_title,
            c.full_name,
            c.email,
            a.match_score,
            a.matched_skills,
            a.screened_at
        FROM applications a
        JOIN jobs j ON j.job_id = a.job_id
        JOIN candidates c ON c.candidate_id = a.candidate_id
        ORDER BY a.match_score DESC, a.screened_at DESC
        LIMIT 20
        """
    )
    skill_rows = fetch_all("SELECT skills FROM candidates")
    skill_count = {}
    for row in skill_rows:
        for skill in split_skills(row["skills"]):
            skill_count[skill] = skill_count.get(skill, 0) + 1
    popular_skills = sorted(skill_count.items(), key=lambda item: item[1], reverse=True)[:10]
    return render_template(
        "reports.html",
        top_applications=top_applications,
        popular_skills=popular_skills,
    )


if __name__ == "__main__":
    app.run(debug=True)
