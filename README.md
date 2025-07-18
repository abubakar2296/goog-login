# Google Login App

A simple web application with Google OAuth authentication built with React and Node.js.

## Features

- Google OAuth 2.0 authentication
- Modern React frontend with Tailwind CSS
- FastAPI backend with session management
- Protected routes
- User profile display

## Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Google Cloud Console account

## Setup

### 1. Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API
4. Go to "Credentials" and create an OAuth 2.0 Client ID
5. Add authorized redirect URIs:
   - `http://localhost:3000/auth/google/callback` (for development)
   - `http://localhost:8000/auth/google/callback` (for production)
6. Copy your Client ID and Client Secret

### 2. Environment Variables

Create a `.env` file in the server directory:

```env
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
SESSION_SECRET=your_session_secret
PORT=3001
```

Copy the example file:
```bash
cp server/env.example server/.env
```

### 3. Installation

```bash
# Install all dependencies
npm run install-all

# Start development servers
npm run dev
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

## Project Structure

```
├── client/          # React frontend
├── server/          # Express backend
├── package.json     # Root package.json
└── README.md        # This file
```

## Usage

1. Open http://localhost:3000 in your browser
2. Click "Login with Google"
3. Authorize the application
4. View your profile information

## Technologies Used

- **Frontend**: React, Tailwind CSS, React Router
- **Backend**: Python, FastAPI, Authlib
- **Authentication**: Google OAuth 2.0
- **Session Management**: Starlette Sessions 