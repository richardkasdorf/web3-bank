from fastapi import FastAPI
from accounts.routes import account_routers
from dotenv import load_dotenv
from db.database import engine, Base
from blockchain_services.routes.route_circle_listener import router as webhooks_router
from blockchain_services.routes.route_blockchain_transfer import router as blockchain_transfer
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

load_dotenv()

app = FastAPI(
    title="Banco Digital com Stablecoin",
    description="API de banco digital integrada com USDC na Sepolia",
    version="1.0.0"
)

origins = [
    "http://localhost:5173",  # Porta padrão do Vite
    "http://localhost:5174",  # A porta atual que o Vite abriu!
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
]

# CORS Middleware config
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # URL access permission
    allow_credentials=True,         # Cookies/headers auth permission
    allow_methods=["*"],            # Method permission (GET, POST, PUT, DELETE, etc)
    allow_headers=["*"],            # Permit all headers (Authorization Bearer included)
)


# Internal Route - Bank Operation
for router in account_routers:
    app.include_router(router)

# Blockchain Route - Withdraw USDC
app.include_router(blockchain_transfer)

# Blockchain Route - Circle Listener
app.include_router(webhooks_router)


