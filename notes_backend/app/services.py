"""
Service for handling note operations with sqlite3.

Author: Kavia Code Generation Agent
"""

import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from .models import Note

DB_PATH = os.environ.get("NOTES_DB_PATH", "notes.db")

def _dict_factory(cursor, row):
    """Converts a sqlite3 row to a dict for easier conversion to Note."""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@contextmanager
def get_db():
    """Context manager for the DB connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = _dict_factory
    try:
        yield conn
    finally:
        conn.close()

# PUBLIC_INTERFACE
def init_db():
    """Initializes the notes table if it does not exist."""
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        conn.commit()

# PUBLIC_INTERFACE
def create_note(title, content) -> Note:
    """Inserts a new note and returns it."""
    now = datetime.utcnow().isoformat()
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO notes (title, content, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (title, content, now, now),
        )
        conn.commit()
        new_id = cur.lastrowid
        cur.execute("SELECT * FROM notes WHERE id = ?", (new_id,))
        row = cur.fetchone()
        note = Note(
            id=row["id"],
            title=row["title"],
            content=row["content"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )
        return note

# PUBLIC_INTERFACE
def get_all_notes():
    """Retrieves all notes as a list of Note."""
    with get_db() as conn:
        cur = conn.execute("SELECT * FROM notes ORDER BY created_at DESC")
        rows = cur.fetchall()
        return [
            Note(
                id=row["id"],
                title=row["title"],
                content=row["content"],
                created_at=datetime.fromisoformat(row["created_at"]),
                updated_at=datetime.fromisoformat(row["updated_at"]),
            )
            for row in rows
        ]

# PUBLIC_INTERFACE
def get_note(note_id: int):
    """Gets a single note by id."""
    with get_db() as conn:
        cur = conn.execute("SELECT * FROM notes WHERE id=?", (note_id,))
        row = cur.fetchone()
        if row:
            return Note(
                id=row["id"],
                title=row["title"],
                content=row["content"],
                created_at=datetime.fromisoformat(row["created_at"]),
                updated_at=datetime.fromisoformat(row["updated_at"]),
            )
        return None

# PUBLIC_INTERFACE
def update_note(note_id: int, title: str, content: str):
    """Updates an existing note and returns it, or None if not found."""
    now = datetime.utcnow().isoformat()
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "UPDATE notes SET title=?, content=?, updated_at=? WHERE id=?",
            (title, content, now, note_id),
        )
        conn.commit()
        if cur.rowcount == 0:
            return None
        cur.execute("SELECT * FROM notes WHERE id=?", (note_id,))
        row = cur.fetchone()
        return Note(
            id=row["id"],
            title=row["title"],
            content=row["content"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )

# PUBLIC_INTERFACE
def delete_note(note_id: int):
    """Deletes a note by ID. Returns True if deleted, False otherwise."""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM notes WHERE id=?", (note_id,))
        conn.commit()
        return cur.rowcount > 0
