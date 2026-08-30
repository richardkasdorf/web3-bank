# Base de Conhecimento RAG - Banco Digital USDC

Este documento serve como banco de dados vetorial (RAG) para o assistente de IA do banco digital. Ele contém as regras de KYC, fluxos de transação e as dúvidas mais frequentes (FAQ) sobre a operação com a stablecoin USDC.

---

## 1. Diretrizes de KYC (Know Your Customer) e Compliance

### Níveis de Verificação de Conta
* **Nível 1 (Básico):** Limite diário de \$5.000 USDC. Exige nome completo, data de nascimento, e-mail e telefone validado.
* **Nível 2 (Verificado):** Limite diário de \$50.000 USDC. Exige foto do documento de identidade (RG, CNH ou Passaporte) e selfie biométrica.
* **Nível 3 (Pro):** Sem limites operacionais estritos. Exige comprovante de residência atualizado (últimos 90 dias) e comprovação de origem de fundos para aportes volumosos.

### Sinais de Alerta (Red Flags) de Prevenção à Lavagem de Dinheiro (AML)
* **Fracionamento:** Múltiplas transações de valores imediatamente abaixo do limite de monitoramento de \$10.000 USDC.
* **Inconsistência:** Movimentações incompatíveis com a renda declarada pelo perfil do usuário.
* **Contas de Alto Risco:** Tentativas de envio ou recebimento de fundos vinculados a carteiras sancionadas ou mixers de criptomoedas (ex: Tornado Cash).

---

## 2. Fluxo de Transações com USDC

### Depósito (Fiat para USDC)
1. **Solicitação:** O usuário solicita um depósito em moeda fiduciária (ex: via Pix ou transferência bancária).
2. **Conversão:** O banco recebe os fundos e emite a quantidade equivalente em USDC na proporção exata de 1:1.
3. **Crédito:** O saldo em USDC fica disponível na conta digital do usuário em até 10 minutos após a compensação fiduciária.

### Envio de USDC (Cadeia / Blockchain)
1. **Redes Suportadas:** O banco opera nativamente via rede **Ethereum** para garantir escalabilidade.
2. **Validação de Endereço:** A IA ou o app deve validar se o endereço de destino (chave pública de 42 caracteres começando com `0x`) pertence à mesma rede selecionada pelo usuário.
3. **Custódia Interna:** Transferências entre usuários do próprio banco digital são instantâneas e possuem taxa zero (off-chain).

### Saque (USDC para Fiat)
1. **Conversão Reversa:** O usuário vende seus USDC dentro do app.
2. **Liquidação:** O banco queima ou retém os USDC e inicia a transferência fiduciária para a conta bancária de mesma titularidade do usuário.

---

## 3. FAQ (Perguntas Frequentes) do Banco Digital

### Q1: O que é a USDC e qual a sua segurança?
A USD Coin (USDC) é uma stablecoin emparelhada ao dólar americano na proporção de 1:1. Ela é emitida pela Circle e é totalmente auditada, garantindo que cada token em circulação possui um dólar equivalente em reservas de dinheiro ou títulos do Tesouro Americano de curto prazo.

### Q2: Minha transação de USDC está travada. O que fazer?
* **Transferência Interna:** Ocorre instantaneamente. Verifique se o saldo do remetente foi debitado.
* **Transferência Externa (Blockchain):** Solicite o Hash da Transação (TxID). Utilize um explorador de blocos (como PolygonScan ou Arbiscan) para verificar o status do processamento na rede. Se estiver "Pendente", a rede blockchain está congestionada e é necessário aguardar.

### Q3: Posso cancelar uma transferência de USDC já enviada?
**Não.** Uma vez que a transação é confirmada e registrada na blockchain, ela se torna irreversível. Sempre confira o endereço de destino e a rede selecionada antes de confirmar com sua senha.

### Q4: Quais são as taxas aplicadas pelo banco?
* **Abertura e Manutenção de Conta:** Gratuita.
* **Transferências Internas:** Taxa zero.
* **Saques e Depósitos em Fiat:** Taxa fixa de 0.5% sobre o valor convertido.
* **Envio para Carteiras Externas:** Taxa de rede flutuante (gás) repassada integralmente ao usuário.
