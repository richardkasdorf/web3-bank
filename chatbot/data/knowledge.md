# Knowledge Base

## Data Used

Describe if you used the files from the `data` folder, for example:

| File | Format | Use in the Agent |
|---------|---------|---------------------|
| `history_chat.csv` | CSV | Contextualize previous interactions |
| `risk_profile.json` | JSON | Personalize recommendations by assessing the profile |
| `invest_options.json` | JSON | Suggest products suited to the profile |
| `transactions.csv` | CSV | Analyze the customer's spending patterns |

> [!TIP]
> **Want a more robust dataset?** You can use public datasets from [Hugging Face](https://huggingface.co) related to finance, as long as they are suitable for the challenge context.

---

## Data Adaptations

Initially, a yield based on the United States interest rate will be offered, simply for maintaining a minimum amount of 1.00 USDC in the account. It is required to accept the terms and conditions for it to start generating yields.

---

## Integration Strategy

### How is the data loaded?

```python
services.py
```

### How is the data used in the prompt?

```test
RISK PROFILE:
Will be submitted to a quiz, and the result will direct to a conservative, moderate, or aggressive profile.

CHAT HISTORY:
Improve the user experience with preferences and data analysis already saved. Faster and more accurate answers, without the need to explain a situation more than once.

CUSTOMER TRANSACTIONS:
Spending will be analyzed, used for credit analysis, fraud prevention, and targeted offers. Also offer support and tips through the chat.

INVESTMENT OPTIONS:
Offer and explain investment options, primarily recommending options compatible with the risk profile.

```

---

## Example of Assembled Context

```
NeonDB... In Progress
```
