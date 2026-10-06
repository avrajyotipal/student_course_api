from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from models import Student, Course, Enrollment
from schemas import (
    CourseCreate,
    CourseResponse,
    EnrollmentCreate,
    EnrollmentResponse
)


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Student Course Enrollment API",
    description="FastAPI application for student course enrollment",
    version="1.0.0"
)


# --------------------------------------------------
# POST /courses
# Create a new course
# --------------------------------------------------

@app.post(
    "/courses",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED
)
def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db)
):

    new_course = Course(
        name=course.name,
        description=course.description
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course


# --------------------------------------------------
# GET /courses
# Get all courses
# --------------------------------------------------

@app.get(
    "/courses",
    response_model=list[CourseResponse]
)
def get_courses(
    db: Session = Depends(get_db)
):

    courses = db.query(Course).all()

    return courses


# --------------------------------------------------
# POST /enroll
# Enroll a student in a course
# --------------------------------------------------

@app.post(
    "/enroll",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED
)
def enroll_student(
    enrollment: EnrollmentCreate,
    db: Session = Depends(get_db)
):

    # Check student
    student = db.query(Student).filter(
        Student.id == enrollment.student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student does not exist"
        )

    # Check course
    course = db.query(Course).filter(
        Course.id == enrollment.course_id
    ).first()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course does not exist"
        )

    # Check duplicate enrollment
    existing_enrollment = db.query(Enrollment).filter(
        Enrollment.student_id == enrollment.student_id,
        Enrollment.course_id == enrollment.course_id
    ).first()

    if existing_enrollment:
        raise HTTPException(
            status_code=400,
            detail="Student is already enrolled in this course"
        )

    # Create enrollment
    new_enrollment = Enrollment(
        student_id=enrollment.student_id,
        course_id=enrollment.course_id
    )

    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)

    return new_enrollment


# --------------------------------------------------
# GET /students/{student_id}/courses
# Get courses for a student
# --------------------------------------------------

@app.get(
    "/students/{student_id}/courses"
)
def get_student_courses(
    student_id: int,
    db: Session = Depends(get_db)
):

    # Check student
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student does not exist"
        )

    enrollments = db.query(Enrollment).filter(
        Enrollment.student_id == student_id
    ).all()

    courses = []

    for enrollment in enrollments:
        courses.append({
            "enrollment_id": enrollment.id,
            "course_id": enrollment.course.id,
            "course_name": enrollment.course.name,
            "description": enrollment.course.description
        })

    return {
        "student_id": student_id,
        "student_name": student.name,
        "courses": courses
    }


# --------------------------------------------------
# DELETE /enroll/{enrollment_id}
# Delete an enrollment
# --------------------------------------------------

@app.delete(
    "/enroll/{enrollment_id}"
)
def delete_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db)
):

    enrollment = db.query(Enrollment).filter(
        Enrollment.id == enrollment_id
    ).first()

    if not enrollment:
        raise HTTPException(
            status_code=404,
            detail="Enrollment does not exist"
        )

    db.delete(enrollment)
    db.commit()

    return {
        "message": "Enrollment deleted successfully",
        "enrollment_id": enrollment_id
    }