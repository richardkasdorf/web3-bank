from fastapi import FastAPI, Depends
from accounts.routes import account_routers
from blockchain_services.routes.route_blockchain_transfer import router as external_transfer
from dotenv import load_dotenv
from db.database import engine, Base

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
app.include_router(external_transfer, prefix="/external_transfer")




