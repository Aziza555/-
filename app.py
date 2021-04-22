from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema
from flask_rest_jsonapi import Api, ResourceDetail, ResourceList
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os


app = Flask(__name__)
 
database_location = os.getcwd()+'\\app.db'
 

app.config['FLASK_ADMIN_SWATCH'] = 'flatly'

 
admin = Admin(app, name='Администратор', template_mode='bootstrap3')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+database_location
 
db = SQLAlchemy(app)
 
 
class Dog(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    type_dog = db.Column(db.String)
    count = db.Column(db.Integer)
    description = db.Column(db.Text)
    brought_in = db.Column(db.Date)
 
 
class DogSchema(Schema):
    class Meta:
        type_ = 'собака'
        self_view = 'dog_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'Dog_list'
 
    id = fields.Integer(as_string=True)
    type_Dog = fields.Str(required = True)
    weight = fields.Integer(as_string=True)
    brought_in = fields.Date()
 
class DogList(ResourceList):
    schema = DogSchema
    data_layer = {'session': db.session,
                  'model': Dog} 
 
class DogDetail(ResourceDetail):
    schema = DogSchema
    data_layer = {'session': db.session,
                  'model': Dog}
 
 
api = Api(app)
api.route(DogList, 'Dog_list', '/Dog')
api.route(DogDetail, 'Dog_detail', '/Dog/<int:id>')
 

admin.add_view(ModelView(Dog, db.session))
 
 
 
 
if __name__ == '__main__':
    app.run(debug=True)
