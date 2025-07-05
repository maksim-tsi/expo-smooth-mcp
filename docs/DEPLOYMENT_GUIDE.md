
# Deployment Guide: Hugging Face Spaces

- **Version:** 1.0
- **Status:** Final
- **Last Updated:** 2025-07-05 by Maksim Ilin
- **Summary:** This guide provides the official step-by-step process for deploying the `expo-smooth-mcp` Gradio application to Hugging Face Spaces.

---

## 1. Objective

The purpose of this guide is to ensure a consistent, repeatable, and successful deployment process. Following these steps will publish the current state of the `main` branch to our public-facing demo on Hugging Face Spaces.

## 2. Prerequisites

Before you can deploy, you must have the following set up on your local machine:

1.  **Hugging Face Account:** You must have a registered account on [huggingface.co](https://huggingface.co).
2.  **`huggingface_hub` Library:** This library provides the command-line interface (CLI) for interacting with the Hub. If you haven't installed it, run:
    ```bash
    pip install "huggingface_hub[cli]"
    ```
3.  **CLI Login:** You must be logged into your Hugging Face account via the CLI. Run the following command and enter your credentials. You will need an Access Token with `write` permissions, which you can generate from your Hugging Face account settings.
    ```bash
    huggingface-cli login
    ```
4.  **Local Git Repository:** You must have a local clone of the project repository.

## 3. One-Time Setup: Connecting the Git Remote

You only need to perform this step once per local clone of the repository. This command links our local repository to the Hugging Face Spaces Git repository.

1.  Navigate to your local project directory:
    ```bash
    cd /path/to/expo-smooth-mcp
    ```

2.  Add the Hugging Face repository as a new remote. We will name it `hf` for clarity. (Replace `YOUR_USERNAME` and `YOUR_SPACE_NAME` with the actual values).
    ```bash
    git remote add hf https://YOUR_USERNAME:YOUR_HF_TOKEN@huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
    ```
    **Example:**
    ```bash
    # Replace skazo4ny with your username and expo-smooth-mcp with your space name
    git remote add hf https://skazo4ny:hf_..._token...@huggingface.co/spaces/skazo4ny/expo-smooth-mcp
    ```

## 4. Pre-Deployment Checklist

Before pushing, ensure the following are correct. A failure in these checks is the most common reason for a deployment to be rejected.

*   **`README.md` Metadata:** Open the `README.md` file and verify the YAML metadata block at the very top.
    *   `sdk: gradio` must be present.
    *   `app_file: app.py` must point to our main application file.
    *   **Colors:** The `colorFrom` and `colorTo` values **must** be from the approved list: `[red, yellow, green, blue, indigo, purple, pink, gray]`.
    *   **Example (Correct):**
        ```yaml
        ---
        title: Exponential Smoothing for Supply Chain Forecasting
        emoji: 📈
        colorFrom: blue
        colorTo: green
        sdk: gradio
        app_file: app.py
        ---
        ```

*   **`requirements.txt`:** Ensure all required packages are listed in this file. The Hugging Face platform uses this file to build the environment.

*   **Local Changes:** All your local changes must be committed to Git. Run `git status` to ensure your working directory is clean.

## 5. The Deployment Command

Once the pre-deployment checklist is complete, you can deploy the application.

The command pushes the current state of your local `HEAD` (your latest commit) to the `main` branch of the Hugging Face remote (`hf`).

```bash
git push hf HEAD:main
```

**Note on Forcing Pushes:** It is sometimes necessary to use `--force` if the remote history has diverged. However, this should be used with caution. The standard command above is preferred.
**Example Force Push:** `git push hf HEAD:main --force`

After running the command, the Hugging Face platform will start building your application. You can monitor the build process and see any logs directly on your Space's page. If the build is successful, your application will be live.