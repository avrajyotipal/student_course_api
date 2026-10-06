# Student Course Enrollment API

A simple REST API built using **FastAPI** and **SQLAlchemy** that allows students to enroll in courses.

The project demonstrates how to build a database-driven FastAPI application with CRUD operations, Pydantic validation, SQLAlchemy ORM relationships, foreign keys, error handling, and database-level constraints.

---

## 🚀 Features

- Create courses
- Retrieve all courses
- Enroll students in courses
- Prevent duplicate course enrollment
- Retrieve all courses enrolled by a student
- Delete an enrollment
- Validate whether a student exists
- Validate whether a course exists
- Meaningful HTTP error responses
- SQLite database using SQLAlchemy ORM
- Interactive Swagger API documentation

---

## 🛠️ Technologies Used

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Uvicorn
- Swagger / OpenAPI

---

## 📁 Project Structure

```text
student_course_api/
│
├── venv/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── seed.py
├── requirements.txt
├── .gitignore
├── README.md
└── student_course.db

## File Description:

| File                | Purpose                                    |
| ------------------- | ------------------------------------------ |
| `main.py`           | FastAPI application and API endpoints      |
| `database.py`       | Database connection and SQLAlchemy session |
| `models.py`         | SQLAlchemy database models                 |
| `schemas.py`        | Pydantic request and response schemas      |
| `seed.py`           | Creates sample students                    |
| `requirements.txt`  | Python dependencies                        |
| `.gitignore`        | Files excluded from Git                    |
| `README.md`         | Project documentation                      |
| `student_course.db` | SQLite database                            |

