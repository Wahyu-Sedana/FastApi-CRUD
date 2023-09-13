from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Konfigurasi koneksi MySQL
db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "database": os.getenv("DB_DATABASE"),
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

class Mahasiswa(BaseModel):
    nama_lengkap: str
    nim: str
    no_telp: str
    alamat: str
    jurusan: str

@app.post("/mahasiswa/", response_model=Mahasiswa)
async def addMahasiswa(
    nama_lengkap: str = Form(...),
    nim: str = Form(...),
    no_telp: str = Form(...),
    alamat: str = Form(...),
    jurusan: str = Form(...),
):
    try:
        query = "INSERT INTO mahasiswa (nama_lengkap, nim, no_telp, alamat, jurusan) VALUES (%s, %s, %s, %s, %s)"
        values = (
            nama_lengkap,
            nim,
            no_telp,
            alamat,
            jurusan,
        )
        cursor.execute(query, values)
        conn.commit()
        return values
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/mahasiswa/", response_model=list[Mahasiswa])
async def getMahasiswa():
    try:
        query = "SELECT nama_lengkap, nim, no_telp, alamat, jurusan FROM mahasiswa"
        cursor.execute(query)
        result = cursor.fetchall()
        items = [{
            "nama_lengkap": row[0],
            "nim": row[1],
            "no_telp": row[2],
            "alamat": row[3],
            "jurusan": row[4],
        } for row in result]
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/mahasiswa/{mahasiswa_id}", response_model=Mahasiswa)
async def getMahasiswaById(mahasiswa_id: int):
    try:
        query = "SELECT * FROM mahasiswa WHERE id = %s"
        cursor.execute(query, (mahasiswa_id,))
        result = cursor.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Mahasiswa not found")
        mahasiswa = Mahasiswa(
            nama_lengkap=result[1],
            nim=result[2],
            no_telp=result[3],
            alamat=result[4],
            jurusan=result[5],
        )
        return mahasiswa
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.put("/mahasiswa/{mahasiswa_id}", response_model=Mahasiswa)
async def updateMahasiswa(
    mahasiswa_id: int,
    nama_lengkap: str = Form(...),
    nim: str = Form(...),
    no_telp: str = Form(...),
    alamat: str = Form(...),
    jurusan: str = Form(...),
):
    try:
        query = "UPDATE mahasiswa SET nama_lengkap = %s, nim = %s, no_telp = %s, alamat = %s, jurusan = %s WHERE id = %s"
        values = (
            nama_lengkap,
            nim,
            no_telp,
            alamat,
            jurusan,
            mahasiswa_id,
        )
        cursor.execute(query, values)
        conn.commit()
        return values
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.delete("/mahasiswa/{mahasiswa_id}", response_model=dict)
async def deleteMahasiswa(mahasiswa_id: int):
    try:
        query = "DELETE FROM mahasiswa WHERE id = %s"
        cursor.execute(query, (mahasiswa_id,))
        conn.commit()
        return {"message": "Mahasiswa deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=os.getenv("DB_HOST"), port=os.getenv("DB_PORT"))
