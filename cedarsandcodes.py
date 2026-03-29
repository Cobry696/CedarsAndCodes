import psycopg2
import hashlib
from argon2 import PasswordHasher
import base64
from email.message import EmailMessage
import ssl
import smtplib
import os
import re

db_up = True # change to true when the database is running

if db_up:
    #Connect to db
    conn = psycopg2.connect( # change to app user
        host="100.66.137.2",
        database="Cedars&Codes",  
        user="colby",
        password="pass1", 
        port="5432"
    )
    # conn = psycopg2.connect(
    #     host="10.30.31.153",
    #     database="Cedars&Codes",
    #     user="app_user",
    #     password="E8S5NB4D27g3",
    #     port="5432"
    # )
    cursor = conn.cursor()
    print("Connected successfully!")

# Email notifciation
def send_email(fnm: str, to_email: str):
    email_sender = "savetheshow67@gmail.com"
    email_password = "zbsejfgcbpvdoebb"
    
    subject = "Welcome to Cedars & Codes"
    body = f"""Dear {fnm},

Welcome! Your Cedars & Codes account has been successfully created!

Best regards,
Cedars & Codes Team
"""
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = to_email
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, to_email, em.as_string())
    except Exception as e:
        print(f"Failed to send email: {e}")


# functions
def CreateUser(username: str, email: str, password: str, first_name: str = "", last_name: str = "") -> bool:
    ph = PasswordHasher()
    hashed_pw = ph.hash(password)
    hashed_b64 = base64.b64encode(hashed_pw.encode("utf-8")).decode("utf-8")
    
    cursor.execute("SELECT 1 FROM users WHERE username = %s OR email = %s", (username, email))
    if cursor.fetchone():
        print("Username or email already exists!")
        return False
    
    cursor.execute("""
        INSERT INTO users (email, username, password, first_name, last_name)
        VALUES (%s, %s, %s, %s, %s)
    """, (email, username, hashed_b64, first_name, last_name))
    conn.commit()
    
    send_email(username, email)
    return True

def DeleteUser(email: str) -> bool:
    cursor.execute("SELECT 1 FROM users WHERE email = %s", (email,))
    if not cursor.fetchone():
        print("User not found!")
        return False
    
    cursor.execute("DELETE FROM users WHERE email = %s", (email,))
    conn.commit()
    return True

def Login(username: str, password: str, pass_missing: bool):

    if not db_up:
        return True, "abc" # this abc is here so the program doesnt get confused when it asks for the missing piece
    
    if re.match(r".+@.+\..+", username): # check if user entered an email instead
        cursor.execute("SELECT password FROM users WHERE email = %s", (username.lower(),))
        result = cursor.fetchone()
        if pass_missing: # might mess stuff up im not sure how psycopg2 works
            cursor.execute("SELECT username FROM users WHERE email = %s", (username.lower(),))
            missing = cursor.fetchone()
    else:
        cursor.execute("SELECT password FROM users WHERE username = %s", (username.lower(),))
        result = cursor.fetchone()
        if pass_missing:
            cursor.execute("SELECT email FROM users WHERE username = %s", (username.lower(),))
            missing = cursor.fetchone()
    if not result:
        return False
    
    hashed_b64 = result[0]
    hashed_pw = base64.b64decode(hashed_b64.encode("utf-8")).decode("utf-8")
    
    ph = PasswordHasher()
    try:
        ph.verify(hashed_pw, password)
        if pass_missing and missing != None:
            return True,missing[0].lower()
        else:
            return True
    except Exception:
        return False
    
def AddLanguage(language_name: str) -> bool:
    cursor.execute("SELECT 1 FROM languages WHERE language_name = %s", (language_name,))
    if cursor.fetchone():
        print("Language already exists!")
        return False
    
    cursor.execute("INSERT INTO languages (language_name) VALUES (%s)", (language_name,))
    conn.commit()
    return True

def AddSnippet(user_email: str, title: str, code_content: str,
               description: str = "", input_types: str = "", output_types: str = "", 
               language: str = "") -> bool:
    
    cursor.execute("""
        INSERT INTO snippets (user_email, title, code_content, description, input_types, output_types)
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING snippet_id
    """, (user_email, title, code_content, description, input_types, output_types))
    
    snippet_id = cursor.fetchone()[0]
    
    cursor.execute("SELECT language_id FROM languages WHERE language_name = %s", (language,))
    lang = cursor.fetchone()
    if lang:
        language_id = lang[0]
    else:
        cursor.execute("INSERT INTO languages (language_name) VALUES (%s) RETURNING language_id", (language,))
        language_id = cursor.fetchone()[0]
    
    cursor.execute("INSERT INTO snippet_languages (snippet_id, language_id) VALUES (%s, %s)", (snippet_id, language_id))
    
    conn.commit()
    return True

# Fetch snippets by language
def fetch_snippets_by_language(language_name: str):
    cursor.execute("""
        SELECT s.snippet_id, s.title, s.code_content, s.description
        FROM snippets s
        JOIN snippet_languages sl ON s.snippet_id = sl.snippet_id
        JOIN languages l ON sl.language_id = l.language_id
        WHERE l.language_name = %s
    """, (language_name,))
    
    return cursor.fetchall()

# Fetch snippets by search as well as filter the snippets with language and stuff
def fetch_snippets(search_term: str = "", search_by: str = "title", language_name: str = "", input_types: list = [], output_types: list = []):
    # We want to check against each of these parameters by
    # seeing if the search term is contained in the title or description depending on searchBy (0)
    # seeing if the language names match (1)
    # checking if the input types are included in the input types of the snippet (2)
    # checking if the output types are included in the output types of the snippet (3)
    # do this by incrementally building a query and list of inputs to the query

    query = """
            SELECT s.snippet_id, s.title, s.code_content, s.description
            FROM snippets s
            JOIN snippet_languages sl ON s.snippet_id = sl.snippet_id
            JOIN languages l ON sl.language_id = l.language_id 
        """

    queryInputs = ()

    # adding the actual search term part (0)
    if search_term != "":
        if search_by == "title":
            query += "WHERE s.title ILIKE %s "
        elif search_by == "description":
            query += "WHERE s.description ILIKE %s "
        queryInputs += (search_term,)

    # (1)
    if language_name != "":
        query += "WHERE l.language_name = %s "
        queryInputs += (language_name,)

    #(2)
    if len(input_types) > 0:
        query += "WHERE s.input_types LIKE %s "
        input_types_string = ",".join(input_types)
        queryInputs += (input_types_string,)

    #(3)
    if len(output_types) > 0:
        query += "WHERE s.output_types LIKE %s "
        output_types_string = ",".join(output_types)
        queryInputs += (output_types_string,)

    print(query)
    print(queryInputs)
    cursor.execute(query, queryInputs)
    return cursor.fetchall()

def get_languages():
    cursor.execute("""
    SELECT language_name FROM languages
    """)
    return cursor.fetchall()