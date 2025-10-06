from pydantic import BaseModel, Field, constr
class InferenceIn(BaseModel):
    text: constr(min_length=1, max_length=5000) = Field(..., description="Content to classify")
class InferenceOut(BaseModel):
    label: str
    score: float
    request_id: str
