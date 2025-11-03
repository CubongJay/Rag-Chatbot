from app.domain.interfaces.vector_repository import VectorRepository


class RetrieveContextUsecase:
    """Use case for retrieving context vectors."""

    def __init__(self, vector_repo: VectorRepository):
        self.vector_repo = vector_repo

    def execute(self, query: str):
        """Retrieve most relevant documents for a given query."""
        return self.vector_repo.query(txt=query)
