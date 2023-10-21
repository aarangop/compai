import os

import click
from google.api_core import retry


def get_api_key():
    # Load API key
    with open("api-key", "r") as f:
        return f.read()


prompt_template = """
{priming}
{question}
{decorator}
"""

import google.generativeai as palm


def try_read_file(potential_path):
    if potential_path is None:
        return None
    if os.path.exists(potential_path):
        with open(potential_path, "r") as f:
            return f.read()
    return None


def get_prompt(priming: str, question: str, decorator: str):
    priming_file_contents = try_read_file(priming)
    if priming_file_contents is not None:
        priming = priming_file_contents

    question_file_contents = try_read_file(question)
    if question_file_contents is not None:
        question = question_file_contents

    decorator_file_contents = try_read_file(decorator)
    if decorator_file_contents is not None:
        decorator = decorator_file_contents

    return prompt_template.format(priming=priming, question=question, decorator=decorator)


def prompt_code(priming: str, code_file: str, decorator: str):
    with open(code_file, "r") as f:
        code = f.read()
    return prompt_template.format(priming=priming, question=code, decorator=decorator)


def configure_api():
    palm.configure(
        api_key=get_api_key(),
        transport="rest"
    )


def print_completion_results(completion, prompt=None):
    if prompt:
        print("Completion generated for prompt: \n")
        print(prompt)
        print("########################################\n\n")
    print("Completion: \n")
    print(completion.result)


@retry.Retry()
def generate_text(prompt, model, temperature=0.0):
    return palm.generate_text(prompt=prompt, model=model, temperature=temperature)


@click.group()
def compai():
    pass


@click.command()
@click.option("--priming", help="String to prime the LLM prompt")
@click.option("--decorator", help="Decorator to your prompt")
@click.option("-o", "--output", default="./result.md", help="File to write output")
@click.option("-t", "--temperature", default=0.7, help="Model temperature, use 0 for more deterministic completions.")
@click.option("-m", "--model-name", default="text-bison-001", help="LLM model for this query")
@click.argument("question")
def complete(question, priming, decorator, model_name, temperature, output):
    configure_api()
    model = next(filter(lambda m: model_name in m.name, palm.list_models()), None)
    if not model:
        raise ValueError(f"Model {model}")
    print(f"Using model {model.name}")
    prompt = get_prompt(priming, question, decorator)
    completion = palm.generate_text(prompt=prompt, model=model,
                                    temperature=temperature)
    print(f"Generated completion for prompt:\n {prompt}\n\n")

    if output is not None:
        with open(output, "w") as f:
            f.write(completion.result)
    else:
        print_completion_results(completion)


@click.command()
def available_models():
    configure_api()
    for m in palm.list_models():
        print(f"name: {m.name}")
        print(f"description: {m.description}")
        print(f"generation methods: {m.supported_generation_methods}")


compai.add_command(complete)
compai.add_command(available_models)

if __name__ == '__main__':
    compai()
