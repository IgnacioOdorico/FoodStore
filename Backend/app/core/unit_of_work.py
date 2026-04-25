from abc import ABC, abstractmethod
from sqlmodel import Session
from app.core.database import SessionLocal

class AbstractUnitOfWork(ABC):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.rollback()

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError

class UnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.session_factory = SessionLocal

    def __enter__(self):
        self.session = self.session_factory()
        return super().__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__exit__(exc_type, exc_val, exc_tb)
        self.session.expunge_all()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
