  
import os
from flask import Flask, render_template,request, redirect, url_for, session
from supabase import create_client, Client
# from supabase.query_builder import eq
from dotenv import load_dotenv


app = Flask(__name__)
app = Flask(__name__, static_folder="./static")


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
        projects = supabase.table("Projects").select("*").execute().data
        employees = supabase.table("Employees").select("*").execute().data
        
        # If logged in, render the home page with user's username
        return render_template('index.html', username=session['username'], projects=projects,employees=employees)
    else:
        # If not logged in, redirect to the login page
        return redirect(url_for('login'))
    
@app.route('/project/<int:idProject>')
def project(idProject):
    # Fetch the project from your database
   result1 = supabase.table('Projects').select('*').eq('idProject', idProject).execute()
   project = result1.data[0] if result1.data else None
# Fetch all projects from your database
   result2 = supabase.table('Projects').select('*').execute()
   projects = result2.data if result2.data else []
   employees = supabase.table("Employees").select("*").execute().data

 # Render the 'project-page.html' template with the project and projects data
   return render_template('project-page.html', username=session['username'],project=project, projects=projects,employees=employees)

@app.route('/add')
def add():
    return render_template('add_project.html')

@app.route('/upload_cv')
def upload_cv():
    # Render the upload CV page
    return render_template('upload_cv.html')

@app.route('/employee')
def employee():
    # Fetch all employees from your database
    result = supabase.table('Employees').select('*').eq('idEmployee').execute()
    employees = result.data if result.data else []
    # Render the 'user_profile/user_profile.html' template with the employees data
    return render_template('user_profile/user_profile.html', employees=employees)

@app.route('/about')
def about():
    # Render the 'pages-about.html' template
    return render_template('user_profile/about.html')
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
    























# Run the application
if __name__ == "__main__":
    app.run(debug=True)