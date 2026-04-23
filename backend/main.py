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
        from transformers import AutoTokenizer, AutoModelForCausalLM
        from diffusers import AutoPipelineForText2Audio
        import torch

        #music generation model from ACE-Step
        self.music_model = ACEStepPipeline(
            checkpoint_dir = "/models",
            dtype = "bfloat16",
            torch_compile = False,
            cpu_offload = False,
            overlapped_decode = False
        )

        #large language model for text processing

        self.tokenizer = AutoTokenizer.from_pretrained(model_id)

        self.llm_model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype="auto",
            device_map="auto",
            cache_dir="/.cache/huggingface"
        )

 # Stable Diffusion Model (thumbnails)
        self.image_pipe = AutoPipelineForText2Image.from_pretrained(
            "stabilityai/sdxl-turbo", torch_dtype=torch.float16, variant="fp16", cache_dir="/.cache/huggingface")
        self.image_pipe.to("cuda")



@app.local_entrypoint()
def main():
    server = MusicGenServer()
    endpoint_url = server.generate_with_described_lyrics.get_web_url()

    request_data = GenerateWithDescribedLyricsRequest(
        prompt="rave, funk, 140BPM, disco",
        described_lyrics="lyrics about water bottles",
        guidance_scale=15
    )

    payload = request_data.model_dump()

    response = requests.post(endpoint_url, json=payload)
    response.raise_for_status()
    result = GenerateMusicResponseS3(**response.json())

    print(
        f"Success: {result.s3_key} {result.cover_image_s3_key} {result.categories}")