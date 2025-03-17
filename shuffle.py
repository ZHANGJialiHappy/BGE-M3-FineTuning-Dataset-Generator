import random

def shuffle_json_lines(input_file: str, output_file: str):
    # 读取文件内容
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 打乱顺序
    random.shuffle(lines)
    
    # 将打乱顺序后的内容写回文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)

if __name__ == "__main__":
    input_file = 'train_dataset/dataset.jsonl'
    output_file = 'train_dataset/shuffled_dataset.jsonl'
    shuffle_json_lines(input_file, output_file)