from agent import AutonomousAgent

def main():
    print("==============================================")
    print("🚀 Tool-Use Autonomous Agent Framework 🚀")
    print("==============================================")
    
    try:
        agent = AutonomousAgent()
        
        # Simulating a complex request from a company stakeholder
        prompt = """
        Leia a seguinte solicitação:
        'O cliente de CPF cus_00000503 comprou um pacote de serviços de R$ 1500.50. 
        Por favor, emita o boleto com vencimento para 2026-10-01 e depois envie 
        um email para financeiro@empresa.com avisando que a fatura foi gerada e enviando o link do boleto.'
        
        Realize essas tarefas.
        """
        
        print("\n[User Request]:")
        print(prompt.strip())
        
        final_answer = agent.run(prompt)
        
        print("\n==============================================")
        print("🎯 [FINAL ANSWER] 🎯")
        print(final_answer)
        print("==============================================")
        
    except ValueError as e:
        print(f"\n[Setup Error] {e}")
        print("Please check the .env.example file and set your environment variables.")

if __name__ == "__main__":
    main()
