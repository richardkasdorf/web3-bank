from fastapi import FastAPI
from accounts.routes import account_routers
from blockchain_services.routes.route_withdraw import router as withdraw_router
from dotenv import load_dotenv

# python -m uvicorn app:app --reload START !!!!!!!!!!!!!

load_dotenv()

app = FastAPI(
    title="Banco Digital com Stablecoin",
    description="API de banco digital integrada com USDC na Sepolia",
    version="1.0.0"
)

for router in account_routers:
    app.include_router(router)


# Blockchain Route - Withdraw USDC
app.include_router(withdraw_router, prefix="/api")





