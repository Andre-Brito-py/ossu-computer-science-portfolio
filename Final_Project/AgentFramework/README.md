# Tool-Use Autonomous Agent Framework

Este é o Projeto Final (Capstone) do meu currículo de Ciência da Computação (OSSU).

## O Problema
IAs tradicionais baseadas em chat atuam apenas de forma passiva, gerando texto. No mundo corporativo, precisamos de **Agentes** capazes de entender fluxos e operar ferramentas do mundo real (Bancos de Dados, ERPs, APIs financeiras) de forma autônoma.

## A Solução
Este repositório contém um framework de IA baseado no paradigma **ReAct (Reasoning + Acting)**.
O agente é capaz de:
1. Receber uma solicitação natural (ex: "Gere um boleto e envie para o email X").
2. Pensar passo-a-passo no que deve ser feito.
3. Chamar as APIs corretas (como o Asaas para geração de boletos ou SMTP para e-mails).
4. **Human-In-The-Loop**: Antes de executar ações destrutivas ou de alto risco financeiro (como gerar a cobrança), o agente interrompe a execução e exige que um supervisor humano digite (y/n) no terminal para autorizar a operação.

## Arquitetura
- `agent.py`: O cérebro. Orquestra as chamadas para a LLM, analisa o output estruturado (JSON) e controla o estado.
- `tools.py`: Onde as integrações de API real (Banco, E-mail) estão implementadas.
- `verification.py`: Módulo interceptador de segurança (Human-In-The-Loop).
- `main.py`: Ponto de entrada do sistema.

## Como rodar localmente
1. Instale as dependências: `pip install -r requirements.txt`
2. Configure as credenciais copiando o `.env.example` para as suas variáveis de ambiente reais.
3. Execute `python main.py` e observe o raciocínio da IA em tempo real!
