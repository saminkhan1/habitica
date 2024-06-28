import os
import requests
from datetime import datetime, timedelta, time
import logging
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

API_URL = "https://habitica.com/api/v3/tasks/user"
USER_ID = os.getenv("USER_ID")
API_TOKEN = os.getenv("API_TOKEN")

HEADERS = {
    "x-api-user": USER_ID,
    "x-api-key": API_TOKEN,
    "Content-Type": "application/json",
}

logging.basicConfig(filename="app.log", level=logging.INFO)  # Example logging setup


def create_todo(text, due_date, note=""):
    """
    Creates a new todo task on Habitica.

    Args:
        text (str): The text of the todo task.
        due_date (datetime): The due date of the todo task.
        note (str): Additional notes for the todo task. The note should be a string that provides
                    additional context or information related to the task. It can include URLs or
                    any relevant details. Defaults to an empty string if not provided.

    Returns:
        None
    """
    if not isinstance(due_date, datetime):
        raise ValueError("due_date must be a datetime object")

    data = {
        "text": str(text),
        "type": "todo",
        "date": due_date.strftime("%Y-%m-%d"),
        "notes": str(note),
        "priority": 2,
    }

    try:
        response = requests.post(API_URL, json=data, headers=HEADERS)
        response.raise_for_status()
        logging.info(
            "Todo '%s' created successfully for %s", text, due_date.strftime("%Y-%m-%d")
        )
    except requests.exceptions.HTTPError as err:
        logging.error(
            "Failed to create todo for %s. HTTP error occurred: %s",
            due_date.strftime("%Y-%m-%d"),
            err,
        )
    except requests.exceptions.RequestException as err:
        logging.error("Failed to create todo due to network issues: %s", err)


def generate_due_dates(base_date, days):
    """
    Generate a list of due dates set to 11:00 PM on each day specified by `days`.

    Args:
        base_date (datetime): The starting date.
        days (tuple of int): Days to add to the base date.

    Returns:
        list of datetime: List of due dates at 11:00 PM.
    """
    due_dates = []
    for day in days:
        due_datetime = datetime.combine(
            base_date + timedelta(days=day), time(hour=23, minute=0)
        )
        due_dates.append(due_datetime)
    return due_dates


def main():
    """
    Main function to create tasks on Habitica.

    This function repeatedly prompts the user for todo titles and notes, generates a list of
    due dates, and creates the tasks on Habitica for each due date until the user decides to stop.
    """
    today = datetime.now()
    due_dates = generate_due_dates(today, (2, 7, 14, 30, 90))

    while True:
        text = input("Enter the todo title (or type 'done' to finish): ")
        if text.lower() == "done":
            break
        note = input("Enter the todo note: ")

        for due_date in due_dates:
            create_todo(text, due_date, note)


if __name__ == "__main__":
    main()
