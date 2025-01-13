# Import necessary libraries
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

# Import the application configuration
from config import configure

# Load the application settings using a configuration utility
settings = configure()

# Create a FastAPI instance
app = FastAPI()


# Define a response model using Pydantic for structured output
class ResponseModel(BaseModel):
    message: str


# Function to generate a greeting message
def greet(name: str) -> str:
    """
    Generate a greeting message for the given name.

    Args:
        name (str): The name to greet.

    Returns:
        str: A greeting message.
    """
    return f"Hello {name}"


# Define a health check endpoint
@app.get("/hello/health", response_model=ResponseModel)
def health_handler():
    """
    Health check endpoint to verify if the API is running.

    Returns:
        ResponseModel: A message confirming the API's health.
    """
    return ResponseModel(message="Ok")


# Define a dynamic greeting endpoint
@app.get("/hello/{name}", response_model=ResponseModel)
def hello_handler(name: str) -> ResponseModel:
    """
    Endpoint to greet a user with a custom name.

    Args:
        name (str): The name to greet.

    Returns:
        ResponseModel: A greeting message.
    """
    return ResponseModel(message=greet(name))


# Define a root endpoint to handle the base URL
@app.get("/", response_model=ResponseModel)
def root_handler():
    """
    Root endpoint to provide a welcome message.

    Returns:
        ResponseModel: A welcome message.
    """
    return ResponseModel(message="Welcome to the FastAPI app!")


# Define a static /hello endpoint for user-friendly access
@app.get("/hello", response_model=ResponseModel)
def hello_root_handler():
    """
    Static /hello endpoint to provide a generic greeting message.

    Returns:
        ResponseModel: A generic greeting message.
    """
    return ResponseModel(message="Welcome to the hello endpoint!")


# Main entry point to run the application
if __name__ == "__main__":
    """
    Run the FastAPI application using Uvicorn.

    Host: 0.0.0.0 (listens on all network interfaces)
    Port: Defined in the application settings
    Log Level: Configurable via application settings
    """
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=settings.port,
        log_level=settings.log_level(),
    )
