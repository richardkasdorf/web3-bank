from fastapi import FastAPI, Depends
from accounts.routes import account_routers
from blockchain_services.routes.route_withdraw import router as withdraw_router
from dotenv import load_dotenv
from blockchain_services.services.blockchain import get_bank_address

# python -m uvicorn app:app --reload START !!!!!!!!!!!!!

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
app.include_router(withdraw_router, prefix="/api")




