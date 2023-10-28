import os
import shutil

import pytest
from google.generativeai.types import Model

from compaipair.config.cli_functions import init


@pytest.fixture
def compai_test_cache_path():
    return os.path.join(os.path.expanduser("~"), ".compai-test")


@pytest.fixture(autouse=True)
def create_test_env(compai_test_cache_path):
    """Creates test environment.

    This fixture sets the following environment variables:

    * COMPAI_CACHE_PATH: Path to the test cache directory.
    * GOOGLE_GENERATIVE_AI_API_KEY: Empty string to disable the API key check.

    The test cache directory is created if it does not exist.

    After the test is finished, the cache directory is deleted if it exists.

    If the test environment was previously created, it is reset by deleting the
    cache directory and setting the environment variables to their previous
    values.

    Args:
        compai_test_cache_path (str): Path to the test cache directory.

    Returns:
        None

    """
    prev_cache_path = (
        os.environ["COMPAI_CACHE_PATH"] if "COMPAI_CACHE_PATH" in os.environ else None
    )
    os.environ["COMPAI_CACHE_PATH"] = compai_test_cache_path
    os.environ["GOOGLE_GENERATIVEAI_API_KEY"] = "ThisIsAnAPIKey"

    if not os.path.exists(compai_test_cache_path):
        os.mkdir(compai_test_cache_path)

    yield

    if os.path.exists(compai_test_cache_path):
        shutil.rmtree(compai_test_cache_path)
    if prev_cache_path is not None:
        os.environ["COMPAI_CACHE_PATH"] = prev_cache_path


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
