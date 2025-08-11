"""
Blueprint for Notes API (CRUD operations).

Author: Kavia Code Generation Agent
"""

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from ..schemas import NoteSchema
from ..services import (
    get_all_notes,
    create_note,
    get_note,
    update_note,
    delete_note,
)

blp = Blueprint(
    "Notes",
    "notes",
    url_prefix="/notes",
    description="Operations on notes (CRUD)"
)

@blp.route("/")
class NotesListAPI(MethodView):
    # PUBLIC_INTERFACE
    @blp.response(200, NoteSchema(many=True))
    def get(self):
        """
        Get a list of all notes.
        """
        return get_all_notes()

    # PUBLIC_INTERFACE
    @blp.arguments(NoteSchema, location="json")
    @blp.response(201, NoteSchema)
    def post(self, new_data):
        """
        Create a new note.

        Request JSON body:
        {
            "title": "Note title",
            "content": "Note content"
        }
        """
        return create_note(title=new_data["title"], content=new_data["content"])

@blp.route("/<int:note_id>")
class NoteAPI(MethodView):
    # PUBLIC_INTERFACE
    @blp.response(200, NoteSchema)
    def get(self, note_id):
        """
        Retrieve a single note by its ID.
        """
        note = get_note(note_id)
        if not note:
            abort(404, message="Note not found")
        return note

    # PUBLIC_INTERFACE
    @blp.arguments(NoteSchema, location="json")
    @blp.response(200, NoteSchema)
    def put(self, update_data, note_id):
        """
        Update an existing note.

        Request JSON body:
        {
            "title": "New Title",
            "content": "New content"
        }
        """
        note = update_note(note_id, update_data["title"], update_data["content"])
        if not note:
            abort(404, message="Note not found")
        return note

    # PUBLIC_INTERFACE
    def delete(self, note_id):
        """
        Delete a note by ID.

        Returns 204 if successful, 404 if not found.
        """
        deleted = delete_note(note_id)
        if not deleted:
            abort(404, message="Note not found")
        return "", 204
