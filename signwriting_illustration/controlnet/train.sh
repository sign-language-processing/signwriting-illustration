#!/bin/bash

#SBATCH --job-name=train-nlcontrolnetlb
#SBATCH --time=168:00:00
#SBATCH --cpus-per-task=8
#SBATCH --mem=32GB
#SBATCH --output=controlnet-job.out

#SBATCH --ntasks=1
#SBATCH --gres gpu:1
#SBATCH --constraint=GPUMEM80GB

set -e # exit on error
set -x # echo commands

module load gpu
module load cuda

module load anaconda3
source activate controlnet

CURRENT_DIR=$(pwd)

# Verify GPU with PyTorch
python3 -c "import torch; print(torch.cuda.is_available())"

MODELS_DIR="/scratch/$(whoami)/huggingface/models/"
mkdir -p $MODELS_DIR

# Download Stable Diffusion Checkpoint
STABLE_DIFFUSION_PATH="$MODELS_DIR/v2-1_512-ema-pruned.ckpt"
[ ! -f "$STABLE_DIFFUSION_PATH" ] && \
wget -O "$STABLE_DIFFUSION_PATH" https://huggingface.co/stabilityai/stable-diffusion-2-1-base/resolve/main/v2-1_512-ema-pruned.ckpt

# Download ControlNet repository if not exists
[ ! -d "ControlNet" ] && \
git clone https://github.com/lllyasviel/ControlNet.git

conda env update --name controlnet --file ControlNet/environment.yaml

# Remove old training files
rm -f ControlNet/dataset.py
rm -f ControlNet/train.py

# Copy training files
cp dataset.py ControlNet/dataset.py
cp train.py ControlNet/train.py

cd ControlNet

# Add ControlNet to the checkpoint
STABLE_CONTROLNET_PATH="$MODELS_DIR/control_sd21_ini.ckpt"
[ ! -f "$STABLE_CONTROLNET_PATH" ] && \
python tool_add_control_sd21.py "$STABLE_DIFFUSION_PATH" "$STABLE_CONTROLNET_PATH"

# Symlink lightning_logs
[ ! -d "$MODELS_DIR/lightning_logs" ] && \
mkdir -p "$MODELS_DIR/lightning_logs" && \
ln -s "$MODELS_DIR/lightning_logs" lightning_logs

# Train model
python train.py --train-path="../../../train" --resume-path="$STABLE_CONTROLNET_PATH"


# sbatch train.sh
# srun --pty -n 1 -c 2 --time=01:00:00 --gres=gpu:1 --constraint=GPUMEM80GB --mem=128G bash -l
# cd /home/amoryo/sign-language/signwriting-illustration/signwriting_illustration/controlnet

# srun --pty -n 1 -c 2 --time=01:00:00 --gres=gpu:1 --mem=32G bash -l
# cd /home/amoryo/sign-language/signwriting-illustration/signwriting_illustration/controlnet/ControlNet
# conda activate controlnet
# python predict.py --data-path="../../../train" --checkpoint-path="/home/amoryo/sign-language/signwriting-illustration/signwriting_illustration/controlnet/ControlNet/lightning_logs/version_6635784/checkpoints/epoch=499-step=88999.ckpt"
