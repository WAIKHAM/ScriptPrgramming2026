# My OOP Task Manager CLI

A command-line interface (CLI) application for managing your daily tasks, built with Object-Oriented Programming (OOP) principles.
This version refactors the previous procedural approach into a more organized and scalable structure using `Task` and `TaskManager` classes.

## Features

* **Add Tasks**: Add new tasks with a description.
* **List Tasks**: View all your tasks, showing their ID, description, and status.
* **Complete Tasks**: Mark tasks as completed by their ID.
* **Delete Tasks**: Remove tasks by their ID.
* **Persistence**: Tasks are saved to `data/tasks.json` and loaded automatically upon startup.

## OOP Design

* **`Task` Class**: Represents an individual task with attributes like `id`, `description`, and `completed`.
* **`TaskManager` Class**: Manages the collection of `Task` objects, handling all operations (add, list, complete, delete) and data persistence (loading/saving).

## How to Run

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/my-oop-task-manager.git](https://github.com/YOUR_USERNAME/my-oop-task-manager.git)
    cd my-oop-task-manager
    ```
2.  **Run the application:**
    ```bash
    python main.py
    ```

## Project Structure

```
my-oop-task-manager/
├── src/
│ ├── init.py # Makes 'src' a Python package
│ ├── task.py # Defines the Task class
│ └── task_manager.py # Defines the TaskManager class (handles all core logic and data)
├── data/
│ └── tasks.json # Stores your tasks (created automatically)
├── main.py # The main entry point of the application
├── .gitignore # Specifies files/folders to ignore in Git
└── README.md # This file!

```

## Contributing

Feel free to fork this repository, add features, or improve existing ones!

## License

This project is open source. (You might add a specific license here later, e.g., MIT)
