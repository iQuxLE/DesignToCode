import os
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

from mistralai import Mistral
from pydantic import BaseModel, Field

from dotenv import load_dotenv

class MistralResponse(BaseModel):
    generated_text: str
    # other fields as needed



class MistralRequestPayload(BaseModel):
    # adjust fields as necessary
    model: str
    messages: List[Dict[str, Any]]
    prompt: Optional[str] = None
    suffix: Optional[str] = None
    temperature: float = 0.7
    top_p: float = 1.0


# MistralClient use
# -> generate_prompt = PromptGenerator(text, messages)

# -> client = MistralClient
# -> img_description = client.describe_image(prompt)
# -> code_response = client.design_code_for_img(img_description)

@dataclass
class MistralImageToCodeClient:
    api_key: Optional[str]
    client: Mistral = field(init=False)
    endpoint: str = "https://api.mistral.ai/v1/generate"
    img_model: str = "pixtral-12b-2409"
    code_model: str = "codestral-latest"


    def __post_init__(self):
        load_dotenv()
        if self.api_key is None:
            self.api_key = os.getenv("MISTRAL_API_KEY")
            if self.api_key is None:
                raise (
                    "The api_key client option must be set either by passing api_key to the client or by setting the MISTRAL_API_KEY environment variable"
                )
        self.client = Mistral(self.api_key)


    def describe_image(self, base64_image: str) -> Optional[str]:
        """
        Sends an image URL to the image model and retrieves a description.

        Args:
            image_path (str): URL of the image to describe.

        Returns:
            Optional[str]: Description of the image or None if failed.
        """
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe the given image. The image is a Figma design that has to be implemnted with all its contents."
                                             "Be as descriptive as possible and try to evaluate all the little aspects and things that should be needed"
                                             "Together with this you get additional context in form of a JSON which helps you to design css and html and the"
                                             "You task would be to generate a HTML for the Figma design."
                                             },
                    {"type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{base64_image}"}
                ]
            }
        ]

        payload = MistralRequestPayload(
            model=self.img_model,
            messages=messages
        )

        try:
            response = self.client.chat.complete(
                model=payload.model,
                messages=payload.messages
            )
            description = response.choices[0].message.content
            print(f"Image Description: {description}")
            return description
        except Exception as e:
            print(f"Error describing image: {e}")
            return None

    def design_code_for_img(
            self,
            description: str,
            prompt_template: Optional[str] = None,
            suffix: Optional[str] = None
    ) -> Optional[str]:
        """
        Generates code based on the image description using the code model.

        Args:
            description (str): Description of the image.
            prompt_template (Optional[str]): Template for the prompt.
            suffix (Optional[str]): Suffix to append to the prompt.

        Returns:
            Optional[str]: Generated code or None if failed.
        """
        if not prompt_template:
            prompt_template = f"Based on the following description, write the corresponding code:\n\n{description}\n\nCode:"

        payload = MistralRequestPayload(
            model=self.code_model,
            prompt=prompt_template,
            suffix=suffix if suffix else "",
            temperature=0,
            top_p=1.0
        )

        try:
            response = self.client.fim.complete(
                model=payload.model,
                prompt=payload.prompt,
                suffix=payload.suffix,
                temperature=payload.temperature,
                top_p=payload.top_p,
            )
            code = response.choices[0].message.content
            print(f"Generated Code:\n{code}")
            return code
        except Exception as e:
            print(f"Error generating code: {e}")
            return None



    def send_request(self, payload: MistralRequestPayload) -> Optional[Any]:
        """
        Sends a generic request to Mistral's API.

        Args:
            payload (MistralRequestPayload): The request payload.

        Returns:
            Optional[Any]: The API response or None if failed.
        """
        try:
            if payload.model.startswith("pixtral"):
                response = self.client.chat.complete(
                    model=payload.model,
                    messages=payload.messages
                )
            elif payload.model.startswith("codestral"):
                response = self.client.fim.complete(
                    model=payload.model,
                    prompt=payload.prompt,
                    suffix=payload.suffix,
                    temperature=payload.temperature,
                    top_p=payload.top_p,
                )
            else:
                print(f"Unsupported model: {payload.model}")
                return None
            return response
        except Exception as e:
            print(f"Error sending request: {e}")
            return None

