import flask
from flask import Flask
from flask import render_template
from flask import request,flash,url_for,redirect
from flask_sqlalchemy import SQLAlchemy

# from requests import session




app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///week7_database.sqlite3'
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

class Enrollments(db.Model):
    __tablename__ = 'enrollments'
    enrollment_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    estudent_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable = False)
    ecourse_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable = False)

class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    course_code = db.Column(db.String, nullable = False, unique = True)
    course_name = db.Column(db.String, nullable =False)
    course_description = db.Column(db.String)
    students = db.relationship('Student', secondary = 'enrollments')

class Student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    roll_number = db.Column(db.String, nullable =False, unique = True)
    first_name = db.Column(db.String, nullable =False)
    last_name = db.Column(db.String)
    courses = db.relationship('Course', secondary = 'enrollments')


    
@app.route('/', methods = ['GET', 'POST'])
def home():
    students = Student.query.all()
    if students:
     return render_template('index.html', rows = students)
    else:
        return render_template('initial.html') 

@app.route('/courses' , methods = ['GET','POST'])
def course():
    courses = Course.query.all()
    if courses:
        return render_template('course_index.html', rows = courses)
    else:
        return render_template('course_initial.html')    

@app.route('/student/<int:stud_id>/update', methods = ['GET', 'POST'])
def update(stud_id):
    if request.method == 'GET':
        student = Student.query.get(stud_id)
        courses = Course.query.all()
        return render_template('update.html', student = student , courses = courses)

    elif request.method == 'POST':
        first_name = request.form['f_name']
        last_name = request.form['l_name']
       
        student = Student.query.get(stud_id)
        student.first_name = first_name
        student.last_name = last_name
        
        course = request.form['course']
        enroll = Enrollments(estudent_id = stud_id, ecourse_id = int(course[0]))
        db.session.add(enroll)       

        db.session.flush()    
        db.session.commit()
        return flask.redirect('/')

@app.route('/course/<int:course_id>/update' , methods = ['GET','POST'])
def course_update(course_id):
    if request.method == 'GET':
        course = Course.query.get(course_id)
        return render_template('course_update.html',course = course)
    elif request.method == 'POST':
        course_name = request.form['c_name']
        course_description = request.form['desc']
        course = Course.query.get(course_id)
        course.course_name = course_name
        course.course_description = course_description

        db.session.commit()
        return flask.redirect('/courses')       

@app.route('/student/<int:student_id>/delete', methods = ['GET'])
def delete(student_id):
   student = Student.query.get(student_id)
   enr = Enrollments.query.filter_by(estudent_id = student_id).all()
   for i in enr:
    db.session.delete(i)
   db.session.delete(student)
   db.session.commit()
   return flask.redirect('/')

@app.route('/course/<int:course_id>/delete',methods = ['GET','POST'])
def course_delete(course_id):
    course = Course.query.get(course_id)
    course_enr = Enrollments.query.filter_by(ecourse_id = course_id).all()
    for i in course_enr:
        db.session.delete(i)
    db.session.delete(course)
    db.session.commit()
    return flask.redirect('/')    


@app.route('/student/create', methods = ['GET', 'POST'])
def addStudent():
    if request.method == 'GET':
        return render_template('add.html')
    elif request.method == 'POST':
        try:
            roll_number = request.form['roll']
            first_name = request.form['f_name']
            last_name = request.form['l_name']
            student = Student(roll_number = roll_number, first_name = first_name, last_name = last_name)
            db.session.add(student)
            db.session.flush()
            courses = request.form.getlist('courses')
            for course in courses:
                enroll = Enrollments(estudent_id = student.student_id, ecourse_id = int(course[-1]))
                db.session.add(enroll)
        except:
            db.session.rollback()
            return render_template('wrong.html')
        else:
            db.session.commit()
            return flask.redirect('/')

@app.route('/course/create',methods = ['GET','POST'])
def addCourse():
    if request.method == 'GET':
        return render_template('course_add.html')
    elif request.method == 'POST':
        try:
            course_code = request.form['code']
            course_name = request.form['c_name']
            course_description = request.form['desc']
            course = Course(course_code = course_code , course_name = course_name , course_description = course_description)
            db.session.add(course)
            db.session.flush()
        except:
            db.session.rollback()
            return render_template('course_wrong.html')
        else:
            db.session.commit()
            return flask.redirect('/courses')        


@app.route('/student/<int:student_id>', methods = ['GET','POST'])
def studentDetails(student_id):
    student=Student.query.get(student_id)
    return render_template("details.html",student=student)   


@app.route('/course/<int:course_id>',methods = ['GET','POST'])
def courseDetails(course_id):
    course = Course.query.get(course_id)
    return render_template('course_details.html',course = course)


@app.route('/student/<int:student_id>/withdraw/<int:course_id>' , methods = ['GET' , 'POST'])
def withdraw(student_id,course_id):
    course = Course.query.get(course_id)
    student = Student.query.get(student_id)
    enr = Enrollments.query.filter_by(estudent_id = student_id , ecourse_id = course_id).all()
    for i in enr:
      db.session.delete(i)
    db.session.commit()
    return flask.redirect('/')


if __name__ == '__main__':
    app.run(debug = True)