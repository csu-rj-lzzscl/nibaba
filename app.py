from flask import Flask,render_template,flash,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)

app.secret_key = 'test'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@127.0.0.1:3306/teachSystem?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class Classroom(db.Model):
    __tablename__ = 'classrooms'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255),nullable=False)

    students = db.relationship('Student',backref='classroom')
    courses = db.relationship('Course',backref='classroom')


class Teacher(db.Model):
    __tablename__ = 'teachers'

    username = db.Column(db.String(255),primary_key=True)
    password = db.Column(db.String(16),nullable=False)
    telephone = db.Column(db.String(11),nullable=False)
    email = db.Column(db.String(255),nullable=False)

    courses = db.relationship('Course',backref='teacher')

    def __repr__(self):
        return '<Teacher: %s %s %s>' %(self.username,self.telephone,self.email)


class Student(db.Model):
    __tablename__ = 'students'

    username = db.Column(db.String(255),primary_key=True)
    password = db.Column(db.String(16),nullable=False)
    telephone = db.Column(db.String(11),nullable=False)
    email = db.Column(db.String(255),nullable=False)
    classroom_id = db.Column(db.Integer,db.ForeignKey('classrooms.id'))

    def __repr__(self):
        return '<Student: %s %s %s %s>' %(self.username,self.telephone,self.email,self.classroom_id)


class Course(db.Model):
    __tablename__  = 'courses'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255),nullable=True)
    teacher_name = db.Column(db.String(255),db.ForeignKey('teachers.username'))
    classroom_id = db.Column(db.Integer,db.ForeignKey('classrooms.id'))

    def __repr__(self):
        return '<Course: %s %s %s>' %(self.name,self.teacher_name,self.classroom_id)


@app.route('/',methods=['GET','POST'])
def index():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_type = request.form.get('user_type')

        if not all([username,password]):
            flash('请补全用户信息')
        else:
            if user_type == "student":
                student = Student.query.filter_by(username=username, password=password).first()

                if student:
                    return 'success'
                else:
                    flash('用户名不存在或密码错误')
            else:
                teacher = Teacher.query.filter_by(username=username,password=password).first()

                if teacher:
                    return 'success2'
                else:
                    flash('用户名不存在或密码错误')

    return render_template('login.html')


@app.route('/register_student',methods=['GET','POST'])
def register_student():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        telephone = request.form.get('telephone')
        email = request.form.get('email')
        classroom_id = request.form.get('classroom')

        student = Student.query.filter_by(username=username).first()

        if not all([username,password,telephone,email,classroom_id]):
            return redirect(url_for('register_student'))

        else:
            if student:
                flash('该用户名已存在')
            else:
                try:
                    new_student = Student(username=username, password=password, telephone=telephone,
                                          email=email,classroom_id=classroom_id)
                    db.session.add(new_student)
                    db.session.commit()
                    return render_template('login.html')
                except Exception as e:
                    print(e)
                    flash('添加用户失败')
                    db.session.rollback()

    return render_template('register_student.html')


@app.route('/register_teacher',methods=['GET','POST'])
def register_teacher():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        telephone = request.form.get('telephone')
        email = request.form.get('email')

        teacher = Teacher.query.filter_by(username=username).first()

        if not all([username,password,telephone,email]):
            return redirect(url_for('register_teacher'))

        else:
            if teacher:
                flash('该用户名已存在')
            else:
                try:
                    new_teacher = Student(username=username, password=password, telephone=telephone,
                                          email=email)
                    db.session.add(new_teacher)
                    db.session.commit()
                    return render_template('login.html')
                except Exception as e:
                    print(e)
                    flash('添加用户失败')
                    db.session.rollback()

    return render_template('register_teacher.html')


if __name__ == '__main__':
    app.run()
