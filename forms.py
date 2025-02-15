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
    name = StringField('学生姓名', validators=[DataRequired()])
    id_last_four = StringField('身份证后4位', validators=[DataRequired()],
                              description='如果身份证最后一位是X，请输入大写X')
    submit = SubmitField('查询')
