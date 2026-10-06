from database import SessionLocal
from models import Student


db = SessionLocal()

students = [
    Student(name="Rahul"),
    Student(name="Priya"),
    Student(name="Amit")
]

db.add_all(students)
db.commit()

print("Students created successfully.")

db.close()