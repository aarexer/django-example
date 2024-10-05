from functools import lru_cache

from punq import Container

from core.apps.customers.services.auth import (
    AuthService,
    BaseAuthService,
)
from core.apps.customers.services.codes import (
    BaseCodeService,
    DjangoCacheCodeService,
)
from core.apps.customers.services.customers import (
    BaseCustomerService,
    OrmCustomerService,
)
from core.apps.customers.services.senders import (
    BaseSenderService,
    DummySenderService,
)
from core.apps.products.services.products import (
    BaseProductService,
    OrmProductService,
)
from core.apps.products.services.reviews import (
    BaseReviewService,
    BaseReviewValidatorService,
    ComposedReviewValidatorService,
    OrmReviewService,
    ReviewRatingValidatorService,
    SingleReviewValidatorService,
)
from core.apps.products.use_cases.reviews.create import CreateReviewUseCase


@lru_cache(1)
def get_container() -> Container:
    return _initialize_containers()


def _initialize_containers() -> Container:
    container = Container()

    def build_validators() -> BaseReviewValidatorService:
        return ComposedReviewValidatorService(
            validators=[
                container.resolve(SingleReviewValidatorService),
                container.resolve(ReviewRatingValidatorService),
            ],
        )

    # initialize products
    container.register(BaseProductService, OrmProductService)

    # initialize customers
    container.register(BaseCustomerService, OrmCustomerService)
    container.register(BaseCodeService, DjangoCacheCodeService)
    container.register(BaseSenderService, DummySenderService)
    container.register(BaseAuthService, AuthService)
    container.register(BaseReviewService, OrmReviewService)

    container.register(SingleReviewValidatorService)
    container.register(ReviewRatingValidatorService)
    container.register(
        BaseReviewValidatorService,
        ComposedReviewValidatorService, validators=[
            container.resolve(SingleReviewValidatorService),
            container.resolve(ReviewRatingValidatorService),
        ],
    )
    container.register(BaseReviewValidatorService, factory=build_validators)

    container.register(CreateReviewUseCase)

    return container
