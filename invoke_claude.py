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

def generate_query(content):
    prompt = f"""
    Generate a question related to the following content. Only provide the question without any additional text.

    Content:
    {content}
    """
    
    return invoke_claude_3_with_text(prompt)
