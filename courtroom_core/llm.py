"""Databricks MLflow deployment client and chat wrapper."""
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

import mlflow.deployments

from courtroom_core.settings import LLM_ENDPOINT

_client = None

def get_client():
    global _client
    if _client is None:
        try:
            _client = mlflow.deployments.get_deploy_client("databricks")
        except Exception as e:
            raise RuntimeError(
                "Databricks authentication failed (MLflow cannot open a deployment client).\n\n"
                "What to do:\n"
                "• Add a `.env` file in the project folder with:\n"
                "  DATABRICKS_HOST=https://<your-workspace>.cloud.databricks.com\n"
                "  DATABRICKS_TOKEN=<personal access token>\n"
                "• Or configure the CLI: `databricks auth login`\n\n"
                "Reference: https://docs.databricks.com/en/dev-tools/auth/index.html#unified-auth\n\n"
                f"Original error: {e}"
            ) from e
    return _client


def ask_llm(prompt: str, system: str = "", language: str = "en") -> str:
    """Call the LLM with an optional system prompt and language support."""
    client = get_client()
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    response = client.predict(
        endpoint=LLM_ENDPOINT,
        inputs={"messages": messages}
    )

    if isinstance(response, dict) and "choices" in response:
        return response["choices"][0]["message"]["content"].strip()
    return str(response).strip()

