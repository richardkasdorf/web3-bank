import os
from openai import OpenAI

class ChatbotService:

    def __init__(self):
        self.system_instruction = (
            "Você é o assistente virtual inteligente da plataforma fintech Circle. "
            "Seu objetivo é ajudar os usuários de forma clara, educada e concisa sobre "
            "questões financeiras, transações de criptoativos (como USDC) e saldos. "
            "Responda sempre em português do Brasil e mantenha um tom profissional, mas amigável."
        )

    def generate_reply(self, user_message: str) -> str:

        user_lower = user_message.lower()
        
        # Respostas inteligentes baseadas em palavras-chave
        if "saldo" in user_lower or "dinheiro" in user_lower or "usdc" in user_lower:
            return "O seu saldo em USDC é atualizado em tempo real diretamente da blockchain. Você pode visualizá-lo no card azul no topo da página."
        
        if "extrato" in user_lower or "data" in user_lower or "transação" in user_lower:
            return "Você pode filtrar o seu extrato escolhendo as datas 'De' e 'Até' logo acima da tabela de transações. O sistema recarregará os dados automaticamente."
            
        if "sair" in user_lower or "logout" in user_lower:
            return "Para encerrar sua sessão com segurança, basta clicar no botão vermelho 'Sair' no canto superior direito do seu painel."

        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            raise ValueError("OpenAI Key not found in .env.")

        try:
            client = OpenAI(api_key=api_key)
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self.system_instruction},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=250
            )
            return response.choices.message.content
        except Exception as e:
            print(f"[OpenAI SDK Error]: {str(e)}")
            raise e
