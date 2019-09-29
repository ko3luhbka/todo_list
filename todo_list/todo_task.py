from enum import Enum


class TaskStatus(Enum):
    NOTSTARTED = 'Not Started'
    INPROGRESS = 'In Progress'
    COMPLETED = 'Completed'
