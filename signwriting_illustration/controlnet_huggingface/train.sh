#!/bin/bash

#SBATCH --job-name=train-controlnet-hf
#SBATCH --time=168:00:00
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
huggingface-cli login --token $HUGGINGFACE_TOKEN

# Convert to huggingface dataset
HF_DATASET_DIR="/scratch/$(whoami)/signwriting-illustration"
mkdir -p $HF_DATASET_DIR

[ ! -f "$HF_DATASET_DIR/dataset_dict.json" ] && \
python dataset.py --train-path="../../train" \
    --output-path="$HF_DATASET_DIR"

# Verify GPU with PyTorch
python3 -c "import torch; print(torch.cuda.is_available())"

CURRENT_DIR=$(pwd)

CACHE_DIR="/scratch/$(whoami)/huggingface/cache"
mkdir -p $CACHE_DIR

# Download diffusers repository if not exists
[ ! -d "diffusers" ] && \
git clone https://github.com/huggingface/diffusers.git

# Install diffusers
pip install ./diffusers

OUTPUT_DIR="/scratch/$(whoami)/models/sd-controlnet-signwriting"
mkdir -p $OUTPUT_DIR

! accelerate launch diffusers/examples/controlnet/train_controlnet.py \
 --pretrained_model_name_or_path="runwayml/stable-diffusion-v1-5" \
 --output_dir="$OUTPUT_DIR" \
 --train_data_dir="$HF_DATASET_DIR" \
 --conditioning_image_column=control_image \
 --image_column=image \
 --caption_column=caption \
 --resolution=512 \
 --learning_rate=1e-5 \
 --validation_image "./validation/0a4b3c71265bb3a726457837428dda78.png" "./validation/0a5922fe2c638e6776bd62f623145004.png" "./validation/1c9f1a53106f64c682cf5d009ee7156f.png" \
 --validation_prompt "An illustration of a man with short hair" "An illustration of a woman with short hair" "An illustration of Barack Obama" \
 --train_batch_size=4 \
 --num_train_epochs=500 \
 --tracker_project_name="sd-controlnet-signwriting" \
 --hub_model_id="sign/signwriting-illustration" \
 --enable_xformers_memory_efficient_attention \
 --checkpointing_steps=5000 \
 --validation_steps=1000 \
 --report_to wandb \
 --push_to_hub

# srun --pty -n 1 -c 2 --time=01:00:00 --gres=gpu:1 --constraint=GPUMEM80GB --mem=128G bash -l