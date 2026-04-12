from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# ดึงข้อมูลจากไฟล์ที่แยกออกไป
from project_data import PROJECT_DETAILS
from database import get_db_connection, init_db

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

init_db()

# ─── Routes ──────────────────────────────────────────────────────────────────

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/resume")
async def resume(request: Request):
    return templates.TemplateResponse("resume.html", {"request": request})

@app.get("/projects")
async def projects(request: Request):
    conn = get_db_connection()
    projects = conn.execute('SELECT * FROM projects').fetchall()
    conn.close()
    return templates.TemplateResponse("projects.html", {"request": request, "projects": projects})

@app.get("/projects/{project_id}")
async def project_detail(request: Request, project_id: int):
    detail = PROJECT_DETAILS.get(project_id)
    if not detail:
        return RedirectResponse(url="/projects")
    return templates.TemplateResponse("project_detail.html", {
        "request": request,
        "project_id": project_id,
        "detail": detail
    })

@app.get("/contact")
async def contact_form(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})

@app.post("/contact")
async def submit_contact(request: Request, name: str = Form(...), message: str = Form(...)):
    conn = get_db_connection()
    conn.execute('INSERT INTO messages (name, message) VALUES (?, ?)', (name, message))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/messages", status_code=303)

@app.get("/messages")
async def messages(request: Request):
    conn = get_db_connection()
    msgs = conn.execute('SELECT * FROM messages').fetchall()
    conn.close()
    return templates.TemplateResponse("messages.html", {"request": request, "messages": msgs})