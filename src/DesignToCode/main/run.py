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

        # INITIALISE FIRST IMAGE DESCRIPTION AND INITIAL CODE
        initial_description, initial_code, image_path = client.initialise_html_code(
                initial_encoded_img=base64image,
                figma_json_context=json
            )

        # ENCODE THE NEW IMAGE
        new_encodedbase64_image = image_encoder.encode_base64(image_path=image_path)

        # START MANUAL ITERATIVE IMPROVEMENT
        updated_description, updated_comparison, updated_code, updated_image_path = client.iterate_and_improve(
            initial_encoded_image=base64image,
            new_encoded_image=new_encodedbase64_image,
            initial_description=initial_description,
            figma_json_context=json,
            initial_code=initial_code,
        )


        new_encodedbase64_image = image_encoder.encode_base64(image_path=updated_image_path)


        updated_description, updated_comparison, updated_code, updated_image_path = client.iterate_and_improve(
            initial_encoded_image=base64image,
            new_encoded_image=new_encodedbase64_image,
            initial_description=initial_description,
            figma_json_context=json,
            initial_code=initial_code,
            updated_code=updated_code,
            out="3_iterative_pmg_from_html"
        )

        new_encodedbase64_image = image_encoder.encode_base64(image_path=updated_image_path)


        updated_description, updated_comparison, updated_code, updated_image_path = client.iterate_and_improve(
            initial_encoded_image=base64image,
            new_encoded_image=new_encodedbase64_image,
            initial_description=initial_description,
            figma_json_context=json,
            initial_code=initial_code,
            updated_code=updated_code,
            out="4_iterative_pmg_from_html"
        )

        new_encodedbase64_image = image_encoder.encode_base64(image_path=updated_image_path)

        updated_description, updated_comparison, updated_code, updated_image_path = client.iterate_and_improve(
            initial_encoded_image=base64image,
            new_encoded_image=new_encodedbase64_image,
            initial_description=initial_description,
            figma_json_context=json,
            initial_code=initial_code,
            updated_code=updated_code,
            out="5_iterative_pmg_from_html"
        )



if __name__ == "__main__":
    runner = Runner()
    runner.run()