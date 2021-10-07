from flask import render_template, redirect, request, jsonify
from . import user_bp
import app.models as models
from app.student.forms import UserForm, CollegeForm, CourseForm
from app import mysql

def fetch_from_table(table_name, column):
    cursor = mysql.connection.cursor()
    sql = f"SELECT {column} from {table_name}"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

#student routes
@user_bp.route('/user')
@user_bp.route('/index')
def index():
    users = models.Students.all()
    return render_template('index.html', data=users,title='Home',something='something')

@user_bp.route('/user/register', methods=['POST','GET'])
def register():
    form = UserForm(request.form)
    form.course.choices=[]

    for row in fetch_from_table('course', 'code'):
        course = str(row[0])
        form.course.choices += [(course, course)]

    if request.method == 'POST' and form.validate():
        user = models.Students(id=form.id.data, firstname=form.firstname.data, lastname=form.lastname.data, course=form.course.data, year=form.year.data, gender=form.gender.data,)
        user.add()
        return redirect('/user')
    else:
        return render_template('signup.html', form=form, geturl='.register')

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
        form = UserForm(request.form["id"],request.form["firstname"],request.form["lastname"],request.form["course"],request.form["year"],request.form["gender"])
    
    form.course.choices=[]
    for row in fetch_from_table('course', 'code'):
        course = str(row[0])
        form.course.choices += [(course, course)]

    if request.method == 'POST' and form.validate():
        user = models.Students(id=form.id.data, firstname=form.firstname.data, lastname=form.lastname.data, course=form.course.data, year=form.year.data, gender=form.gender.data,)
        user.edit()
        return redirect('/user')
    else:
        return render_template('signup.html', form=form, geturl='.editroute')           

#college routes
@user_bp.route('/college')
def colindex():
    colleges = models.Colleges.all()
    return render_template('college.html', data=colleges,title='College List', something='something')

@user_bp.route('/college/new', methods=['POST','GET'])
def colreg():
    form = CollegeForm(request.form)

    if request.method == 'POST' and form.validate():
        college = models.Colleges(code=form.code.data, name=form.name.data)
        college.add()
        return redirect('/college')
    else:
        return render_template('colcourseform.html', form=form, geturl='.colreg')

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
        return render_template('colcourseform.html', form=form, geturl='.colledit')

#course routes
@user_bp.route('/course')
def courseindex():
    colleges = models.Courses.all()
    return render_template('course.html', data=colleges,title='Course List', something='something')

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
        return render_template('colcourseform.html', form=form, geturl='.coursereg')

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
        return render_template('colcourseform.html', form=form, geturl='.courseedit')                
