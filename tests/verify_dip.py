import sys
import os
import asyncio
from typing import List, Dict, Any, AsyncGenerator

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.agent import ZenithAgent
from src.core.config import Config
from src.core.database import PersistenceLayer
from src.core.agent import ZenithAgent
from src.core.config import Config
from src.core.database import PersistenceLayer
from src.core.llm.provider import LLMProvider

# Mock Heavy Services
class MockService:
    def __init__(self): pass

# --- Mock Implementations ---

class MockRepository:
    def create_session(self, session_id: str, user_id: str) -> None:
        print(f"[MockDB] Session created: {session_id}")

    def log_interaction(self, session_id: str, user_id: str, role: str, content: str, metadata: dict = None) -> None:
        print(f"[MockDB] Logged interaction: {role} - {content[:20]}...")

    def get_history(self, session_id: str, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        print("[MockDB] Returning empty history")
        return []

    def log_usage(self, user_id: str, session_id: str, model: str, input_tokens: int, output_tokens: int, total_tokens: int) -> None:
        print(f"[MockDB] Logged usage: {total_tokens} tokens")

class MockSession:
    def __init__(self):
        self._history = []
    
    @property
    def history(self):
        return self._history
    
    @history.setter
    def history(self, value):
        self._history = value

    async def send_message_async(self, message: str):
        return "Mock Response"

class MockLLM(LLMProvider):
    def configure(self, api_key: str):
        pass

    def start_chat(self, history: List[Dict[str, Any]] = None) -> Any:
        print("[MockLLM] Chat started")
        return MockSession()

    async def generate_content_async(self, prompt: str, **kwargs) -> str:
        return "Mock Response"

    async def send_message_async(self, session: Any, message: str, stream: bool = False) -> AsyncGenerator[str, None]:
        print(f"[MockLLM] Sending message: {message}")
        yield "This "
        yield "is "
        yield "a "
        yield "mock "
        yield "response."


# --- Verification ---

def verify_dip():
    print("--- Verifying DIP Refactoring ---")
    
    # 1. Setup Config (Mocked)
    # 1. Setup Config (Mocked)
    # Pydantic Settings will read env, but we can override args.
    # Note: Properties like DATA_DIR are computed, not passed in init.
    config = Config(
        GOOGLE_API_KEY="mock_key",
        MODEL_NAME="mock_model",
        TEMPERATURE=0.0,
        SUPABASE_URL="https://mock.supabase.co",
        SUPABASE_KEY="mock_supabase_key"
    )
    
    # 2. Setup Mocks (Dependencies)
    mock_db = MockRepository()
    mock_llm = MockLLM()
    
    print("\n1. Instantiating ZenithAgent with Mocks...")
    try:
        agent = ZenithAgent(
            config=config,
            system_instruction="You are a test bot.",
            db=mock_db,   
            llm=mock_llm,
            knowledge_base=MockService(),
            context_builder=MockService(),
            analyzer=MockService(),
            judge=MockService(),
            memory=MockService(),
            validator=MockService()
        )
        print("✅ ZenithAgent instantiated successfully!")
    except Exception as e:
        print(f"❌ Failed to instantiate ZenithAgent: {e}")
        return

    print("\n2. Checking Attributes...")
    # Skipping isinstance check because PersistenceLayer is not @runtime_checkable
    # The fact that we are here means instantiation succeeded with a Mock object.
    
    # Check if the injected dependencies are actually our mocks
    print(f"   agent.db is mock_db: {agent.db is mock_db}")
    print(f"   agent.llm is mock_llm: {agent.llm is mock_llm}")

    if agent.db is mock_db and agent.llm is mock_llm:
        print("✅ Dependencies correctly injected.")
    else:
        print("❌ Dependency injection failed.")

    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    verify_dip()
