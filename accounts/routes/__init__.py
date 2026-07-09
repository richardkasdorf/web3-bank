from .route_list_accounts import router as list_accounts
from .route_add_accounts import router as add_accounts
from .route_update_accounts import router as update_accounts
from .route_update_password import router as update_password
from .route_login_account import router as login_account
from .route_balance_accounts import router as balance_account
from .route_statement_accounts import router as statement_accounts

account_routers = [list_accounts, 
    add_accounts, 
    update_accounts, 
    update_password, 
    login_account, 
    balance_account, 
    statement_accounts
]

