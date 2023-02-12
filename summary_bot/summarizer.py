import logging

import torch
from transformers import BartForConditionalGeneration, AutoTokenizer, pipeline

logging.info("Loading the summarization models")

# MODEL_NAME = "facebook/bart-large-cnn"
MODEL_NAME = "sshleifer/distilbart-cnn-12-6"
MAX_TOKENS = 1024
model = BartForConditionalGeneration.from_pretrained(MODEL_NAME)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)


def _prettify_one_line(line: str) -> str:
    if line.startswith("."):
        line = line[1:]
    return line.strip()


def prettify(text: str) -> str:
    parts = [_prettify_one_line(part) for part in text.split(" .") if len(part) > 3]
    return ".\n".join(parts)


async def summarize_article(content: str, message=None) -> str:
    """
    Summarize the article with Hugging Face's Bart model
    """
    content_parts_dict = await prepare_batch(content, message)
    content_parts_summaries_encoded = model.generate(
        content_parts_dict["input_ids"],
        num_beams=3,
        min_length=50,
        max_length=200,
        early_stopping=True,
    )
    content_parts_summaries = tokenizer.batch_decode(
        content_parts_summaries_encoded,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    )
    summary = "\n".join(
        [
            prettify(content_parts_summary)
            for content_parts_summary in content_parts_summaries
        ]
    )
    return summary


async def prepare_batch(content, message):
    # Create a batch of text parts of max size
    # https://towardsdatascience.com/how-to-apply-transformers-to-any-length-of-text-a5601410af7f

    inputs = tokenizer.encode_plus(
        content, return_tensors="pt", add_special_tokens=False
    )
    input_id_chunks = list(inputs["input_ids"][0].split(MAX_TOKENS - 2))
    mask_chunks = list(inputs["attention_mask"][0].split(MAX_TOKENS - 2))
    num_parts = len(input_id_chunks)
    print("Len", num_parts)
    if message:
        await message.reply(f"The article is long, splitting into {num_parts} parts...")
    # get required padding length
    for i in range(num_parts):
        pad_len = MAX_TOKENS - 2 - input_id_chunks[i].shape[0]
        # check if tensor length satisfies required chunk size
        if pad_len > 0:
            # if padding length is more than 0, we must add padding
            input_id_chunks[i] = torch.cat(
                [input_id_chunks[i], torch.Tensor([0] * pad_len)]
            )
            mask_chunks[i] = torch.cat([mask_chunks[i], torch.Tensor([0] * pad_len)])
    input_ids = torch.stack(input_id_chunks)
    attention_mask = torch.stack(mask_chunks)
    return {"input_ids": input_ids.long(), "attention_mask": attention_mask.int()}
