import psycopg2
import hashlib
from argon2 import PasswordHasher
import base64
from email.message import EmailMessage
import ssl
import smtplib
import os

#Connect to db
conn = psycopg2.connect(
    host="localhost",
    database="Cedars&Codes",  
    user="postgres",
    password="sami67706940",
    port="5432"
)
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

def Login(username: str, password: str) -> bool:
    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    if not result:
        return False
    
    hashed_b64 = result[0]
    hashed_pw = base64.b64decode(hashed_b64.encode("utf-8")).decode("utf-8")
    
    ph = PasswordHasher()
    try:
        ph.verify(hashed_pw, password)
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
               snippet_type: str = "", languages: list = []) -> bool:
    
    cursor.execute("""
        INSERT INTO snippets (user_email, title, code_content, description, input_types, output_types, snippet_type)
        VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING snippet_id
    """, (user_email, title, code_content, description, input_types, output_types, snippet_type))
    
    snippet_id = cursor.fetchone()[0]
    
    for lang_name in languages:
        cursor.execute("SELECT language_id FROM languages WHERE language_name = %s", (lang_name,))
        lang = cursor.fetchone()
        if lang:
            language_id = lang[0]
        else:
            cursor.execute("INSERT INTO languages (language_name) VALUES (%s) RETURNING language_id", (lang_name,))
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

def fetchPython():
    return fetch_snippets_by_language("Python")

def fetchC():
    return fetch_snippets_by_language("C")

def fetchJava():
    return fetch_snippets_by_language("Java")

def fetchRust():
    return fetch_snippets_by_language("Rust")

def fetchCplusplus():
    return fetch_snippets_by_language("C++")
