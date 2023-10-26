from rich.console import Console
from rich.markdown import Markdown

from compaipair.types.completion_template import CompletionTemplate
from compaipair.utils import close_db

console = Console()


def new_template(name: str, priming: str = "", decorator: str = ""):
    return CompletionTemplate(name=name, priming=priming, decorator=decorator).save()


def edit_template(name: str, priming: str = None, decorator: str = None):
    existing_template = CompletionTemplate.find_template(name)
    return existing_template.update_template(priming=priming, decorator=decorator)


template_output_template = """# {template_name}
## Priming
{priming}
## Decorator
{decorator}
## Example prompt:
{example_prompt}"""


def show_templates(name: str = None, verbose: bool = False):
    templates = CompletionTemplate.find_templates(name)

    if verbose:
        sample_question = "How to iterate through a list of strings?"
        output = "\n---\n".join(
            [
                template_output_template.format(
                    template_name=template.name,
                    priming=template.priming,
                    decorator=template.decorator,
                    example_prompt=template.prompt(sample_question),
                )
                for template in templates
            ]
        )
    else:
        output = "\n".join([f"- {template.name}" for template in templates])
    console.print(Markdown(output))
    close_db()
