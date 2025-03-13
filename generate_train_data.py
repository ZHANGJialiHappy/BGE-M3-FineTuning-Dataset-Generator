import json
import os
from data_utils import get_clean_data, compute_sorted_distance_indices # add new
from invoke_claude import generate_query
from generate_negs import get_100_random_embeddings_text_by_cosine
from alarm_utils import truncate_id, format_pos, generate_random_neg_samples
from tqdm import tqdm


uuid1_data='uuid1_data/data-1741610373529.csv'
uuid1_garbage_embedding='uuid1_data/garbage_embedding.csv'
clean_data = get_clean_data(uuid1_data, uuid1_garbage_embedding, 2500)
sorted_indices=compute_sorted_distance_indices(clean_data) # add new

def generate_dataset():
    with open("dataset.jsonl", 'w', encoding='utf-8') as f:
        for current_index, (_, _, embedding_text, _) in tqdm(enumerate(clean_data), total=len(clean_data)):
            query = generate_query(embedding_text)
            pos = [embedding_text]
            neg = get_100_random_embeddings_text_by_cosine(current_index, clean_data, sorted_indices)
            
            data = {
                "query": query,
                "pos": pos,
                "neg": neg
            }
            
            f.write(json.dumps(data) + '\n')

        file_path = os.path.join('alarm_data', 'ERCS_AlarmDescription.en.txt_mk2.json')
        with open(file_path, 'r', encoding='utf-8') as alarm_f:
            alarms = json.load(alarm_f).get('alarms', [])

            for i, alarm in enumerate(alarms):
                if 30 <= i < 680: 
                    query = truncate_id(alarm['id'])      # EGRCU-SWDogDact quetion nr. 1
                    pos = [format_pos(alarm)] # ？其它文件也有相同的alarm，并且有不同的suggested_action
                    neg =  generate_random_neg_samples(alarms, i)          
                    data = {
                        "query": query,
                        "pos": pos,
                        "neg": neg
                    }
                    
                    f.write(json.dumps(data) + '\n')

        file_path = os.path.join('alarm_data', 'ME_AlarmDescription.en.txt_egen3.json')
        with open(file_path, 'r', encoding='utf-8') as alarm_f:
            alarms = json.load(alarm_f).get('alarms', [])

            for i, alarm in enumerate(alarms):
                
                if 30 <= i < 7000:

                    if i < 2000:            
                        query = f"How do I troubleshoot {truncate_id(alarm['id'])}?" # quetion nr.2

                    elif 2000 <= i < 3500:            
                        query = f"What causes this alarm {truncate_id(alarm['id'])}?" # quetion nr.3
        
                    elif 3500 <= i < 5000:            
                        query = f"What are the effects of the {truncate_id(alarm['id'])} alarm on the system?" # quetion nr.4
            
                    else:            
                        query = f"What operational issues can arise due to the {truncate_id(alarm['id'])} alarm?" # quetion nr. 9
                    
                    pos = [format_pos(alarm)] 
                    neg =  generate_random_neg_samples(alarms, i)   

                    data = {
                        "query": query,
                        "pos": pos,
                        "neg": neg
                    }
                    
                    f.write(json.dumps(data) + '\n')

        file_path = os.path.join('alarm_data', 'ME_AlarmDescription.en.txt_mk2.json')
        with open(file_path, 'r', encoding='utf-8') as alarm_f:
            alarms = json.load(alarm_f).get('alarms', [])

            for i, alarm in enumerate(alarms):
                
                if 30 <= i < 2300:
                    if i < 1500:            
                        query = f"What are the common troubleshooting steps for {truncate_id(alarm['id'])}?" # quetion nr.5
            
                    else:            
                        query = f"What are the potential causes of the {truncate_id(alarm['id'])} alarm?" # quetion nr.6
                    
                    pos = [format_pos(alarm)] 
                    neg =  generate_random_neg_samples(alarms, i)    

                    data = {
                        "query": query,
                        "pos": pos,
                        "neg": neg
                    }
                    
                    f.write(json.dumps(data) + '\n')

        file_path = os.path.join('alarm_data', 'ME-B_AlarmDescription.en.txt_mk2.json')
        with open(file_path, 'r', encoding='utf-8') as alarm_f:
            alarms = json.load(alarm_f).get('alarms', [])

            for i, alarm in enumerate(alarms):
                
                if 30 <= i < 1500:
                    if i < 700:            
                        query = f"What are the recommended maintenance procedures for systems with {truncate_id(alarm['id'])} alarms?" # quetion nr.7
            
                    else:            
                        query = f"Are there any known issues related to {truncate_id(alarm['id'])}?" # quetion nr.8
                    
                    pos = [format_pos(alarm)] 
                    neg =  generate_random_neg_samples(alarms, i)    

                    data = {
                        "query": query,
                        "pos": pos,
                        "neg": neg
                    }
                    
                    f.write(json.dumps(data) + '\n')

        file_path = os.path.join('alarm_data', 'PVU-CS-SW_AlarmDescription.en.txt_egen3.json')
        with open(file_path, 'r', encoding='utf-8') as alarm_f:
            alarms = json.load(alarm_f).get('alarms', [])

            for i, alarm in enumerate(alarms):
                
                if 30 <= i < 870:
                    query = f"What are the suggested actions to resolve the {truncate_id(alarm['id'])} alarm?"  # quetion nr. 10
                    pos = [format_pos(alarm)] 
                    neg =  generate_random_neg_samples(alarms, i) 

                    data = {
                        "query": query,
                        "pos": pos,
                        "neg": neg
                    }
                    
                    f.write(json.dumps(data) + '\n')

if __name__ == "__main__":
    generate_dataset()
        