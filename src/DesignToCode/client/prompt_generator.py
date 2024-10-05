from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class PromptGenerator:

    @staticmethod
    def generate_initial_image_description_prompt(base64_image: str, json_context) -> List[Dict[str, Any]]:
        message = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text":
                        f"""
                        Describe the given image in most detail as possible. 
                        Describe data you see as well as colour of items.
                        Include the orientation of objects.
                        
                        Use the help of the JSON context you have. This Json context is a figma created json that 
                        describes all objects and its parameter for the given picture to be implemented into HTML.
                        
                        Additional context: {json_context}
                        """
                     },
                    {"type": "image_url",
                     "image_url": f"data:image/jpeg;base64,{base64_image}"}
                ]
            }
        ]
        return message

    @staticmethod
    def generate_further_iterative_image_description_prompt(old_base64_image: str, new_base64_image: str,
                                                            old_description: str, old_json_context) -> List[
        Dict[str, Any]]:
        message = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text":
                        f"""
                        Describe the given image in most detail as possible. 
                        Describe data you see as well as colour of items.
                        Include the orientation of objects and compare how they should be with help of the JSON context
                        you have. This Json context is a figma created json that describes all objects and its parameters
                        for the given picture to be implemented into HTML.
                        
                        Your task is to compare it in detail to the old description of the image and the json context on
                        how it should be looking. 
                        
                        The old description:\n
                        {old_description}
                        
                        The JSON context: \n
                        {old_json_context}
                        
                        Only output the difference of both descriptions into the answer and point out what has to be 
                        changed to improve it.
                    
                        
                        """
                     },
                    {"type": "image_url",
                     "image_url": f"data:image/jpeg;base64,{old_base64_image}"},
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{new_base64_image}"
                    }
                ]
            }
        ]
        return message

    @staticmethod
    def generate_initial_code_prompt(description: str, json_context: Optional[str] = None) -> str:
        prompt_template = (
            f"Your task is to write the correct HTML code for the given JSON in context.\n "
            f"Use the JSON context given which contains all data needed from Figma and as \n"
            f"well the description of the image provided.\n "
            f"IMAGE DESCRIPTION:\n"
            f"{description}\n\n"

            f"JSON CONTEXT:\n"
            f"{json_context}\n\n"
            "Make sure the output is a complete html file to be ready to go on the web.\n"
            "The file should contain the usual start of an html like:"
            """
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title></title>
            """

        )
        return prompt_template


    @staticmethod
    def generate_iterative_code_prompt(
            old_description: Optional[str],
            new_description: Optional[str],
            description_comparison: Optional[str],
            old_code,
            json_context: Optional[str] = None

        ) -> str:
        prompt_template = (
            f"You get the old description of a image that should be transferred to html code with help of a JSON context "
            f"which describes all parameters and objects inside this image as "
            f""
            f"and the new description and the comparison of descriptions"
            f"of a previous response to the original image description."
            f"Given that can you try to find out what you would need to change to the old code."
            f"Use the JSON context given which contains all data needed from Figma and as \n"
            f"well the description of the image provided.\n "
            
            f"The old description"
            f"{old_description}"
            
            f"The new description: "
            f"{new_description}"
            
            f"Comparison to the old description:\n"
            f"{description_comparison}\n\n"
            
            f" Old code:"
            f" {old_code}"

            f"JSON CONTEXT:\n"
            f"{json_context}\n\n"
            "Make sure the output is a complete html file to be ready to go on the web.\n"
            "The file should contain the usual start of an html like:"
            """
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title></title>
            """

        )
        return prompt_template
