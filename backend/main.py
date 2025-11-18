from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from database import db, create_document, get_documents
from schemas import Hunter, Guild, Quest, Shadow, User

app = FastAPI(title="Solo Leveling: Awakened Chronicles API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoginRequest(BaseModel):
    email: str
    password: str


@app.get("/")
async def root():
    return {"message": "Solo Leveling API is running"}


@app.get("/test")
async def test_db():
    status = {
        "backend": "ok",
        "database": "connected" if db is not None else "unavailable",
        "database_url": "configured" if db is not None else "missing",
        "database_name": db.name if db is not None else None,
        "connection_status": "ok" if db is not None else "no db",
        "collections": list(db.list_collection_names()) if db is not None else []
    }
    return status


# Hunters
@app.post("/hunters", response_model=dict)
async def create_hunter(hunter: Hunter):
    hunter_id = create_document("hunter", hunter)
    return {"id": hunter_id}

@app.get("/hunters", response_model=List[dict])
async def list_hunters(rank: Optional[str] = None):
    filt = {"rank": rank} if rank else {}
    return get_documents("hunter", filt)


# Guilds
@app.post("/guilds", response_model=dict)
async def create_guild(guild: Guild):
    guild_id = create_document("guild", guild)
    return {"id": guild_id}

@app.get("/guilds", response_model=List[dict])
async def list_guilds():
    return get_documents("guild")


# Quests
@app.post("/quests", response_model=dict)
async def create_quest(quest: Quest):
    quest_id = create_document("quest", quest)
    return {"id": quest_id}

@app.get("/quests", response_model=List[dict])
async def list_quests():
    return get_documents("quest")


# Shadows
@app.post("/shadows", response_model=dict)
async def create_shadow(shadow: Shadow):
    shadow_id = create_document("shadow", shadow)
    return {"id": shadow_id}

@app.get("/shadows", response_model=List[dict])
async def list_shadows():
    return get_documents("shadow")


# Authentication (demo only; no real hashing here)
@app.post("/login")
async def login(body: LoginRequest):
    users = get_documents("user", {"email": body.email})
    if not users:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # For demo purposes, accept any password
    user = users[0]
    return {
        "email": user.get("email"),
        "display_name": user.get("display_name"),
        "hunter_rank": user.get("hunter_rank", "E"),
        "achievements": user.get("achievements", [])
    }

@app.post("/signup")
async def signup(user: User):
    user_id = create_document("user", user)
    return {"id": user_id}
