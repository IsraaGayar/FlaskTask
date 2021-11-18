from datetime import datetime

from flask_sqlalchemy import SQLAlchemy #import db api

# db_israa= SQLAlchemy() #instantiate sql alchemy class
# class todo(db_israa.Model):
#     id= db_israa.Column()


db = SQLAlchemy()  # instantiate sql alchemy class


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(125),nullable=False)
    description = db.Column(db.Text)
    finished = db.Column(db.Boolean)
    created_at=db.Column(db.DateTime)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.created_at= datetime.now()