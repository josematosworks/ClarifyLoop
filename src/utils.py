import logging
import os
import shutil
from datetime import datetime

def setup_logging(log_dir='logs'):
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_filename = f'swarm_{timestamp}.log'
    logging.basicConfig(
        filename=os.path.join(log_dir, log_filename),
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return log_filename

def clean_agent_outputs(output_dir="agent_outputs"):
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

def log_agent_action(agent_name, action, result=None):
    separator = "-" * 120  
    logging.info(separator)  
    logging.info(f"{agent_name} - Action: {action}")
    if result:
        logging.info(f"{agent_name} - Result: {result}")  
    logging.info(separator)  

def log_agent_output(agent_name, output, step_number, filename=None, output_dir="agent_outputs"):
    os.makedirs(output_dir, exist_ok=True)
    if filename is None:
        filename = f"{step_number:03d}_{agent_name.replace(' ', '_').lower()}_output.txt"
    file_path = os.path.join(output_dir, filename)
    with open(file_path, 'w') as file:
        file.write(output)
    logging.info(f"Logged {agent_name} output to {file_path}")
