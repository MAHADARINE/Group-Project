from supabase import create_client

# Replace with your Supabase project details
url = "https://dqkquwhmpmmswxcyrqem.supabase.co"
anon_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRxa3F1d2htcG1tc3d4Y3lycWVtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTQ3NDI3MzYsImV4cCI6MjAzMDMxODczNn0.laxhsxnF-Sbsh_FhulaODDPgFeUxKWKfWPUO20RG_tE"

supabase = create_client(url, anon_key)
