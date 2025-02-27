import boto3
import json
from queries import get_query_pos_embedding_nth
from generate_negs import execute_query


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

def filter_data(data):
    prompt = f"""
    I have a list of strings. In this list, there are some garbage strings. 
    Please filter out the garbage string, don't change the string. 
    At last it only returns the cleaned string list in the format ['str', 'str')].

    Only return one cleaned list without any additional text.
    
    Example of provided data: 
    [ 
    '
        Emergency operation

        1. <a href="index.html">9836048</a>
        2. <a href="936084363.html">TCR16 0287-2</a>
        3. <a href="936178443.html">Installation/maintenance instructions</a>
        4. Emergency operation

        | Emergency operation | ID |
        | --- | --- |
        | <a href="55644222731.html"></a><a href="C2 0287 500.11-01.html"></a><a href="../../Torm" target="_blank"></a> | <a href="55644222731.html"></a><a href="C2 0287 500.11-01.html">C2 0287 500.11-01</a> |

        Emergency operation
        ===================

        Copyright © 2023 MAN Energy Solutions

        <a class="schema-navbar-brand" href="index.html"><img class="schema-navbar-logo" src="../assets/img/MAN_pm_pos_rgb_300.png"/></a>


        * <a href="index.html">Home</a>
        * Language
        * <a href="936181131.html">english</a>

        * <a href="index.html">Home</a>
        ', 
    '

        <a href="index.html">9836048</a>
        <a href="936084363.html">TCR16 0287-2</a>
        <a href="936178443.html">Installation/maintenance instructions</a>
        4. <a href="936193803.html">Installation and maintenance</a>
        5. <a href="C2 0287 500.41-04.html">C2 0287 500.41-04</a>

        ### 

        Copyright © 2023 MAN Energy Solutions

        <a class="schema-navbar-brand" href="index.html"><img class="schema-navbar-logo" src="../assets/img/MAN_pm_pos_rgb_300.png"/></a>

        * <a href="index.html">Home</a>
        * Language
        * <a href="4336454283.html">english</a>
        * <a href="index.html">Home</a>
    ']
    
    example of filtered data:
    [ 
    '
        Emergency operation

        1. <a href="index.html">9836048</a>
        2. <a href="936084363.html">TCR16 0287-2</a>
        3. <a href="936178443.html">Installation/maintenance instructions</a>
        4. Emergency operation

        | Emergency operation | ID |
        | --- | --- |
        | <a href="55644222731.html"></a><a href="C2 0287 500.11-01.html"></a><a href="../../Torm" target="_blank"></a> | <a href="55644222731.html"></a><a href="C2 0287 500.11-01.html">C2 0287 500.11-01</a> |

        Emergency operation
        ===================

        Copyright © 2023 MAN Energy Solutions

        <a class="schema-navbar-brand" href="index.html"><img class="schema-navbar-logo" src="../assets/img/MAN_pm_pos_rgb_300.png"/></a>


        * <a href="index.html">Home</a>
        * Language
        * <a href="936181131.html">english</a>

        * <a href="index.html">Home</a>
        '
    ]

    The characteristic of garbage strings is that there are not many words after a series of ordered lists, often only ### before "Copyright © 2023 MAN Energy Solutions".

    Provided data:
    {data}
    """
    
    return invoke_claude_3_with_text(prompt)

if __name__ == "__main__":
#     guide_book_content = """
# \ufeffPrepare for descaling\n\n1. <a href="index.html">Default title</a>\n2. <a href="75137745931.html"><p>4208001-1<sub></sub></p></a>\n3. <a href="75139298315.html"><p>Cooling Water System</p></a>\n4. <a href="75139312139.html"><p>Description</p></a>\n5. <a href="5045-0200-0002.html">5045-0200-0002</a>\n6. <a href="7417734539.html"><p>Cleaning and Inhibiting Procedure</p></a>\n7. <a href="7417790347.html"><p>Descaling</p></a>\n8. Prepare for descaling\n\n### Prepare for descaling\n\nFill up with clean tap water.  \nHeat the water to a maximum of 70°C, and circulate it continuously.  \n  \n NOTICE Some ready-mixed cleaning agents are specified to be used at a lower temperature. This 
# maximum temperature must be adhered to.\n\nCopyright © 2024 MAN Energy Solutions\n\n<a class="schema-navbar-brand" href="index.html"><img class="schema-navbar-logo" src="../assets/img/MAN_pm_pos_rgb_300.png"/></a>\n\n\n* <a href="index.html">Home</a>\n* Language\n* <a href="../en-GB/7417799307.html">english</a>\n\n* <a href="index.html">Home</a>
#     """
    
#     query = generate_query(guide_book_content)
#     print(query)

    result = execute_query(get_query_pos_embedding_nth(1))
    embedding_texts = [item[1] for item in result]
    filtered_data = filter_data(embedding_texts)
    print(filtered_data)



###
