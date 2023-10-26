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
    """
    Class to generate text completions using the Palm API.

    Args:
        model (Model | str): The model to use for completion. If a string is
            provided, it will be used to select a model from the list of
            available models. If None, the default model will be used.
        template (str | CompletionTemplate | None): The template to use for
            generating the completion prompt. If a string is provided, it will
            be used to find a template by name. If None, the default template
            will be used.
        question (str): The question to be completed.
        priming (str): The priming text to be used before the question.
        decorator (str): The decorator text to be used after the question.
        temperature (float): The temperature to use for completion.
        api_key (str): The API key to use for the Palm API. If None, the
            default API key will be used.
    """

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
        """
        Generate the completion.

        Returns:
            A Completion object containing the generated text.
        """
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
        """
        Get the completion prompt.

        Returns:
            A string containing the completion prompt.
        """

        return prompt_template.format(
            priming=self.priming, question=self.question, decorator=self.decorator
        ).strip()
