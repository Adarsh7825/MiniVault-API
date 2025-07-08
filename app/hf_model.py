import torch
from pathlib import Path
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    RepetitionPenaltyLogitsProcessor,
    LogitsProcessorList,
)

MODEL_NAME = "distilgpt2"
MODEL_DIR = Path("./models") / MODEL_NAME

tokenizer = None
model = None


def ensure_model_downloaded():
    if not MODEL_DIR.exists() or not (MODEL_DIR / "tokenizer_config.json").exists():
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        _model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
        MODEL_DIR.mkdir(parents=True, exist_ok=True)
        _tokenizer.save_pretrained(str(MODEL_DIR))
        _model.save_pretrained(str(MODEL_DIR))


def load_model():
    global tokenizer, model
    tokenizer = AutoTokenizer.from_pretrained(str(MODEL_DIR))
    model = AutoModelForCausalLM.from_pretrained(str(MODEL_DIR))
    model.eval()


@torch.no_grad()
def generate_tokens(prompt: str, max_new_tokens: int = 50):
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    output_ids = input_ids
    repetition_penalty = 1.2
    logits_processor = LogitsProcessorList([
        RepetitionPenaltyLogitsProcessor(penalty=repetition_penalty)
    ])
    for _ in range(max_new_tokens):
        outputs = model(output_ids)
        logits = outputs.logits[:, -1, :]
        logits = logits_processor(output_ids, logits)
        next_token_id = torch.argmax(logits, dim=-1).unsqueeze(0)
        output_ids = torch.cat([output_ids, next_token_id], dim=1)
        token = tokenizer.decode(next_token_id[0])
        yield token
        if tokenizer.eos_token_id is not None and next_token_id.item() == tokenizer.eos_token_id:
            break
