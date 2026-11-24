import sqlite3
import json
import urllib.request
from typing import Dict, Any


class ServiceDatabase:
    """Gerencia conexões e consultas seguras (somente leitura) em banco SQL."""

    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self._setup_sample_data()

    def _setup_sample_data(self) -> None:
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY,
                cliente TEXT NOT NULL,
                status TEXT NOT NULL,
                previsao_entrega TEXT NOT NULL
            )
        """)
        cursor.executemany(
            "INSERT INTO pedidos (id, cliente, status, previsao_entrega) VALUES (?, ?, ?, ?)",
            [
                (101, "Maria Silva", "Em rota de entrega", "Hoje, 18:30"),
                (102, "João Santos", "Em preparação", "Hoje, 19:15"),
            ],
        )
        self.conn.commit()

    def get_order_status(self, order_id: int) -> Dict[str, Any]:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, cliente, status, previsao_entrega FROM pedidos WHERE id = ?",
            (order_id,),
        )
        row = cursor.fetchone()
        if not row:
            return {"encontrado": False, "mensagem": "Pedido não localizado."}
        return {
            "encontrado": True,
            "pedido_id": row[0],
            "cliente": row[1],
            "status": row[2],
            "previsao_entrega": row[3],
        }


class AIAttendanceAgent:
    """Agente de IA para automação de atendimento e integração via API REST."""

    def __init__(self, api_endpoint: str, api_key: str, db: ServiceDatabase):
        self.api_endpoint = api_endpoint
        self.api_key = api_key
        self.db = db

    def build_structured_prompt(self, user_message: str, order_context: Dict[str, Any]) -> str:
        return (
            "Você é um assistente virtual de atendimento ao cliente. "
            "Responda de forma clara, objetiva e cordial usando apenas os dados abaixo.\n"
            f"Dados do pedido (JSON): {json.dumps(order_context, ensure_ascii=False)}\n"
            f"Pergunta do cliente: {user_message}"
        )

    def handle_customer_query(self, order_id: int, user_message: str) -> Dict[str, Any]:
        order_data = self.db.get_order_status(order_id)
        prompt = self.build_structured_prompt(user_message, order_data)

        # Estrutura pronta para envio via API REST a um provedor LLM
        payload = json.dumps({"prompt": prompt, "temperature": 0.2}).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        request = urllib.request.Request(
            self.api_endpoint, data=payload, headers=headers, method="POST"
        )

        return {
            "status_integracao": "pronto_para_envio_rest",
            "endpoint": request.full_url,
            "contexto_sql": order_data,
            "prompt_gerado": prompt,
        }


if __name__ == "__main__":
    database = ServiceDatabase()
    agent = AIAttendanceAgent(
        api_endpoint="https://api.exemplo-llm.com/v1/chat/completions",
        api_key="SUA_CHAVE_API_AQUI",
        db=database,
    )
    resultado = agent.handle_customer_query(101, "Onde está o meu pedido 101?")
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
