from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.model import generate_response, generate_llm_response
from app.logger import log_interaction
import time

router = APIRouter()


class Prompt(BaseModel):
    prompt: str
    stream: bool = False
    use_llm: bool = False


@router.post("/generate", tags=["Generation"])
async def generate(prompt: Prompt, request: Request):
    if prompt.use_llm:
        if prompt.stream:
            from app.hf_model import ensure_model_downloaded, load_model, generate_tokens
            ensure_model_downloaded()
            load_model()

            def token_stream():
                for token in generate_tokens(prompt.prompt):
                    yield token
            log_interaction(prompt.prompt, "[streamed LLM response]")
            return StreamingResponse(token_stream(), media_type="text/plain")
        else:
            response_text = generate_llm_response(prompt.prompt)
            log_interaction(prompt.prompt, response_text)
            return {"response": response_text}
    else:
        response_text = generate_response(prompt.prompt)
        log_interaction(prompt.prompt, response_text)
        if prompt.stream:
            def word_stream():
                for word in response_text.split():
                    yield word + " "
                    time.sleep(0.15)
            return StreamingResponse(word_stream(), media_type="text/plain")
        return {"response": response_text}
