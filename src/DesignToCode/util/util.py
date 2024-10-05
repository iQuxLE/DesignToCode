import logging
import re
from pathlib import Path
from typing import Dict


def parse_new_and_compared_description_seperately(new_and_compared_description: Dict) -> tuple[str, str]:
    new_description = ""
    comparison_of_descriptions = ""
    if isinstance(new_and_compared_description, Dict):
        for k, _ in new_and_compared_description.items():
            new_description = k["new_description"]
            comparison_of_descriptions = k["comparison_of_old_and_new_description"]
    else:
        raise ValueError("Output format of previous response is not JSON")

    return new_description, comparison_of_descriptions


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

def convertapi_call(
        convertapi,
        html_file_path,
        out_filename,
        image_output_directory: str = "/Users/carlo/PycharmProjects/DesignToCode/src/DesignToCode/output"
):
    convertapi.api_credentials = 'secret_xsDD6o46ZhquOH5H'
    convertapi.convert('png', {
        'File': f'{html_file_path}',
        'FileName': f'{out_filename}',
        'ConversionDelay': '3',
        'Version': '126'
    }, from_format='html').save_files(image_output_directory)

    full_image_file_output_path = image_output_directory + "/" + out_filename
    return full_image_file_output_path

