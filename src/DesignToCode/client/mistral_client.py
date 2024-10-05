import logging
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List, Dict, Any
import convertapi
from convertapi import client
from mistralai import Mistral
from pydantic import BaseModel, Field

from dotenv import load_dotenv

from DesignToCode.client.prompt_generator import PromptGenerator


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


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

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


    def describe_image(self, prompt) -> Optional[str]:
        """
        Sends an image URL to the image model and retrieves a description.

        Args:
            image_path (str): URL of the image to describe.

        Returns:
            Optional[str]: Description of the image or None if failed.
        """

        payload = MistralRequestPayload(
            model=self.img_model,
            messages=prompt,
        )

        try:
            response = self.client.chat.complete(
                model=payload.model,
                messages=payload.messages
            )
            html = response.choices[0].message.content
            return html
        except Exception as e:
            logging.warning(f"Error describing image: {e}")
            return None

    def generate_code(
            self,
            prompt_template: str,
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
        try:
            response = self.client.fim.complete(
                model=self.code_model,
                prompt=prompt_template,
                suffix=suffix if suffix else "",
                temperature=0,
                # top_p=1.0,
            )
            code = response.choices[0].message.content
            return code
        except Exception as e:
            logging.warning(f"Error generating code: {e}")
            return None


    @staticmethod
    def save_generate_code_to_html(code):
        def extract_html_code(text):
            pattern = re.compile(r"```html(.*?)```", re.DOTALL)
            match = pattern.search(text)

            if match:
                return match.group(1).strip()
            else:
                raise ValueError("No HTML code block found in the input text.")

        def save_to_html_file(html_code, file_name="output.html"):
            file_path = Path(file_name).resolve()
            logging.info(file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(html_code)
            return file_path

        html_code = extract_html_code(code)
        file_path = save_to_html_file(html_code, "sample_output.html")
        return html_code, file_path

    @staticmethod
    def convertapi_call(convertapi, path, out):
        # path = path to html generated
        #
        convertapi.api_credentials = 'secret_xsDD6o46ZhquOH5H'
        convertapi.convert('png', {
            'File': f'{path}',
            'FileName': f'{out}',
            'ConversionDelay': '3',
            'Version': '126'
        }, from_format='html').save_files("/Users/carlo/PycharmProjects/DesignToCode/src/DesignToCode/output")
        logging.info("done")

    def initialise_html_code(self, initial_encoded_img, figma_json_context, out: str = "initial_png_from_html", ):
        prompt_generator = PromptGenerator()
        initial_pixtral_prompt = prompt_generator.generate_initial_image_description_prompt(initial_encoded_img, figma_json_context)

        image_description = self.describe_image(
            prompt = initial_pixtral_prompt
            )

        logging.info("IMAGE DESCRIPTION DONE")
        logging.info(f"{image_description}")

        initial_code_prompt = prompt_generator.generate_initial_code_prompt(
            description=image_description,
            json_context=figma_json_context
        )
        code = self.generate_code(
            prompt_template=initial_code_prompt
        )

        logging.info("CODE DONE")
        logging.info(f"{code}")

        # safe to html
        html_file, path = self.save_generate_code_to_html(code)
        logging.info(f" PATH = {path}")
        self.convertapi_call(convertapi, path, out)

        return image_description, code

    def iterate_and_improve(self, initial_encoded_image, initial_description, new_encoded_image, figma_json_context ):
        prompt_generator = PromptGenerator()
        compare_description_prompt = prompt_generator.generate_further_iterative_image_description_prompt(
            old_description=initial_description,
            old_base64_image=initial_encoded_image,
            new_base64_image=new_encoded_image,
            old_json_context=figma_json_context
        )

        compared_description = self.describe_image(
            prompt=compare_description_prompt
        )

        new_code_prompt = prompt_generator.generate_initial_code_prompt(
            description=compared_description,
            json_context=figma_json_context
        )

        code = self.generate_code(
            prompt_template=new_code_prompt
        )


