## Habitica Todo Creator

This Python program automates the creation of todo tasks on your Habitica account. It allows you to define tasks with specific text, notes, and due dates.

**Features:**

* Creates Habitica todo tasks
* Supports due dates at 11:00 PM on specified days
* Handles notes and defaults to an empty string when not provided
* Logs successful creations and errors

**Requirements:**

* Python 3.x
* `requests` library (install with `pip install requests`)
* `dotenv` library (install with `pip install python-dotenv`)
* A Habitica account with API access enabled

**Instructions:**

1. **Set up Habitica API Access:**

   - Go to your Habitica settings ([https://habitica.com/user/settings/general](https://habitica.com/user/settings/general)).
   - Generate a new API token.
   - Create a file named `.env` in the same directory as this program. Add the following lines to the file, replacing the placeholders with your actual values:

     ```
     USER_ID=<your_habitica_user_id>
     API_TOKEN=<your_habitica_api_token>
     ```

2. **Customize Tasks:**

   - Modify the `tasks` list in the `main` function to define your desired todo tasks. Each task is a tuple containing:
      - Text (str): The main content of the todo task.
      - Notes (str, optional): Additional information related to the task. Can include URLs. Defaults to an empty string if not provided.
    - Modify the second parameter to the function `generate_due_dates` to change the days you want the task to be due. You can have one day or multiple days based on your needs.

3. **Run the Program:**

   - Open a terminal or command prompt and navigate to the directory containing this program and the `.env` file.
   - Run the program using:

     ```bash
     python habitica-script.py
     ```

**Example Usage:**

```python
tasks = [
    ("Sample Todo Task 1", "https://www.google.com"),
    ("Sample Todo Task 2", "https://www.wikipedia.org"),
    ("Sample Todo Task 3",),  # No note provided, should default to ""
]


today = datetime.now()
due_dates = generate_due_dates(today, (2, 7, 14))  # Create tasks due in 2, 7, and 14 days

for task in tasks:
    text = task[0]
    note = task[1] if len(task) > 1 else ""
    for due_date in due_dates:
        create_todo(text, due_date, note)
```

This example will create three Habitica todo tasks:

1. "Sample Todo Task 1" with a note linking to a google.
2. "Sample Todo Task 2",with a note linking to wikipedia.
3. "Sample Todo Task 3"" with no note.

    all of the todo task will repeat 3 times each due in 2, 7, 14 days from today

**Logging:**

The program logs its activity to a file named `app.log` in the same directory. It records successful todo creations and any errors encountered during the process.

**Additional Notes:**

* The program currently generates due dates set to 11:00 PM. You can modify the `generate_due_dates` function if you need different times.
* Consider adding error handling for potential issues like missing environment variables or invalid API credentials.
