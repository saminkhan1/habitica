import os
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/tasks"]


def get_tasks_service() -> Any:
    """
    Create and return a Google Tasks service object.

    Returns:
        Any: A Google Tasks service object.

    Raises:
        IOError: If there's an error reading or writing credential files.
        HttpError: If there's an error in the API request.
        RuntimeError: For other unexpected errors.
    """
    try:
        creds = None
        if os.path.exists("token.json"):
            try:
                creds = Credentials.from_authorized_user_file("token.json", SCOPES)
            except IOError as e:
                logger.error(f"Error reading token file: {str(e)}")
                creds = None

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except HttpError as e:
                    logger.error(f"Error refreshing credentials: {str(e)}")
                    creds = None

            if not creds:
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        "credentials.json", SCOPES
                    )
                    creds = flow.run_local_server(port=0)
                except IOError as e:
                    raise IOError(f"Error reading client secret file: {str(e)}")
                except HttpError as e:
                    raise HttpError(f"Error in authorization flow: {str(e)}")

            # Save the credentials for the next run
            try:
                with open("token.json", "w") as token:
                    token.write(creds.to_json())
            except IOError as e:
                logger.error(f"Error writing token file: {str(e)}")

        return build("tasks", "v1", credentials=creds)
    except Exception as e:
        raise RuntimeError(f"Unexpected error creating Tasks service: {str(e)}")


def list_task_lists(service: Any) -> List[Dict[str, str]]:
    """
    List all task lists for the authenticated user.

    Args:
        service (Any): Authenticated Google Tasks service instance.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing task list information.

    Raises:
        HttpError: If there's an error in the API request.
    """
    try:
        results = service.tasklists().list().execute()
        task_lists = results.get("items", [])
        return [
            {"id": task_list["id"], "title": task_list["title"]}
            for task_list in task_lists
        ]
    except HttpError as error:
        logger.error(f"An error occurred while listing task lists: {error}")
        raise


def create_todo(
    service: Any, tasklist_id: str, text: str, due_date: datetime, note: str = ""
) -> None:
    """
    Creates a new todo task on Google Tasks.

    Args:
        service (Any): Authenticated Google Tasks service instance.
        tasklist_id (str): The ID of the task list to add the task to.
        text (str): The text of the todo task.
        due_date (datetime): The due date of the todo task.
        note (str): Additional notes for the todo task.

    Raises:
        ValueError: If due_date is not a datetime object.
        HttpError: If there's an error in the API request.
    """
    if not isinstance(due_date, datetime):
        raise ValueError("due_date must be a datetime object")

    task = {
        "title": str(text),
        "notes": str(note),
        "due": due_date.isoformat() + "Z",  # 'Z' indicates UTC time
    }

    try:
        result = service.tasks().insert(tasklist=tasklist_id, body=task).execute()
        logger.info(
            "Todo '%s' created successfully for %s in task list %s",
            text,
            due_date.strftime("%Y-%m-%d"),
            tasklist_id,
        )
    except HttpError as error:
        logger.error(
            "Failed to create todo for %s in task list %s. Error: %s",
            due_date.strftime("%Y-%m-%d"),
            tasklist_id,
            str(error),
        )
        raise


def generate_due_dates(base_date: datetime, days: tuple) -> List[datetime]:
    """
    Generate a list of due dates set to 11:00 PM on each day specified by `days`.

    Args:
        base_date (datetime): The starting date.
        days (tuple of int): Days to add to the base date.

    Returns:
        List[datetime]: List of due dates at 11:00 PM.
    """
    return [
        datetime.combine(
            base_date + timedelta(days=day), datetime.min.time().replace(hour=23)
        )
        for day in days
    ]


def main() -> None:
    """
    Main function to create tasks on Google Tasks.

    This function lists all task lists, prompts the user to select a task list,
    then repeatedly prompts the user for todo titles and notes, generates a list of
    due dates, and creates the tasks on Google Tasks for each due date until the user decides to stop.
    """
    try:
        service = get_tasks_service()

        # List all task lists
        task_lists = list_task_lists(service)
        print("Available task lists:")
        for i, task_list in enumerate(task_lists, 1):
            print(f"{i}. {task_list['title']}")

        # Ask user to select a task list
        while True:
            try:
                selection = (
                    int(input("Enter the number of the task list you want to use: "))
                    - 1
                )
                if 0 <= selection < len(task_lists):
                    selected_list = task_lists[selection]
                    break
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Please enter a valid number.")

        print(f"Selected task list: {selected_list['title']}")

        today = datetime.now()
        due_dates = generate_due_dates(today, (2, 7, 14, 30, 90))

        while True:
            text = input("Enter the todo title (or type 'done' to finish): ")
            if text.lower() == "done":
                break
            note = input("Enter the todo note: ")

            for due_date in due_dates:
                create_todo(service, selected_list["id"], text, due_date, note)

    except IOError as e:
        logger.error(f"IO Error: {str(e)}")
    except HttpError as e:
        logger.error(f"HTTP Error: {str(e)}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()
