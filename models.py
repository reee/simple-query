from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    id_card = db.Column(db.String(18), nullable=False)
    parent_phone =  db.Column(db.String(15))
    class_name = db.Column(db.String(50), nullable=False)
    classroom = db.Column(db.String(50))
    teacher_name = db.Column(db.String(100))
    teacher_phone = db.Column(db.String(15))
    dormitory = db.Column(db.String(100))  # New field for dormitory arrangement

    def __repr__(self):
        return f"Student(name={self.name}, id_card={self.id_card}, class_name={self.class_name}, classroom={self.classroom}, teacher_name={self.teacher_name}, teacher_phone={self.teacher_phone}, dormitory={self.dormitory})"