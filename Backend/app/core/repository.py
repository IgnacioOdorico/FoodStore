from typing import Generic, TypeVar, Type, List, Optional, Any
from sqlmodel import SQLModel, Session, select

# T = TypeVar: Esto es GENÉRICOS. Me permite que este repositorio funcione 
# para cualquier modelo (Producto, Categoría, Ingrediente) sin repetir código.
T = TypeVar("T", bound=SQLModel)

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: Session):
        self.model = model
        self.session = session

    def get(self, id: Any) -> Optional[T]:
        # El .get es el método más rápido de SQLAlchemy para buscar por ID.
        entity = self.session.get(self.model, id)
        # VALIDACIÓN SOFT DELETE: Si el objeto tiene fecha de borrado, para la app "no existe".
        if entity and hasattr(entity, "deleted_at") and entity.deleted_at is not None:
            return None
        return entity

    def list(self) -> List[T]:
        statement = select(self.model)
        # Filtro automático: solo traigo lo que no esté marcado como borrado.
        if hasattr(self.model, "deleted_at"):
            statement = statement.where(self.model.deleted_at == None)
        return self.session.exec(statement).all()

    def create(self, entity: T) -> T:
        # Solo agrego el objeto a la sesión. El commit lo hace el Unit of Work después.
        self.session.add(entity)
        return entity

    def delete(self, id: Any) -> bool:
        entity = self.get(id)
        if entity:
            # LÓGICA DE SOFT DELETE:
            # Si el modelo tiene el campo 'deleted_at', en lugar de borrarlo, 
            # le grabo la fecha actual. Así los datos quedan para auditoría.
            if hasattr(entity, "deleted_at"):
                from datetime import datetime
                entity.deleted_at = datetime.now()
                self.session.add(entity)
            else:
                # Si no tiene ese campo, lo borro físicamente.
                self.session.delete(entity)
            return True
        return False

    def update(self, entity: T) -> T:
        # En SQLModel/SQLAlchemy, agregar un objeto con un ID existente hace un UPDATE.
        self.session.add(entity)
        return entity
