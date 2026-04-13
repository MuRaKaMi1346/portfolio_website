from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from project_data import PROJECT_DETAILS
from database import get_db_connection, init_db

app = FastAPI()

# ─── Session Middleware (change secret_key to something strong in production) ─
app.add_middleware(SessionMiddleware, secret_key="change-this-secret-key")

origins = [
    "https://MuRaKaMi1346.github.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

init_db()

# ─── Credentials ─────────────────────────────────────────────────────────────
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

# ─── Routes ──────────────────────────────────────────────────────────────────

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/resume")
async def resume(request: Request):
    return templates.TemplateResponse(request=request, name="resume.html")

@app.get("/projects")
async def projects(request: Request):
    conn = get_db_connection()
    projects = conn.execute('SELECT * FROM projects').fetchall()
    conn.close()
    return templates.TemplateResponse(request=request, name="projects.html", context={"projects": projects})

@app.get("/projects/{project_id}")
async def project_detail(request: Request, project_id: int):
    detail = PROJECT_DETAILS.get(project_id)
    if not detail:
        return RedirectResponse(url="/projects")
    return templates.TemplateResponse(request=request, name="project_detail.html", context={
        "project_id": project_id,
        "detail": detail
    })

@app.get("/contact")
async def contact_form(request: Request):
    return templates.TemplateResponse(request=request, name="contact.html")

@app.post("/contact")
async def submit_contact(request: Request, name: str = Form(...), message: str = Form(...)):
    conn = get_db_connection()
    conn.execute('INSERT INTO messages (name, message) VALUES (?, ?)', (name, message))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/contact", status_code=303)

# ─── Inbox Login ─────────────────────────────────────────────────────────────

@app.get("/inbox")
async def inbox_login(request: Request):
    if request.session.get("authenticated"):
        return RedirectResponse(url="/messages")
    return templates.TemplateResponse(request=request, name="inbox_login.html", context={"error": None})

@app.post("/inbox")
async def inbox_login_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        request.session["authenticated"] = True
        return RedirectResponse(url="/messages", status_code=303)
    return templates.TemplateResponse(request=request, name="inbox_login.html", context={"error": "Invalid username or password."})

@app.get("/inbox/logout")
async def inbox_logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/inbox")

# ─── Messages (protected) ────────────────────────────────────────────────────

@app.get("/messages")
async def messages(request: Request):
    if not request.session.get("authenticated"):
        return RedirectResponse(url="/inbox")
    conn = get_db_connection()
    msgs = conn.execute('SELECT * FROM messages').fetchall()
    conn.close()
    return templates.TemplateResponse(request=request, name="messages.html", context={"messages": msgs})
