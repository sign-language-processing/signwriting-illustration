import torch
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, UniPCMultistepScheduler, \
    StableDiffusionControlNetImg2ImgPipeline
from PIL import Image


def get_pipeline(pipeline_cls):
    controlnet = ControlNetModel.from_pretrained("sign/signwriting-illustration", torch_dtype=torch.float16)
    pipe = pipeline_cls.from_pretrained("runwayml/stable-diffusion-v1-5", controlnet=controlnet,
                                        safety_checker=None, torch_dtype=torch.float16)

    # Instead of using Stable Diffusion's default PNDMScheduler,
    # we use one of the currently fastest diffusion model schedulers, called UniPCMultistepScheduler.
    pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)

    # the pipeline automatically takes care of GPU memory management.
    pipe.enable_model_cpu_offload()

    # attention layer acceleration
    pipe.enable_xformers_memory_efficient_attention()

    return pipe


def image_grid(imgs, rows, cols):
    assert len(imgs) == rows * cols

    w, h = imgs[0].size
    grid = Image.new("RGB", size=(cols * w, rows * h))

    for i, img in enumerate(imgs):
        grid.paste(img, box=(i % cols * w, i // cols * h))
    return grid


if __name__ == "__main__":
    PIPELINE = "normal"

    if PIPELINE == "img2img":
        pipeline = get_pipeline(StableDiffusionControlNetImg2ImgPipeline)
    else:
        pipeline = get_pipeline(StableDiffusionControlNetPipeline)

    signwriting_images = [
        Image.new('RGB', (512, 512), 'white'),
        Image.open("controlnet_huggingface/validation/0a4b3c71265bb3a726457837428dda78.png"),
        Image.open("controlnet_huggingface/validation/0a5922fe2c638e6776bd62f623145004.png"),
        Image.open("controlnet_huggingface/validation/1c9f1a53106f64c682cf5d009ee7156f.png"),
    ]

    prompt = "An illustration of a man with short hair, with black arrows."
    negative_prompt = "lowres, text, error, cropped, worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, out of frame, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck, username, watermark, signature"
    seeds = 4
    batch = seeds * len(signwriting_images)

    # Params for pipeline
    batch_prompts = [prompt] * batch
    batch_signwriting_images = [im for im in signwriting_images for _ in range(seeds)]
    batch_negative_prompts = [negative_prompt] * batch
    batch_seeds = [torch.Generator().manual_seed(i)
                   for j in range(len(signwriting_images))
                   for i in range(seeds)]  # 0,1,2,0,1,2,0,1,2...
    num_inference_steps = 20
    strength = 1.0
    guidance_scale = 7.5

    if PIPELINE == "img2img":
        img2img_init = Image.new('RGB', (512, 512), 'white')

        output = pipeline(
            prompt=batch_prompts,
            image=[img2img_init] * batch,
            control_image=batch_signwriting_images,
            negative_prompt=batch_negative_prompts,
            generator=batch_seeds,
            num_inference_steps=num_inference_steps,
            strength=strength,
            controlnet_conditioning_scale=strength,
            guidance_scale=guidance_scale,
        )
    else:
        output = pipeline(
            prompt=batch_prompts,
            image=batch_signwriting_images,
            negative_prompt=batch_negative_prompts,
            generator=batch_seeds,
            num_inference_steps=num_inference_steps,
            strength=strength,
            guidance_scale=guidance_scale,
        )

    # Add SignWriting Sources
    copy_images = list(output.images)
    for i, img in reversed(list(enumerate(signwriting_images))):
        output.images.insert(i * seeds, img)

    grid = image_grid(output.images, len(signwriting_images), seeds + 1)
    grid.save("illustration.png")
