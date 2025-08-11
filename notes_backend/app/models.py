"""
Models for the notes backend. Currently, only Note is implemented.

Author: Kavia Code Generation Agent
"""

from dataclasses import dataclass
from datetime import datetime

# PUBLIC_INTERFACE
@dataclass
class Note:
    """
    Represents a Note object.

    Attributes:
        id (int): The note's unique identifier.
        title (str): The title of the note.
        content (str): The note's content.
        created_at (datetime): Creation date and time.
        updated_at (datetime): Last update date and time.
    """
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
