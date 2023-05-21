import json
import re

def process_json(json_obj):
    for key, value in json_obj.items():
        if isinstance(value, list):
            json_obj[key] = [process_string(item) for item in value]
        elif isinstance(value, dict):
            json_obj[key] = process_json(value)
    
    return json_obj

def process_string(text):
    return re.sub(r'\\u[0-9a-fA-F]{4}', '', text.replace('\r', '').replace('\t', '').replace('\n', ''))

# Save output to file
def save_to_file(output_path, json_data_store):
  with open(output_path, 'w') as outfile:
    json.dump(json_data_store, outfile, indent=4, ensure_ascii=False)


if __name__ == "__main__":


  input_file_path='datasets/CaliforniaGraph/CaliforniaGraph_crawling.json'
  output_file_path='datasets/CaliforniaGraph/CaliforniaGraph_crawling_processed.json'
  # Assuming you have your JSON stored in a file called 'data.json'
  with open(input_file_path) as file:
    json_data = json.load(file)

  processed_data = process_json(json_data)

  save_to_file(output_file_path, processed_data)
  