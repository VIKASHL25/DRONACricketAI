from services.groq_service import generate_strategy

def coach_agent(context, win_probability):
    prompt=f"""
    Match Situation:
    {context}

    Simulated Win Probability: {win_probability}

    Recommend optimal field placement and bowling strategy.
    """

    return generate_strategy(prompt)
