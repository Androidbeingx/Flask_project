# All for user APP
 
**Creator** : Andrea DAWBIO1 

>This md resums the function of the app.
This app is a mix for user entertainig.

>Tools: Python, Flask, Flask-SQLAlchemy, Sqlite3, html, jinja2, css.

## Contents:
-Directories: 
    -database:
        -facts.db
        -factsdb_origin.py
        -tasks.db
    -static:
        -css:
            -facts.css
            -gallery.css
            -main.css
            -quote.css
            -tasks.css
        -images:
            -gallery: 15 images .jpg
            - 4 images .png       
    -templates:
        -facts.html
        -gallery.html
        -index.html
        -quote.html
        -tasks.html
-Files:
    -app.py
    -Models.py
    -this file(All for user.md)


## Main page
> Contains an input to add a string by the user. Returns a greeting.
>Have a left nav to move to another pages.

## Gallery
>Declare the path of the local images.
>Displays as a gallery in the web with a home button to redirect to the main page.

## Tasks App
>Creates a db in blank
-Allows input(add) of a task(string) giving it a id
-Update the task as completed or not completed
-Delete the task

## Facts DB
>Database of useless facts
-Search by a fact
-Add id, theme, and fact via input
>/api/<route>
-Search by theme in the url
-Search by id or theme or fact in the url
-Shows all the facts json format via url 
>Shows a json result 

## The Quote
>Takes a random quote of a dictionary
>Displays in the web with a home button to redirect the main page.


