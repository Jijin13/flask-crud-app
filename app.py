from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()


class Enroll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    rollnumber = db.Column(db.Integer, unique=True, nullable=False)
    enrolled_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Data %r>' % self.id
    
def is_valid_name(name):
    if isinstance(name, str) and name.replace(" ", "").isalpha():
        return True
    return False

def is_valid_rollnumber(rollnumber):
    if rollnumber.isdigit():
        return True
    return False

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        student_name = request.form['name']
        student_rollnumber = request.form['rollnumber']

        if not is_valid_name(student_name):
            return "Enter a valid student name"
        
        if not is_valid_rollnumber(student_rollnumber):
            return "Enter a valid roll number"

        existing_data = Enroll.query.filter_by(rollnumber=student_rollnumber).first()
        if existing_data:
            return "Roll number already exist"
        
        new_data = Enroll(name=student_name, rollnumber=student_rollnumber)

        try:
            db.session.add(new_data)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your data'
    else:
        datas = Enroll.query.order_by(Enroll.enrolled_date).all()
        return render_template('index.html', datas=datas)
    
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    data = Enroll.query.get_or_404(id)
    
    if request.method == 'POST':
        data.name = request.form['name']
        data.rollnumber = request.form['rollnumber']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('edit.html', data=data)
    
@app.route('/delete/<int:id>')
def delete(id):
    data = Enroll.query.get_or_404(id)

    try:
        db.session.delete(data)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem in deleting that data'

if __name__ == '__main__':
    app.run(debug=True, port=5001)