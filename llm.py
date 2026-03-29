from config import GROQ_API_KEY
from groq import Groq
from tools import send_email
import json

client = Groq(
    api_key=GROQ_API_KEY,
)

tool_schema = {
  "type": "function",
  "function": {
    "name": "send_email",
    "description": "This can send emails.",
    "parameters": {
      "type": "object",
      "properties": {
        "receiver_mail" :{
            "type" : "string",
            "description": "Mail of the receiver."
        },
        "subject" :{
            "type" : "string",
            "description": "Subject of the mail."
        },
        "content" :{
            "type" : "string",
            "description": "content of the mail."
        }
      },
      "required": ["receiver_mail","subject","content"]
    }
  }
}

available_functions = {
    "send_email": send_email,
   
}

def execute_tool_call(tool_call):
    """Parse and execute a single tool call"""
    function_name = tool_call.function.name
    function_to_call = available_functions[function_name]
    function_args = json.loads(tool_call.function.arguments)
    
    # Call the function with unpacked arguments
    return function_to_call(**function_args)
messages=[ 
            {
             "role":"system",
             "content": "You are a helpful AI assistant and your creator is Gitanshi Gupta."            
             }
        ]
def generate_response(prompt):
    messages.append({"role": "user",
                "content": prompt})

    response = client.chat.completions.create(
        messages= messages,
        model="openai/gpt-oss-120b",
        tools=[tool_schema]
    )
    
    messages.append(response.choices[0].message)

    # 2. Check for tool calls
    # kya groq tool call karna chahta hai?
    if response.choices[0].message.tool_calls:
        # 3. Execute each tool call (using the helper function from step 2)
        for tool_call in response.choices[0].message.tool_calls:
            function_response = execute_tool_call(tool_call)
            
            # Add tool result to messages
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_call.function.name,
                "content": str(function_response)
            })
        
        # 4. Send results back and get final response
        final = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages
        )
        messages.append(final.choices[0].message)
        return final.choices[0].message.content

    return response.choices[0].message.content

# while True:
#     input_prompt = input("Enter your prompt: ")
#     response = generate_response(input_prompt)
#     print("Response: ", response)