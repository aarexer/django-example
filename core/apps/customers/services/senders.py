from abc import (
    ABC,
    abstractmethod,
)

from core.apps.customers.entities.customers import CustomerEntity


class BaseSenderService(ABC):
    @abstractmethod
    def send_code(self, code: str, customer: CustomerEntity) -> None:
        ...


class DummySenderService(BaseSenderService):
    def send_code(self, code: str, customer: CustomerEntity) -> None:
        print(f'Code {code} sent to user {customer}')
