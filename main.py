from fastapi import FastAPI, File, UploadFile, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import csv
import io
from typing import Dict, Any
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "SecureUpload API Ready"}

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    x_upload_token_3056: str = Header(None)
):
    # Authentication
    if x_upload_token_3056 != "o16hrb3objnq5ic8":
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # File type validation
    allowed_types = {".csv", ".json", ".txt"}
    if not file.filename or "." not in file.filename:
        raise HTTPException(status_code=400, detail="Invalid filename")
    
    file_ext = "." + file.filename.split(".")[-1].lower()
    if file_ext not in allowed_types:
        raise HTTPException(status_code=400, detail="Only .csv, .json, .txt allowed")
    
    # File size (91KB)
    content = await file.read()
    if len(content) > 93081:
        raise HTTPException(status_code=413, detail="File too large (max 91KB)")
    
    # CSV Processing
    if file_ext == ".csv":
        try:
            csv_data = io.StringIO(content.decode("utf-8"))
            reader = csv.DictReader(csv_data)
            rows = list(reader)
            
            total_value = 0
            category_counts = {}
            
            for row in rows:
                if 'value' in row and row['value']:
                    total_value += float(row['value'] or 0)
                if 'category' in row:
                    category_counts[row['category']] = category_counts.get(row['category'], 0) + 1
            
            return {
                "email": "22f2000984@ds.study.iitm.ac.in",
                "filename": file.filename,
                "rows": len(rows),
                "columns": reader.fieldnames,
                "totalValue": round(total_value, 1),
                "categoryCounts": category_counts
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid CSV format")
    
    return {"message": f"File {file.filename} received successfully"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)