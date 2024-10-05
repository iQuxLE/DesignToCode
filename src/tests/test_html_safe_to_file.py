from DesignToCode.client.mistral_client import MistralImageToCodeClient

text_with_html = """
                ```html
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>Sample HTML</title>
                </head>
                <body>
                    <h1>Hello, World!</h1>
                </body>
                </html>
                ```
                 """

def test_safe_to_html_file():
    client = MistralImageToCodeClient(api_key=None)
    html_code, path = client.save_generate_code_to_html(text_with_html)
    print("html code = ",html_code)
    print("path = ",path)