VEA Frontend (React + Tailwind) - Bright Theme

How to run locally:

1. Install Node.js (v16+ recommended) and npm.
2. In this folder run:
   npm install
   npm start

3. The app will open at http://localhost:3000

Environment:
- The frontend expects a backend API base URL in REACT_APP_API_BASE (default http://localhost:8000).
  You can set it in a .env file:
    REACT_APP_API_BASE=http://localhost:8000

Integration with your project:
- Copy this entire folder into your project directory or run it separately.
- The app will try to load local blueprint files at /data/venues/<venue_id>.json served from the same origin.
- For production, host backend separately (Render) and set REACT_APP_API_BASE accordingly.

Notes:
- This project does not include node_modules. Run npm install to fetch dependencies.
