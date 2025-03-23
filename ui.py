import webview
import argparse
import json
import base64

def generate_html(changes):
    code_block_template = """
    <div class="code_block">
        <h3>{filename}</h3>
        <div class="container">
            <div class="actual_code"><pre>{actual_code}</pre></div>
            <div class="modified_code"><pre>{modification}</pre></div>
        </div>
    </div>
    """
    
    code_blocks = "".join([
        code_block_template.format(
            filename=change.get("filename", "Untitled"),
            actual_code=change["actual_code"],
            modification=change["modification"]
        ) for change in changes
    ])
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Code Comparison</title>
        <style>
            .container{{
                display: flex;
                flex-direction: row;
                justify-content: space-around;
            }}
            .main_container{{
                display: flex;
                flex-direction: column;
            }}
            h1, h3{{
                text-align: center;
            }}
            .code_block{{
                margin-bottom: 4rem;
                border: 1px solid #ccc;
                padding: 10px;
                border-radius: 5px;
                background: #f9f9f9;
            }}
            pre{{
                white-space: pre-wrap;
                word-wrap: break-word;
                background: #eee;
                padding: 10px;
                border-radius: 5px;
            }}
        </style>
    </head>
    <body>
        <h1>Changes</h1>
        <div class="main_container">
            {code_blocks}
        </div>
    </body>
    </html>
    """
    return html_content

def main():
    parser = argparse.ArgumentParser(description="Render code changes in a webview.")
    parser.add_argument("--files", type=str, help="Base64-encoded JSON list of file changes")
    args = parser.parse_args()

    # Decode the Base64 input
    try:
        decoded_json = base64.b64decode(args.files).decode("utf-8")
        changes = json.loads(decoded_json)
    except Exception as e:
        print(f"Error decoding input: {e}")
        return

    html_output = generate_html(changes)
    webview.create_window("Code Comparison", html=html_output)
    webview.start()

if __name__ == "__main__":
    main()
