import os
import json
from dotenv import load_dotenv
import openai
from autogen import AssistantAgent

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load role and user data
def load_json_file(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

BASE_DIR = os.path.dirname(__file__)
roles_data = load_json_file(os.path.join(BASE_DIR, "project_roles_knowledge.json"))
users_data = load_json_file(os.path.join(BASE_DIR, "user_mapping.json"))

# Prepare context string
def build_context():
    context = f"### Company Info:\nCompany Name: {users_data.get('companyName')}\nCompany ID: {users_data.get('companyId')}\n"
    context += "\n### Roles and Permissions:\n"
    
    for role, info in roles_data.items():
        context += f"\n**{role}**\nDescription: {info['description']}\n"
        context += f"Permissions: {', '.join(info['permissions'])}\n"
        context += f"Reports To: {info['reports_to'] or 'None'}\n"

    context += "\n\n### Users:\n"
    for user_id, user_info in users_data["users"].items():
        context += f"\nName: {user_info['name']}\n"
        context += f"Roles: {', '.join(user_info['roles'])}\n"
        context += f"Designation: {user_info['designation']}\n"

    return context


# LLM config for Ollama
llm_config = {
    "config_list": [
        {
            "model": "llama2:latest",  # Match your local Ollama model name
            "api_key": "ollama-local",  # Dummy key for compatibility
            "base_url": "http://localhost:11434/v1",
            "price": [0.01, 0.05]
        }
    ],
    "cache_seed": 42,
    "temperature": 0,
}

# Create assistant agent
assistant = AssistantAgent(name="assistant", llm_config=llm_config)

# Ask logic (single-turn)
# def ask_ai(question: str):
#     context = build_context()
#     full_prompt = f"{context}\n\n### Question:\n{question}"

#     response = assistant.generate_reply(messages=[
#         {"role": "user", "content": full_prompt}
#     ])

#     return response


def ask_ai(question: str):
    context = build_context()
    full_prompt = f"""{context}

### Instruction:
Only use the information above to answer the following question. Do not use any external knowledge.

### Question:
{question}
"""

    print("===== Prompt Sent to Assistant =====")
    print(full_prompt)
    print("====================================")

    response = assistant.generate_reply(messages=[
        {"role": "user", "content": full_prompt}
    ])

    if "company name" in question.lower():
        company_name = users_data.get("companyName", "Unknown Company")
        return f"The company name is: {company_name}"

    return response.get("content") if isinstance(response, dict) else str(response)


