---
title: Exponential Smoothing for Supply Chain Forecasting
emoji: 📈
colorFrom: blue
colorTo: green
sdk: gradio
app_file: app.py
python_version: 3.10
requirements_file: requirements.txt
---

# Exponential Smoothing Forecasting via Model Context Protocol (MCP)

This repository contains the implementation for our research on provisioning established statistical methods to Large Language Model (LLM) agents. It features a Gradio web application that provides an interactive demonstration of Exponential Smoothing for time-series forecasting, using a real-world Supply Chain Management (SCM) dataset.

## Research Context and Motivation

This project serves as a proof-of-concept for research aimed at enhancing LLM-based assistants with robust, traditional statistical capabilities. While LLMs excel at reasoning and language, they are not inherently reliable for precise mathematical forecasting.

Our central hypothesis is that by encapsulating trusted statistical models (like Exponential Smoothing) as tools and serving them via the **Model Context Protocol (MCP)**, we can create AI agents that are both conversational and quantitatively sound. This approach allows an LLM to "call" the statistical tool when a user asks for a forecast, grounding its response in a proven algorithm.

## System Architecture

The system is designed with a clear separation of concerns, enabling the LLM to leverage a specialized forecasting tool:

```
+-----------+       +------------------+       +---------------------+
|   User    | <---> |  Gradio Web App  | <---> |   LLM-based Agent   |
+-----------+       +------------------+       +----------+----------+
                                                          |
                                  (MCP Request: "Forecast SKU X")
                                                          |
                                                 +--------v--------+
                                                 |    MCP Server   |
                                                 | (Python/Flask)  |
                                                 +--------+--------+
                                                          |
                                              +-----------v-----------+
                                              | Exponential Smoothing |
                                              |   (statsmodels)       |
                                              +-----------------------+
```

## Live Demo (Hugging Face Space)

You can try out the live Gradio application hosted on Hugging Face Spaces. This demo allows you to select a product and visualize its demand forecast.

**[Visit the Hugging Face Space here!](YOUR_HUGGING_FACE_SPACE_URL_HERE)**
*(e.g., https://huggingface.co/spaces/your-username/expo-smooth-mcp)*

## GitHub Repository

The complete source code for this project is hosted publicly on GitHub. You are welcome to explore the implementation, open issues, or suggest improvements.

**[Visit the GitHub Repository here!](YOUR_GITHUB_REPO_URL_HERE)**
*(e.g., https://github.com/your-username/expo-smooth-mcp)*

## Dataset

This demonstration uses a real-world public dataset to ensure the results are relevant and reproducible.

*   **Title:** FMCG Sales Demand Forecasting and Optimization
*   **Source:** Kaggle
*   **Link:** [https://www.kaggle.com/datasets/krishanukalita/fmcg-sales-demand-forecasting-and-optimization](https://www.kaggle.com/datasets/krishanukalita/fmcg-sales-demand-forecasting-and-optimization)
*   **Description:** The dataset contains daily order quantities for various products across different warehouses, making it ideal for demonstrating time-series forecasting.

## Getting Started (Local Development)

To set up and run this project on your local machine, please follow the instructions below.

### For External Contributors (Recommended Method)

If you are contributing for the first time or prefer using standard Python virtual environments, this is the recommended approach.

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/maksim-tsi/expo-smooth-mcp.git
    cd expo-smooth-mcp
    ```

2.  **Create and Activate a Virtual Environment:**
    We recommend using `venv`, which is included with Python.
    ```bash
    # Create the environment
    python -m venv venv

    # Activate the environment
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    Install all required packages using `pip`.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Gradio Application:**
    ```bash
    python app.py
    ```
    Access the application in your browser at the local URL provided (e.g., `http://127.0.0.1:7860/`).

---

<details>
<summary><b>Alternative Setup for Conda Users</b></summary>

If you prefer using `conda` for environment management, you can follow these steps to create a new, dedicated environment for this project.

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/maksim-tsi/expo-smooth-mcp.git
    cd expo-smooth-mcp
    ```

2.  **Create and Activate a Conda Environment:**
    This command creates a new environment named `expo-smooth-mcp` with the specified Python version.
    ```bash
    conda create --name expo-smooth-mcp python=3.10 -y
    conda activate expo-smooth-mcp
    ```

3.  **Install Dependencies:**
    Once the environment is active, install the required packages using `pip`.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Gradio Application:**
    ```bash
    python app.py
    ```

</details>

<br>

<details>
<summary><b>For the Core Development Team (Internal)</b></summary>

This section is for the core team using the pre-configured `tsi` conda environment.

1.  **Clone the Repository (if you haven't already):**
    ```bash
    git clone git@github.com-alternative:maksim-tsi/expo-smooth-mcp.git
    cd expo-smooth-mcp
    ```

2.  **Activate the Shared Environment:**
    ```bash
    conda activate tsi
    ```

3.  **Sync Dependencies:**
    Even when using a shared environment, it's crucial to ensure you have the exact package versions for this project. This command will update/install the necessary dependencies within the active `tsi` environment.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Gradio Application:**
    ```bash
    python app.py
    ```

</details>

## Contribution

Contributions to this research project are welcome. Please feel free to fork the repository, create a new branch for your feature or bug fix, and submit a Pull Request.

## Citation

*A placeholder for our future publication will be added here upon acceptance.*