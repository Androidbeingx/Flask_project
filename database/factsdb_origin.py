"""File with the functions to create and add data of the Facts db"""
#-----------------------------------------------------------------------------------------------------------
import sqlite3 as sql
#-----------------------------------------------------------------------------------------------------------
#Local path of the database
DB_PATH = "/home/andreamm/Documents/M03/Python basics vscode/practica_uf5_uf6/database/facts.db"

#-----------------------------------------------------------------------------------------------------------
#CREATE FUNCTION OF THE DATABASE
#-----------------------------------------------------------------------------------------------------------
def createDB():
    """Creates the table facts to the facts db."""

    conn= sql.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE facts(
            id integer,
            theme text,
            fact text
            )"""
    )
    conn.commit()
    conn.close()

#-----------------------------------------------------------------------------------------------------------
#ADD FUNCTION, WITH MANY VALUES AT THE BEGINING
#-----------------------------------------------------------------------------------------------------------

def addValues():
    """Add rows to the facts table"""

    conn= sql.connect(DB_PATH)
    cursor = conn.cursor()

    facts = [
        (1,'Space','...each time you see a full moon you always see the same side?'),
        (2,'Dates','...months that start on a Sunday will always have a Friday the 13th?'),
        (3,'Countries','...Australia was originally called New Holland?'),
        (4,'History','...tennis was originally played with bare hands?'),
        (5,'Nature','...lemons contain more sugar than strawberries?'),
        (6,'Time','...the longest possible eclipse of the sun is 7.31 minutes?'),
        (7,'Movies','...all of the clocks in the movie "Pulp Fiction" are fixed to 4:20?'),
        (8,'First','...the ancient Greeks first grew carrots as a form of medicine and not a food?'),
        (9,'Colour','...blonde beards grow faster than darker beards?'),
        (10,'Nature','...birds need gravity to swallow?'),  
    ]

    cursor.executemany("""INSERT INTO facts VALUES(?,?,?)""", facts)    
    conn.commit()
    conn.close()   

#-----------------------------------------------------------------------------------------------------------
#MAIN
#-----------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    
    createDB()
    addValues()     