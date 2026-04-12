from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# ดึงข้อมูลจากไฟล์ที่แยกออกไป
from project_data import PROJECT_DETAILS
from database import get_db_connection, init_db

app = FastAPI()

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
    return RedirectResponse(url="/messages", status_code=303)

@app.get("/messages")
async def messages(request: Request):
    conn = get_db_connection()
    msgs = conn.execute('SELECT * FROM messages').fetchall()
    conn.close()
    return templates.TemplateResponse(request=request, name="messages.html", context={"messages": msgs})