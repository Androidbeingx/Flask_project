"""
    THE MEGA UI INTERFACE:
    There are diferent webs in a unic index
    Theme: just entertaiment
    UF5 BLOCK: INDEX, GALLERY, THE QUOTE
    With flask requests, response, random imports
    UF6 BLOCK: TASKS, FACTS
    two diferent data base with diferent display
    EVERY page has a HOME button to return to the main index.html

"""

#----------------------------------------------------------------------------------------------
#ALL IMPORTS
#----------------------------------------------------------------------------------------------

from flask import Flask, render_template,request, flash,redirect,url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from logging import exception
from Models import Facts
import random
import os

#----------------------------------------------------------------------------------------------
#CONFIG. OF THE APP
#----------------------------------------------------------------------------------------------
module_name: str   = __name__
app:         Flask = Flask(module_name, static_url_path='/static')
app.secret_key = "something_weird404"

#Config. of the databases
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database/tasks.db'
app.config['SQLALCHEMY_BINDS'] = {
     'facts':        'sqlite:///database/facts.db'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#----------------------------------------------------------------------------------------------
#HOME PAGE, MAIN ROUTE
#Menu display, and gretting functions for the user
#----------------------------------------------------------------------------------------------
@app.route("/")
def index():
    """Renders a template with a form"""

    flash("What is your name?" )
    return render_template("index.html")

@app.route("/greet", methods=["POST", "GET"])
def greet():
    """Takes the string of the input and send a response with it"""

    flash("Hi " + str(request.form['name_input']) + ", great to see you!")
    return render_template("index.html")

#----------------------------------------------------------------------------------------------
#GALLERY PAGE
#Displays a gallery of photos.
#----------------------------------------------------------------------------------------------
@app.route("/image")
def gallery():

    """
    With a local path like reference, it displays a gallery of images.
    """   

    title_page = os.path.join('static', 'images', 'gallery')

    app.config["UPLOAD_FOLDER"] = title_page

    images_list = os.listdir('static/images/gallery')

    image_list = ['images/gallery/' + image for image in images_list]


    return render_template("gallery.html", image_gallery=image_list)
    

#----------------------------------------------------------------------------------------------
#TO DO APP            ***WARNING*** Class does not allow to be imported in the Models module***
#App tha save your tasks like an agenda
#----------------------------------------------------------------------------------------------
class Todo(db.Model): #type:ignore
     id:       int   = db.Column(db.Integer, primary_key=True)
     title:    str   = db.Column(db.String(100))
     complete: str   = db.Column(db.Boolean)
#----------------------------------------------------------------------------------------------
#Main route of tasks app
#----------------------------------------------------------------------------------------------
@app.route('/tasks')
def main_tasks():
    """Request to de db to show all the rows in it, rendered in a html"""

    #show all the tasks
    todo_list: list[str] = Todo.query.all()
    return render_template('tasks.html', todo_list=todo_list)

#----------------------------------------------------------------------------------------------
#CRUD Functions to the tasks.db with diferent routes. ADD, UPDATE, DELETE
#----------------------------------------------------------------------------------------------
@app.route("/tasks/add", methods=["POST"])
def add():
    """Adds a new task or string via input and redirects to the main route"""

    #add new item to the db
    title_task:   str  = request.form.get("title")
    new_todo:     Todo = Todo(title=title_task, complete=False)
    db.session.add(new_todo)
    db.session.commit()

    return redirect(url_for("main_tasks"))

@app.route("/tasks/update/<int:todo_id>")
def update(todo_id):
    """
    Updates the status of a row in the db, identified by the id, returns to the main route.
    """

    #update status 
    todo:   list[str] = Todo.query.filter_by(id=todo_id).first()
    todo.complete     = not todo.complete
    db.session.commit()
    
    return redirect(url_for("main_tasks")) 

@app.route("/tasks/delete/<int:todo_id>")
def delete(todo_id):
    """Deletes a row in the db,matching id's, returns to the main route"""

    #delete row
    todo:     list[str] = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    
    return redirect(url_for("main_tasks")) 


#----------------------------------------------------------------------------------------------
#FACTS DB
#A database of interesting but useless facts about the world and history.
#Two blocks, one gets data via url and the second block with forms and inputs
#----------------------------------------------------------------------------------------------
#Main route of facts db
#----------------------------------------------------------------------------------------------
@app.route("/facts")
def facts_main():
    """Request to de db to show all the rows in it, rendered in a html"""

    facts:  list[str]       = Facts.query.all()
    facts:  list[list[str]] = [fact.serialize() for fact in facts]

    return render_template("facts.html", facts=facts)

#----------------------------------------------------------------------------------------------
#Block of getting data via url
#----------------------------------------------------------------------------------------------
@app.route("/facts/api/facts", methods=["GET"])
def getFacts():
    """Request of all the objects in the db, returns a json format data"""

    try:
        facts:    list[str]       = Facts.query.all()
        toReturn: list[list[str]] = [fact.serialize() for fact in facts]

        return jsonify(toReturn), 200

    except Exception:
        exception("[SERVER]: Error")
        return jsonify({"msg": "An error ocurred"}), 500

@app.route("/facts/api/fact", methods=["GET"])
def getFactByTheme():
    """
    Request via url theme of a row, 
    returns the first response in json format data if exists
    DISPLAY EXAMPLE: url?theme=<value>
    """

    try:
        theme_name:      str       = request.args["theme"]
        fact:       list[str]      = Facts.query.filter_by(theme=theme_name).first()
        if not fact:
            return jsonify({"msg": "This theme does not exist"}), 200
        else:
            return jsonify(fact.serialize()), 200    

    except Exception:
        exception("[SERVER]: Error")
        return jsonify({"msg": "An error ocurred"}), 500

@app.route("/facts/api/findfact", methods=["GET"])
def getFact():
    """
    Request via url theme or/and id or/and fact of a row, 
    returns the first response in json format data if exists.
    DISPLAY EXAMPLE: url?theme=<value>&id=<value>
    """
    try:
        fields: dict = {}
        if "id" in request.args:
            fields["id"]= request.args["id"]

        if "theme" in request.args:
            fields["theme"]= request.args["theme"]

        if "fact" in request.args:
            fields["fact"]= request.args["fact"]    

       
        fact: list[str] = Facts.query.filter_by(**fields).first()

        if not fact:
            return jsonify({"msg": "This fact does not exist in the database"}), 200
        else:
            return jsonify(fact.serialize()), 200    

    except Exception:
        exception("[SERVER]: Error")
        return jsonify({"msg": "An error ocurred"}), 500

#----------------------------------------------------------------------------------------------
#Block of retriving data and adding via inputs, forms
#----------------------------------------------------------------------------------------------
@app.route("/facts/api/addfact", methods=["POST"])
def addfact():
    """
    With the template facts.html, the user add a new object(id, theme, fact) to the db.
    Will be returned a json format data with the values inserted.
    """

    try:
        id:     int  = request.form["id"]
        theme:  str  = request.form["theme"]
        fact:   str  = request.form["fact"]

        fact:  Facts = Facts(id, theme, fact)
        db.session.add(fact)
        db.session.commit()

        return jsonify(fact.serialize()),200
        
    except Exception:
        exception("\n[SERVER]: Error in toute /api/addfact. Log: \n")
        return jsonify({"msg": "An error ocurred"}), 500    

       
@app.route("/facts/api/searchfact", methods=["POST"])
def serchFactForm():
    """
    With the facts.html, the user could search a fact by theme.
    The first one that matches will be returnes as json data.
    """

    try:
        theme_name: str  = request.form["theme"]
        fact:       list = Facts.query.filter(Facts.theme.like(f"%{theme_name}%")).first()
        
        if not fact:
            return jsonify({"msg": "This theme does not exist"}), 200
        else:
            return jsonify(fact.serialize()), 200    

    except Exception:
        exception("[SERVER]: Error in route facts/api/searchfact")
        return jsonify({"msg": "An error ocurred"}), 500   

#----------------------------------------------------------------------------------------------
#THE QUOTE APP
#Shows a random quote on every display
#----------------------------------------------------------------------------------------------
@app.route("/quotes")
def main_quote():
    """Random choose of a dictionary with a quote to be displayed in quote.html"""

    db: list[dict] = [
        {'character': 'Mother Teresa',
         'quote':     'Spread love everywhere you go. Let no one ever come to you without leaving happier.' },

        {'character': 'Benjamin Franklin',
         'quote':     'Tell me and I forget. Teach me and I remember. Involve me and I learn. ' },

        {'character': 'James Cameron',
         'quote':     'If you set your goals ridiculously high and it is a failure, you will fail above everyone else is success.' },

        {'character': 'D.H.Lawrence',
         'quote':     'Life is ours to be spent, not to be saved.' },

        {'character': 'Theodore Roosvelt',
         'quote':     'Believe you can and you are halfway there.' },

        {'character': 'Anne Frank',
         'quote':     'How wonderful it is that nobody need wait a single moment before starting to improve the world.' },

        {'character': 'Nelson Mandela',
         'quote':     'The greatest glory in living lies not in never falling, but in rising every time we fall.' },

        {'character': 'Ralph Waldo Emerson',
         'quote':     'Do not go where the path may lead, go instead where there is no path and leave a trail.' },

        {'character': 'Margaret Mead',
         'quote':     'Always remember that you are absolutely unique. Just like everyone else.' },

        {'character': 'Helen Keller',
         'quote':     'Life is either a daring adventure or nothing at all.' }            
  
    ]

    choice: dict = random.choice(db)
    
    return render_template('quote.html', **choice)


#----------------------------------------------------------------------------------------------
#MAIN
#----------------------------------------------------------------------------------------------
if __name__ == '__main__':

    #Create the task database
    db.create_all()

    app.run(debug=True)    