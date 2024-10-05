from typing import Dict, List, Any, Optional

from pydantic import BaseModel


class MistralJSONResponse(BaseModel):
    obj: Dict[str, str]


class MistralRequestPayload(BaseModel):
    model: str
    response_format: Optional[Dict]
    messages: List[Dict[str, Any]]
    prompt: Optional[str] = None
    suffix: Optional[str] = None
    # temperature: float = 0.7
    top_p: float = 1.0

# this should in perfect case go into the run to track and train models
class ResponseTracker(BaseModel):
    old_description: str
    new_description: str
    json_context: Dict
    description_comparison: str
    initial_code: str
    updated_code: Optional[str]