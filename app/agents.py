from pydantic_ai import Agent, ModelRetry, RunContext
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_gla import GoogleGLAProvider

from app.config import settings
from app.models import (
    ASK_ABOUT_WEATHER,
    GENERIC_QUESTION,
    MATH,
    Intent,
    LocationInformation,
)

# Initialize the model
model = GeminiModel(
    settings.gemini_model_name,
    provider=GoogleGLAProvider(api_key=settings.gemini_api_key),
)

# Intent Classifier Agent
intent_agent = Agent(
    model,
    system_prompt=(
        "Identify the user's question from the provided message\n"
        f"Choose from these options: `{MATH}`, `{ASK_ABOUT_WEATHER}`, "
        f"and `{GENERIC_QUESTION}`."
    ),
    output_type=Intent,
)


@intent_agent.output_validator
def validate_result(ctx: RunContext[None], result: Intent) -> Intent:
    if result.intent not in [MATH, ASK_ABOUT_WEATHER, GENERIC_QUESTION]:
        raise ModelRetry(
            f"Invalid action. Please choose from `{MATH}`, "
            f"`{ASK_ABOUT_WEATHER}`, `{GENERIC_QUESTION}`"
        )
    return result


# Location Extractor Agent
location_extractor_agent = Agent(
    model,
    system_prompt=(
        "Extract the city name, state code, country code from the user's query.\n"
        "Default to Jakarta if you can't find it. "
        "City name, state code (only for the US) and country code divided by comma. "
        "Use ISO 3166 country codes."
    ),
    output_type=LocationInformation,
)

# General Extractor Agent
extractor_agent = Agent(model)

# LLM Agent for generic questions
llm_agent = Agent(model, system_prompt="Answer concisely.")
