from .database import db

class Student(db.Model):
    __tablename__ = 'student'
    rollno = db.Column(db.String, primary_key = True)
    name = db.Column(db.String)

class Courses(db.Model):
    __tablename__ = 'courses'
    courseno = db.Column(db.String, primary_key = True)
    coursename = db.Column(db.String, unique = True)
    credits = db.Column(db.Integer)

class Grades(db.Model):
    __tablename__ = 'grades'
    rollno = db.Column(db.String, db.ForeignKey("student.rollno"), primary_key = True, nullable = False)
    coursno = db.Column(db.String, db.ForeignKey("courses.courseno"), primary_key = True, nullable = False)
    grade = db.Column(db.String)
    attendance = db.Column(db.String)