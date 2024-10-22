from agents import reader_agent 

def ask_clarification_question(question, options=None):
    print(f"\nClarification needed: {question}")
    if options:
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
    while True:
        answer = input("Please choose an option number or provide your own answer: ").strip()
        if options and answer.isdigit() and 1 <= int(answer) <= len(options):
            return options[int(answer) - 1]
        elif answer:
            return answer
        else:
            print("Invalid input. Please try again.")

def parse_clarification_response(response):
    if "No further clarification needed" in response:
        return []

    questions = []
    lines = response.strip().split('\n')
    current_question = None
    options = []

    for line in lines:
        line = line.strip()
        if line.startswith("Question"):
            if current_question:
                questions.append((current_question, options))
                options = []
            current_question = line.split(":", 1)[-1].strip()
        elif line and (line[0].isdigit() and (line[1] == '.' or line[1] == ')')):
            option = line.split('.', 1)[-1].strip() if '.' in line else line.split(')', 1)[-1].strip()
            options.append(option)
    if current_question:
        questions.append((current_question, options))
    return questions

def update_requirements_content(client, content, clarifications):
    # Prepare the prompt for the agent
    clarification_text = "\n\n".join(
        [f"Question: {q}\nAnswer: {a}" for q, a in clarifications]
    )
    prompt = f"""Based on the current requirements and the new clarifications provided, 
    generate an updated version of the requirements document. 
    Incorporate all the clarifications into the appropriate sections of the requirements.

    Current Requirements:
    {content}

    New Clarifications:
    {clarification_text}

    Please provide a well-structured, updated requirements document that incorporates this new information.
    """

    # Call the reader_agent to generate updated requirements
    response = client.run(
        agent=reader_agent,
        messages=[{"role": "user", "content": prompt}],
    )

    # Return the updated requirements
    return response.messages[-1]["content"]
