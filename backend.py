import mysql.connector                      # lets Python talk to MySQL
import hashlib                              # used to scramble (hash) passwords

ADMIN_PASSKEY = "green123"                  # secret code needed to register as Admin (change it)

conn = mysql.connector.connect(host="localhost", user="root", password="your_mysql_password")  # connect to MySQL (change the password)
cur = conn.cursor()                         # the cursor is what runs SQL commands

cur.execute("CREATE DATABASE IF NOT EXISTS greencare")   # make the database if it doesn't exist
cur.execute("USE greencare")                              # start using that database
cur.execute("""CREATE TABLE IF NOT EXISTS users(
                   username VARCHAR(50),
                   user_type VARCHAR(10),
                   password VARCHAR(64),
                   PRIMARY KEY (username, user_type))""")  # make the users table; the same username can't repeat for one user type

def hash_password(password):                              # turns a password into scrambled text
    return hashlib.sha256(password.encode()).hexdigest()  # same password always gives the same 64-character result

def create_user(username, password, passkey, user_type): # called by the register button
    if user_type == "Admin" and passkey != ADMIN_PASSKEY: # Admins must know the pass keypython -m pip install mysql-connector-python
        return False, "Wrong pass key"                    # tell the GUI it failed and why
    try:                                                  # try to save the account
        cur.execute("INSERT INTO users VALUES (%s,%s,%s)",
                    (username.strip(), user_type, hash_password(password)))  # add a row with the hashed password
        conn.commit()                                     # make the change permanent
        return True, "Account created successfully!"      # tell the GUI it worked
    except mysql.connector.IntegrityError:                # happens if the username already exists
        return False, "Username already exists"          # tell the GUI why it failed

def check_login(username, password, user_type):           # called by the login button
    cur.execute("SELECT password FROM users WHERE username=%s AND user_type=%s",
                (username.strip(), user_type))            # look up the saved hash for this user
    row = cur.fetchone()                                  # get the matching row, or None if no such user
    return row is not None and row[0] == hash_password(password)  # True only if the user exists and the hashes match