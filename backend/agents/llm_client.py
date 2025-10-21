from typing import List, Dict
from ..utils.config import Config
from ..utils.logger import logger

# NOTE: We keep it pluggable—use Vertex Gemini if configured, else a stub.
# You can swap to langchain-google-vertexai integrations if desired.

class LLMClient:
    def __init__(self):
        self.use_vertex = Config.USE_VERTEX_GEMINI
        self.model_name = Config.GEMINI_MODEL
        if self.use_vertex:
            try:
                from langchain_community.chat_models import ChatVertexAI
                self.client = ChatVertexAI(
                    model_name=self.model_name,
                    location=Config.VERTEX_LOCATION,
                    project=Config.VERTEX_PROJECT_ID,
                    temperature=0.2,
                )
                logger.info(f"LLM: Using VertexAI {self.model_name}")
            except Exception as e:
                logger.exception(e)
                logger.warning("Falling back to local stub LLM.")
                self.use_vertex = False
                self.client = None
        else:
            self.client = None
            logger.info("LLM: Using local stub.")

    def generate(self, system: str, messages: List[Dict[str, str]]) -> str:
        """
        messages: [{"role":"user"/"assistant","content":"..."}]
        """
        if self.use_vertex and self.client:
            # Convert to LC messages
            from langchain.schema import SystemMessage, HumanMessage, AIMessage
            lc_messages = []
            if system:
                lc_messages.append(SystemMessage(content=system))
            for m in messages:
                if m["role"] == "user":
                    lc_messages.append(HumanMessage(content=m["content"]))
                else:
                    lc_messages.append(AIMessage(content=m["content"]))
            resp = self.client(lc_messages)
            return resp.content if hasattr(resp, "content") else str(resp)

        # Stub response for dev
        user_last = ""
        for m in messages[::-1]:
            if m["role"] == "user":
                user_last = m["content"]
                break
        return f"[DEV LLM STUB] Summary: {user_last[:220]}"
