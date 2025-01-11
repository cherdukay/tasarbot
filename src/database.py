import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        # Veri dizini yoksa oluştur
        if not os.path.exists('data'):
            os.makedirs('data')
        
        self.db_path = 'data/tasarbot.db'
        self._create_tables()

    def _create_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Projeler tablosunu oluştur
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    created_at TEXT NOT NULL
                )
            ''')
            
            # Analizler tablosunu oluştur
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS analyses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER,
                    analysis_type TEXT NOT NULL,
                    content TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (project_id) REFERENCES projects (id)
                )
            ''')
            
            conn.commit()

    def save_project(self, project):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Projeyi ekle veya güncelle
            cursor.execute('''
                INSERT OR REPLACE INTO projects (name, description, created_at)
                VALUES (?, ?, ?)
            ''', (project.name, project.description, project.created_at))
            
            project_id = cursor.lastrowid
            
            # Analizleri kaydet
            if project.analyses:
                for analysis_type, content in project.analyses.items():
                    cursor.execute('''
                        INSERT OR REPLACE INTO analyses 
                        (project_id, analysis_type, content, created_at)
                        VALUES (?, ?, ?, ?)
                    ''', (project_id, analysis_type, content, datetime.now().isoformat()))
            
            conn.commit()
            return project_id

    def load_project(self, project_id=None, project_name=None):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if project_id:
                cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
            elif project_name:
                cursor.execute('SELECT * FROM projects WHERE name = ?', (project_name,))
            else:
                return None
                
            project_data = cursor.fetchone()
            if not project_data:
                return None
                
            # Analizleri al
            cursor.execute('SELECT analysis_type, content FROM analyses WHERE project_id = ?', 
                         (project_data[0],))
            analyses = {row[0]: row[1] for row in cursor.fetchall()}
            
            return {
                'id': project_data[0],
                'name': project_data[1],
                'description': project_data[2],
                'created_at': project_data[3],
                'analyses': analyses
            }

    def list_projects(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name FROM projects')
            return cursor.fetchall()