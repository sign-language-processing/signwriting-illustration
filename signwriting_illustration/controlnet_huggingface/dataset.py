import json
import argparse
from pathlib import Path
from PIL import Image

import datasets


class SignWritingIllustrationDataset(datasets.GeneratorBasedBuilder):
    def __init__(self, train_path: Path, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.data = []
        self.train_path = train_path
        with open(train_path / 'prompt.json', 'rt') as f:
            for line in f:
                self.data.append(json.loads(line))

    def _info(self):
        return datasets.DatasetInfo(
            dataset_name="sw_illustration_hf",
            features=datasets.Features(
                {
                    "control_image": datasets.Image(),
                    "image": datasets.Image(),
                    "caption": datasets.Value(dtype='string', id=None)
                }
            )
        )

    def _split_generators(self, dl_manager):
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={})
        ]

    def _generate_examples(self, **unused_kwargs):
        for i, item in enumerate(self.data):
            signwriting = Image.open(str(self.train_path / item['source']))
            illustration = Image.open(str(self.train_path / item['target']))

            yield i, {
                "control_image": signwriting,
                "image": illustration,
                "caption": item['prompt']
            }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train-path", type=str, required=True)
    parser.add_argument("--output-path", type=str, required=True)
    args = parser.parse_args()

    train_path = Path(args.train_path)
    output_path = Path(args.output_path)

    output_path.mkdir(parents=True, exist_ok=True)

    dataset = SignWritingIllustrationDataset(train_path)
    dataset.download_and_prepare(output_path)
    dataset.as_dataset().save_to_disk(output_path)
