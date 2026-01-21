import asyncio
import os
import sys
import json

# Ensure src is in path
sys.path.append(os.getcwd())

from src.core.memory import StrategicMemory
from src.core.config import Config

async def main():
    print("--- Zenith Memory Verification ---")
    
    # Mock Config
    try:
        config = Config.load()
    except Exception as e:
        print(f"Failed to load config: {e}")
        return

    # Initialize Memory
    print("Initializing StrategicMemory...")
    memory = StrategicMemory(config)
    
    # FORCE INITIAL SAVE to verify file system access
    print("\nTest 0: Force Save...")
    memory.save_memory()
    memory_path = os.path.join(os.getcwd(), "data", "memory.json")
    
    if os.path.exists(memory_path):
        print("✅ Memory file successfully created.")
    else:
        print("❌ Failed to create memory file.")
        return

    # Test 1: Entity Extraction
    print("\nTest 1: Extacting Entities...")
    user_input = "Meu nome é Stuart e eu estou trabalhando no projeto Zenith."
    model_output = "Olá Stuart! Ótimo saber que você está focado no Zenith."
    
    await memory.extract_entities_async(user_input, model_output)
    
    # Check if saved to JSON
    if os.path.exists(memory_path):
        with open(memory_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            print(f"✅ Memory JSON exists. Profile: {data.get('user_profile')}")
            
            # Simple check if 'Stuart' or 'Zenith' is in the profile (keys or values)
            profile_str = str(data.get('user_profile'))
            if "Stuart" in profile_str or "Zenith" in profile_str:
                print("✅ Entities correctly extracted.")
            else:
                print("⚠️ Entities NOT found in profile (LLM might have skipped).")
    else:
        print("❌ Memory JSON file missing after Test 1.")

    # Test 2: Consolidation
    print("\nTest 2: Consolidating Memory...")
    old_messages = [
        type('obj', (object,), {'role': 'user', 'parts': [type('obj', (object,), {'text': 'Eu gosto de Python.'})]})(),
        type('obj', (object,), {'role': 'model', 'parts': [type('obj', (object,), {'text': 'Python é excelente.'})]})()
    ]
    
    await memory.consolidate_memory_async(old_messages)
    
    if os.path.exists(memory_path):
        with open(memory_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            summary = data.get("master_summary")
            print(f"✅ Master Summary updated: {summary[:50]}...")
            if len(summary) > 5:
                 print("✅ Consolidation successful.")
            else:
                 print("⚠️ Summary is empty.")
    else:
        print("❌ Memory JSON file missing after Test 2.")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
