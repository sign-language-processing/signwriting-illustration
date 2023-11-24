# ControlNet

Following: https://github.com/lllyasviel/ControlNet/blob/main/docs/train.md


## Training

Run `train.sh` using slurm.

```bash
sbatch train.sh
```

It will save intermediate images in `image_log`.

```bash
rsync -avz --progress s3it:/home/amoryo/sign-language/signwriting-illustration/signwriting_illustration/controlnet/ControlNet/image_log ControlNet/
```