# test_llm.py  — create this at the project root
from llm_sdk import Small_LLM_Model

print("Loading model...")
model = Small_LLM_Model()   # downloads Qwen3-0.6B on first run (~1.5GB)

prompt = "What is the capital of France?"
ids = model.encode(prompt).squeeze(0).tolist()
logits = model.get_logits_from_input_ids(ids)

# pick the top token
best_id = max(range(len(logits)), key=lambda i: logits[i])
result = model.decode([best_id])

print(f"Top next token: {repr(result)}")
print("LLM is working correctly ✓")
