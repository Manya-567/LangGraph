# # backend/app/main.py
# from fastapi import FastAPI
# from app.routes import user

# app = FastAPI(title="Payroll Report Agent")

# # Include router
# app.include_router(user.router)



# backend/app/main.py
from fastapi import FastAPI
from app.routes import user

app = FastAPI(title="Real-Time Payroll Report Agent")
app.include_router(user.router)
