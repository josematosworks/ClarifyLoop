import os
import logging

def save_updated_requirements_file(base_file_path, content):
    version = 1
    base, ext = os.path.splitext(base_file_path)
    while os.path.exists(f"{base}_v{version}{ext}"):
        version += 1
    new_file_path = f"{base}_v{version}{ext}"
    with open(new_file_path, 'w') as file:
        file.write(content)
    logging.info(f"Updated requirements saved to {new_file_path}")
    return new_file_path
