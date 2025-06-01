import asyncio
import nest_asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
import os
import inspect

# Load environment variables from .env file
load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")

if not gemini_key:
    raise ValueError("GEMINI_API_KEY is not set")

print(f"API Key loaded: {gemini_key[:8]}...")  # Only print first 8 chars for security

external_client = AsyncOpenAI(
    api_key=gemini_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash-exp",
    openai_client=external_client,
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,
)

async def main():
    agent = Agent(
        name="HelloAgent",
        model=model,
        instructions="You are a friendly agent that greets users."
    )

    try:
        prompt = input("Enter a prompt: ")
        while prompt != "exit":
            result = await Runner.run(agent, str.lower(prompt), run_config=config)
            print("\nResult:")
            print(result)
            prompt = input("\nEnter a prompt: ")  # Ask for new prompt after each response
            
    except Exception as e:
        print(f"\nError: {str(e)}")
        if "quota" in str(e).lower():
            print("\nYour API quota has been exhausted. Please:")
            print("1. Check your Google AI Studio dashboard for quota status")
            print("2. Wait for quota reset or upgrade your plan")
            print("3. Try using a different API key")

if __name__ == "__main__":
    asyncio.run(main())
    







