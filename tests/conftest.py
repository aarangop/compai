import os
import shutil

import pytest
from google.generativeai.types import Model

from compaipair.config.cli_functions import init


@pytest.fixture(autouse=True)
def create_test_env():
    test_cache_path = os.path.join(os.path.expanduser("~"), ".compai-test")
    os.environ["COMPAI_CACHE_PATH"] = test_cache_path
    init(api_key=";ldsakgfjkljhadfgl")
    yield
    shutil.rmtree(test_cache_path)
    os.environ["COMPAI_CACHE_PATH"] = os.path.join(os.path.expanduser("~"), ".compai")


@pytest.fixture
def models():
    return [
        Model(
            name="model-1",
            base_model_id="model-1",
            description="AI model 1",
            version="1",
            display_name="model-1",
            input_token_limit=1000,
            output_token_limit=1000,
            supported_generation_methods=["text"],
        ),
        Model(
            name="model-2",
            base_model_id="model-2",
            description="AI model 2",
            version="2",
            display_name="model-2",
            input_token_limit=1000,
            output_token_limit=1000,
            supported_generation_methods=["text"],
        ),
    ]


@pytest.fixture
def model():
    return Model(
        name="model-1",
        base_model_id="model-1",
        description="AI model 1",
        version="1",
        display_name="model-1",
        input_token_limit=1000,
        output_token_limit=1000,
        supported_generation_methods=["text"],
    )
