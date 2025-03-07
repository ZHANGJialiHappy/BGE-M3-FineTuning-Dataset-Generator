import random

def truncate_id(alarm_id):
    if not isinstance(alarm_id, list):
        alarm_id = alarm_id.split(', ')
    if len(alarm_id) > 3:
        alarm_id = alarm_id[:3]
    return ', '.join(alarm_id)

def format_pos(alarm):
    alarm_id = alarm.get('id', '')
    data_tree_path = alarm.get('data_tree_path', '')
    description = alarm.get('long_description', '')
    cause = alarm.get('cause', '')
    effect = alarm.get('effect', '')
    suggested_action = alarm.get('suggested_action', '')

    formatted_pos = f"""
Alarm {alarm_id}
====================================

{data_tree_path}

Description
-----------

{description}

Cause
-----

{cause}

Effect
------

{effect}

Suggested actions
-----------------

{suggested_action}
"""
    return formatted_pos.strip()

def generate_neg_samples(alarm_data, current_alarm, random_nr=15):
    all_alarms = [format_pos(a) for a in alarm_data.get('alarms', []) if a != current_alarm]
    return random.sample(all_alarms, min(random_nr, len(all_alarms)))

def generate_random_neg_samples(alarms, current_index, random_nr1=8, random_nr2=7):
    neg1 = [format_pos(alarms[i]) for i in random.sample(range(0, current_index), random_nr1)]
    neg2 = [format_pos(alarms[i]) for i in random.sample(range(current_index+1, len(alarms)), random_nr2)]
    return neg1 + neg2

if __name__ == "__main__":

    # alarm_list=["PVCU1-STermEn1", "PVCU2-STermEn2","PVCU3-STermEn3", "PVCU1-STermEn4", "PVCU2-STermEn56","PVCU3-STermEn7", "PVCU1-STermEn78", "PVCU2-STermEn9","PVCU3-STermEn10", "PVCU1-STermEn11", "PVCU2-ST12"]
    # alarm_string="EGRCU-SInvParm, EGRI1-SInvParm, EGRI2-SInvParm, EGRI3-SInvParm, SCRCU-SInvParm, SCRI1-SInvParm, SCRI2-SInvParm"

    # print(truncate_id(alarm_list))
    # print(truncate_id(alarm_string))
    alarm={
            "id": "EGRCU-SWDogDact",
            "synopsis": "Watchdogs deactivated",
            "data_tree_path": "EGRCU->System->Watchdogs deactivated",
            "long_description": "EGRCU watchdog disabled.",
            "cause": "Orange DIP-switch is set to 'Off'.",
            "effect": "No effect on engine performance. The EGRCU Controller may respond incorrectly to any software and hardware failures.",
            "suggested_action": "Set orange DIP-switch to 'On'."
        }
    print(format_pos(alarm))