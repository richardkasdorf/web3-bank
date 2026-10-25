from fastapi import FastAPI
from accounts.routes import account_routers
from dotenv import load_dotenv
from db.database import engine, Base
from blockchain_services.routes.route_circle_listener import router as webhooks_router
from blockchain_services.routes.route_blockchain_transfer import router as blockchain_transfer
from chatbot.route_chatbot import router as chatbot_router
from fastapi.middleware.cors import CORSMiddleware
from blockchain_services.routes.route_transaction_status import router as transaction_status_router
import os

Base.metadata.create_all(bind=engine)

load_dotenv()

app = FastAPI(
    title="Web3 BANK",
    description="Digital Banking API Integrated with USDC in Sepolia",
    version="1.0.0"
)

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
]

# CORS Middleware config
FRONTEND_ORIGINS = [
    o.strip()
    for o in os.getenv(
        "FRONTEND_ORIGINS",
        "https://web3-bank-frontend-steel.vercel.app",
    ).split(",")
    if o.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,          # URL access permission -> substituir qnd for teste local **allow_origins=origins**
    allow_credentials=True,         # Cookies/headers auth permission
    allow_methods=["GET", "POST", "OPTIONS"],            # Method permission (GET, POST, PUT, DELETE, etc)
    allow_headers=["Content-Type", "Authorization"],            # Permit all headers (Authorization Bearer included)
    expose_headers=["*"],
)

# Internal Route - Bank Operation
for router in account_routers:
    app.include_router(router)

# Blockchain Route - Withdraw USDC
app.include_router(blockchain_transfer)

# Blockchain Route - Circle Listener
app.include_router(webhooks_router)

# ChatBot
app.include_router(chatbot_router)

# Blockchain Route - Transaction Status Stream
app.include_router(transaction_status_router)


