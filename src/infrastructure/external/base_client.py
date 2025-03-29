from abc import abstractmethod, ABC

from src.domain.value_objects import UserData


class Client(ABC):

    @abstractmethod
    async def get_user_data(self, *args, **kwargs) -> UserData:
        raise NotImplementedError
