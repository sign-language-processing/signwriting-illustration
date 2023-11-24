# SignWriting Illustration

Based on [sign/translate#114](https://github.com/sign/translate/issues/114).

People without previous SignWriting experience have a hard time understanding SignWriting notation.

This project aims to provide an alternative view to SignWriting, using computer generated illustrations of the signs.

## Data

We use multiple data sources with SignWriting and illustrations:

1. [Vokabeltrainer](datasets/Vokabeltrainer/README.md) - Swiss-German lexicon
2. [SignPuddle LSF-CH](datasets/SignPuddle/README.md) - Swiss-French lexicon

The illustrations are of different people, usually in grayscale.
We use ChatGPT to generate the prompt to describe every illustration.

### Examples

|              |                                   00004                                    |                                   00007                                    |                                   00015                                    |
|:------------:|:--------------------------------------------------------------------------:|:--------------------------------------------------------------------------:|:--------------------------------------------------------------------------:|
|    Video     |  <img src="datasets/Vokabeltrainer/sw_examples/00004.gif" width="150px">   |  <img src="datasets/Vokabeltrainer/sw_examples/00007.gif" width="150px">   |  <img src="datasets/Vokabeltrainer/sw_examples/00015.gif" width="150px">   |
| SignWriting  |   <img src="datasets/Vokabeltrainer/sw_examples/00004.png" width="50px">   |   <img src="datasets/Vokabeltrainer/sw_examples/00007.png" width="50px">   |   <img src="datasets/Vokabeltrainer/sw_examples/00015.png" width="50px">   |
| Illustration | <img src="datasets/Vokabeltrainer/illustrations/00004.png" height="150px"> | <img src="datasets/Vokabeltrainer/illustrations/00007.png" height="150px"> | <img src="datasets/Vokabeltrainer/illustrations/00015.png" height="150px"> | 
|    Prompt    |      An illustration of a person with short hair, with black arrows.       |       An illustration of a woman with short hair, with black arrows.       |      An illustration of a man with short hair. The arrows are black.       |

## Training

### Prompt information

The prompt should include if this is an image or an illustration, if it colored or black and white, man
or woman, hair style, and watermark. (see [train/prompt.json](train/prompt.json) for values)

### Data Preparation

1. `create_images.py` - Generate parallel images - we create parallel files with the same name in directories
   `train/A` and `train/B` to include the SignWriting (B) and illustration (A) in the same resolution (512x512).
2. `create_prompts.py` - Generate prompts - we use ChatGPT to generate the prompt for every illustration.
   All of the prompts are then stored in `train/prompt.json`. (a `JSONL` file
   with `{source: ..., target: ..., prompt: ...}`).
   Cost per 1000 illustrations is about $5.

### Model Training

We train a ControlNet model to control Stable Diffusion given the prompt and SignWriting image, generate the relevant
illustration. This process benefits from the pretrained generative image diffusion model.


## Inference

In inference time, we still give the control image of the new SignWriting image, but can control for the prompt.
For example, we can always say "An illustration of a man with short hair." for consistency of character.
This also removes any watermarks from the data, since watermarked illustrations are prompted with the watermark.



# TODO

3. Align the Vokabeltrainer SignWriting to the illustrations
5. Generate prompts for all illustrations and images
6. Train a model to generate the illustrations from the prompts
