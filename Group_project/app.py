  
import os
from django import db
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
    
@app.route('/project/<idProject>')
def project(idProject):
    # Fetch the project from your database
   result1 = supabase.table('Projects').select('*').eq('idProject', idProject).execute()
   project = result1.data[0] if result1.data else None
# Fetch all projects from your database
   result2 = supabase.table('Projects').select('*').execute()
   projects = result2.data if result2.data else []
   employees = supabase.table("Employees").select("*").execute().data
   agenda = supabase.table("Agenda").select("*").eq('idProject', idProject).execute().data

 # Render the 'project-page.html' template with the project and projects data
   return render_template('project-page.html',agenda=agenda,idProject=idProject, username=session['username'],project=project, projects=projects,employees=employees)



@app.route('/project/<idProject>/add-meeting', methods=['POST'])
def project_post(idProject):
    date = request.form.get('date')
    info = request.form.get('info')
    type = request.form.get('type')

    result = supabase.table('Agenda').insert({
        'idProject': idProject,
        'Date': date,
        'Type': type,
        'Info': info
        }
        ).execute()

    return redirect(url_for('project', idProject=idProject))




@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        ProjectName = request.form.get('ProjectName')
        ProjectDesc = request.form.get('ProjectDesc')
        NumOfEmployees = request.form.get('NumOfEmployees')
        Progress = 0
        features = []  # List to store features

        # Extract feature data from the form
        for i in range(1, 6):  # Assuming a maximum of 5 features
            feature_name = request.form.get(f'F{i}')
            if feature_name:
                features.append({'featureName': feature_name})

        # Insert project data into the Projects table
        project_result = supabase.table('Projects').insert({
            'ProjectName': ProjectName,
            'ProjectDesc': ProjectDesc,
            'NumOfEmployees': NumOfEmployees,
            'Progress': Progress
        }).execute()

        if 'error' in project_result and project_result['error']:
            return render_template('error.html', error='An error occurred while adding the project.')

        project_id = project_result.data[0]['idProject']
        # Insert feature data into the Features table
        for feature in features:
            feature_result = supabase.table('Features').insert({
                'idProject': project_id,
                'featureName': feature['featureName']
            }).execute()

            if 'error' in feature_result and feature_result['error']:
                return render_template('error.html', error='An error occurred while adding features to the project.')

        
    return render_template('add_project.html')


@app.route('/upload_cv')
def upload_cv():
    # Render the upload CV page
    return render_template('upload_cv.html')
@app.route('/employee/<int:idEmployee>')
def employee(idEmployee):
    result = supabase.table('Employees').select('*').eq('idEmployee', idEmployee).execute()
    result19 = supabase.table('EmployeePerProject').select('*').eq('idEmployee', idEmployee).execute()
    result20 = supabase.table('Rating').select('*').eq('idEmployee', idEmployee).execute()
    EmployeePerProject = result19.data[0] if result19.data else None
    Rating = result20.data[0] if result20.data else None
    employee = result.data[0] if result.data else None
    # result2 = supabase.table('Projects').select('*').execute()
    # projects = result2.data if result2.data else []
    if EmployeePerProject:
        idProject = EmployeePerProject['idProject']
        project_result = supabase.table('Projects').select('*').eq('idProject', idProject).execute()
        projects = project_result.data[0] if project_result.data else None
    else:
        projects = None

    return render_template('users_profile.html',projects=projects, employee=employee, EmployeePerProject=EmployeePerProject, Rating=Rating)
# @app.route('/employee/<int:idEmployee>')
# def employee(idEmployee):
#     result = supabase.table('Employees').select('*').eq('idEmployee', idEmployee).execute()
#     result19 = supabase.table('EmployeePerProject').select('*').eq('idEmployee', idEmployee).execute()
#     result20 = supabase.table('Rating').select('*').eq('idEmployee', idEmployee).execute()
#     EmployeePerProject = result19.data[0] if result19.data else None
#     Rating = result20.data[0] if result20.data else None
#     employee = result.data[0] if result.data else None
#     project = supabase.table("EmployeePerProject").options(joinedload("Projects")).filter_by(idProject=idProject)

#     return render_template('users_profile.html', project=project,employee=employee, EmployeePerProject=EmployeePerProject, Rating=Rating)
@app.route('/about')
def about():
    # Render the 'pages-about.html' template
    return render_template('user_profile/about.html')
# Login route, supporting both GET and POST methods
@app.route('/results')
def results():
    projects = supabase.table("Projects").select("*").execute().data
    employees = supabase.table("Employees").select("*").execute().data
      
    return render_template('result_page.html',username=session['username'], projects=projects,employees=employees)


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