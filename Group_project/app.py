import os
from flask import Flask, render_template
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
