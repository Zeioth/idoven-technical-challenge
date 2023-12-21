
from fastapi import FastAPI
from utils.db import connect_db, disconnect_db
from utils.db import create_tables, create_user
from endpoints.ecgs import router as ecgs_router
from endpoints.users import router as users_router

app = FastAPI()


# ON SERVER START
# =============================================================================


# SETUP DATABASE
# --------------
@app.on_event("startup")
async def startup_event():
    """Connects to the database and creates the initial data."""
    await connect_db()
    await create_tables()
    await create_user("admin", "admin", "admin")
    await create_user("user", "user", "user")
    await create_user("user2", "user2", "user")


@app.on_event("shutdown")
async def shutdown_event():
    """Disconnects from the database before the server stops."""
    await disconnect_db()


# EXPOSE ENDPOINTS
# ----------------
app.include_router(ecgs_router, prefix="", tags=["ecgs"])
app.include_router(users_router, prefix="", tags=["users"])
