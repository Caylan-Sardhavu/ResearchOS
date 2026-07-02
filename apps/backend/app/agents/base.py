from pydantic import BaseModel


class AgentProfile(BaseModel):
    name: str
    department: str
    role: str
    description: str