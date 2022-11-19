"""Model of the Facts database"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Facts(db.Model):  #type:ignore
    __bind_key__ = 'facts'  #to identify the database that it use
    id:     int = db.Column(db.Integer, primary_key=True, nullable=False)
    theme:  str = db.Column(db.String(100))
    fact:   str = db.Column(db.String(800))


    def __init__(self, id, theme, fact):
        super().__init__()
        self.id:    int  = id
        self.theme: str  = theme
        self.fact:  str  = fact


    def __str__(self) -> str: #Print the database via terminal
        return "\nId: {}. Theme: {}. Fact: {}.\n".format(
            self.id, self.theme, self.fact
        )

    def serialize(self): #Makes a dictionary of every object in the db
        return {
            "id": self.id,
            "theme": self.theme,
            "fact": self.fact
        }    

