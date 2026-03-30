from blockchain_services.services.blockchain import w3, get_usdc_balance, BANK_ADDRESS

def test_connection():
    print("-" * 30)
    # 1. Testar conexão básica com o Provider (Infura/Alchemy)
    if w3.is_connected():
        print(f"✅ Conectado à rede Sepolia!")
    else:
        print("❌ Falha na conexão. Verifique seu SEPOLIA_RPC no .env")
        return

    # 2. Verificar se o Banco tem ETH para pagar o Gas
    balance_wei = w3.eth.get_balance(BANK_ADDRESS)
    balance_eth = w3.from_wei(balance_wei, 'ether')
    print(f"💰 Saldo de ETH do Banco: {balance_eth} ETH")

    # 3. Testar leitura do contrato USDC
    try:
        bank_usdc = get_usdc_balance(BANK_ADDRESS)
        print(f"💵 Saldo de USDC do Banco: {bank_usdc} USDC")
        print("✅ Leitura do contrato funcionando!")
    except Exception as e:
        print(f"❌ Erro ao ler contrato: {e}")
    
    print("-" * 30)

if __name__ == "__main__":
    test_connection()
