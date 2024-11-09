
import pandas as pd
import sqlite3
db_path=None
def set_db_path(path):
    global db_path
    db_path=path
    init_db()
    print(db_path)
def init_db():
    app_directory = db_path  # Kivy automatically sets this for Android
    conn = sqlite3.connect(app_directory)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS article (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code INT NOT NULL,
            ref TEXT NOT NULL,
            des TEXT NOT NULL,
            colis REAL NOT NULL
        )
    ''')
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS inventory (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        code INTEGER NOT NULL,
                        ref TEXT NOT NULL,
                        des TEXT NOT NULL,
                        colis REAL NOT NULL,
                        unit REAL NOT NULL,
                        quantity_in_colis REAL NOT NULL,
                        date_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP  -- Default to current date and time
                    )''')
    
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS user (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT NOT NULL,
                        password TEXT NOT NULL
                        )''')
    conn.commit()
    conn.close()

def update_articles(articles_data):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM article')
        
        cursor.executemany('INSERT INTO article (code, ref,des,colis) VALUES (?, ?, ?, ?)', articles_data)
        conn.commit()  # Commit the transaction to save changes
        cursor.close()
        conn.close()   # Close the connection
def update_user(email,password):
       
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS user (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT NOT NULL,
                        password TEXT NOT NULL
                        )''')
        cursor.execute('DELETE FROM user')
        cursor.execute('INSERT INTO user (email, password) VALUES (?, ?)', (email,password))
        conn.commit()  # Commit the transaction to save changes
        cursor.close()
        conn.close() 
def import_excel_to_db(file_path):
    df = pd.read_excel(file_path,skiprows=4)
    df=df.dropna(subset=["Code","Référence 1","Désignation FR","Unité/Colis"])
    articles_data = [(row['Code'],row['Référence 1'],row['Désignation FR'], row['Unité/Colis']) for _, row in df.iterrows()]

    update_articles(articles_data)
def get_user_data():
  try:
    app_directory = db_path  # Assuming `db_path` is the path to the database file
    conn = sqlite3.connect(app_directory)
    cursor = conn.cursor()
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS user(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT NOT NULL,
                        password TEXT NOT NULL
                        )''')
    # Retrieve all rows from the article table
    cursor.execute("SELECT password FROM user")
    rows = cursor.fetchall()
    return str(rows[0][0])
  except:return ""
""" update_user("omar","rai")
print(get_user_data()) """
def get_article_list():
    app_directory = db_path  # Assuming `db_path` is the path to the database file
    conn = sqlite3.connect(app_directory)
    cursor = conn.cursor()
    
    # Retrieve all rows from the article table
    cursor.execute("SELECT code, ref, des, colis FROM article")
    rows = cursor.fetchall()
    
    # Convert rows into the desired list of dictionaries
    client_list = [
        {
            'Code': str(row[0]),            # Convert code to string if needed
            'Référence 1': row[1],
            'Désignation FR': row[2],
            'Unité/Colis': str(int(row[3])) # Convert colis to string for consistency
        }
        for row in rows
    ]
    
    conn.close()
    return client_list

def get_inventory_list():
    
    app_directory = db_path  # Assuming `db_path` is the path to the database file
    conn = sqlite3.connect(app_directory)
    cursor = conn.cursor()
    
    # Retrieve all rows from the article table
    cursor.execute("SELECT code, ref, des, colis,unit,id FROM inventory")
    rows = cursor.fetchall()
    
    # Convert rows into the desired list of dictionaries
    client_list = [
        {
             "Code":str(row[0]),     
            'Référence 1': row[1],
            'Désignation FR': row[2],
            'colis': str(int(row[3])),
            'unit': str(int(row[4])),
            "id":str(int(row[5]))
            
            
                         
                          # Convert colis to string for consistency
        } 
        for row in rows
    ]
    
    conn.close()
    return client_list

def add_article(articles_data):
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.executemany('INSERT INTO inventory (code, ref,des,colis,unit,quantity_in_colis) VALUES (?, ?, ?, ?, ?, ?)', articles_data)
        conn.commit()  # Commit the transaction to save changes
        cursor.close()
        conn.close()   # Close the connection
        
def update_inventory(id, new_colis, new_unit):
    
    """Update the 'colis' and 'unit' fields in the inventory table based on the given id."""
    # Connect to the SQLite database (replace 'your_database.db' with your database name)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Execute the update query
    cursor.execute('''
        UPDATE inventory
        SET colis = ?, unit = ?
        WHERE id = ?
    ''', (new_colis, new_unit, id))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
def delete_inventory_item(id):
    
    
    """Delete a row from the inventory table based on the given id."""
    # Connect to the SQLite database (replace 'your_database.db' with your database name)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Execute the delete query
    cursor.execute('''
        DELETE FROM inventory
        WHERE id = ?
    ''', (id,))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    
    
def clear_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Execute the delete query
    cursor.execute('''
        DELETE FROM inventory
        
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    
def export_inventory_to_excel(file_path='inventory.xlsx'):
    # Connect to the SQLite database
    
    conn = sqlite3.connect(db_path)

    # Query to fetch data from the inventory table
    query = "SELECT * FROM inventory"

    # Use pandas to read the SQL query into a DataFrame
    df = pd.read_sql_query(query, conn)
    # Close the database connection
    conn.close()
    # Export the DataFrame to an Excel fil
    df.to_excel(file_path, index=False, sheet_name='Inventory')
   

