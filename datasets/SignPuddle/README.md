# SignPuddle

The [Swiss-French SignPuddle](https://www.signbank.org/signpuddle2.0/index.php?ui=1&sgn=49) includes around 5000 entries in SignWriting with an illustration.

## Data

We collected the data using `collect_data.py`.

### Issues

Since this data is unstructured, we assume all `png` files are illustrations, and all `jpg` files are pictographs.

This means that we have multiple types of data:

| Type                    | Example                                |
|-------------------------|----------------------------------------|
| Noise                   | ![noise](illustrations/2.png)          |
| No-person Illustration  | ![illustration](illustrations/16.png)  |
| Blurry Illustration     | ![illustration](illustrations/14.png)  |
| HD Illustration         | ![illustration](illustrations/10.png)  |
| HD Colored Illustration | ![illustration](illustrations/379.png) |
| Corrupted               | ![illustration](illustrations/13.png)  |
| Blurry Image + Arrows   | ![illustration](illustrations/22.png)  |
| HD Image                | ![illustration](illustrations/826.png) |

Ideally, we should be able to classify these images, and apply some "tag" in their prompt.
We should not train on corrupted or noise images.

