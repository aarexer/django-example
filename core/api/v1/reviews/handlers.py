from django.http import HttpRequest
from ninja import (
    Header,
    Router,
)
from ninja.errors import HttpError

from core.api.schemas import ApiResponse
from core.api.v1.reviews.schemas import (
    ReviewInSchema,
    ReviewOutSchema,
)
from core.apps.common.exceptions import ServiceException
from core.apps.products.use_cases.reviews.create import CreateReviewUseCase
from core.project.containers import get_container


router = Router(tags=['Review'])


@router.post('{product_id}/reviews', response=ApiResponse[ReviewOutSchema], operation_id='createReview')
def create_review_handler(
    request: HttpRequest,
    product_id: int,
    schema: ReviewInSchema,
    token: str = Header(alias='Auth-Token'),
) -> ApiResponse[ReviewOutSchema]:

    container = get_container()

    useCase: CreateReviewUseCase = container.resolve(CreateReviewUseCase)

    try:
        result = useCase.execute(
            customer_token=token,
            product_id=product_id,
            review=schema.to_entity(),
        )
    except ServiceException as err:
        raise HttpError(status_code=400, message=err.message)

    return ApiResponse(data=ReviewOutSchema.from_entity(result))
