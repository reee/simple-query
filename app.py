from flask import Flask, flash, render_template, request, redirect, url_for
from forms import UploadForm, SearchForm
from models import db, Student
from flask_bootstrap import Bootstrap5
import pandas as pd

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        name = search_form.name.data
        students = Student.query.filter_by(name=name).all()
        return render_template('result.html', students=students)
            
    return render_template('index.html', form=search_form)

@app.route('/iRszpC8A', methods=['GET', 'POST'])
def upload():
    upload_form = UploadForm()
    if upload_form.validate_on_submit():
        file = upload_form.file.data
        try:
            # 清空数据库
            Student.query.delete()
            db.session.commit()

            # 解析上传的 Excel 文件并导入数据库
            df = pd.read_excel(file)
            num_imported = 0
            for index, row in df.iterrows():
                student = Student(
                    name=row['姓名'],
                    id_card=row['身份证号'],
                    class_name=row['班级'],
                    classroom=row['教室位置'],
                    teacher_name=row['班主任姓名'],
                    teacher_phone=row['班主任电话']
                )
                db.session.add(student)
                num_imported += 1
            db.session.commit()

            flash(f'成功导入 {num_imported} 条信息。', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(e, 'error')
            db.session.rollback()

    return render_template('import.html', form=upload_form)

if __name__ == '__main__':
    app.run(debug=True)
