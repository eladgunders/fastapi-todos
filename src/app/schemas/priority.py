from pydantic import create_model_from_typeddict
from app.types.priority import Priority as PriorityType

Priority = create_model_from_typeddict(PriorityType)
