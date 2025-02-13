import boto3
import json

def invoke_claude_3_with_text(prompt):

    client = boto3.client(
        service_name="bedrock-runtime",
        region_name="us-east-1",
    )

    model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    
    response = client.invoke_model(
        modelId=model_id,
        body=json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "temperature": 0,
                "max_tokens": 3500,
                "stop_sequences": ["Human:", "\n\nHuman:", "</Answer>", "\n</Answer>"],
                "system": "give me your name",
                "messages": [
                    {
                        "role": "user",
                        "content": [{"type": "text", "text": prompt}],
                    },
                    {
                        "role": "assistant",
                        "content": [{"type": "text", "text": "<Answer>"}],
                    },
                ],
            }
        ),
    )

    result = json.loads(response.get("body").read())
    output_list = result.get("content", [])

    # return output_list[0]["text"]
    return output_list[0]["text"] if output_list else {}

def generate_jsonl_data(content):
    prompt = f"""
    Based on the provided content, generate a question related to this content.
    
    
    Guide Book Content:
    {content}
    """
    # give an exmple
    # convert html to chapter
    
    return invoke_claude_3_with_text(prompt)

if __name__ == "__main__":
    guide_book_content = """
\ufeffPrepare for descaling\n\n1. <a href="index.html">Default title</a>\n2. <a href="75137745931.html"><p>4208001-1<sub></sub></p></a>\n3. <a href="75139298315.html"><p>Cooling Water System</p></a>\n4. <a href="75139312139.html"><p>Description</p></a>\n5. <a href="5045-0200-0002.html">5045-0200-0002</a>\n6. <a href="7417734539.html"><p>Cleaning and Inhibiting Procedure</p></a>\n7. <a href="7417790347.html"><p>Descaling</p></a>\n8. Prepare for descaling\n\n### Prepare for descaling\n\nFill up with clean tap water.  \nHeat the water to a maximum of 70°C, and circulate it continuously.  \n  \n NOTICE Some ready-mixed cleaning agents are specified to be used at a lower temperature. This 
maximum temperature must be adhered to.\n\nCopyright © 2024 MAN Energy Solutions\n\n<a class="schema-navbar-brand" href="index.html"><img class="schema-navbar-logo" src="../assets/img/MAN_pm_pos_rgb_300.png"/></a>\n\n\n* <a href="index.html">Home</a>\n* Language\n* <a href="../en-GB/7417799307.html">english</a>\n\n* <a href="index.html">Home</a>
    """
    
    jsonl_data = generate_jsonl_data(guide_book_content)
    print(jsonl_data)
