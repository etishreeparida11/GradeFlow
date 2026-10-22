
import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash

# Load .env from the same folder as app.py
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env", override=True)

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "gradeflow-local-dev-key")


def get_db_connection():
    # Reload environment settings before connecting
    load_dotenv(BASE_DIR / ".env", override=True)
    password = os.getenv("MYSQL_PASSWORD")
    if not password:
        raise RuntimeError(
            "MYSQL_PASSWORD is missing. Check the .env file beside app.py."
        )

    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=password,
        database=os.getenv("MYSQL_DATABASE", "StudentDB")
    )


@app.route("/")
def home():
    db = None
    cursor = None

    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT student_id, student_name, marks, department,
                   GetGrade(marks) AS grade
            FROM Students
            ORDER BY student_id
        """)
        students = cursor.fetchall()

        cursor.execute("""
            SELECT COUNT(*) AS total,
                   COALESCE(ROUND(AVG(marks), 2), 0) AS average,
                   COALESCE(SUM(CASE WHEN marks >= 40 THEN 1 ELSE 0 END), 0)
                       AS passed,
                   COALESCE(SUM(CASE WHEN marks < 40 THEN 1 ELSE 0 END), 0)
                       AS failed,
                   COALESCE(SUM(CASE WHEN marks >= 80 THEN 1 ELSE 0 END), 0)
                       AS grade_a
            FROM Students
        """)
        stats = cursor.fetchone()

        return render_template(
            "index.html",
            students=students,
            stats=stats
        )

    except (mysql.connector.Error, RuntimeError) as error:
        app.logger.error("GradeFlow database error: %s", error)
        return (
            "Unable to connect to GradeFlow's database. "
            "Check your .env settings, MySQL service, and database objects. "
            "See the VS Code terminal for details.",
            500
        )

    finally:
        if cursor is not None:
            cursor.close()
        if db is not None and db.is_connected():
            db.close()


@app.route("/add", methods=["POST"])
def add_student():
    db = None
    cursor = None

    try:
        student_id = int(request.form["student_id"])
        student_name = request.form["student_name"].strip()
        marks = float(request.form["marks"])
        department = request.form["department"].strip()

        if not student_name or not department:
            flash("Please fill in every field.", "error")
            return redirect(url_for("home"))

        if not 0 <= marks <= 100:
            flash("Marks must be between 0 and 100.", "error")
            return redirect(url_for("home"))

        db = get_db_connection()
        cursor = db.cursor()
        cursor.callproc(
            "AddStudent",
            (student_id, student_name, marks, department)
        )
        db.commit()
        flash("Student added successfully!", "success")

    except (ValueError, KeyError):
        flash("Enter a valid student ID, name, marks, and department.", "error")

    except mysql.connector.Error as error:
        if db is not None:
            db.rollback()
        app.logger.error("Could not add student: %s", error)
        flash("Could not add student. Check the ID and database settings.", "error")

    except RuntimeError as error:
        app.logger.error("Database configuration error: %s", error)
        flash("MySQL password is missing. Check your .env file.", "error")

    finally:
        if cursor is not None:
            cursor.close()
        if db is not None and db.is_connected():
            db.close()

    return redirect(url_for("home"))


@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    db = None
    cursor = None

    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(
            "DELETE FROM Students WHERE student_id = %s",
            (student_id,)
        )
        db.commit()

        if cursor.rowcount:
            flash("Student deleted successfully.", "success")
        else:
            flash("Student record was not found.", "error")

    except (mysql.connector.Error, RuntimeError) as error:
        if db is not None:
            db.rollback()
        app.logger.error("Could not delete student: %s", error)
        flash("Could not delete student. Check the database connection.", "error")

    finally:
        if cursor is not None:
            cursor.close()
        if db is not None and db.is_connected():
            db.close()

    return redirect(url_for("home"))


if __name__ == "__main__":
    # Keep debug mode for local development only
    app.run(debug=True)
