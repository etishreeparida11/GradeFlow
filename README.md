GradeFlow — Student Record Management System

GradeFlow is a web-based student management application built using Python, Flask, and MySQL. It helps users manage student records, calculate grades, and monitor academic performance through a simple dashboard.

Features

- Student Dashboard: View all registered students.
- Grade Calculation: Automatically calculate grades using a MySQL stored function.
- Add Students: Register students with their ID, name, marks, and department.
- Delete Students: Remove student records.
- Performance Statistics: Display total students, average marks, and Grade A student count.
- MySQL Integration: Store and retrieve student data from a MySQL database.
- Responsive Interface: Dashboard styling using HTML and CSS.

Technologies Used

- Python
- Flask
- MySQL
- MySQL Workbench
- HTML
- CSS
- Visual Studio Code

Project Structure

```text
GradeFlow/
├── app.py
├── schema.sql
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   └── index.html
└── static/
    └── style.css
```

 Prerequisites

Install the following before running the application:

- Python 3
- MySQL Server
- MySQL Workbench (recommended for database management)
- Git

 Installation and Setup

 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd GradeFlow
```

Replace `YOUR_REPOSITORY_URL` with your GitHub repository URL.

 2. Create a Python virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

 4. Configure MySQL

Open MySQL Workbench and create the `StudentDB` database, the `Students` table, the `GetGrade` function, and the `AddStudent` stored procedure.

Use `schema.sql` as the database setup reference. If the database and objects already exist, do not execute the script unnecessarily.

 5. Configure database credentials

Set your MySQL host, username, password, and database name in a local `.env` file. Do not upload this file to GitHub.

Ensure `app.py` reads these settings from environment variables.

 6. Run the application

```bash
python app.py
```

Open this address in your browser:

```text
http://127.0.0.1:5000
```

Keep the Flask terminal running while using the dashboard.

 Grade Calculation

| Marks | Grade |
|---|---|
| 80–100 | A |
| 60–79.99 | B |
| 40–59.99 | C |
| Below 40 | Fail |

The grade is calculated using the MySQL `GetGrade()` function.

 Database

The `Students` table stores:

- Student ID
- Student name
- Marks
- Department

The `AddStudent` stored procedure inserts new student records.

 Future Enhancements

- Edit student records
- Search and filter students
- Grade distribution charts
- Student login and authentication
- Export student reports

 Author

Name : Etishree Parida
UID : 26MCC20037
University: Chandigarh University
Course : Mca CC&Devops

Developed as an academic mini-project to demonstrate Python web development, MySQL database operations, stored functions, and stored procedures.

 License

This project is intended for educational purposes. Add a license if you plan to distribute it publicly.