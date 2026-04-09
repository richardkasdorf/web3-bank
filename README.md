# Web3-Integrated Bank System API
A modular digital banking core system featuring internal instant transfers and **Stablecoin (USDC)** withdrawals on the Ethereum Sepolia Testnet.

## Project Structure
The project follows a domain-driven modular architecture for scalability and clean code:

```text
project-root/                      
├── accounts/                       
│   ├── routes/                     
│   │   ├── __init__.py
│   │   ├── route_add_accounts.py
|   |   ├── route_intrabank_transfer.py
│   │   ├── route_list_accounts.py
|   |   ├── route_login_account.py
│   │   ├── route_update_accounts.py
│   │   └── route_update_password.py
│   ├── __init__.py
│   ├── auth_model.py               
│   ├── models.py                   
│   └── schemas.py                  
├── blockchain_services/                             
│   ├── routes/
│   │   ├── __init__.py
│   │   └── route_withdraw.py
│   └── services/
│   │   ├── __init__.py
│   │   └── blockchain.py
├── db/                             
│   ├── __init__.py
│   ├── crud.py                     
│   └── database.py
├── app.py                          
└── test_blockchain.py
```

## Roadmap & Future Features
This project is under active development. Below is the roadmap for upcoming features:

## Tech Stack
* **FastAPI:** High-performance web framework.
* **SQLAlchemy:** Object-Relational Mapping (ORM).
* **Web3.py:** Ethereum blockchain interaction.
* **SQLite:** Local database for development.
* **Pydantic:** Data validation and settings management.

## Installation & Setup
* Clone the repository: ...
* Install dependencies: pip install -r requirements.txt
* Environment Variables (.env): Create a .env file in the root directory:
SEPOLIA_RPC=your_infura_or_alchemy_url
BANK_PRIVATE_KEY=your_64_char_private_key
USDC_CONTRACT=0x1c7D4B196Cb0232b3044B3374241B7454231f855
* Run the API: python -m uvicorn app:app --reload

## Security & Core
* Security & Password Hashing: Implement BCrypt/Argon2.
* Audit & Log System: Detailed transaction and event logging.
* Custom Exceptions: Centralized API error handling.
* Unit Testing: Full coverage for routes and CRUD logic.













