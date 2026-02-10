from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, user, account, transaction, dashboard

app = FastAPI(title="Banking App Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(account.router, prefix="/accounts", tags=["accounts"])
app.include_router(transaction.router, prefix="/transactions", tags=["transactions"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])

@app.get('/')
async def health():
    return {"status": "ok", "service": "Banking App Backend"}

@app.get('/health')
async def health_check():
    return {"status": "healthy"}
