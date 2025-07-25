# personal assistant by hamza khan

import datetime
import json
from typing import List, Dict

# scheduler agent
def scheduler_agent(topics: List[str], deadline: str) -> List[Dict]:
    try:
        deadline_date = datetime.datetime.strptime(deadline, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD.")
    
    today = datetime.date.today()
    days_remaining = (deadline_date - today).days
    if days_remaining <= 0:
        raise ValueError("Deadline must be a future date.")
    
    study_days = max(1, days_remaining // len(topics))
    study_plan = []
    current_day = today

    for topic in topics:
        end_day = current_day + datetime.timedelta(days=study_days - 1)
        study_plan.append({
            "topic": topic,
            "start_date": str(current_day),
            "end_date": str(end_day) 
        })
        current_day = end_day + datetime.timedelta(days=1)
    
    return study_plan  # <-- moved outside the loop

# research agent
def research_agent(topic: str) -> List[str]:  # <-- missing colon fixed
    return [
        f"What is {topic}? - https://www.wikipedia.org/{topic.replace(' ', '_')}",
        f"Youtube Intro to {topic} - https://www.youtube.com/results?search_query=introduction+to+{topic.replace(' ', '+')}",
        f"Benefits and Risks of {topic} - https://medium.com/tag/{topic.replace(' ', '-')}",
        f"Research Paper on {topic} - https://scholar.google.com/scholar?q={topic.replace(' ', '+')}"
    ]

# summarize agent
def summarizer_agent(snippets: List[str]) -> str:
    return " | ".join(snippets)  # <-- incorrect .json fixed to .join

def run_study_assistant():
    topics_input = input("Enter your study topics separated by commas: ")  # fixed typo
    deadline = input("Enter your study deadline (YYYY-MM-DD): ")  # fixed typo
    topics = [t.strip() for t in topics_input.split(",") if t.strip()]

    if not topics:
        print("No valid topic is entered.")
        return

    try:
        study_plan = scheduler_agent(topics, deadline)  # <-- fixed assignment and spelling
    except Exception as e:
        print("Error:", e)
        return

    full_output = []

    for item in study_plan:
        topic = item["topic"]
        print(f"\nResearching: {topic}")
        research = research_agent(topic)  # <-- fixed assignment operator
        summary = summarizer_agent(research)  # <-- fixed assignment operator

        item_output = {
            "topic": topic,
            "start_date": item["start_date"],
            "end_date": item["end_date"],
            "summary": summary
        }
        full_output.append(item_output)
        print(f"Summary for {topic}:\n{summary}")  # <-- fixed typo: Summary → summary

    with open("study_assistant_output.json", "w") as f:
        json.dump(full_output, f, indent=4)

    print("\nStudy plan and summaries are saved in 'study_assistant_output.json'.")

if __name__ == "__main__":
    run_study_assistant()
