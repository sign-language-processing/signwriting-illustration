You can browse the web for any information you need.
We are writing an academic paper about the following project:

```md
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
```

Here is information about sign language writing systems (that you can copy to the paper):

```latex
Writing systems represent signs as discrete visual features. Some systems are written
linearly, and others use graphemes in two dimensions. While various
universal
\citep{writing:sutton1990lessons, writing:prillwitz1990hamburg} and
language-specific notation systems
\citep{writing:stokoe2005sign, writing:kakumasu1968urubu, writing:bergman1977tecknad}
have been proposed, no writing system has been adopted widely by any
sign language community, and the lack of standards hinders the exchange
and unification of resources and applications between projects. The
figure above depicts two universal writing systems: SignWriting
\citep{writing:sutton1990lessons}, a two-dimensional pictographic
system, and HamNoSys \citep{writing:prillwitz1990hamburg}, a linear
stream of graphemes designed to be machine-readable.
```

And about notation, we want to say that all notation is bad. all notation has downsides.
If we notate in HamNoSys, it is less easily readable, and more difficult to notate, but is more easily digestable by
computers.
SignWriting is easier to read, but harder to encode on the computer. Illustrations are very easy to read, but time
consuming to create, and are less abstract than the notation systems, sometimes making them unnecessarily complicated.

Different datasets come with various notations, but illustrations are by far the most digestable by humans, requiring no
expert linguistic knowledge.

The paper is titled "Automatic Sign Language Illustration Using SignWriting"

The abstract is:

```latex
\begin{abstract}
The representation of signed languages faces significant challenges due to the complexities of various writing systems. Traditional notations such as HamNoSys and SignWriting, though beneficial, demand specialized linguistic expertise for effective use. This paper introduces a novel methodology that leverages illustrations as a more accessible form of visualization, particularly for those without prior SignWriting experience. We integrate diverse datasets that include parallel SignWriting and corresponding illustrations. Utilizing a ControlNet model, we guide Stable Diffusion in the generation of sign language illustrations from SignWriting inputs. The outcome is a model that can generate clear, intuitive illustrations of sign language, significantly reducing the barriers to understanding and employing sign language notation. Our approach presents a promising new direction in sign language representation, enhancing accessibility and reducing dependence on expert linguistic knowledge.
\end{abstract}
```

Our table of contents is:

1. **Introduction**
    - Overview of sign language writing systems and the challenge of adoption by users. Discussion of the importance and
      potential of sign language illustrations in making notation more accessible (not replacing notation).
    - Discussion of the advantages and limitations of using illustrations over traditional notation systems. 
      Discussion on the impact of this approach on accessibility and understanding of sign language notations.

2. **Background**
    - Examination of existing writing systems for sign languages, focusing on HamNoSys and SignWriting. Discussion of
      their adoption and limitations, and the role of illustrations in sign language representation.
    - Explain what is ControlNet

3. **Data**
    - Description of the data sources, including the characteristics of the SignWriting data and the
      illustrations. Discussion on the diversity and quality of the datasets.
    - Show table of dataset examples

4. **Methodology**
    - Explanation of the technical process, including the generation of parallel images and prompts, and the use of
      ControlNet model with Stable Diffusion.

5. **Inference and Application**
    - Discussion on how the model is used in practice for inference, including the handling of new SignWriting inputs
      and the generation of consistent character illustrations. Show results for new SignWriting.

6. **Conclusions and Future Work**
    - Summarizing the findings, the significance of the project in the broader context, and potential future directions
      for research and application.


Please write the Introduction section. Include references when needed using \cite{??} and placeholders using \fix{@@}: