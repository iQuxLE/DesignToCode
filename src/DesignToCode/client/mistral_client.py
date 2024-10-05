import logging
import os
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

import convertapi
from mistralai import Mistral
from pydantic import BaseModel

from dotenv import load_dotenv

from DesignToCode.client.prompt_generator import PromptGenerator
from DesignToCode.util.util import parse_new_and_compared_description_seperately, convertapi_call, \
    save_generate_code_to_html


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


    def describe_image(self, prompt) -> Optional[Any]:
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
            response_format={
                "type": "json_object"
            }
        )
        try:
            response = self.client.chat.complete(
                model=payload.model,
                messages=payload.messages,
                response_format=payload.response_format
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


    def initialise_html_code(
            self,
            initial_encoded_img,
            figma_json_context,
            out: str = "1_initial_png_from_html"
    ):
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
        html_file, path = save_generate_code_to_html(code)
        logging.info(f" PATH = {path}")
        output_file_path = convertapi_call(convertapi, path, out)

        return image_description, code, output_file_path

    def iterate_and_improve(
            self,
            initial_encoded_image,
            initial_description,
            new_encoded_image,
            figma_json_context,
            initial_code,
            updated_code: Optional,
            out:str = "2_iterative_pmg_from_html"
    ):
        prompt_generator = PromptGenerator()

        # PIXTRAL
        compare_description_prompt = prompt_generator.generate_further_iterative_image_description_prompt(
            old_description=initial_description,
            old_base64_image=initial_encoded_image,
            new_base64_image=new_encoded_image,
            old_json_context=figma_json_context
        )

        new_and_compared_description = self.describe_image(
            prompt=compare_description_prompt
        )

        updated_description, comparison_of_descriptions = parse_new_and_compared_description_seperately(new_and_compared_description)

        # CODE
        # check if updated code otherwise different prompt
        if updated_code is None:
            new_code_prompt = prompt_generator.generate_iterative_code_prompt(
                old_description=initial_description,
                new_description=updated_description,
                description_comparison=comparison_of_descriptions,
                initial_code=initial_code,
                json_context=figma_json_context
            )
        else:
            new_code_prompt = prompt_generator.generate_updated_code_prompt(
                old_description=initial_description,
                new_description=updated_description,
                description_comparison=comparison_of_descriptions,
                initial_code=initial_code,
                updated_code=updated_code,
                json_context=figma_json_context
            )

        updated_code = self.generate_code(
            prompt_template=new_code_prompt
        )

        html_file, path = save_generate_code_to_html(updated_code)
        logging.info(f" PATH = {path}")
        output_file_path  = convertapi_call(convertapi, path, out)

        return updated_description, comparison_of_descriptions, updated_code, output_file_path




