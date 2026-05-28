from fastapi import FastAPI
from accounts.routes import account_routers
from dotenv import load_dotenv
from db.database import engine, Base
from blockchain_services.routes.route_circle_listener import router as webhooks_router
from blockchain_services.routes.route_blockchain_transfer import router as blockchain_transfer

Base.metadata.create_all(bind=engine)

load_dotenv()

app = FastAPI(
    title="Banco Digital com Stablecoin",
    description="API de banco digital integrada com USDC na Sepolia",
    version="1.0.0"
)

# Internal Route - Bank Operation
for router in account_routers:
    app.include_router(router)

# Blockchain Route - Withdraw USDC
app.include_router(blockchain_transfer)

# Blockchain Route - Circle Listener
app.include_router(webhooks_router)


