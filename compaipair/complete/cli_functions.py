import google.generativeai as palm

from compaipair.utils import configure_palm_api


def available_models():
    configure_palm_api()
    for m in palm.list_models():
        print(f"name: {m.name}")
        print(f"description: {m.description}")
        print(f"generation methods: {m.supported_generation_methods}")


def complete(question, priming, decorator, model_name, temperature, output):
    pass
    # model = next(filter(lambda m: model_name in m.name, palm.list_models()), None)
    # if not model:
    #     raise ValueError(f"Model {model}")
    # print(f"Using model {model.name}")
    # completion = CompaiCompletion(model, question, priming, decorator)
    # print(f"Generated completion for prompt:\n {completion.prompt}\n\n")
    #
    # if output is not None:
    #     with open(output, "w") as f:
    #         f.write(completion.complete().result)
    # else:
    #     print_completion_results(completion)
