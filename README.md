# ACE-step-music-gen

This repository contains an AI music generation application using the ACE-Step model.

## Overview
The application is designed to run on [Modal](https://modal.com/), utilizing serverless GPUs to deploy and run the AI model. The main application configures a container environment with the necessary dependencies (PyTorch, Transformers, Diffusers, etc.) to perform music generation.

## Project Structure

- `backend/`: Contains the backend code and Modal application definitions.
  - `main.py`: The entrypoint for the Modal application (`music-gen`). Sets up the environment, clones the ACE-Step repository, and defines the `MusicGenServer` which loads the `ACEStepPipeline`.
  - `prompts.py`: Code or configurations related to music generation prompt schemas.
  - `requirements.txt`: Python dependencies needed for the application.

## Prerequisites

- [Python 3.x](https://www.python.org/)
- A [Modal](https://modal.com/) account for deploying the serverless functions.
- (Optional) AWS account if using `boto3` for S3 storage integrations as implied by dependencies.

## Setup & Deployment

1. Install the required Python packages (if running or testing pieces locally):
   ```bash
   pip install -r backend/requirements.txt
   ```

2. Make sure you have `modal` installed and authenticated with your Modal account:
   ```bash
   pip install modal
   modal setup
   ```

3. Run or deploy the application to Modal:
   ```bash
   modal run backend/main.py
   ```
   *(Note: The exact command might differ depending on how your Modal web endpoints or functions are exposed within `main.py`.)*
