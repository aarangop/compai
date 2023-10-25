import google.generativeai as palm
from google.generativeai.types import Model, Completion

from compaipair.utils import configure_palm_api

prompt_template = """
{priming}
{question}
{decorator}
"""


class CompaiCompletion:
    model: Model
    priming: str
    question: str
    decorator: str
    result: Completion

    def __init__(
        self,
        model: Model,
        question: str,
        priming: str = "",
        decorator: str = "",
        temperature: float = 0.7,
    ):
        self.model = model
        self.question = question
        self.priming = priming
        self.decorator = decorator
        self.temperature = temperature

    def complete(self):
        configure_palm_api()
        return palm.generate_text(
            prompt=self.prompt, model=self.model, temperature=self.temperature
        )

    @property
    def prompt(self):
        return prompt_template.format(
            priming=self.priming, question=self.question, decorator=self.decorator
        ).strip()
