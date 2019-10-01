from enum import Enum


class TaskStatus(Enum):
    """Class representing ToDo list task statuses."""

    not_started = "Not Started"
    in_progress = "In Progress"
    completed = "Completed"
