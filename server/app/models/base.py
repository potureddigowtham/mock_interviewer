"""Base model for all database models."""
from typing import Any, Dict, Type, TypeVar

from sqlalchemy import Column, DateTime, Integer, func, inspect
from sqlalchemy.ext.declarative import as_declarative, declared_attr

# For type hints
ModelType = TypeVar('ModelType', bound='Base')

@as_declarative()
class Base:
    """Base class for all database models.
    
    Attributes:
        id: Primary key
        created_at: Timestamp of record creation
        updated_at: Timestamp of last update
    """
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), 
                       onupdate=func.now(), nullable=False)

    @declared_attr
    def __tablename__(cls) -> str:
        """
        Generate __tablename__ automatically.
        Converts 'ModelName' to 'model_names'
        """
        return f"{cls.__name__.lower()}s"

    def to_dict(self) -> Dict[str, Any]:
        """Convert model instance to dictionary.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the model
        """
        result = {}
        for column in self.__table__.columns:  # type: ignore
            column_name = str(column.name)
            column_value = getattr(self, column_name)
            
            # Convert datetime to ISO format if it's a datetime object
            if hasattr(column_value, 'isoformat'):
                column_value = column_value.isoformat()
                
            result[column_name] = column_value
            
        return result
