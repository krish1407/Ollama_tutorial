# ~/miniconda3/bin/conda init zsh
# conda activate ollama_setup  



import ollama

client = ollama.Client()
model = "llama3.1:8b"

prompt = "what is python?"

response = client.generate(model=model, prompt=prompt)
print(response.response)