from flask import render_template, redirect, request, jsonify
from . import user_bp
import app.models as models
from app.student.forms import UserForm
from app import mysql

def fetch_from_table(table_name, column):
    cursor = mysql.connection.cursor()
    sql = f"SELECT {column} from {table_name}"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

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