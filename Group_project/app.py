  
import os
from flask import Flask, render_template? request, redirect, url_for, session
from supabase import create_client, Client
# from supabase.query_builder import eq
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash


load_dotenv(".env")  # take environment variables from .env.

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")


supabase: Client = create_client(supabase_url=url, supabase_key=key)
supabase.auth.session = {"access_token": "sbp_e4a465e5d5ab80d88d726d3880b272be35139305"}

app = Flask(__name__, static_folder="./static")
app.secret_key = 'c912f6b46e8d6e351efdb8b8a4f3ed14'  # Secret key for secure sessions



@app.route('/')
def home():
    # Check if 'username' is stored in session
    if 'username' in session:
        # If logged in, render the home page with user's username
        return render_template('index.html', username=session['username'])
    else:
        # If not logged in, redirect to the login page
        return redirect(url_for('login'))

@app.route('/project/<int:project_id>')
def project(idProject):
    result = supabase.table("Projects").select('*').execute()

    print(result.data)
    return render_template('project-page.html', project=result)

@app.route('/employee')
def employee():
    return render_template('user_profile/user_profile.html')

if __name__ == '__main__':
    app.run(debug=True)
# Login route, supporting both GET and POST methods
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve username and password from form data
        username = request.form['username']
        password = request.form['password']
        
        print(f"Debug: Attempting to log in with username={username} and password={password}")
        
        result = supabase.table("admins").select("*").eq("username", username).eq("password", password).execute()
        
        print("Query Result:", result.data)
        # Check if the query was successful and if a user exists
        if result.data and len(result.data) > 0:
            session['username'] = username  # Store the username in session
            return redirect(url_for('home'))  # Redirect to home page after successful login
        else:
            # If login failed, render the login page with an error message
            return render_template('pages-login.html', error='Invalid username or password')
    
    return render_template('pages-login.html')
# Logout route
@app.route('/logout')
def logout():
    # Remove 'username' from session to log the user out
    session.pop('username', None)
    return redirect(url_for('login'))  # Redirect to login page after logout

# Run the application
if __name__ == "__main__":
    app.run(debug=True)
