import google.generativeai as palm
from google.generativeai.types import Model, Completion

from compaipair.types.completion_template import CompletionTemplate
from compaipair.utils import configure_palm_api, get_available_models, get_api_key

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
    api_key: str
    template: CompletionTemplate | None

    def __init__(
        self,
        model: Model | str,
        template: str = None,
        question: str = "",
        priming: str = "",
        decorator: str = "",
        temperature: float = 0.7,
        api_key: str = None,
        input: str = None,
    ):
        self.temperature = temperature

        self.question = question
        if template is None:
            self.priming = priming
            self.decorator = decorator
        if template is not None:
            template = CompletionTemplate.find_template(template)
            self.priming = template.priming if template.priming else priming
            self.decorator = template.decorator if template.decorator else decorator

        if api_key is None:
            self.api_key = get_api_key()

        configure_palm_api(api_key=self.api_key)

        if isinstance(model, Model):
            self.model = model
        elif model is None:
            self.model = self.get_model()
        else:
            self.model = self.get_model(model)

    def complete(self) -> Completion:
        self.result = palm.generate_text(
            prompt=self.prompt, model=self.model, temperature=self.temperature
        )
        return self.result

    @staticmethod
    def get_model(model: str = "text-bison-001") -> Model:
        models = list(get_available_models())
        return next(filter(lambda m: model in m.name, models), models[1])

    @property
    def prompt(self):
        return prompt_template.format(
            priming=self.priming, question=self.question, decorator=self.decorator
        ).strip()
