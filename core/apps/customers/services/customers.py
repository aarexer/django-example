from abc import (
    ABC,
    abstractmethod,
)
from uuid import uuid4

from core.apps.customers.entities.customers import CustomerEntity
from core.apps.customers.exceptions.customers import CustomerTokenInvalid
from core.apps.customers.models.customers import Customer as CustomerModel


class BaseCustomerService(ABC):
    @abstractmethod
    def get(self, phone: str) -> CustomerEntity:
        ...

    @abstractmethod
    def get_or_create(self, phone: str) -> CustomerEntity:
        ...

    @abstractmethod
    def generate_token(self, customer: CustomerEntity) -> str:
        ...

    @abstractmethod
    def get_by_token(self, token: str) -> CustomerEntity:
        ...


class OrmCustomerService(BaseCustomerService):
    def get(self, phone: str) -> CustomerEntity:
        customer_model = CustomerModel.objects.get(phone=phone)

        return customer_model.to_entity()

    def get_or_create(self, phone: str) -> CustomerEntity:
        customer_model, _ = CustomerModel.objects.get_or_create(phone=phone)

        return customer_model.to_entity()

    def generate_token(self, customer: CustomerEntity) -> str:
        new_token = str(uuid4())
        CustomerModel.objects.filter(phone=customer.phone).update(
            token=new_token,
        )

        return new_token

    def get_by_token(self, token: str) -> CustomerEntity:
        try:
            customer_dto = CustomerModel.objects.get(token=token)
        except CustomerModel.DoesNotExist:
            raise CustomerTokenInvalid(token=token)

        return customer_dto.to_entity()
