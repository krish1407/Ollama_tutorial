
## To create a custom model
### 1. create a model file and then run the below command
# ollama create mlops-assistant -f Modelfile

###################
# Check the prompt used to create the model
###############
# ollama show mlops-assistant


######################
#### multiple modelfiles
######################
# modelfiles/
#   analyst.Modelfile
#   reporter.Modelfile
######################
# for bashscript
######################
# ollama create analyst-model -f modelfiles/analyst.Modelfile
# ollama create reporter-model -f modelfiles/reporter.Modelfile

######################
# for loop
######################
# for f in modelfiles/*.Modelfile; do
#   name=$(basename "$f" .Modelfile)
#   ollama create "$name" -f "$f"
# done

############################
###### analyst.Modelfile ###
############################
# FROM mistral

# PARAMETER temperature 0.2
# PARAMETER top_p 0.9

# SYSTEM """
# You are a senior data analyst.
# Your job:
# - Clean and transform datasets logically
# - Write SQL, PySpark, and Python pandas code
# - Detect anomalies in data
# - Explain transformations step by step
# - Prefer correctness over verbosity
# - Always validate assumptions before answering
# """

# TEMPLATE """
# User Query:
# {{ .Prompt }}

# Analyst Response:
# """


######################
# reporter.Modelfile #
######################
# FROM mistral

# PARAMETER temperature 0.7
# PARAMETER top_p 0.95

# SYSTEM """
# You are a reporting and business insights assistant.
# Your job:
# - Convert analytics output into business-friendly insights
# - Summarize trends clearly
# - Create executive-ready narratives
# - Avoid technical jargon unless asked
# - Focus on "what this means" not "how it was computed"
# """

# TEMPLATE """
# Context:
# {{ .Prompt }}

# Executive Summary:
# """





# payload = {
#     "model": "mlops-assistant",
#     "messages": [
#         {
#             "role": "user",
#             "content": "Optimize this PySpark join"
#         }
#     ]
# }