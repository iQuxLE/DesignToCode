from src.DesignToCode.client.mistral_client import MistralImageToCodeClient
from src.DesignToCode.visual.image_encoder import ImageEncoder
from src.DesignToCode.wrapper.json_wrapper import JsonWrapper


class Runner:

    @staticmethod
    def run():
        image_encoder = ImageEncoder()
        json_wrapper = JsonWrapper()
        client = MistralImageToCodeClient(api_key=None)
        base64image = image_encoder.encode_base64(
            image_path="/Users/carlo/PycharmProjects/DesignToCode/src/DesignToCode/input/image/rendered_component.png")
        json = json_wrapper.read(
            json_source="/Users/carlo/PycharmProjects/DesignToCode/src/DesignToCode/input/json/context.json")

        # # Step 1: Describe the image
        # description = client.describe_image(
        #     base64_image=base64image,
        #     json_context=json
        #     )
        # if not description:
        #     print("Failed to get image description.")
        #     return

        # print(description)

        # Step 2: Generate code based on the image description
        # code = client.generate_code(json_context=json, prompt_template=None)
        # print(code)
        # if not code:
        #     print("Failed to generate code.")
        #     return
        initial_description, initial_code = client.initialise_html_code(
                initial_encoded_img=base64image,
                figma_json_context=json
            )

if __name__ == "__main__":
    runner = Runner()
    runner.run()