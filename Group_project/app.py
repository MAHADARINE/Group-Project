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

# result = supabase.auth.sign_in_with_password({"email":'maha.bazouzi@ensia.edu.dz', "password":'GroupProject#2024'})
# if result.error:
#     print(f"An error occurred: {result.error.message}")
# else:
#     print("Signed in successfully")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/project/<int:idProject>')
@app.route('/project/<int:idProject>')
def project(idProject):
    # Fetch the project from your database
   result1 = supabase.table('Projects').select('*').eq('idProject', idProject).execute()
   project = result1.data[0] if result1.data else None
# Fetch all projects from your database
   result2 = supabase.table('Projects').select('*').execute()
   projects = result2.data if result2.data else []
 # Render the 'project-page.html' template with the project and projects data
   return render_template('project-page.html', project=project, projects=projects)
@app.route('/add')
def add():
    return render_template('add_project.html')
@app.route('/employee')
def employee():
    # Fetch all employees from your database
    result = supabase.table('Employees').select('*').eq('idEmployee').execute()
    employees = result.data if result.data else []
    # Render the 'user_profile/user_profile.html' template with the employees data
    return render_template('user_profile/user_profile.html', employees=employees)
@app.route('/contact')
def contact():
    # Render the 'pages-contact.html' template
    return render_template('pages-contact.html')
@app.route('/about')
def about():
    # Render the 'pages-about.html' template
    return render_template('user_profile/about.html')
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

if __name__ == '__main__':
    app.run(debug=True)
