import os
from datetime import datetime, timedelta
import logging
from typing import List, Optional, Dict
from dotenv import load_dotenv
from todoist_api_python.api import TodoistAPI

# Load environment variables from a .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    filename="todoist_tasks.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Initialize Todoist API
API_TOKEN = os.getenv("TODOIST_API")
if not API_TOKEN:
    raise ValueError("TODOIST_API not found in environment variables")
api = TodoistAPI(API_TOKEN)


def create_todo(
    content: str,
    due_date: datetime,
    priority: int,
    description: str = "",
    project_id: Optional[str] = None,
) -> None:
    """
    Creates a new todo task on Todoist.

    Args:
        content (str): The content of the todo task.
        due_date (datetime): The due date of the todo task.
        priority (int): The priority of the task (1-4).
        description (str, optional): Additional description for the todo task.
        project_id (str, optional): The ID of the project to add the task to.

    Raises:
        ValueError: If due_date is not a datetime object.
    """
    if not isinstance(due_date, datetime):
        raise ValueError("due_date must be a datetime object")

    due_string = due_date.strftime("%Y-%m-%d at %H:%M")

    try:
        task = api.add_task(
            content=content,
            description=description,
            project_id=project_id,
            due_string=due_string,
            due_lang="en",
            priority=priority,
        )
        logging.info(
            f"Todo '{content}' created successfully for {due_date.strftime('%Y-%m-%d %H:%M')}"
        )
    except Exception as error:
        logging.error(
            f"Failed to create todo '{content}' for {due_date.strftime('%Y-%m-%d %H:%M')}. Error: {error}"
        )


def get_projects() -> Dict[str, str]:
    """
    Fetches all projects from Todoist.

    Returns:
        Dict[str, str]: A dictionary of project names to project IDs.
    """
    try:
        projects = api.get_projects()
        return {project.name: project.id for project in projects}
    except Exception as error:
        logging.error(f"Failed to fetch projects. Error: {error}")
        return {}


def select_project(projects: Dict[str, str]) -> Optional[str]:
    """
    Allows the user to select a project interactively.

    Args:
        projects (Dict[str, str]): A dictionary of project names to project IDs.

    Returns:
        Optional[str]: The selected project ID, or None for Inbox.
    """
    print("\nAvailable projects:")
    for i, name in enumerate(projects.keys(), 1):
        print(f"{i}. {name}")

    while True:
        try:
            choice = int(input("\nEnter the number of the project: "))
            if choice == 0:
                return None
            if 1 <= choice <= len(projects):
                return list(projects.values())[choice - 1]
            print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_priority() -> int:
    """
    Prompts the user to select a priority level.

    Returns:
        int: The selected priority level (1-4).
    """
    while True:
        try:
            priority = int(
                input("Enter priority (1: Low, 2: Medium, 3: High, 4: Urgent): ")
            )
            if 1 <= priority <= 4:
                return priority
            print("Invalid priority. Please enter a number between 1 and 4.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def generate_spaced_repetition_dates(base_date: datetime) -> List[datetime]:
    """
    Generate a list of due dates for spaced repetition.

    Args:
        base_date (datetime): The starting date.

    Returns:
        List[datetime]: List of due dates at 11:00 PM for days 2, 7, 14, 30, and 90.
    """
    intervals = [2, 7, 14, 30, 90]
    return [
        datetime.combine(
            base_date + timedelta(days=interval),
            datetime.min.time().replace(hour=23, minute=0),
        )
        for interval in intervals
    ]


def main():
    """
    Main function to create tasks on Todoist with spaced repetition.

    This function prompts the user for todo details, generates spaced repetition due dates,
    and creates the tasks on Todoist for each due date.
    """
    projects = get_projects()
    project_id = select_project(projects)

    while True:
        content = input("Enter the todo content (or type 'done' to finish): ")
        if content.lower() == "done":
            break

        description = input("Enter the todo description (optional): ")
        priority = get_priority()

        base_date = datetime.now()
        due_dates = generate_spaced_repetition_dates(base_date)

        for due_date in due_dates:
            create_todo(content, due_date, priority, description, project_id)

        print(f"Created 5 tasks for '{content}' with spaced repetition due dates:")
        for i, date in enumerate(due_dates, 1):
            print(f"  {i}. {date.strftime('%Y-%m-%d %H:%M')}")


if __name__ == "__main__":
    main()
