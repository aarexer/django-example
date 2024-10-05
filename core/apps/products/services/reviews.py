from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from core.apps.customers.entities.customers import CustomerEntity
from core.apps.products.entities.products import Product as ProductEntity
from core.apps.products.entities.reviews import Review as ReviewEntity
from core.apps.products.exceptions.reviews import (
    ReviewInvalidRating,
    SingleReviewException,
)
from core.apps.products.models.reviews import Review as ReviewModel


class BaseReviewService(ABC):
    @abstractmethod
    def check_review_exist(self, product: ProductEntity, customer: CustomerEntity) -> bool:
        ...

    @abstractmethod
    def save(self, customer: CustomerEntity, product: ProductEntity, review: ReviewEntity) -> ReviewEntity:
        ...


class OrmReviewService(BaseReviewService):
    def check_review_exist(self, product: ProductEntity, customer: CustomerEntity) -> bool:
        return ReviewModel.objects.filter(
            product_id=product.id,
            customer_id=customer.id,
        ).exists()

    def save(self, customer: CustomerEntity, product: ProductEntity, review: ReviewEntity) -> ReviewEntity:
        review_dto: ReviewModel = ReviewModel.from_entity(
            customer=customer,
            product=product,
            review=review,
        )

        review_dto.save()

        return review_dto.to_entity()


class BaseReviewValidatorService(ABC):
    @abstractmethod
    def validate(
        self,
        review: ReviewEntity,
        customer: CustomerEntity | None = None,
        product: ProductEntity | None = None,
    ):
        ...


@dataclass(frozen=True, eq=False)
class ReviewRatingValidatorService(BaseReviewValidatorService):
    def validate(
        self,
        review: ReviewEntity,
        *args,
        **kwargs,
    ):
        # TODO: константы
        if not (1 <= review.rating <= 5):
            raise ReviewInvalidRating(rating=review.rating)


@dataclass(frozen=True, eq=False)
class SingleReviewValidatorService(BaseReviewValidatorService):
    service: BaseReviewService

    def validate(
        self,
        customer: CustomerEntity,
        product: ProductEntity,
        *args,
        **kwargs,
    ):
        if self.service.check_review_exist(product=product, customer=customer):
            raise SingleReviewException(
                product_id=product.id, customer_id=customer.id,
            )


@dataclass(frozen=True, eq=False)
class ComposedReviewValidatorService(BaseReviewValidatorService):
    validators: list[BaseReviewValidatorService]

    def validate(
        self,
        review: ReviewEntity,
        customer: CustomerEntity | None = None,
        product: ProductEntity | None = None,
    ):
        for validator in self.validators:
            validator.validate(
                review=review,
                customer=customer,
                product=product,
            )
