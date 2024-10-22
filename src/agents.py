from swarm import Agent

def read_requirements(file_path):
    """
    Reads the contents of the specified requirements file.

    Args:
        file_path (str): The path to the requirements file.

    Returns:
        str: The contents of the file.
    """
    with open(file_path, 'r') as file:
        return file.read()

# Updated Reader Agent with more detailed instructions
reader_agent = Agent(
    name="Reader Agent",
    instructions=(
        "You are responsible for reading and analyzing the contents of the provided requirements file. "
        "Your goal is to extract high-level requirements that outline the key objectives, deliverables, "
        "and any other important details mentioned in the document. The extracted requirements should be "
        "concise but cover all major points that stakeholders should be aware of to proceed with further "
        "clarifications or implementation."
    ),
    functions=[read_requirements],  # This agent uses the `read_requirements` function to read the file
)

# Updated Clarification Agent with more detailed instructions
clarification_agent = Agent(
    name="Clarification Agent",
    instructions=(
        "You are tasked with identifying any ambiguous or unclear requirements that need clarification. "
        "For each ambiguous requirement, generate a precise question to clarify it. In addition, provide "
        "multiple-choice answers or suggestions to resolve the ambiguity. The answers should be direct solutions, "
        "not additional questions, to ensure the requirement becomes clear and actionable after this step. "
        "Your objective is to eliminate any vagueness or uncertainty in the requirements, ensuring they can be "
        "implemented with confidence."
    ),
)

# IEEE 830 Compliant Requirements Writer Agent
ieee_830_agent = Agent(
    name="IEEE 830 Requirements Writer",
    instructions=(
        "You are an expert in writing software requirements specifications that adhere to the IEEE 830 standard. "
        "Your task is to take the clarified requirements and structure them into a comprehensive, well-organized "
        "document that follows the IEEE 830 standard. This includes:\n"
        "1. Introduction (purpose, scope, definitions, references, overview)\n"
        "2. Overall description (product perspective, product functions, user characteristics, constraints, assumptions and dependencies)\n"
        "3. Specific requirements (external interfaces, functions, performance requirements, logical database requirements, design constraints, software system attributes)\n"
        "4. Appendices (as needed)\n\n"
        "Ensure that each requirement is:\n"
        "- Correct\n"
        "- Unambiguous\n"
        "- Complete\n"
        "- Consistent\n"
        "- Ranked for importance and/or stability\n"
        "- Verifiable\n"
        "- Modifiable\n"
        "- Traceable\n\n"
        "Organize the requirements in a hierarchical manner and use consistent terminology throughout the document."
    ),
)
