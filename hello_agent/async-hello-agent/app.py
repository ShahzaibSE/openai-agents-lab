import chainlit as cl
from gemini_service import Agent, Runner, model, config
import json

def safe_serialize(obj, depth=0, max_depth=3, seen=None):
    """Safely serialize an object to JSON by converting non-serializable parts to strings."""
    if seen is None:
        seen = set()
    
    # Handle depth limit
    if depth > max_depth:
        return str(obj)
    
    # Handle circular references
    obj_id = id(obj)
    if obj_id in seen:
        return f"<circular reference to {type(obj).__name__}>"
    seen.add(obj_id)
    
    try:
        if hasattr(obj, '__dict__'):
            return {k: safe_serialize(v, depth + 1, max_depth, seen) for k, v in obj.__dict__.items()}
        elif isinstance(obj, (list, tuple)):
            return [safe_serialize(item, depth + 1, max_depth, seen) for item in obj]
        elif isinstance(obj, dict):
            return {k: safe_serialize(v, depth + 1, max_depth, seen) for k, v in obj.items()}
        else:
            return str(obj)
    finally:
        seen.remove(obj_id)

@cl.on_chat_start
async def start():
    agent = Agent(
        name="HelloAgent",
        model=model,
        instructions="You are a friendly agent that greets users."
    )
    cl.user_session.set("agent", agent)

@cl.on_message
async def main(message: cl.Message):
    agent = cl.user_session.get("agent")
    
    try:
        result = await Runner.run(agent, message.content, run_config=config)
        
        # Debug logging in console
        print("\nResult object inspection:")
        print(json.dumps({
            'type': type(result).__name__,
            'dir': dir(result),
            'dict': {k: str(v) for k, v in result.__dict__.items()},
            'str': str(result)
        }, indent=2))
        
        # Display only the final_output in UI
        if hasattr(result, 'final_output'):
            await cl.Message(content=result.final_output).send()
        else:
            await cl.Message(content=str(result)).send()
            
    except Exception as e:
        error_message = f"Error: {str(e)}"
        if "quota" in str(e).lower():
            error_message += "\n\nYour API quota has been exhausted. Please:\n1. Check your Google AI Studio dashboard for quota status\n2. Wait for quota reset or upgrade your plan\n3. Try using a different API key"
        await cl.Message(content=error_message).send() 