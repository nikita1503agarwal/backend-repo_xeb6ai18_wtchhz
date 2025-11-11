import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from typing import Any, Dict, List, Optional
from bson import ObjectId

from schemas import ContactMessage, SiteSettings, Project, ProjectUpdate
from database import create_document, get_documents

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Backend!"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.post("/api/contact")
def submit_contact(payload: Dict[str, Any]):
    """Accept contact form submissions and store in MongoDB."""
    try:
        data = ContactMessage(**payload)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())

    try:
        inserted_id = create_document("contactmessage", data)
        return {"status": "ok", "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Admin: Site settings (single doc)
@app.get("/api/admin/settings")
def get_settings():
    try:
        items = get_documents("sitesettings", {}, limit=1)
        if items:
            doc = items[0]
            doc["_id"] = str(doc.get("_id"))
            return doc
        # if not exists, create defaults
        default = SiteSettings().model_dump()
        create_document("sitesettings", default)
        return default
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/admin/settings")
def upsert_settings(payload: Dict[str, Any]):
    from database import db
    try:
        data = SiteSettings(**payload)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())
    try:
        if db is None:
            raise Exception("Database not available")
        col = db["sitesettings"]
        existing = col.find_one({})
        if existing:
            col.update_one({"_id": existing["_id"]}, {"$set": data.model_dump()})
            return {"status": "updated"}
        else:
            _id = create_document("sitesettings", data)
            return {"status": "created", "id": _id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Admin: Projects CRUD
@app.get("/api/admin/projects")
def list_projects(tag: Optional[str] = None):
    try:
        filter_q = {"tag": tag} if tag else {}
        items = get_documents("project", filter_q)
        for it in items:
            it["_id"] = str(it.get("_id"))
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/admin/projects")
def create_project(payload: Dict[str, Any]):
    try:
        data = Project(**payload)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())
    try:
        _id = create_document("project", data)
        return {"status": "created", "id": _id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/admin/projects/{project_id}")
def update_project(project_id: str, payload: Dict[str, Any]):
    from database import db
    try:
        data = ProjectUpdate(**payload)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())
    try:
        if db is None:
            raise Exception("Database not available")
        col = db["project"]
        res = col.update_one({"_id": ObjectId(project_id)}, {"$set": {k: v for k, v in data.model_dump().items() if v is not None}})
        if res.matched_count == 0:
            raise HTTPException(status_code=404, detail="Project not found")
        return {"status": "updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/admin/projects/{project_id}")
def delete_project(project_id: str):
    from database import db
    try:
        if db is None:
            raise Exception("Database not available")
        col = db["project"]
        res = col.delete_one({"_id": ObjectId(project_id)})
        if res.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Project not found")
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        # Try to import database module
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            # Try to list collections to verify connectivity
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]  # Show first 10 collections
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
