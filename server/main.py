from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
import os
from dotenv import load_dotenv
import json
import httpx

# Load environment variables
load_dotenv()

app = FastAPI(title="Google Login API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session middleware
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET", "your-secret-key")
)

# OAuth setup
oauth = OAuth()

oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v2/',
    client_kwargs={'scope': 'openid email profile'},
)

@app.get("/")
async def root():
    return {"message": "Google Login API is running"}

@app.get("/auth/google")
async def google_login(request: Request):
    """Initiate Google OAuth login"""
    redirect_uri = request.url_for('auth_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/auth/google/callback")
async def auth_callback(request: Request):
    """Handle Google OAuth callback"""
    try:
        print("Starting OAuth callback...")
        
        # Get the authorization code from the request
        code = request.query_params.get('code')
        state = request.query_params.get('state')
        
        if not code:
            raise HTTPException(status_code=400, detail="No authorization code received")
        
        print(f"Authorization code received: {code}")
        
        # Exchange code for access token manually
        token_url = 'https://oauth2.googleapis.com/token'
        token_data = {
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': 'http://localhost:8000/auth/google/callback'
        }
        
        async with httpx.AsyncClient() as client:
            # Get access token
            token_resp = await client.post(token_url, data=token_data)
            token_resp.raise_for_status()
            token_info = token_resp.json()
            print(f"Token info: {token_info}")
            
            # Get user info using the access token
            headers = {'Authorization': f'Bearer {token_info["access_token"]}'}
            user_resp = await client.get('https://www.googleapis.com/oauth2/v2/userinfo', headers=headers)
            user_resp.raise_for_status()
            user_info = user_resp.json()
            print(f"User info: {user_info}")
        
        # Check if email domain is allowed
        user_email = user_info.get('email', '')
        if not user_email.endswith('@thexcrm.com'):
            print(f"Access denied for email: {user_email}")
            return RedirectResponse(url="http://localhost:3000/login?error=unauthorized_domain")
        
        # Store user info in session
        request.session['user'] = {
            'id': user_info.get('id'),
            'email': user_info.get('email'),
            'name': user_info.get('name'),
            'picture': user_info.get('picture')
        }
        
        print(f"User {user_email} stored in session, redirecting...")
        # Redirect to frontend
        return RedirectResponse(url="http://localhost:3000/dashboard")
    except Exception as e:
        print(f"OAuth error: {str(e)}")  # Debug logging
        import traceback
        traceback.print_exc()  # Print full stack trace
        raise HTTPException(status_code=400, detail=f"Authentication failed: {str(e)}")

@app.get("/api/user")
async def get_user(request: Request):
    """Get current user information"""
    user = request.session.get('user')
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

@app.post("/api/logout")
async def logout(request: Request):
    """Logout user"""
    request.session.clear()
    return {"message": "Logged out successfully"}

@app.get("/api/auth-status")
async def auth_status(request: Request):
    """Check authentication status"""
    user = request.session.get('user')
    return {"authenticated": user is not None, "user": user}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 