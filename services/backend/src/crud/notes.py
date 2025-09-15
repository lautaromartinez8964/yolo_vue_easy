from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist

from src.database.models import Notes
from src.schemas.notes import NoteOutSchema

async def get_notes():
    """
    List all notes.
    Returns a list of NoteOutSchema items serialized from all Notes.
    """
    return await NoteOutSchema.from_queryset(Notes.all())

async def get_note(note_id) -> NoteOutSchema:
    """
    Retrieve a single note by id.
    Raises 404 if not found.
    """
    try:
        return await NoteOutSchema.from_queryset_single(Notes.get(id=note_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Note {note_id} not found")

async def create_note(note, current_user) -> NoteOutSchema:
    """
    Create a note for the current user.
    - Sets author_id from current_user
    - Returns the created note serialized as NoteOutSchema
    """
    note_dict = note.dict(exclude_unset=True)
    note_dict["author_id"] = current_user.id
    note_obj = await Notes.create(**note_dict)
    return await NoteOutSchema.from_tortoise_orm(note_obj)

async def update_note(note_id, note, current_user) -> NoteOutSchema:
    """
    Update a note by id.
    Only the author can update the note; otherwise 403 is raised.
    Raises 404 if the note does not exist.
    """
    try:
        db_note = await NoteOutSchema.from_queryset_single(Notes.get(id=note_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Note {note_id} not found")
    
    if db_note.author.id == current_user.id:
        await Notes.filter(id=note_id).update(**note.dict(exclude_unset=True))
        return await NoteOutSchema.from_queryset_single(Notes.get(id=note_id))
    
    raise HTTPException(status_code=403, detail=f"Not authorized to update")

async def delete_note(note_id, current_user):
    """
    Delete a note by id.
    Only the author can delete; non-author gets 403.
    Raises 404 if the note does not exist.
    """
    db_note = await Notes.get_or_none(id=note_id)
    if db_note is None:
        raise HTTPException(status_code=404, detail=f"Note {note_id} not found")
    
    if db_note.author_id == current_user.id:
        deleted_count = await Notes.filter(id=note_id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"Note {note_id} not found")
        return f"Deleted note {note_id}"

    raise HTTPException(status_code=403, detail=f"Not authorized to delete")
        
   