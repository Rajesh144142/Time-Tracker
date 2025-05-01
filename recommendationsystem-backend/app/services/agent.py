import os
import json
from typing import Dict, Any
from datetime import datetime, timedelta
from autogen import AssistantAgent, UserProxyAgent

class RecommendationSystem:
    def __init__(self):
        self.config = self._load_config()
        self.assistant, self.verifier, self.user_proxy = self._initialize_agents()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration and data files"""
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(BASE_DIR, "data")
        
        return {
            "roles_data": self._load_json_file(os.path.join(data_dir, "project_roles_knowledge.json")),
            "users_data": self._load_json_file(os.path.join(data_dir, "user_mapping.json")),
            "llm_config": {
                "config_list": [
                    {
                        "model": "llama2:latest",
                        "base_url": "http://localhost:11434/v1",
                        "api_key": "ollama",
                        "price": [0.0, 0.0]
                    }
                ],
                "cache_seed": 42,
                "temperature": 0.5,
            }
        }

    def _load_json_file(self, file_path: str) -> Dict[str, Any]:
        """Helper to load JSON files"""
        with open(file_path, "r") as f:
            return json.load(f)

    def _initialize_agents(self):
        """Initialize and configure all agents"""
        assistant = AssistantAgent(
            name="recommender",
            system_message="""You are a helpful recommendation assistant. 
            Use only the provided context to answer questions about company roles, 
            permissions, and user information. If information is not available, 
            respond with "I don't know".""",
            llm_config=self.config["llm_config"]
        )
        
        verifier = AssistantAgent(
            name="verifier",
            system_message="""You are a quality assurance verifier. Your tasks:
            1. Verify answers match the provided context exactly
            2. Check for hallucinations or made-up information
            3. Ensure responses are professional and helpful
            4. If correct, respond with "VERIFIED: <response>"
            5. If incorrect, provide "CORRECTED: <new response>"
            6. Always include "TERMINATE" at the end""",
            llm_config=self.config["llm_config"]
        )
        
        user_proxy = UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=0,
            is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""),
            code_execution_config=False,
        )
        
        return assistant, verifier, user_proxy

    def build_context(self) -> str:
        """Build the context string from loaded data"""
        context = [
            f"### Company Info:",
            f"Company Name: {self.config['users_data'].get('companyName')}",
            f"Company ID: {self.config['users_data'].get('companyId')}\n",
            "### Roles and Permissions:"
        ]
        
        for role, info in self.config["roles_data"].items():
            context.extend([
                f"\n**{role}**",
                f"Description: {info['description']}",
                f"Permissions: {', '.join(info['permissions'])}",
                f"Reports To: {info['reports_to'] or 'None'}"
            ])
        
        context.append("\n### Users:")
        for user_id, user_info in self.config["users_data"]["users"].items():
            context.extend([
                f"\nName: {user_info['name']}",
                f"Roles: {', '.join(user_info['roles'])}",
                f"Designation: {user_info['designation']}"
            ])
        
        return "\n".join(context)

    def ask_ai(self, question: str, timeout_seconds: int = 30) -> str:
        """
        Process a question through recommendation system with verification
        Args:
            question: The question to ask
            timeout_seconds: Maximum time allowed for processing
        Returns:
            str: The verified response
        Raises:
            TimeoutError: If processing takes too long
        """
        start_time = datetime.now()
        context = self.build_context()
        
        try:
            # Initial recommendation
            self.user_proxy.reset()
            initial_prompt = f"""{context}\n\n### Question:\n{question}\n\nAnswer:"""
            
            self.user_proxy.initiate_chat(
                self.assistant,
                message=initial_prompt,
                clear_history=True
            )
            
            if datetime.now() - start_time > timedelta(seconds=timeout_seconds):
                raise TimeoutError("Initial recommendation timed out")
                
            initial_response = self.user_proxy.last_message()["content"]
            
            # Verification step
            self.user_proxy.reset()
            verify_prompt = f"""Verify this response:
            Question: {question}
            Context: {context}
            Response: {initial_response}
            
            Instructions:
            1. If correct, respond with "VERIFIED: <response> TERMINATE"
            2. If incorrect, respond with "CORRECTED: <new response> TERMINATE"
            3. Never add any additional commentary"""
            
            self.user_proxy.initiate_chat(
                self.verifier,
                message=verify_prompt,
                clear_history=True
            )
            
            if datetime.now() - start_time > timedelta(seconds=timeout_seconds):
                raise TimeoutError("Verification timed out")
                
            final_response = self.user_proxy.last_message()["content"]
            
            # Parse response
            if "VERIFIED:" in final_response:
                return final_response.split("VERIFIED:")[1].replace("TERMINATE", "").strip()
            elif "CORRECTED:" in final_response:
                return final_response.split("CORRECTED:")[1].replace("TERMINATE", "").strip()
            return final_response
            
        except Exception as e:
            self.user_proxy.reset()
            raise e

# Singleton instance
recommendation_system = RecommendationSystem()

def ask_ai(question: str) -> str:
    """Public interface for the recommendation system"""
    return recommendation_system.ask_ai(question)