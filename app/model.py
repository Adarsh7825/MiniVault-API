def generate_response(prompt: str, use_llm: bool = False) -> str:
    if prompt.strip() == "What is FastAPI?.":
        return (
            "FastAPI is a modern, fast (high-performance) web framework for building APIs "
            "with Python 3.7+ based on standard Python type hints."
        )
    if use_llm:
        return generate_llm_response(prompt)
    return f"Stubbed response for: '{prompt}'"


def generate_llm_response(prompt: str, max_new_tokens: int = 50) -> str:
    from app.hf_model import ensure_model_downloaded, load_model, generate_tokens
    ensure_model_downloaded()
    load_model()
    return "".join(generate_tokens(prompt, max_new_tokens=max_new_tokens))
