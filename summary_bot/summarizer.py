import logging

import torch
from transformers import BartForConditionalGeneration, AutoTokenizer

# MODEL_NAME = "facebook/bart-large-cnn"
DEFAULT_MODEL_NAME = "sshleifer/distilbart-cnn-12-6"


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class SummaryModel(metaclass=Singleton):
    def __init__(self, model_name, max_tokens=1024):
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.model, self.tokenizer = self.load_model()

    @staticmethod
    def get_model_args():
        return {
            "num_beams": 3,
            "min_length": 50,
            "max_length": 200,
            "early_stopping": True,
        }

    @staticmethod
    def get_tokenizer_args():
        return {
            "skip_special_tokens": True,
            "clean_up_tokenization_spaces": False,
        }

    def load_model(self):
        logging.info(f"Loading the summarization model {self.model_name}")
        model = BartForConditionalGeneration.from_pretrained(self.model_name)
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        model.eval()
        return model, tokenizer

    async def prepare_batch(self, content, message):
        # Create a batch of text parts of max size
        # https://towardsdatascience.com/how-to-apply-transformers-to-any-length-of-text-a5601410af7f

        inputs = self.tokenizer.encode_plus(
            content, return_tensors="pt", add_special_tokens=False
        )
        input_id_chunks = list(inputs["input_ids"][0].split(self.max_tokens - 2))
        mask_chunks = list(inputs["attention_mask"][0].split(self.max_tokens - 2))
        num_parts = len(input_id_chunks)
        print("Len", num_parts)
        if message:
            await message.reply(
                f"The article is long, splitting into {num_parts} parts..."
            )
        # get required padding length
        for i in range(num_parts):
            pad_len = self.max_tokens - 2 - input_id_chunks[i].shape[0]
            # check if tensor length satisfies required chunk size
            if pad_len > 0:
                # if padding length is more than 0, we must add padding
                input_id_chunks[i] = torch.cat(
                    [input_id_chunks[i], torch.Tensor([0] * pad_len)]
                )
                mask_chunks[i] = torch.cat(
                    [mask_chunks[i], torch.Tensor([0] * pad_len)]
                )
        input_ids = torch.stack(input_id_chunks)
        attention_mask = torch.stack(mask_chunks)
        return {"input_ids": input_ids.long(), "attention_mask": attention_mask.int()}

    def get_summary(self, input_dict: dict):
        summary_encoded = self.model.generate(
            input_dict["input_ids"], **self.get_model_args()
        )
        summary = self.tokenizer.batch_decode(
            summary_encoded, **self.get_tokenizer_args()
        )
        return summary


def _prettify_one(line: str) -> str:
    if line.startswith("."):
        line = line[1:]
    return line.strip()


def prettify(text: str) -> str:
    parts = [_prettify_one(part) for part in text.split(" .") if len(part) > 3]
    return ".\n".join(parts)


async def summarize_article(
    content: str, message=None, model_name=DEFAULT_MODEL_NAME
) -> str:
    """
    Summarize the article with Hugging Face's Bart model
    """
    model = SummaryModel(model_name)
    content_parts_dict = await model.prepare_batch(content, message)
    content_parts_summaries = model.get_summary(content_parts_dict)
    summary = "\n".join([prettify(summary) for summary in content_parts_summaries])
    return summary
