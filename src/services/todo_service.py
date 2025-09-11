from domain.models.todo import Todo, Subject, TutorProfile, Message, Conversation, Rating, Review
from domain.models.itodo_repository import ITodoRepository, ISubjectRepository, ITutorProfileRepository, IMessageRepository, IConversationRepository, IRatingRepository, IReviewRepository
from typing import List, Optional

class TodoService:
    def __init__(self, repository: ITodoRepository):
        self.repository = repository

    def create_todo(self, title: str, description: str, status: str, created_at, updated_at) -> Todo:
        todo = Todo(id=None, title=title, description=description, status=status, created_at=created_at, updated_at=updated_at)
        return self.repository.add(todo)

    def get_todo(self, todo_id: int) -> Optional[Todo]:
        return self.repository.get_by_id(todo_id)

    def list_todos(self) -> List[Todo]:
        return self.repository.list()

    def update_todo(self, todo_id: int, title: str, description: str, status: str, created_at, updated_at) -> Todo:
        todo = Todo(id=todo_id, title=title, description=description, status=status, created_at=created_at, updated_at=updated_at)
        return self.repository.update(todo)

    def delete_todo(self, todo_id: int) -> None:
        self.repository.delete(todo_id) 

class SubjectService:
    def __init__(self, repository: ISubjectRepository):
        self.repository = repository

    def create_subject(self, name: str, description: str) -> Subject:
        subject = Subject(id=None, name=name, description=description)
        return self.repository.add(subject)

    def get_subject(self, subject_id: int) -> Optional[Subject]:
        return self.repository.get_by_id(subject_id)

    def list_subjects(self) -> List[Subject]:
        return self.repository.list()

    def update_subject(self, subject_id: int, name: str, description: str) -> Subject:
        subject = Subject(id=subject_id, name=name, description=description)
        return self.repository.update(subject)

    def delete_subject(self, subject_id: int) -> None:
        self.repository.delete(subject_id)

class TutorProfileService:
    def __init__(self, repository: ITutorProfileRepository):
        self.repository = repository

    def create_profile(self, name: str, email: str, phone: str) -> TutorProfile:
        profile = TutorProfile(id=None, name=name, email=email, phone=phone)
        return self.repository.add(profile)

    def get_profile(self, profile_id: int) -> Optional[TutorProfile]:
        return self.repository.get_by_id(profile_id)

    def list_profiles(self) -> List[TutorProfile]:
        return self.repository.list()

    def update_profile(self, profile_id: int, name: str, email: str, phone: str) -> TutorProfile:
        profile = TutorProfile(id=profile_id, name=name, email=email, phone=phone)
        return self.repository.update(profile)

    def delete_profile(self, profile_id: int) -> None:
        self.repository.delete(profile_id)

class MessageService:
    def __init__(self, repository: IMessageRepository):
        self.repository = repository

    def create_message(self, content: str, sender_id: int, receiver_id: int, created_at, updated_at) -> Message:
        message = Message(id=None, content=content, sender_id=sender_id, receiver_id=receiver_id, created_at=created_at, updated_at=updated_at)
        return self.repository.add(message)

    def get_message(self, message_id: int) -> Optional[Message]:
        return self.repository.get_by_id(message_id)

    def list_messages(self) -> List[Message]:
        return self.repository.list()

    def update_message(self, message_id: int, content: str, sender_id: int, receiver_id: int, created_at, updated_at) -> Message:
        message = Message(id=message_id, content=content, sender_id=sender_id, receiver_id=receiver_id, created_at=created_at, updated_at=updated_at)
        return self.repository.update(message)

    def delete_message(self, message_id: int) -> None:
        self.repository.delete(message_id)

class ConversationService:
    def __init__(self, repository: IConversationRepository):
        self.repository = repository

    def create_conversation(self, sender_id: int, receiver_id: int, message: str, created_at, updated_at) -> Conversation:
        conversation = Conversation(
            id=None,
            sender_id=sender_id,
            receiver_id=receiver_id,
            message=message,
            created_at=created_at,
            updated_at=updated_at
        )
        return self.repository.add(conversation)

    def get_conversation(self, conversation_id: int) -> Optional[Conversation]:
        return self.repository.get_by_id(conversation_id)

    def list_conversations(self) -> List[Conversation]:
        return self.repository.list()

    def update_conversation(self, conversation_id: int, sender_id: int, receiver_id: int, message: str, created_at, updated_at) -> Conversation:
        conversation = Conversation(
            id=conversation_id,
            sender_id=sender_id,
            receiver_id=receiver_id,
            message=message,
            created_at=created_at,
            updated_at=updated_at
        )
        return self.repository.update(conversation)

    def delete_conversation(self, conversation_id: int) -> None:
        self.repository.delete(conversation_id)

class RatingService:
    def __init__(self, repository: IRatingRepository):
        self.repository = repository

    def create_rating(self, user_id: int, item_id: int, score: float, comment: str, created_at, updated_at) -> Rating:
        rating = Rating(
            id=None,
            user_id=user_id,
            item_id=item_id,
            score=score,
            comment=comment,
            created_at=created_at,
            updated_at=updated_at
        )
        return self.repository.add(rating)

    def get_rating(self, rating_id: int) -> Optional[Rating]:
        return self.repository.get_by_id(rating_id)

    def list_ratings(self) -> List[Rating]:
        return self.repository.list()

    def update_rating(self, rating_id: int, user_id: int, item_id: int, score: float, comment: str, created_at, updated_at) -> Rating:
        rating = Rating(
            id=rating_id,
            user_id=user_id,
            item_id=item_id,
            score=score,
            comment=comment,
            created_at=created_at,
            updated_at=updated_at
        )
        return self.repository.update(rating)

    def delete_rating(self, rating_id: int) -> None:
        self.repository.delete(rating_id)

class ReviewService:
    def __init__(self, repository: IReviewRepository):
        self.repository = repository

    def create_review(self, user_id: int, item_id: int, title: str, content: str, rating: float, created_at, updated_at) -> Review:
        review = Review(
            id=None,
            user_id=user_id,
            item_id=item_id,
            title=title,
            content=content,
            rating=rating,
            created_at=created_at,
            updated_at=updated_at
        )
        return self.repository.add(review)

    def get_review(self, review_id: int) -> Optional[Review]:
        return self.repository.get_by_id(review_id)

    def list_reviews(self) -> List[Review]:
        return self.repository.list()

    def update_review(self, review_id: int, user_id: int, item_id: int, title: str, content: str, rating: float, created_at, updated_at) -> Review:
        review = Review(
            id=review_id,
            user_id=user_id,
            item_id=item_id,
            title=title,
            content=content,
            rating=rating,
            created_at=created_at,
            updated_at=updated_at
        )
        return self.repository.update(review)

    def delete_review(self, review_id: int) -> None:
        self.repository.delete(review_id)

