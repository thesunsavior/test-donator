from pydantic import BaseModel, Field
from typing import Optional

class TestCase(BaseModel):
    input: dict
    output: dict
    description: Optional[str] = None



