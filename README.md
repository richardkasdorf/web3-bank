# Web3-Integrated Bank System API
A modular digital banking core system featuring internal instant transfers and **Stablecoin (USDC)** withdrawals on the Ethereum Sepolia Testnet.

## Project Structure
The project follows a domain-driven modular architecture for scalability and clean code:

```text
📁 project-root/                      
├── 📁 accounts/                       
│   ├── 📁 routes/                     
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
├── 📁 blockchain_services/                             
│   ├── 📁 routes/
│   │   ├── __init__.py
│   │   └── route_withdraw.py
│   └── 📁 services/
│   │   ├── __init__.py
│   │   └── blockchain.py
├── 📁 chatbot/                             
│   ├── __init__.py
│   ├── models.py                     
│   ├── route_chatbot.py
│   └── services.py
├── 📁 db/                             
│   ├── __init__.py
│   ├── crud.py                     
│   └── database.py
├── app.py  
├── docker-compose.yml
├── Dockerfile                         
└── test_blockchain.py
```

## Roadmap & Future Features
This project is under active development. Below is the roadmap for upcoming features:

## Tech Stack
* **FastAPI:** High-performance web framework.
* **SQLAlchemy:** Object-Relational Mapping (ORM).
* **Web3.py:** Ethereum blockchain interaction.
* **SQLite:** Local database for development (test only).
* **Pydantic:** Data validation and settings management.
* **NeonDB:** Srverless open-source PostgreSQL database.

## Installation & Setup
* Clone the repository: ...
* Install dependencies: pip install -r requirements.txt
* Environment Variables (.env): Create a .env file in the root directory:
```env
DATABASE_URL=postgresql://user:password@db:5432/bank_db
CIRCLE_API_KEY=your_circle_key
OPENAI_API_KEY=your_openai_key
```

### 2. Start the Project
Run the following command to start the database and the API:

```bash
docker-compose up --build
```

### 3. Access the API
Open your browser and go to:
* **API Docs**: `http://localhost:8000/docs` (Swagger UI)

## Security & Core
* Security & Password Hashing: Implement BCrypt/Argon2.
* Audit & Log System: Detailed transaction and event logging.
* Custom Exceptions: Centralized API error handling.
* Unit Testing: Full coverage for routes and CRUD logic.













