from flask import Flask, jsonify, request
from flask_restful import Api,Resource
from models import Todo,db

# inherit from flask
app= Flask(__name__)
# create API for our app
todoApi= Api(app)
# setting files to include the database,(here we are using sqllite database)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS']=False
#
# todoList=[
#     {'l1':'Mylist1'},
#     {'l2':'Mylist2'},
# ]
# @app.route('/hello', methods =['GET'])
# def helloView():
#     return 'HEllo from the other side'
#
# @app.route('/todo', methods =['GET'])
# def ListTask():
#     return jsonify(todoList)
#
# @app.route('/todoitem/<int:taskId>', methods =['GET'])
# def taskView(taskId):
#     myTask=todoList[taskId]
#     print(myTask)
#     return jsonify(myTask)
#
#

# tasks with parameters (inhirets from Resources
class todoRUD(Resource):
    # if the request is get(dont change the function name)
    def get(self,**kwargs):
        task = Todo.query.get(kwargs.get('id'))
        try:
            mytask = {
                'name': task.name,
                'id': task.id,
                # 'created_at': task.created_at,
                'description': task.description
            }
            return mytask,200
        except Exception as e :
            print(e)
            return {'error': 'no such task'}

        # if i added a date to my responce, i need to jsonify it
        # return jsonify(mytask)

    # if the request is delete (dont change the function name)
    def delete(self,**kwargs):
        task = Todo.query.get(kwargs.get('id'))
        try:
            db.session.delete(task)
            db.session.commit()
            return {'success': 'task deleted successfully '}
        except Exception as e:
            print(e)
            return {'error': 'no such task'}

    # if the request is patch(dont change the function name)
    def patch(self,**kwargs):
        task = Todo.query.get(kwargs.get('id'))
        try:
            if request.form.get('name'):
                task.name=request.form.get('name')
            if request.form.get('description'):
                task.description=request.form.get('description')
            if request.form.get('finished'):
                task.finished=request.form.get('finished')
            db.session.commit()
            return {'success': 'task deleted successfully '}
        except Exception as e:
            print(e)
            return {'error': 'no such task'}
# tasks without parameter
class todoLC(Resource):
    # if the request is post(dont change the function name)
    def post(self):
        mydata={
            'name': request.form.get('name'),
            'description': request.form.get('description'),
            'finished': False
        }
        task = Todo(**mydata)
        print(mydata)
        db.session.add(task)  # add to database but not yet committed
        db.session.commit()  # commit the sql statement to insert into the task table
        return {'success': 'task added successfully '}
    # if the request is get without parameters(dont change the function name)
    def get(self):
        tasks= Todo.query.filter().all()
        newtask=[]
        for task in tasks:
            mytask = {
                'name': task.name,
                'id': task.id,
                'created_at': task.created_at,
                'description': task.description
            }
            newtask.append(mytask)
        return jsonify(newtask)

# for tasks with no parameter routing (call class todoLC)
todoApi.add_resource(todoLC, '/api/v2/todo')
# for tasks with parameter URL routing (call class todoRUD)
todoApi.add_resource(todoRUD, '/api/v2/todo/<int:id>')


db.init_app(app)
# to create the database models (check if created) at the start of running the app
# you can change the database namee from the import
@app.before_first_request
def intiate_dbtablles():
    db.create_all()

# to run the app
app.run()