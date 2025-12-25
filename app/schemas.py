from pydantic import BaseModel, Field


class PromptRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="User prompt sent to the LLM")


class PromptResponse(BaseModel):
    response: str = Field(..., description="LLM generated response")
