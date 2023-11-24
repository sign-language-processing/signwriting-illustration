"""Adapted from https://github.com/lllyasviel/ControlNet/blob/main/tutorial_dataset.py"""

import json
from pathlib import Path

import cv2
import numpy as np

from torch.utils.data import Dataset


class MyDataset(Dataset):
    def __init__(self, train_path: Path):
        self.data = []
        self.train_path = train_path
        with open(train_path / 'prompt.json', 'rt') as f:
            for line in f:
                self.data.append(json.loads(line))

    def __len__(self):
        return len(self.data)

    def get_raw(self, idx):
        item = self.data[idx]

        source_filename = item['source']
        target_filename = item['target']
        prompt = item['prompt']

        source = cv2.imread(str(self.train_path / source_filename))
        target = cv2.imread(str(self.train_path / target_filename))

        # Do not forget that OpenCV read images in BGR order.
        source = cv2.cvtColor(source, cv2.COLOR_BGR2RGB)
        target = cv2.cvtColor(target, cv2.COLOR_BGR2RGB)

        return dict(jpg=target, txt=prompt, hint=source)

    def __getitem__(self, idx):
        raw = self.get_raw(idx)
        source = raw['hint']
        target = raw['jpg']
        prompt = raw['txt']

        # Normalize source images to [0, 1].
        source = source.astype(np.float32) / 255.0

        # Normalize target images to [-1, 1].
        target = (target.astype(np.float32) / 127.5) - 1.0

        return dict(jpg=target, txt=prompt, hint=source)
