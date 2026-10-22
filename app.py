import os
from dotenv import load_dotenv

load_dotenv()
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "gradeflow-local-key"


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("Etisql@123"),
        database="StudentDB"
    )

@app.route("/")
def home():
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
               COALESCE(ROUND(AVG(marks), 2), 0) AS average
        FROM Students
    """)
    stats = cursor.fetchone()

    cursor.close()
    db.close()

    return render_template(
        "index.html",
        students=students,
        stats=stats
    )


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
            flash("Please fill in all fields.", "error")
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
        flash("Please enter valid student details.", "error")

    except mysql.connector.Error as error:
        flash(f"Database error: {error}", "error")

    finally:
        if cursor is not None:
            cursor.close()
        if db is not None:
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
        flash("Student deleted successfully.", "success")

    except mysql.connector.Error as error:
        flash(f"Database error: {error}", "error")

    finally:
        if cursor is not None:
            cursor.close()
        if db is not None:
            db.close()

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
