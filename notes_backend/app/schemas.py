"""
Marshmallow schemas for serializing and deserializing notes.

Author: Kavia Code Generation Agent
"""

from marshmallow import Schema, fields

# PUBLIC_INTERFACE
class NoteSchema(Schema):
    """Schema for notes serialization/deserialization."""
    id = fields.Integer(dump_only=True, description="Unique ID of the note")
    title = fields.String(required=True, description="Title of the note")
    content = fields.String(required=True, description="Content of the note")
    created_at = fields.DateTime(dump_only=True, description="Creation timestamp")
    updated_at = fields.DateTime(dump_only=True, description="Last updated timestamp")
