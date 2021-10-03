from app import mysql



class Students(object):

    def __init__(self, firstname=None, lastname=None, course=None, id=None, year=None, gender=None):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.course = course
        self.year = year
        self.gender = gender

    def add(self):
        cursor = mysql.connection.cursor()

        sql = f"INSERT INTO student(id, lastname, firstname, course, yearlevel, gender) \
                VALUES('{self.id}', '{self.firstname}', '{self.lastname}', '{self.course}','{self.year}','{self.gender}')" 

        cursor.execute(sql)
        mysql.connection.commit()

    def edit(self):
        cursor = mysql.connection.cursor()
        print("OVER HERE")
        print(self.gender)
        sql = f"UPDATE student SET lastname = '{self.firstname}', firstname = '{self.lastname}', course = '{self.course}', yearlevel = '{self.year}', gender = '{self.gender}'\
             WHERE id = '{self.id}'"
        try:
            cursor.execute(sql)
        except Exception as e:
            print(e)
        mysql.connection.commit()

    @classmethod
    def all(cls):
        cursor = mysql.connection.cursor()

        sql = "SELECT * from student"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    @classmethod
    def delete(cls,id):
        try:
            cursor = mysql.connection.cursor()
            sql = f"DELETE from student where id= {id}"
            cursor.execute(sql)
            mysql.connection.commit()
            return True
        except:
            return False

    @staticmethod
    def search(id):
        cursor = mysql.connection.cursor()
        sql = f"SELECT * from student where id = '{id}'"
        cursor.execute(sql)
        student = cursor.fetchall()
        print("HEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
        print(student)
        
        return student

        
