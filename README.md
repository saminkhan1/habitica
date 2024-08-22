
<h1 align="center">TODO-POMODORO</h1>

<p align="center">
	<img src="https://img.shields.io/github/license/saminkhan1/todo-pomodoro?style=flat&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/saminkhan1/todo-pomodoro?style=flat&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/saminkhan1/todo-pomodoro?style=flat&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/saminkhan1/todo-pomodoro?style=flat&color=0080ff" alt="repo-language-count">
</p>

<hr>

## Quick Links

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Modules](#modules)
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The **TODO-POMODORO** project provides an efficient task management solution by integrating with popular platforms like Habitica, Todoist, and Google Tasks. It simplifies task creation, allowing users to manage tasks with due dates and details across multiple platforms via scripts like `habitica-script.py`, `todoist-script.py`, and `google_task-script.py`. This tool is designed for individuals aiming to enhance productivity and organization.

---

## Repository Structure

```sh
└── todo-pomodoro/
    ├── README.md
    ├── google_task-script.py
    ├── habitica-script.py
    └── todoist-script.py
```

---


## Modules

<details closed><summary>.</summary>

| File                                                                                                   | Summary                                                                                                                                                                                                    |
| ---                                                                                                    | ---                                                                                                                                                                                                        |
| [habitica-script.py](https://github.com/saminkhan1/todo-pomodoro/blob/master/habitica-script.py)       | **habitica-script.py:** This script automates the creation of tasks in Habitica by interacting with the Habitica API. It prompts the user for task details, including title and notes, and schedules tasks based on spaced repetition. The script handles due dates, error logging, and ensures tasks are created with specific priorities. |
| [todoist-script.py](https://github.com/saminkhan1/todo-pomodoro/blob/master/todoist-script.py)         | **todoist-script.py:** This script integrates with the Todoist API to create and manage tasks with priority and spaced repetition. It fetches available projects, prompts the user for task details, and schedules tasks with due dates for spaced repetition. The script logs each task creation process and handles errors effectively.|
| [google_task-script.py](https://github.com/saminkhan1/todo-pomodoro/blob/master/google_task-script.py) | **google_task-script.py:** This script interacts with the Google Tasks API to create and manage tasks within Google Tasks. It includes functionality to authenticate users, list task lists, create new tasks with due dates, and handle errors gracefully. The script prompts the user to select a task list and enter details for the tasks they wish to create, then schedules the tasks based on predefined due dates.                                                                                                           |

</details>

---

## Getting Started

### Installation

1. Clone the repository:

```sh
git clone https://github.com/saminkhan1/todo-pomodoro
```

2. Navigate to the project directory:

```sh
cd todo-pomodoro
```

3. Install the required dependencies:

```sh
pip install -r requirements.txt
```

### Running TODO-POMODORO

To start the application (for example google task version), run:

```sh
python google_task-script.py
```

---

## Contributing

Contributions are welcome! Here’s how you can contribute:

- **[Submit Pull Requests](https://github.com/saminkhan1/todo-pomodoro/blob/main/CONTRIBUTING.md)**: Review open PRs, or submit your own.
- **[Join Discussions](https://github.com/saminkhan1/todo-pomodoro/discussions)**: Share insights, ask questions, or provide feedback.
- **[Report Issues](https://github.com/saminkhan1/todo-pomodoro/issues)**: Log bugs or feature requests.

<details>
    <summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Fork the project repository to your GitHub account.
2. **Clone Locally**: Clone the forked repository to your local machine.
   ```sh
   git clone https://github.com/saminkhan1/todo-pomodoro
   ```
3. **Create a New Branch**: Work on a new branch.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Changes**: Develop and test your changes locally.
5. **Commit Changes**: Commit with a clear message.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to GitHub**: Push changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original repository.

</details>

---

## License

This project is licensed under the [INSERT LICENSE NAME](https://choosealicense.com/licenses) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.

---

[**Return to Quick Links**](#quick-links)

---

This version is concise, focusing on the most critical information while removing unnecessary sections.