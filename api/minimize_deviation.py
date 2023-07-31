from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from . import MinimizeDeviation
from .utils import find_params_for_best_deviation

minimize_router = APIRouter(prefix="")


@minimize_router.post("/best_params", response_class=StreamingResponse)
async def best_params(pairs_list: MinimizeDeviation):
    a, b, c, image = find_params_for_best_deviation(pairs_list)
    response = StreamingResponse(image, media_type="image/png")
    for h, v in (("X-A", a), ("X-B", b), ("X_C", c)):
        response.headers[h] = str(v)
    return response
