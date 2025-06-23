from jobber_client import get_jobber_data
from zapier_client import get_zapier_data
from validator import validate_and_correct
from sheet_writer import write_to_sheet
from notifier import notify_user

def merge_by_client(jobber_data, zapier_data):
    zapier_map = {entry.get('client_id'): entry for entry in zapier_data if 'client_id' in entry}
    merged = []
    for client in jobber_data:
        client_id = client.get('id')
        if not client_id:
            continue
        merged_entry = client.copy()
        if client_id in zapier_map:
            merged_entry.update(zapier_map[client_id])
        merged.append(merged_entry)
    return merged

def main():
    try:
        jobber_data = get_jobber_data()
        zapier_data = get_zapier_data()
        combined_data = merge_by_client(jobber_data, zapier_data)

        for client_entry in combined_data:
            is_valid, corrected_entry, error = validate_and_correct(client_entry)
            if is_valid:
                write_to_sheet(corrected_entry)
            else:
                notify_user(error, client_entry)

    except Exception as e:
        print("Unexpected error:", e)

if __name__ == "__main__":
    main()
