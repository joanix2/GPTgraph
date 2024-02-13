import uuid

def generate_uuid():
    """
    Génère et retourne un UUID (Universally Unique Identifier).

    Returns:
        str: UUID généré.
    """
    return str(uuid.uuid4())