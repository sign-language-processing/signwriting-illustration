#!/bin/bash

#SBATCH --job-name=train-controlnet-img2img
#SBATCH --time=120:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=16GB
#SBATCH --output=controlnet-job.out

#SBATCH --ntasks=1
#SBATCH --gres gpu:1
#SBATCH --constraint=GPUMEM80GB

set -e # exit on error
set -x # echo commands

module load gpu
module load cuda

module load anaconda3
source activate diffusers

# Install dependencies
pip install diffusers transformers accelerate xformers wandb datasets argparse torchvision huggingface-hub

# Create accelerate config
mkdir -p ~/.cache/huggingface/accelerate
cat > ~/.cache/huggingface/accelerate/default_config.yaml << EOF
compute_environment: LOCAL_MACHINE
distributed_type: NO
downcast_bf16: 'no'
gpu_ids: '0'
machine_rank: 0
main_training_function: main
mixed_precision: fp16
num_machines: 1
num_processes: 1
rdzv_backend: static
same_network: true
tpu_env: []
tpu_use_cluster: false
tpu_use_sudo: false
use_cpu: false
EOF

# Convert to huggingface dataset
HF_DATASET_DIR="/scratch/$(whoami)/signwriting-illustration"
mkdir -p $HF_DATASET_DIR

[ ! -f "$HF_DATASET_DIR/dataset_dict.json" ] && \
python dataset.py --train-path="../../train" \
    --output-path="$HF_DATASET_DIR"

# Verify GPU with PyTorch
python3 -c "import torch; print(torch.cuda.is_available())"

CURRENT_DIR=$(pwd)

# cache download deprecated in new version of huggingface_hub
# CACHE_DIR="/scratch/$(whoami)/huggingface/cache"
# mkdir -p $CACHE_DIR

# Download diffusers repository if not exists
[ ! -d "diffusers" ] && \
git clone https://github.com/huggingface/diffusers.git

# Install diffusers
cd diffusers
pip install -e .
cd ..

OUTPUT_DIR="/scratch/$(whoami)/models/sd-controlnet-img2img"
mkdir -p $OUTPUT_DIR
 
accelerate launch ./diffusers/examples/controlnet/train_controlnet_img2img.py \
 --pretrained_model_name_or_path="runwayml/stable-diffusion-v1-5" \
 --controlnet_model_name_or_path="lllyasviel/sd-controlnet-canny" \
 --output_dir="$OUTPUT_DIR" \
 --train_data_dir="$HF_DATASET_DIR" \
 --conditioning_image_column=control_image \
 --image_column=image \
 --caption_column=caption \
 --resolution=256 \
 --learning_rate=1e-5 \
 --validation_image="$(realpath validation/white_image.png)" \
 --validation_prompt "An illustration of a man with short hair" "An illustration of a woman with short hair" "An illustration of Barack Obama" \
 --train_batch_size=4 \
 --num_train_epochs=500 \
 --tracker_project_name="sd-controlnet-signwriting-img2img" \
 --hub_model_id="sarahahtee/signwriting-illustration-img2img" \
 --enable_xformers_memory_efficient_attention \
 --checkpointing_steps=5000 \
 --validation_steps=1000 \
 --strength=1.0 \
 --controlnet_conditioning_scale=1.0 \
 --mixed_precision="fp16" \
 --scheduler="UniPCMultistep" \
 --report_to="wandb" \
 --push_to_hub 

# export huggingface_token and wandb_api_key in the environment variables
# srun --pty -n 1 -c 2 --time=01:00:00 --gres=gpu:1 --constraint=GPUMEM80GB --mem=128G bash -l