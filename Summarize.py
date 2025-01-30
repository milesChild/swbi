import requests
import json
import csv
from dotenv import load_dotenv
import os

load_dotenv()

# Your API Authorization Key
AUTHORIZATION_KEY = os.getenv("BLAND_API_KEY")  # Replace with your actual API key
BASE_URL = "https://api.bland.ai/v1"

# Headers for authentication
HEADERS = {
    "Authorization": f"Bearer {AUTHORIZATION_KEY}",
    "Content-Type": "application/json"
}

def summarize_call(call_id, goal, questions):
    url = f"https://api.bland.ai/v1/calls/{call_id}/analyze"
    payload = {
        "goal": goal,
        "questions": questions  # Ensure this follows API expected format
    }
    headers = {
        "authorization": AUTHORIZATION_KEY,
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        
        if data["status"] == "success":
            answers = data.get("answers", {})
            print("API Response:", answers)  # Debugging line
            
            # Check structure of answers
            phone_number = answers.get("phone_number", "Unknown")
            summary = answers.get("summary", "No summary available")
            outcome = answers.get("outcome", "Unknown")

            return [phone_number, summary, outcome]
        else:
            print(f"Error analyzing call {call_id}: {data['message']}")
            return None
    else:
        print(f"API request failed for call {call_id} with status code {response.status_code}")
        return None

def get_past_calls(start_date: str, end_date: str):
    """
    Retrieves past calls within the specified date range.
    """
    url = f"{BASE_URL}/calls?ascending=true"
    params = {
        "start_date": start_date,
        "end_date": end_date
    }

    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code == 200:
        calls = response.json().get("calls", [])
        return [call["call_id"] for call in calls]
    else:
        print(f"Failed to retrieve calls: {response.status_code} - {response.text}")
        return []

def save_results_to_csv(results, filename="call_summaries2.csv"):
    """
    Saves the summarized call results to a CSV file.
    """
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["Call ID", "Phone Number", "Summary", "Outcome"])
            writer.writeheader()  # Write column headers
            writer.writerows(results)
        print(f"Results successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving results to file: {e}")

# Example Usage
if __name__ == "__main__":
    # Define the date range (1/29/2025 - 1/29/2025)
    start_date = "2025-01-29"
    end_date = "2025-01-30"

    # Retrieve past calls
    call_ids = get_past_calls(start_date, end_date)

    # Goal and questions for call analysis
    goal = "Determine whether the store had the 1854 rifle in stock or not. If the rifle was out of stock, determine if it was not typically carried at the store or if it just sold out fast."
    questions = [
        ["Was the rifle in stock?","string"],
        ["Is the rifle sold out?","string"],
        ["Does the store carry the rifle?","string"]
    ]

    # Storing call summaries
    call_summaries = []

    for call_id in call_ids:
        print(f"Processing Call ID: {call_id}")
        summary = summarize_call(call_id, goal, questions)
        
        if summary:
            call_summaries.append(summary)

    # Save results to CSV file
    save_results_to_csv(call_summaries2)

    
