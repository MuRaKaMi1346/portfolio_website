# database.py
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('portfolio.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL
        )
    ''')
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM projects")
    if cur.fetchone()[0] == 0:
        projects = [
            ("ML - Wafer defect test project", "Built a complete ML pipeline including preprocessing, feature extraction, and model training"),
            ("AI - Image angle measurement", "Developed an AI-based vision system for object detection using YOLO and OpenCV"),
            ("MLBPM Prediction", "Developed an AI-based system for analyzing audio signals and predicting BPM using machine learning")
        ]
        conn.executemany("INSERT INTO projects (title, description) VALUES (?, ?)", projects)
        conn.commit()
    conn.close()