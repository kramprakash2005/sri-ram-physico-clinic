from app.db import database as db # Corrected import

async def get_next_sequence(name: str) -> int:
    """
    Retrieves the next number from a sequence in the 'counters' collection.
    
    Args:
        name (str): The name of the sequence (e.g., 'patients', 'bills').

    Returns:
        int: The next sequence number.
    """
    ret = await db.counters.find_one_and_update(
        {"_id": name},
        {"$inc": {"sequence_value": 1}},
        upsert=True, # Create the counter if it doesn't exist
        return_document=True
    )
    # If the counter was just created, it might not have the value yet
    if not ret:
        # Retry once if upsert was slow to create
        ret = await db.counters.find_one({"_id": name})

    return ret["sequence_value"]

