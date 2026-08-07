import json
from typing import Type, TypeVar, cast
from pydantic import BaseModel, ValidationError
# pyrefly: ignore [missing-import]
from groq import Groq
# pyrefly: ignore [missing-import]
from groq.types.chat import ChatCompletionMessageParam
from config.settings import settings

T = TypeVar('T', bound=BaseModel)

class LLMProvider:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.LLM_MODEL

    def generate_structured_output(
        self, 
        system_prompt: str, 
        user_prompt: str, 
        response_model: Type[T]
    ) -> T:
        schema = response_model.model_json_schema()
        
        schema_instruction = (
            f"\n\nYou must respond ONLY with a valid JSON object that exactly matches "
            f"the following JSON schema:\n{json.dumps(schema, indent=2)}"
        )
        
        full_system_prompt = system_prompt + schema_instruction
        
        messages: list[ChatCompletionMessageParam] = [
            cast(ChatCompletionMessageParam, {"role": "system", "content": full_system_prompt}),
            cast(ChatCompletionMessageParam, {"role": "user", "content": user_prompt})
        ]

        try:
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=0.0, 
                response_format={"type": "json_object"}
            )
            
            response_content = chat_completion.choices[0].message.content
            if not response_content:
                raise RuntimeError("Received empty response from LLM.")
                
            return response_model.model_validate_json(response_content)
            
        except ValidationError as e:
            raise RuntimeError(f"LLM output failed Pydantic validation: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"LLM API call failed: {str(e)}")

llm_provider = LLMProvider()