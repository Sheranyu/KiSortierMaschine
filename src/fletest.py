from pydantic import BaseModel, Field, ValidationError

class User(BaseModel):
    username: str = Field(title="mein test",description="ichversuch ealles")

try:
    test = User(username="test")
    print(test.model_json_schema().get("properties"))
except ValidationError as e:
    print(e)
