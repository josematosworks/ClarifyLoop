import logging
import os
from swarm import Swarm
from agents import reader_agent, clarification_agent, ieee_830_agent
from utils import (
    setup_logging,
    clean_agent_outputs,
    log_agent_action,
    log_agent_output,
)
from clarification import (
    ask_clarification_question,
    parse_clarification_response,
    update_requirements_content,
)
from file_utils import save_updated_requirements_file

def start_planning_process(client, context_variables):
    """
    Starts the planning process by running the Reader Agent to extract high-level requirements from a file.

    Args:
        client (Swarm): The swarm client to execute the agent.
        context_variables (dict): Context information that includes the file path for the requirements file.

    Returns:
        dict: The updated context with high-level requirements extracted.
    """
    logging.info("Starting the planning process")
    file_path = context_variables["initial_requirements_file_path"]

    # Log and run the Reader Agent to extract high-level requirements from the file
    log_agent_action("Reader Agent", "Reading requirements file")
    response = client.run(
        agent=reader_agent,
        messages=[
            {
                "role": "user",
                "content": f"Please read the requirements from {file_path} and extract high-level requirements."
            }
        ],
        context_variables=context_variables,
    )
    log_agent_action(
        "Reader Agent",
        "Extracted high-level requirements",
        response.messages[-1]["content"]
    )

    # Store the extracted high-level requirements in the context
    response.context_variables["high_level_requirements"] = response.messages[-1]["content"]
    return response

def get_clarification_questions(client, agent, current_requirements, previous_clarifications):
    """
    Identifies ambiguities in the high-level requirements and generates clarification questions.

    Args:
        client (Swarm): The swarm client to execute the agent.
        agent (Agent): The agent responsible for generating clarification questions.
        current_requirements (str): The current version of the requirements to be clarified.
        previous_clarifications (list): A list of previously answered clarification questions.

    Returns:
        str: The agent's response with new clarification questions.
    """
    # Combine current requirements with previous clarifications to avoid redundancy
    if previous_clarifications:
        clarification_text = "\n\n".join(
            [f"Question: {q}\nAnswer: {a}" for q, a in previous_clarifications]
        )
        combined_requirements = f"{current_requirements}\n\nPrevious Clarifications:\n{clarification_text}"
    else:
        combined_requirements = current_requirements

    # Generate a prompt for the Clarification Agent to identify ambiguities
    message = f"""Please identify all ambiguous or vague requirements that need clarification.
Provide clear questions and possible options for clarification for each one.
Ensure your response is strictly formatted as follows, with no additional text:

Question 1: [Your question here]
1. [Option 1]
2. [Option 2]
3. [Option 3]

... and so on.

Do not include any introductions, explanations, or closing remarks.

Current requirements:
{combined_requirements}"""
    
    # Run the Clarification Agent to generate questions
    response = client.run(
        agent=agent,
        messages=[{"role": "user", "content": message}],
    )
    return response.messages[-1]["content"]

def generate_final_requirements(client, initial_requirements, clarifications):
    """
    Generates a final detailed requirements document based on initial requirements and clarifications.

    Args:
        client (Swarm): The swarm client to execute the agent.
        initial_requirements (str): The initial requirements text.
        clarifications (list): List of tuples containing questions and answers from the clarification process.

    Returns:
        str: The final detailed requirements document.
    """
    clarification_text = "\n\n".join(
        [f"Question: {q}\nAnswer: {a}" for q, a in clarifications]
    )
    prompt = f"""Based on the initial requirements and the clarifications provided, 
    generate a comprehensive and detailed final requirements document. 
    Incorporate all the clarifications into the appropriate sections of the requirements.

    Initial Requirements:
    {initial_requirements}

    Clarifications:
    {clarification_text}

    Please provide a well-structured, detailed requirements document that incorporates all this information.
    """

    response = client.run(
        agent=reader_agent,  # Using the reader agent for this task
        messages=[{"role": "user", "content": prompt}],
    )
    return response.messages[-1]["content"]

def generate_ieee_830_requirements(client, final_requirements):
    """
    Generates an IEEE 830 compliant requirements document based on the final requirements.

    Args:
        client (Swarm): The swarm client to execute the agent.
        final_requirements (str): The final requirements text.

    Returns:
        str: The IEEE 830 compliant requirements document.
    """
    prompt = f"""Based on the final requirements provided, generate a comprehensive 
    IEEE 830 compliant software requirements specification document. 
    Ensure that the document follows the structure and guidelines of the IEEE 830 standard.

    Final Requirements:
    {final_requirements}

    Please provide a well-structured, detailed IEEE 830 compliant requirements document.
    """

    response = client.run(
        agent=ieee_830_agent,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.messages[-1]["content"]

def main():
    """
    Main function to orchestrate the reading, extraction, and clarification of requirements.
    Sets up logging, runs the Reader and Clarification Agents, and outputs results.
    """
    log_filename = setup_logging()
    clean_agent_outputs()

    client = Swarm()  # Initialize Swarm client

    # Context for the initial requirements file path
    initial_requirements_file_path = "requirements.txt"
    initial_context = {
        "session_id": "12345",
        "initial_requirements_file_path": initial_requirements_file_path,
        "next_agent": "Reader Agent"
    }

    step_counter = 1  # Initialize step counter for output file numbering

    # Read and log the original requirements file content
    with open(initial_requirements_file_path, 'r') as f:
        original_requirements_content = f.read()
    log_agent_output(
        "Original Requirements",
        original_requirements_content,
        step_counter,
        filename=f"{step_counter:03d}_original_requirements.txt"
    )
    step_counter += 1

    # Start the planning process and extract high-level requirements using the Reader Agent
    response = start_planning_process(client, initial_context)

    # Loop through agents to run the Reader Agent followed by Clarification Agent
    while response.context_variables.get("next_agent"):
        next_agent_name = response.context_variables["next_agent"]
        if next_agent_name == "Reader Agent":
            next_agent = reader_agent
        elif next_agent_name == "Clarification Agent":
            next_agent = clarification_agent
        else:
            logging.error(f"Agent {next_agent_name} not found")
            break

        logging.info(f"Calling {next_agent_name}")

        if next_agent_name == "Reader Agent":
            # Call the Reader Agent to extract high-level requirements
            log_agent_action(next_agent_name, "Reading requirements file")
            response = client.run(
                agent=next_agent,
                messages=[
                    {
                        "role": "user",
                        "content": f"Please read the requirements from {response.context_variables['initial_requirements_file_path']} and extract high-level requirements."
                    }
                ],
                context_variables=response.context_variables,
            )

            # Log and output the high-level requirements
            log_agent_action(
                next_agent_name,
                "Extracted high-level requirements",
                response.messages[-1]["content"]
            )
            log_agent_output(
                next_agent_name,
                response.messages[-1]["content"],
                step_counter,
                filename=f"{step_counter:03d}_high_level_requirements.txt"
            )
            step_counter += 1

            # Store high-level requirements in the context
            response.context_variables['high_level_requirements'] = response.messages[-1]['content']
            response.context_variables["next_agent"] = "Clarification Agent"

        elif next_agent_name == "Clarification Agent":
            # Call the Clarification Agent to clarify ambiguous requirements
            current_requirements = response.context_variables['high_level_requirements']
            clarifications = []
            previously_asked_questions = set()
            loop_count = 0
            max_loops = 10

            while loop_count < max_loops:
                loop_count += 1

                # Generate new clarification questions
                previous_clarifications = clarifications
                clarification_content = get_clarification_questions(
                    client, next_agent, current_requirements, previous_clarifications
                )
                log_agent_action(
                    next_agent_name,
                    "Identified clarification needs",
                    clarification_content
                )
                print(f"\nClarification content:\n{clarification_content}\n")
                logging.info(f"Clarification content: {clarification_content}")

                # Output the clarification questions
                log_agent_output(
                    next_agent_name,
                    clarification_content,
                    step_counter,
                    filename=f"{step_counter:03d}_clarification_loop_{loop_count}_questions.txt"
                )
                step_counter += 1

                # Parse and handle questions
                questions = parse_clarification_response(clarification_content)
                print(f"Parsed questions: {questions}")
                logging.info(f"Parsed questions: {questions}")

                if not questions:
                    print("No clarifications needed or unable to parse questions.")
                    logging.warning("No clarifications needed or unable to parse questions.")
                    break

                # Eliminate duplicate questions and store unique ones
                unique_questions = [
                    (q, opts) for q, opts in questions if q not in previously_asked_questions
                ]
                previously_asked_questions.update(q for q, _ in unique_questions)

                if not unique_questions:
                    print("No new clarifications needed.")
                    logging.info("No new clarifications needed.")
                    break

                num_questions = len(unique_questions)
                print(f"\nClarification Loop {loop_count} - {num_questions} question(s)")
                logging.info(f"Clarification Loop {loop_count} - {num_questions} question(s)")
                loop_clarifications = []

                # Ask user for clarification responses
                for idx, (question, options) in enumerate(unique_questions, 1):
                    user_clarification = ask_clarification_question(question, options)
                    loop_clarifications.append((question, user_clarification))
                    clarifications.append((question, user_clarification))

                # Update requirements with clarified content
                current_requirements = update_requirements_content(client, current_requirements, loop_clarifications)
                response.context_variables['high_level_requirements'] = current_requirements

                log_agent_output(
                    next_agent_name,
                    current_requirements,
                    step_counter,
                    filename=f"{step_counter:03d}_clarification_loop_{loop_count}_updated_high_level_requirements.md"
                )
                step_counter += 1

                log_agent_action(
                    next_agent_name,
                    "Updated requirements content with clarifications",
                    f"Questions answered in loop {loop_count}: {len(loop_clarifications)}"
                )

                # Prompt to continue with more clarifications
                if loop_count < max_loops:
                    continue_prompt = input("\nDo you want to continue with more clarifications? (yes/no): ").lower()
                    if continue_prompt != 'yes':
                        break

            # After the clarification loop ends
            final_requirements = generate_final_requirements(
                client, 
                original_requirements_content, 
                clarifications
            )

            # Output the final requirements
            log_agent_output(
                "Final Requirements",
                final_requirements,
                step_counter,
                filename=f"{step_counter:03d}_final_detailed_requirements.txt"
            )
            step_counter += 1

            # Save the final requirements to a new file
            version = 1
            while True:
                new_requirements_file = f"requirements_v{version}.txt"
                if not os.path.exists(new_requirements_file):
                    break
                version += 1

            # with open(new_requirements_file, 'w') as f:
            #     f.write(final_requirements)

            print(f"Final detailed requirements saved to {new_requirements_file}")
            logging.info(f"Final detailed requirements saved to {new_requirements_file}")

            # Generate IEEE 830 compliant requirements document
            ieee_830_requirements = generate_ieee_830_requirements(client, final_requirements)

            # Output the IEEE 830 compliant requirements
            log_agent_output(
                "IEEE 830 Requirements",
                ieee_830_requirements,
                step_counter,
                filename=f"{step_counter:03d}_requirements.txt"
            )
            step_counter += 1

            # Save the IEEE 830 compliant requirements to a new file
            ieee_830_file = f"requirements_v{version}.md"
            with open(ieee_830_file, 'w') as f:
                f.write(ieee_830_requirements)

            print(f"IEEE 830 compliant requirements saved to {ieee_830_file}")
            logging.info(f"IEEE 830 compliant requirements saved to {ieee_830_file}")

            response.context_variables["next_agent"] = None

    # Output final response from the agent
    if response.messages:
        print(response.messages[-1]["content"])
        logging.info(f"Final response: {response.messages[-1]['content']}")

if __name__ == "__main__":
    main()
