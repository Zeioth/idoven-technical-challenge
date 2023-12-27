from fastapi import FastAPI
from controller.db import db_service
from view.ecgs import router as ecgs_router
from view.users import router as users_router

app = FastAPI()


# ON SERVER START
# =============================================================================


# SETUP DATABASE
# --------------
@app.on_event("startup")
async def startup_event():
    """Connects to the database and creates the initial data."""
    await db_service.connect_db()
    await db_service.create_tables()
    await db_service.create_user("admin", "admin", "admin")
    await db_service.create_user("user", "user", "user")
    await db_service.create_user("user2", "user2", "user")


@app.on_event("shutdown")
async def shutdown_event():
    """Disconnects from the database before the server stops."""
    await db_service.disconnect_db()


# EXPOSE ENDPOINTS
# ----------------
app.include_router(ecgs_router, prefix="", tags=["ecgs"])
app.include_router(users_router, prefix="", tags=["users"])
