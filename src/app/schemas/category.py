from pydantic import create_model_from_typeddict
from app.types.category import Category as CategoryType

Category = create_model_from_typeddict(CategoryType)