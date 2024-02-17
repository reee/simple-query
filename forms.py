from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired

class UploadForm(FlaskForm):
    file = FileField('上传Excel文件', validators=[
        FileRequired(),
        FileAllowed(['xlsx'], '仅支持xlsx文件!')
    ])
    submit = SubmitField('Upload')

class SearchForm(FlaskForm):
    name = StringField('请输入学生姓名', validators=[DataRequired()])
    submit = SubmitField('检索')
