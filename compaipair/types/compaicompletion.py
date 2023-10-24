import google.generativeai as palm
from google.generativeai.types import Model, Completion

from compaipair.utils import configure_palm_api


class CompaiCompletion:
    model: Model
    priming: str
    question: str
    decorator: str
    result: Completion

    @configure_palm_api
    def __init__(
        self,
        model: Model,
        question: str,
        priming: str = None,
        decorator: str = None,
        temperature: float = 0.7,
    ):
        self.model = model
        self.question = question
        self.priming = priming
        self.decorator = decorator
        self.temperature = temperature

    def complete(self):
        return palm.generate_text(
            prompt=self.prompt, model=self.model, temperature=self.temperature
        )

    @property
    def prompt(self):
        return f"{self.priming}\n{self.question}\n{self.decorator}"
