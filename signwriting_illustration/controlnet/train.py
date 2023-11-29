from pathlib import Path
import argparse
# from ControlNet.share import *

import pytorch_lightning as pl
from torch.utils.data import DataLoader
from dataset import MyDataset
from cldm.logger import ImageLogger
from cldm.model import create_model, load_state_dict


def main(train_path: Path, resume_path: Path):
    # Configs
    batch_size = 32
    logger_freq = 300
    learning_rate = 1e-5
    sd_locked = False
    only_mid_control = False

    # First use cpu to load models. Pytorch Lightning will automatically move it to GPUs.
    model = create_model('./models/cldm_v21.yaml').cpu()
    model.load_state_dict(load_state_dict(resume_path, location='cpu'))
    model.learning_rate = learning_rate
    model.sd_locked = sd_locked
    model.only_mid_control = only_mid_control

    # Misc
    dataset = MyDataset(train_path)
    dataloader = DataLoader(dataset, num_workers=0, batch_size=batch_size, shuffle=True)
    logger = ImageLogger(batch_frequency=logger_freq)
    trainer = pl.Trainer(gpus=1, precision=32, callbacks=[logger])

    # Train!
    trainer.fit(model, dataloader)


if __name__ == "__main__":
    # argparse: train-path resume-path
    parser = argparse.ArgumentParser()
    parser.add_argument("--train-path", type=str, required=True)
    parser.add_argument("--resume-path", type=str, required=True)
    args = parser.parse_args()

    train_path = Path(args.train_path)
    resume_path = Path(args.resume_path)

    main(train_path, resume_path)
