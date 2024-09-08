import os
import pandas as pd
import urllib.parse

from flask import Flask, flash, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from sqlalchemy.exc import SQLAlchemyError
from forms import UploadForm, SearchForm
from models import db, Student
from sqlalchemy import func

app = Flask(__name__)
bootstrap = Bootstrap5(app)

# 使用环境变量
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'iHmRCPyQaxz5TDwtZMRa2aRZUUKk')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///students.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        name = search_form.name.data.strip()  # 移除首尾的空白字符
        students = Student.query.filter(func.trim(Student.name) == name).all()
        
        for student in students:
            # URL encode the class name to handle special characters
            student.qr_code = f"{student.class_name}.jpg"
        
        return render_template('result.html', students=students)
    return render_template('index.html', form=search_form)

def process_excel(file):
    df = pd.read_excel(file)
    students = []
    for _, row in df.iterrows():
        student = Student(
            name=row['姓名'],
            id_card=row['身份证号'],
            parent_phone = str(row['家长电话']).split('.')[0] if pd.notna(row['家长电话']) else None,
            class_name=row['班级'],
            classroom=row['教室位置'],
            teacher_name=row['班主任姓名'],
            teacher_phone=row['班主任电话'],
            dormitory=row['寝室安排']  # New field
        )
        students.append(student)
    return students

@app.route('/UN5Ffqie', methods=['GET', 'POST'])
def upload():
    upload_form = UploadForm()
    if upload_form.validate_on_submit():
        file = upload_form.file.data
        try:
            # 清空数据库
            Student.query.delete()
            
            # 解析上传的 Excel 文件并导入数据库
            students = process_excel(file)
            db.session.bulk_save_objects(students)
            db.session.commit()

            flash(f'成功导入 {len(students)} 条信息。', 'success')
            return redirect(url_for('index'))
        except pd.errors.EmptyDataError:
            flash('上传的文件为空，请检查文件内容。', 'error')
        except SQLAlchemyError as e:
            flash(f'数据库错误：{str(e)}', 'error')
        except Exception as e:
            flash(f'发生错误：{str(e)}', 'error')
        finally:
            db.session.rollback()

    return render_template('import.html', form=upload_form)

if __name__ == '__main__':
    app.run(debug=True)
