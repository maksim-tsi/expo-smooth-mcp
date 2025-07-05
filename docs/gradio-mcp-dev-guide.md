# How to Build an MCP Server with Gradio

This guide provides a step-by-step process for creating a Model Context Protocol (MCP) server using the Gradio library. This architecture is central to our project, as it allows an LLM agent to call our Exponential Smoothing model as an external tool.

The information is based on the official Gradio documentation on [Building an MCP Server with Gradio](https://www.gradio.app/guides/building-mcp-server-with-gradio).

## 1. What is an MCP Server?

A Model Context Protocol (MCP) server is a standardized way to expose functions (we'll call them "tools") so they can be discovered and used by Large Language Models (LLMs). This allows us to give an LLM capabilities it doesn't have natively, such as performing precise statistical forecasting.

For our project, the MCP server will expose our `exponential_smoothing_forecast` function as a tool that an LLM agent can call.

## 2. Prerequisites

Ensure you have the necessary libraries installed. The `gradio[mcp]` package includes all required dependencies.

```bash
pip install "gradio[mcp]" uvicorn
```
*   `gradio[mcp]`: Provides the core Gradio library and the MCP server SDK.
*   `uvicorn`: A high-performance ASGI server we will use to run our application.

## 3. Step-by-Step Implementation

Creating the server involves three main steps: defining the tool, creating the server instance, and running it.

### Step 1: Define the Tool Function

A tool is simply a Python function. To make it discoverable by the MCP server, it must have a detailed docstring and clear type hints. The MCP server uses this information to tell the LLM what the tool does and what inputs it expects.

Here is a simple example based on the official guide:

```python
import gradio as gr

def letter_counter(word: str, letter: str) -> int:
    """
    Count the number of occurrences of a specific letter in a word or text.

    Args:
        word (str): The input text to search through.
        letter (str): The letter to search for.

    Returns:
        int: The total count of the letter in the word.
    """
    word = word.lower()
    letter = letter.lower()
    count = word.count(letter)
    return count
```
**Key Points:**
*   **Type Hints (`word: str`)**: These are essential for defining the input/output schema for the tool.
*   **Docstring**: The description and the `Args` block are parsed to create the tool's documentation for the LLM.

### Step 2: Create a Gradio Interface

Next, wrap the function in a standard Gradio `Interface`. This will serve as both our web demo and the foundation for the MCP tool.

```python
# (Continuing from the code above)

demo = gr.Interface(
    fn=letter_counter,
    inputs=[gr.Textbox(label="Word", value="strawberry"), gr.Textbox(label="Letter", value="r")],
    outputs=[gr.Number(label="Count")],
    title="Letter Counter",
    description="Enter text and a letter to count how many times the letter appears."
)
```

### Step 3: Launch the MCP Server

To enable the MCP server, you simply add the `mcp_server=True` argument to the `demo.launch()` method.

Create a file named `mcp_server.py` and combine all the pieces:

```python
# mcp_server.py

import gradio as gr

def letter_counter(word: str, letter: str) -> int:
    """
    Count the number of occurrences of a specific letter in a word or text.

    Args:
        word (str): The input text to search through.
        letter (str): The letter to search for.

    Returns:
        int: The total count of the letter in the word.
    """
    word = word.lower()
    letter = letter.lower()
    count = word.count(letter)
    return count

# Create the Gradio interface
demo = gr.Interface(
    fn=letter_counter,
    inputs=[gr.Textbox(label="Word", value="strawberry"), gr.Textbox(label="Letter", value="r")],
    outputs=[gr.Number(label="Count")],
    title="Letter Counter",
    description="Enter text and a letter to count how many times the letter appears."
)

# Launch the Gradio app AND the MCP server
if __name__ == "__main__":
    demo.launch(mcp_server=True)
```

## 4. Running and Testing the Server

To run the server, use `uvicorn`:

```bash
uvicorn mcp_server:demo --reload
```
*   `mcp_server`: The name of your Python file.
*   `demo`: The name of the `gradio.Interface` object inside your file.
*   `--reload`: Useful for development, as it automatically restarts the server when you save changes.

When you run this, you will see URLs for both the Gradio web app (usually `http://127.0.0.1:8000`) and the MCP server endpoint, which will look like:

`http://127.0.0.1:8000/gradio_api/mcp/sse`

You can test the MCP endpoint directly using a `curl` command to simulate a request from an LLM client.

```bash
curl http://127.0.0.1:8000/gradio_api/mcp/sse \
  -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "method": "letter_counter",
        "params": {
          "word": "banana",
          "letter": "a"
        },
        "id": 1
      }'
```

This command directly calls the `letter_counter` tool and should return a JSON response containing the result (`3`). This confirms our MCP server is working correctly.

This guide will serve as the blueprint for our `mcp_server.py` implementation, where our `letter_counter` function will be replaced with our `exponential_smoothing_forecast` logic.