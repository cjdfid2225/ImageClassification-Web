import os
from flask import Flask, render_template, request, redirect
from models import db, Fcuser

from flask_wtf.csrf import CSRFProtect
from forms import RegisterForm


app = Flask(__name__)

@app.route('/')
def first_page():
    return render_template('first.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        fcuser = Fcuser()
        fcuser.userid = form.data.get('userid')
        fcuser.userheight = form.data.get('userheight')
        fcuser.userweight = form.data.get('userweight')
        fcuser.userold = form.data.get('userold')
        fcuser.usersex = form.data.get('usersex')
        fcuser.password = form.data.get('password')

        db.session.add(fcuser) # 변수에 넣은 회원정보를 db에 저장
        db.session.commit()

        return "가입완료"

    return render_template('register.html', form=form)

@app.route('/info',  methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():

    req = request.form
    print("req: ", req)

    return render_template('upload.html')


if __name__ == '__main__':
    basedir = os.path.abspath(os.path.dirname(__file__)) #db파일을 절대경로로 생성
    dbfile = os.path.join(basedir, 'db.sqlite') #db파일을 절대경로로 생성
    app.config['SQLALCHEMY_DATABASE_URl'] = 'sqlite:///' + dbfile #sqlite 사용
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True #사용자 요청의 끝마다 커밋(데이터베이스에 저장,수정,삭제등의 동작을 쌓아놨던 것들의 실행명령)을 한다
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #수정사항에 대한 track을 하지 않는다. True로 하면 warning 메세지
    app.config['SECRET_KEY'] = 'aiwlgej'

    csrf = CSRFProtect()
    csrf.init_app(app)

    db.init_app(app)
    db.app = app
    db.create_all() #db 생성
    
    app.run( debug=True )