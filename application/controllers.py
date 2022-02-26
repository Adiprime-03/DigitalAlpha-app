from flask import Flask
from flask import render_template as rt
from flask import request
from werkzeug.utils import redirect
from datetime import datetime as dt
from flask import current_app as app
from logging import exception
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time


from application.models import Student, Grades, Courses
from application.database import db
from application.scraping import roll_name

rollno = ""


@app.route("/login", methods =["GET", "POST"])
def login():
    if(request.method == "GET"):
        return rt('login.html', err = "")
    elif(request.method == "POST"):
        user_name = request.form["user_name"]
        password = request.form["password"]
        rollno, name, courseid, coursenames, coursecredits, grades, attendence = roll_name(user_name=user_name.upper(), password=password)
        
        stds = Student.query.all()
        student_names = []
        for std in stds:
            student_names.append(std.name)
        if(name not in student_names):
            std = Student(rollno = rollno, name = name)
            db.session.add(std)
            db.session.commit()

        cs = Courses.query.all()
        cl = []
        for c in cs:
            cl.append(c.courseno)
        for i in range(len(courseid)):
            if(courseid[i] not in cl):
                course = Courses(courseno = courseid[i], coursename = coursenames[i], credits = coursecredits[i])
                db.session.add(course)
                db.session.commit()

        gs = Grades.query.all()
        gl =[]
        for g in gs:
            x = (g.rollno, g.coursno)
            gl.append(x)
        for i in range(len(courseid)):
            y = (rollno, courseid[i])
            if(y not in gl):
                grade = Grades(rollno = rollno, coursno = courseid[i], grade = grades[i], attendance = attendence[i])
                db.session.add(grade)
                db.session.commit()

        return redirect(f"/{rollno}/grades")
    
    else:
        raise exception("Method Unknown")

@app.route("/<rollno>/grades")
def grades(rollno):
    student = Student.query.filter(Student.rollno == rollno.upper()).all()
    grade = Grades.query.filter(Grades.rollno == rollno.upper()).all()

    return rt("grades.html", grade = grade, name = student[0])
