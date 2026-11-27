
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from pathlib import Path

# Model configuration
MODEL_NAME = "distilbert/distilgpt2"
TOP_K = 5

# Sample input prompt
PROMPT = "Artificial intelligence is"

print("=" * 65)
print("       NEXT-TOKEN PROBABILITY ANALYSIS")
print("=" * 65)

# Load tokenizer
print("\nLoading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# Load language model
print("Loading DistilGPT-2 model...")
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
model.eval()

print("Model loaded successfully!")

# Tokenize the input prompt
inputs = tokenizer(PROMPT, return_tensors="pt")

print("\nInput Prompt:", PROMPT)
print("Input Token IDs:", inputs["input_ids"].tolist())

# Perform model inference
with torch.no_grad():
    outputs = model(**inputs)

# Extract logits for the final input position
logits = outputs.logits[0, -1, :]

# Convert logits into probabilities
probabilities = torch.softmax(logits, dim=-1)

# Find the top-k candidates
top_probs, top_indices = torch.topk(probabilities, TOP_K)

# Display results
print("\n" + "=" * 65)
print("NEXT TOKEN CANDIDATES")
print("=" * 65)

print(f"\n{'Rank':<8}{'Token':<20}{'Logit':<15}{'Probability':<15}")
print("-" * 65)

results = []

for rank, (token_id, probability) in enumerate(
    zip(top_indices.tolist(), top_probs.tolist()), start=1
):
    token = tokenizer.decode([token_id])
    logit = logits[token_id].item()

    line = (
        f"{rank:<8}{repr(token):<20}"
        f"{logit:<15.4f}{probability * 100:<14.4f}%"
    )

    print(line)
    results.append(line)

# Identify the most probable next token
best_token_id = top_indices[0].item()
best_token = tokenizer.decode([best_token_id])

print("\nMost probable next token:", repr(best_token))
print("Logits shape:", tuple(outputs.logits.shape))
print("Vocabulary size:", logits.shape[0])

# Save results
output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)

output_file = output_dir / "next_token_results.txt"

with output_file.open("w", encoding="utf-8") as file:
    file.write("NEXT-TOKEN PROBABILITY ANALYSIS\n")
    file.write("=" * 50 + "\n")
    file.write(f"Model: {MODEL_NAME}\n")
    file.write(f"Prompt: {PROMPT}\n")
    file.write(f"Input Token IDs: {inputs['input_ids'].tolist()}\n")
    file.write(f"Logits Shape: {tuple(outputs.logits.shape)}\n")
    file.write(f"Vocabulary Size: {logits.shape[0]}\n\n")
    file.write("Top 5 Next-Token Candidates:\n")
    file.write("-" * 50 + "\n")

    for result in results:
        file.write(result + "\n")

    file.write(f"\nMost probable next token: {best_token!r}\n")

print("\nResults saved to:", output_file)
print("\nExperiment completed successfully!")
