from config import GROQ_API_KEY
from groq import Groq

client = Groq(
    api_key=GROQ_API_KEY,
)

def generate_response(prompt):
    chat_completion = client.chat.completions.create(
        messages=[ 
            {
             "role":"system",
             "content": "You are a helpful AI assistant and your creator is Gitanshi Gupta."            
             },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="groq/compound",
    )
    
    return chat_completion.choices[0].message.content

# while True:
#     input_prompt = input("Enter your prompt: ")
#     response = generate_response(input_prompt)
#     print("Response: ", response)