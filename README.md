# ClarifyLoop

ClarifyLoop is an intelligent requirements clarification and documentation tool that helps transform initial project requirements into a comprehensive, IEEE 830 compliant software requirements specification.

## Features

- Automated reading and extraction of high-level requirements from an initial requirements file
- Interactive clarification process to resolve ambiguities and gather additional details
- Generation of a detailed, structured requirements document
- Conversion of requirements into an IEEE 830 compliant specification
- Logging of all steps and outputs for transparency and traceability

## How It Works

1. **Initial Requirements Reading**: The tool reads an initial requirements file (`requirements.txt`) containing basic project requirements.

2. **High-Level Requirements Extraction**: A Reader Agent extracts and summarizes the high-level requirements from the initial file.

3. **Clarification Loop**: 
   - A Clarification Agent identifies ambiguities and generates specific questions with multiple-choice options.
   - Users interactively respond to these questions, providing clarifications.
   - The process repeats until all ambiguities are resolved or a maximum number of loops is reached.

4. **Final Requirements Generation**: Based on the initial requirements and all clarifications, a detailed final requirements document is generated.

5. **IEEE 830 Compliant Document**: The final requirements are transformed into an IEEE 830 compliant software requirements specification document.

6. **Output**: The tool produces several output files, including:
   - Logs of each step in the process
   - The extracted high-level requirements
   - Clarification questions and answers
   - Updated requirements after each clarification loop
   - The final detailed requirements
   - The IEEE 830 compliant requirements specification

## Usage

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ClarifyLoop.git
   cd ClarifyLoop
   ```
   Don't forget to star the repo if you find it useful! ⭐

2. Set up the OpenAI API key as an environment variable:

   - **Linux or macOS**:
     ```
     export OPENAI_API_KEY=your_api_key_here
     ```

   - **Windows (Command Prompt)**:
     ```
     set OPENAI_API_KEY=your_api_key_here
     ```

   - **Windows (PowerShell)**:
     ```
     $env:OPENAI_API_KEY = "your_api_key_here"
     ```

   Replace `your_api_key_here` with your actual OpenAI API key.

   Note: To make this setting permanent, you can add the export/set command to your shell's configuration file (e.g., `~/.bashrc`, `~/.zshrc`, or create a `.env` file in the project root).

3. Prepare an initial `requirements.txt` file with basic project requirements.

4. Run the main script:
   ```
   python src/main.py
   ```

5. Follow the prompts to provide clarifications as needed.

6. Review the generated output files in the `agent_outputs` directory and the final IEEE 830 compliant specification.

Note: Ensure that you have set the OPENAI_API_KEY environment variable before running the script. The software requires this key to function properly.

## Dependencies

- Python 3.x
- `openai/swarm` library for agent interactions
- Logging and file manipulation utilities

## File Structure

- `src/`
  - `main.py`: Main script orchestrating the entire process
  - `agents.py`: Definitions for Reader, Clarification, and IEEE 830 agents
  - `utils.py`: Utility functions for logging and file operations
  - `clarification.py`: Functions for handling the clarification process
  - `file_utils.py`: Utilities for file manipulation

## Note

This tool is designed to assist in the requirements gathering and documentation process. It aims to produce a comprehensive and well-structured requirements document, but human review and expertise are still crucial for ensuring the final document meets all project-specific needs.
