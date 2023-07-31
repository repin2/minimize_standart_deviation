from pydantic import RootModel, conlist


class MinimizeDeviation(RootModel):
    root: conlist(conlist(float, min_length=2, max_length=2), min_length=1)
