import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_NAME = "distilbert/distilgpt2"

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

print("Loading model...")
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

model.eval()

print("Model loaded successfully!")

prompt = "Artificial intelligence is"

inputs = tokenizer(prompt, return_tensors="pt")

with torch.no_grad():
    outputs = model(**inputs)

logits = outputs.logits

print("\nPrompt:", prompt)
print("Input token IDs:", inputs["input_ids"])
print("Logits shape:", logits.shape)
print("Model test completed!")