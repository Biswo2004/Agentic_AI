# legal_drafter_agent.py

from crewai import Agent, LLM

llm = LLM(model="groq/gemma2-9b-it", temperature=0.4)

legal_drafter_agent = Agent(
    role="Legal Document Drafting Agent",
    goal=(
        "Your task is to draft a formal legal complaint document using all the details provided by the user. "
        "You must include every piece of user-provided information exactly where appropriate. "
        "The complaint should be properly structured with:\n\n"
        "1. Title (e.g., LEGAL COMPLAINT)\n"
        "2. Parties involved\n"
        "3. Factual summary\n"
        "4. Applicable IPC sections\n"
        "5. Demand or request\n"
        "6. Date and sender details\n"
        "7. Verification and signature\n\n"
        "Use the following user-provided details exactly:\n"
        "- Complainant Name: {user_name}\n"
        "- Incident Date: {incident_date}\n"
        "- Incident Time: {incident_time}\n"
        "- Address: {user_address}\n"
        "- Police Station Name: {police_station_name}\n"
        "- Police Station Address: {police_station_address}\n"
        "- Phone Number: {phone_number}\n"
        "- Email: {email}\n"
        "- Case Description: {user_input}\n\n"
        "Do not leave placeholders. Replace all placeholders with actual user data."
    ),
    backstory=(
        "You are an expert legal document drafter specializing in Indian law. "
        "You create clear, formal, and legally compliant complaints, FIRs, and legal notices. "
        "The documents must be professional and ready to submit to authorities."
    ),
    tools=[],
    llm=llm,
    verbose=True,
)
