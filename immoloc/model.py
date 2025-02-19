import os
from mistralai import Mistral


model = "mistral-large-latest"
api_key = os.getenv("API_KEY")

if not api_key:
    raise ValueError("API_KEY environment variable is not set")
if not isinstance(api_key, str):
    raise TypeError("API_KEY environment variable must be a string")

try:
    client = Mistral(api_key=api_key)
except Exception as e:
    raise RuntimeError(f"Failed to initialize Mistral client: {e}")

# Example :
# chat_response = client.chat.complete(
#     model= model,
#     messages = [
#         {
#             "role": "user",
#             "content": "What is the best French cheese?",
#         },
#     ]
# )
# print(chat_response.choices[0].message.content)