class ConversationUseCase:
    def __init__(self, repository):
        self.repository = repository

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, conversation_id: int):
        return self.repository.get_by_id(conversation_id)

    def create(self, data):
        return self.repository.create(data)

    def update(self, conversation_id: int, data):
        return self.repository.update(conversation_id, data)

    def delete(self, conversation_id: int):
        return self.repository.delete(conversation_id)
