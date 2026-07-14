# Base de Conhecimento

## Dados Utilizados

Descreva se usou os arquivos da pasta `data`, por exemplo:

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `history_chat.csv` | CSV | Contextualizar interações anteriores |
| `risk_profile.json` | JSON | Personalizar recomendações avaliando o perfil |
| `invest_options.json` | JSON | Sugerir produtos adequados ao perfil |
| `transactions.csv` | CSV | Analisar padrão de gastos do cliente |

> [!TIP]
> **Quer um dataset mais robusto?** Você pode utilizar datasets públicos do [Hugging Face](https://huggingface.co/datasets) relacionados a finanças, desde que sejam adequados ao contexto do desafio.

---

## Adaptações nos Dados

Inicialmente será oferecido uma remuneração baseado na taxa de juros dos Estados Unidos, apenas por manter em conta uma quantia mínima de 1.00 USDC. Necessário aceitar os termos e condições para que comece a render.

---

## Estratégia de Integração

### Como os dados são carregados?

```python
services.py
```

### Como os dados são usados no prompt?

```test
PERFIL DE RISCO:
Será submetido a um quiz, e o resultado vai direcionar para um perfil conservador, moderado ou arrojado.

HISTÓRICO DE CHAT:
Aprimorar a experiência do usuário, com preferências e analises de dados já salvas. Respostas mais rápidas e precisas, sem necessidade de se explicar uma situação por mais de uma vez.

TRANSAÇÕES DO CLIENTE:
Será analizado os gastos, usados para análize de crétido, prevenção a fraudes, ofertas direcionadas. Oferecer suporte e dicas pelo chat também.

OPÇÕES DE INVESTIMENTO:
Oferecer e explicar opções de investimento, recomendando primeiramente as opções compatíveis com o perfil de risco.

```

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```
Dados do Cliente:
- Nome: João Silva
- Perfil: Moderado
- Saldo disponível: R$ 5.000

Últimas transações:
- 01/11: Supermercado - R$ 450
- 03/11: Streaming - R$ 55
...
```