import sqlite3 
from .modelos import Proyecto, Tarea


DATABASE_NAME = "tareas.db"

def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def crear_tabla():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proyectos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            fecha_inicio TEXT,
            estado TEXT)
        """)
    
    # Crear tabla de tareas
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            fecha_creacion TEXT,
            fecha_limite TEXT,
            prioridad TEXT,
            estado TEXT,
            proyecto_id INTEGER,
            FOREIGN KEY (proyecto_id) REFERENCES proyectos(id)
        )""")
    
    try:
        cursor.execute(""" INSERT INTO proyectos (id, nombre, descripcion, estado) VALUES (0, 'General', 'Proyecto por defecto', 'Activo') """)
    except sqlite3.IntegrityError:
        pass  # El proyecto por defecto ya existe
    
    conn.commit()
    conn.close()

class DBManager:
    def __init__(self):
        crear_tabla()
        
    
    def crear_tarea(self, tarea: Tarea) -> Tarea: # -> significa que retorna un objeto de tipo Tarea
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO tareas (titulo, descripcion, fecha_creacion, fecha_limite, prioridad, estado, proyecto_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (tarea._titulo, tarea._descripcion, tarea._fecha_creacion, tarea._fecha_limite,
            tarea._prioridad, tarea._estado, tarea._proyecto_id))
        
        
        tarea.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return tarea
    
    def obtener_proyectos(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM proyectos")
        filas = cursor.fetchall()
        
        proyectos = []
        for fila in filas:
            proyecto = Proyecto(
                id=fila['id'],
                nombre=fila['nombre'],
                descripcion=fila['descripcion'],
                fecha_inicio=fila['fecha_inicio'],
                estado=fila['estado']
            )
            proyectos.append(proyecto)
        
        conn.close()
        return proyectos
    
    def obtener_tareas(self, estado= None):
        conn = get_connection()
        cursor = conn.cursor()
        
        sql = "SELECT * FROM tareas"
        params = [];
        
        if estado:
            sql += " WHERE estado = ?"
            params.append(estado)
        
        sql += " ORDER BY fecha_limite ASC"
        
        cursor.execute(sql, params)
        filas = cursor.fetchall()
        conn.close()
    
        tareas = []
        for fila in filas:
            tarea = Tarea(
                id=fila['id'],
                titulo=fila['titulo'],
                descripcion=fila['descripcion'],
                fecja_creacion=fila['fecha_creacion'],
                fecha_limite=fila['fecha_limite'],
                prioridad=fila['prioridad'],
                estado=fila['estado'],
                proyecto_id=fila['proyecto_id']
            )
            tareas.append(tarea)
        return tareas
    
# Creando la base de datos y las tablas al importar el módulo
if __name__ == "__main__":
    crear_tabla()
    print(f"Base de datos '{DATABASE_NAME}' creada o verificada correctamente.")
