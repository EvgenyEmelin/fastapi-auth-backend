from fastapi import FastAPI, Depends
from app.database.session import engine, Base
from app.api.v1.dependencies import get_current_user
from app.api.v1 import auth, users, admin, roles

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI(
    title="Проект FastAPI с RBAC",
    version="1.0.0",
    description="API для аутентификации, авторизации и управления ролями"
)


app.include_router(admin.router)  # → /admin/roles/, /admin/permissions/
app.include_router(users.router)  # → /api/users/
app.include_router(roles.router)  # → /api/roles/
app.include_router(auth.router)    # → /auth/register, /auth/login

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/me")
async def read_current_user(current_user=Depends(get_current_user)):
    return current_user