from flask import render_template, redirect, request, jsonify

from app.student import forms
from . import user_bp
import app.models as models
from app.student.forms import UserForm, CollegeForm, CourseForm, SearchForm
from app import mysql
import cloudinary
import cloudinary.uploader
import cloudinary.api

def fetch_from_table(table_name, column):
    cursor = mysql.connection.cursor()
    sql = f"SELECT {column} from {table_name}"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

#student routes
@user_bp.route('/user', methods=['POST','GET'])
def index():
    if request.method == 'GET':
        users = models.Students.all()
        form = SearchForm(request.form)
        return render_template('index.html', data=users,title='Home',form=form, something='Students')
    if request.method == 'POST':
        form = SearchForm(request.form["searchbar"])
        users = models.Students.all()
        final = []
        for data in users:
            for row in data:
                if form.searchbar.data.lower() in row.lower():
                    final.append(data)
                    break
        return render_template('index.html', data=final,title='Home',form=form, something='Students')

@user_bp.route('/user/register', methods=['POST','GET'])
def register():
    form = UserForm(request.form)
    form.course.choices=[]

    for row in fetch_from_table('course', 'code'):
        course = str(row[0])
        form.course.choices += [(course, course)]
    if request.method == 'POST' and form.validate():
        #form.upload.data.filename.split("/")[-1].split(".")[0]
        if bool(form.upload.data):
            req = cloudinary.uploader.upload(form.upload.data.stream, public_id = form.id.data)
            print(req)
            req = req["secure_url"]
        else:
            req=None
        user = models.Students(id=form.id.data, firstname=form.firstname.data, lastname=form.lastname.data, course=form.course.data, year=form.year.data, gender=form.gender.data, url = req)
        user.add()
        return redirect('/user')
    else:
        return render_template('signup.html', form=form, geturl='.register', something='Back to Students')

@user_bp.route("/user/delete", methods=["POST"])
def delete():
    id = request.form['id']
    if models.Students.delete(id):
        return jsonify(success=True,message="Successfully deleted")
    else:
        return jsonify(success=False,message="Failed")        

@user_bp.route("/user/edit", methods=['POST','GET'])
def editroute():
    if request.method == 'GET':
        id = request.args.get("id")
        student = models.Students.search(id)
        form = UserForm(student[0][0],student[0][1],student[0][2],student[0][3],student[0][4],student[0][5])
    else:
        form = UserForm()
    
    form.course.choices=[]
    for row in fetch_from_table('course', 'code'):
        course = str(row[0])
        form.course.choices += [(course, course)]
    print()
    if request.method == 'POST' and form.validate():
        print(form.upload.data)
        if bool(form.upload.data):
            req = cloudinary.uploader.upload(form.upload.data.stream, public_id = form.id.data)
            print(req)
            req=req["secure_url"]
        else:
            req="ignore"
            print(req)
        user = models.Students(id=form.id.data, firstname=form.firstname.data, lastname=form.lastname.data, course=form.course.data, year=form.year.data, gender=form.gender.data,url=req)
        user.edit()
        return redirect('/user')
    else:
        return render_template('signup.html', form=form, geturl='.editroute', something='Back to Students')           

#college routes
@user_bp.route('/college', methods=['POST','GET'])
def colindex():
    if request.method == 'GET':
        colleges = models.Colleges.all()
        form = SearchForm(request.form)
        return render_template('college.html', data=colleges,title='College List', something='Colleges',form=form)
    if request.method == 'POST':
        form = SearchForm(request.form["searchbar"])
        colleges = models.Colleges.all()
        final = []
        for data in colleges:
            for row in data:
                if form.searchbar.data.lower() in row.lower():
                    final.append(data)
                    break
        return render_template('college.html', data=final,title='College List', something='Back to Colleges',form=form)

@user_bp.route('/college/new', methods=['POST','GET'])
def colreg():
    form = CollegeForm(request.form)

    if request.method == 'POST' and form.validate():
        college = models.Colleges(code=form.code.data, name=form.name.data)
        college.add()
        return redirect('/college')
    else:
        return render_template('colcourseform.html', form=form, geturl='.colreg', something='Back to Colleges',bc ="/college")

@user_bp.route("/college/delete", methods=["POST"])
def colldel():
    code = request.form['id']
    if models.Colleges.delete(code):
        return jsonify(success=True,message="Successfully deleted")
    else:
        return jsonify(success=False,message="Failed")   

@user_bp.route("/college/edit", methods=['POST','GET'])
def colledit():
    if request.method == 'GET':
        id = request.args.get("id")
        college = models.Colleges.search(id)
        form = CollegeForm(college[0][0],college[0][1])
    else:
        form = CollegeForm(request.form["code"],request.form["name"])

    if request.method == 'POST' and form.validate():
        user = models.Colleges(code=form.code.data, name=form.name.data)
        user.edit()
        return redirect('/college')
    else:
        return render_template('colcourseform.html', form=form, geturl='.colledit', something='Back to Colleges',bc ="/college")

#course routes
@user_bp.route('/course', methods=['POST','GET'])
def courseindex():
    if request.method == 'GET':
        colleges = models.Courses.all()
        form = SearchForm(request.form)
        return render_template('course.html', data=colleges,title='Course List', something='Courses',form=form)
    if request.method == 'POST':
        form = SearchForm(request.form["searchbar"])
        colleges = models.Courses.all()
        final = []
        for data in colleges:
            for row in data:
                if form.searchbar.data.lower() in row.lower():
                    final.append(data)
                    break
        return render_template('course.html', data=final,title='Course List', something='Back to Courses',form=form)

@user_bp.route('/course/new', methods=['POST','GET'])
def coursereg():
    form = CourseForm(request.form)

    form.college.choices=[]
    for row in fetch_from_table('college', 'code'):
        college = str(row[0])
        form.college.choices += [(college, college)]

    if request.method == 'POST' and form.validate():
        course = models.Courses(code=form.code.data, name=form.name.data, college=form.college.data)
        course.add()
        return redirect('/course')
    else:
        return render_template('colcourseform.html', form=form, geturl='.coursereg', something='Back to Courses',bc ="/course")

@user_bp.route("/course/delete", methods=["POST"])
def coursedel():
    code = request.form['id']
    if models.Courses.delete(code):
        return jsonify(success=True,message="Successfully deleted")
    else:
        return jsonify(success=False,message="Failed")   

@user_bp.route("/course/edit", methods=['POST','GET'])
def courseedit():
    if request.method == 'GET':
        id = request.args.get("id")
        course = models.Courses.search(id)
        form = CourseForm(course[0][0],course[0][1],course[0][2])
    else:
        form = CourseForm(request.form["code"],request.form["name"],request.form["college"])

    form.college.choices=[]
    for row in fetch_from_table('college', 'code'):
        college = str(row[0])
        form.college.choices += [(college, college)]

    if request.method == 'POST' and form.validate():
        course = models.Courses(code=form.code.data, name=form.name.data, college=form.college.data)
        course.edit()
        return redirect('/course')
    else:
        return render_template('colcourseform.html', form=form, geturl='.courseedit', something='Back to Courses',bc ="/course")                
