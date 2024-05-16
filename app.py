from flask import Flask, render_template, request, redirect, url_for, session
from supabase import create_client, Client
from werkzeug.security import generate_password_hash, check_password_hash

# Supabase URL and Key (replace with environment variables in production)
url = 'https://dqkquwhmpmmswxcyrqem.supabase.co'
key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRxa3F1d2htcG1tc3d4Y3lycWVtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTQ3NDI3MzYsImV4cCI6MjAzMDMxODczNn0.laxhsxnF-Sbsh_FhulaODDPgFeUxKWKfWPUO20RG_tE'
supabase: Client = create_client(url, key)
app = Flask(__name__, static_folder="./static")
app.secret_key = 'c912f6b46e8d6e351efdb8b8a4f3ed14'  # Secret key for secure sessions


# Home page route
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

@app.route('/add_project')
def add_project():
    # Render the add project page
    return render_template('add_project.html')

@app.route('/upload_cv')
def upload_cv():
    # Render the upload CV page
    return render_template('upload_cv.html')
@app.route('/contact')
def contact():
    if 'username' in session:
        projects = supabase.table("Projects").select("*").execute().data
        employees = supabase.table("Employees").select("*").execute().data
        return render_template('pages-contact.html',projects=projects, employees=employees)
    else:
        # If not logged in, redirect to the login page
        return redirect(url_for('login'))
# Run the application
if __name__ == "__main__":
    app.run(debug=True)