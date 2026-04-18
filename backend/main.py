import modal
import base64
import os
import boto3
import uuid
import boto3
from typing import List

from pydantic import BaseModel






app = modal.App("music-gen")

# docker image with all dependencies installed

image = {
    modal.Image.debian_slim()
    .apt_install("git")
    .pip_install("requirements.txt")
    .run_commands(["git clone https://github.com/ace-step/ACE-Step.git /tmp/ACE-Step", "cd /tmp/ACE-Step && pip install ."])
    .env({"HF_HOME": "/.cache/huggingface"})
}


# music genserver

class MusicGenServer():
    @modal.enter()
    def load_model(self):
        from acestep.pipelines import ACEStepPipeline

