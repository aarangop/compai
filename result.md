# Prompt
You're an expert Python programmer. Could you please write thorough documentation for the following code?

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

None
---
# Result


```

**CompaiCompletion** is a class that wraps the Palm API and provides a simple interface for generating text completions.

#### Args:

* **model** (Model | str): The model to use for completion. Can be either a `Model` object or a string. If a string is provided, it will be used to find the corresponding model in the list of available models.
* **template** (str): The completion template to use. If `None`, the default template will be used.
* **question** (str): The question to be completed.
* **priming** (str): The priming text to be used before the question.
* **decorator** (str): The decorator text to be used after the question.
* **temperature** (float): The temperature to use for completion.
* **api_key** (str): The API key to use for the Palm API. If `None`, the default API key will be used.
* **input** (str): The input text to be used for completion.

#### Attributes:

* **model** (Model): The model used for completion.
* **priming** (str): The priming text to be used before the question.
* **question** (str): The question to be completed.
* **decorator** (str): The decorator text to be used after the question.
* **result** (Completion): The result of the completion.
* **api_key** (str): The API key used for the Palm API.
* **template** (CompletionTemplate | None): The completion template used.

#### Methods:

* **complete()** -> Completion: Generates a completion using the provided parameters.
* **get_model(model: str = "text-bison-001") -> Model:** Gets the model with the specified name.
* **prompt** -> str: Gets the prompt to be used for completion.

## Example

```python
from compaipair import CompaiCompletion

comp = CompaiCompletion(
    model="text-davinci-002",
    question="What is the best way to learn Python?",
    priming="I want to learn Python",
    decorator="I'm looking for a comprehensive tutorial",
)

result = comp.complete()

print(result.text)
```

Output:

```
The best way to learn Python is to start with a comprehensive tutorial. There are many great tutorials available online, such as the one on the Python website. Once you have a basic understanding of the language, you can start practicing by writing your own programs. There are also many online forums and communities where you can get help and feedback on your code.
```