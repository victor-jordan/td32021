from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///studentsdb.sqlite3'
app.config['SECRET_KEY'] = '5u8x/A%D'

db = SQLAlchemy(app)

ma = Marshmallow(app)

api = Api(app)


class student(db.Model):
    """
      Clase que representa los estudiantes
    """
    id = db.Column('id', db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    edad = db.Column(db.Integer)

    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def __repr__(self):
        return '<Estudiante %s>' % self.nombre


class studentSchema(ma.Schema):
    class Meta:
        fields = ("id", "nombre", "edad")
        model = student


student_schema = studentSchema()
students_schema = studentSchema(many=True)


class studentsListResource(Resource):
    def get(self):
        lista = student.query.all()
        return students_schema.dump(lista)

    def post(self):
        new_student = student(
            nombre=request.json['nombre'],
            edad=request.json['edad']
        )
        db.session.add(new_student)
        db.session.commit()

        return student_schema.dump(new_student)

api.add_resource(studentsListResource, '/estudiantes')


if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)