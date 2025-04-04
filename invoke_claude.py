import boto3
import json
from queries import get_query_pos_embedding_nth
from generate_negs import execute_query
import csv
from urllib.parse import unquote


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

def generate_query_for_alarm(content):
    prompt = f"""
    I will provide you with some content. The first line of the content always starts with "Alarm" followed by an alarm_id. 

    Your task is to generate a question that includes the alarm_id and is directly related to the content provided. 
    Do not include any additional text or explanations, only return the question.

    Content:
    {content}
    """
    
    return invoke_claude_3_with_text(prompt)

if __name__ == "__main__":
    with open("alarm_id_source.csv", mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        # 打开目标文件以追加内容
        with open("alarm_test_dataset.csv", mode='a', encoding='utf-8', newline='') as output_file:
            fieldnames = ["query", "source_uri"]
            csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            
            # 检查文件是否为空，如果为空则写入表头
            output_file.seek(0, 2)  # 移动到文件末尾
            if output_file.tell() == 0:
                csv_writer.writeheader()
            
            # 逐行处理输入文件
            for row in csv_reader:
                source_uri = f"['{unquote(row['source_uri']).split('/')[-1]}']"
                content = row["embedding_text"]
                query = generate_query_for_alarm(content)
                
                # 确保 query 和 source_uri 格式正确
                query = query.strip().replace("\n", " ").replace('"', "'")
                source_uri = source_uri.strip().replace("\n", " ")
                
                # 写入到目标文件
                csv_writer.writerow({"query": query, "source_uri": source_uri})
            


