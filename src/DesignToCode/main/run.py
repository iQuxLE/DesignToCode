from src.DesignToCode.client.mistral_client import MistralImageToCodeClient
from src.DesignToCode.visual.image_encoder import ImageEncoder
from src.DesignToCode.wrapper.json_wrapper import JsonWrapper


class Runner:

    def run(self):
        imageEncoder = ImageEncoder()
        jsonWrapper = JsonWrapper()
        client = MistralImageToCodeClient(api_key=None)
        base64image = imageEncoder.encode_base64(
            image_path="/Users/carlo/PycharmProjects/DesignToCode/src/DesignToCode/input/image/rendered_component.png")
        json = jsonWrapper.read(
            json_source="/Users/carlo/PycharmProjects/DesignToCode/src/DesignToCode/input/json/context.json")

        # Step 1: Describe the image
        description = client.describe_image(
            base64_image=base64image)
        if not description:
            print("Failed to get image description.")
            return

        print(description)

        # # Step 2: Generate code based on the image description
        # code = self.client.design_code_for_img(description)
        # if not code:
        #     print("Failed to generate code.")
        #     return

if __name__ == "__main__":
    runner = Runner()
    runner.run()