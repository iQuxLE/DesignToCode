from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class PromptGenerator:
    base_prompt: str

    @staticmethod
    def generate_image_description_prompt(self, image_url: str) -> List[Dict[str, Any]]:
        return [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What's in this image?"},
                    {"type": "image_url", "image_url": image_url}
                ]
            }
        ]

    def generate_code_prompt(self, description: str, additional_instructions: Optional[str] = None) -> str:
        prompt = f"Based on the following description, write the corresponding code:\n\n{description}\n\nCode:"
        if additional_instructions:
            prompt += f"\n\n{additional_instructions}"
        return prompt