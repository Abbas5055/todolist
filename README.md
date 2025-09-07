# Todo App (Frontend + Flask Backend)

**What this is**
- A simple, polished Todo List web app with a creative frontend and a Flask backend (SQLite).
- Backend serves the API under `/api/todos` and also serves the frontend.
- Designed to impress: clean UI, smooth interactions, responsive layout, and concise code.

**Run locally (Linux / macOS / Windows with WSL or PowerShell)**
1. Make a Python virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate      # macOS / Linux
   venv\Scripts\activate       # Windows PowerShell
   ```
2. Install dependencies:
   ```
   pip install -r backend/requirements.txt
   ```
3. Initialize database (optional — first run will auto-create DB):
   ```
   python backend/db_init.py
   ```
4. Run the app:
   ```
   python backend/app.py
   ```
5. Open the app in your browser:
   - Frontend + API are served at: `http://localhost:5000/`

**API**
- `GET /api/todos` — list todos
- `POST /api/todos` — create todo (JSON: {"title":"text"})
- `PUT /api/todos/<id>` — update (JSON: {"title":"...", "done": true/false})
- `DELETE /api/todos/<id>` — delete

**Notes**
- No external services needed; only Python and standard packages.
- If you want a public URL, run this locally and use an HTTP tunneling service (e.g., ngrok) to expose `http://localhost:5000`.
