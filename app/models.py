from pydantic import BaseModel

# Intent constants
MATH = "math_question"
ASK_ABOUT_WEATHER = "ask_about_weather"
GENERIC_QUESTION = "generic_question"

OUTPUT_MAP = {
    MATH: "math_tool",
    ASK_ABOUT_WEATHER: "weather_tool",
    GENERIC_QUESTION: "llm_tool",
}


class Intent(BaseModel):
    intent: str


class LocationInformation(BaseModel):
    city: str = ""
    state_code: str = ""
    country_code: str = ""


class QueryState(BaseModel):
    query: str
    intent: str | None = None
    result: str | None = None
    location_information: LocationInformation | None = None
    math_expression: str | None = None
