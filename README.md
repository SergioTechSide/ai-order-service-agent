 AI Order Service Agent (`ai-order-service-agent`)

Agente inteligente desenvolvido em **Python** com **Programação Orientada a Objetos (POO)** para automatizar fluxos de atendimento ao cliente, integrando consultas seguras em banco de dados **SQL** com modelos de linguagem via **APIs REST**.

## Problema Resolvido
Em operações de atendimento digital, consultas manuais de status de pedidos geram lentidão e filas de espera. Este projeto estrutura um fluxo automatizado onde:
1. O sistema consulta o banco de dados relacional via **SQL parametrizado** (prevenindo SQL Injection e garantindo integridade dos dados);
2. Os dados retornados são estruturados em **JSON**;
3. Um **prompt contextualizado** é preparado para envio via **API REST** a um modelo de IA generativa, gerando respostas rápidas e precisas ao cliente.

 ## Tecnologias e Conceitos Aplicados
- **Linguagem:** Python 3 (Programação Orientada a Objetos, tipagem estática com `typing`)
- **Banco de Dados:** SQL (`sqlite3` com consultas parametrizadas somente leitura)
- **Integrações:** APIs REST (`urllib.request`, payloads JSON, autenticação via Bearer Token)
- **IA Aplicada:** Engenharia de Prompt estruturada com aterramento em dados reais (*grounding*)
- **Versionamento:** Git e GitHub

 Como Executar Localmente
```bash
git clone https://github.com/SergioTechSide/ai-order-service-agent.git 
cd ai-order-service-agent
python agent_service.py
