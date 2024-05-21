# dr_transcribe

A microservice for assessing audio transcription quality.

## What is it?

The API consists of a single endpoint that takes the key of a file in the S3 bucket. Once the POST request is made, we create a task and send it to Celery worker. The worker will then load the json file from S3, parse it, and calculate the transcription quality using one of the 3 methods that can be configured with env variables. Then, the result is available in the backend configured for Celery. The default is embedding technique, opensource llm and OpenAI techniques are also available. At first request the server will download model files, which is then cached. The model files can directly be embedded to Docker image for faster startup times.

Techniques:

-   Embedding technique: Sliding window of a chunk through out the transcript, and calculating the cosine similarity between the chunk and its neighboars. The average of all the cosine similarities is the final score.

-   LLM perplexity technique: By utilizing LLMs that were trained for Causal tasks, we can calculate the perplexity of the transcript. This is done by using the LLM to generate next token predictions and comparing how far they are from the given text. The lower the perplexity, the more coherant the transcript.

-   Advanced prompting technique: We can craft such a prompt so that the model estimates the quality of the given text within the criteria described. To improve its performance, I used CoT, EmotionPrompting, and ExpertPrompting. I also utilized the json output feature of the new models which lowers the confusion of syntax and inference time.

## Poetry

This project uses poetry. It's a modern dependency management
tool.

To run the project use this set of commands:

```bash
poetry install
poetry run python -m dr_transcribe
```

This will start the server on the configured host.

You can find swagger documentation at `/api/docs`.

You can read more about poetry here: https://python-poetry.org/

## Docker

You can start the project with docker using this command:

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . up --build
```

If you want to develop in docker with autoreload add `-f deploy/docker-compose.dev.yml` to your docker command.
Like this:

```bash
docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . up --build
```

This command exposes the web application on port 8000, mounts current directory and enables autoreload.

But you have to rebuild image every time you modify `poetry.lock` or `pyproject.toml` with this command:

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . build
```

## Project structure

```bash
$ tree "dr_transcribe"
dr_transcribe
├── conftest.py  # Fixtures for all tests.
├── __main__.py  # Startup script. Starts uvicorn.
├── services  # Package for different external services such as rabbit or redis etc.
├── settings.py  # Main configuration settings for project.
├── static  # Static content.
├── tests  # Tests for project.
└── web  # Package contains web server. Handlers, startup config.
    ├── api  # Package with all handlers.
    │   └── router.py  # Main router.
    ├── application.py  # FastAPI application configuration.
    └── lifetime.py  # Contains actions to perform on startup and shutdown.
```

## Configuration

This application can be configured with environment variables.

You can create `.env` file by copying the existing `.env.example` in the root directory and place all
environment variables here.

All environment variables should start with "DR*TRANSCRIBE*" prefix.

For example if you see in your "dr_transcribe/settings.py" a variable named like
`random_parameter`, you should provide the "DR_TRANSCRIBE_RANDOM_PARAMETER"
variable to configure the value. This behaviour can be changed by overriding `env_prefix` property
in `dr_transcribe.settings.Settings.Config`.

An example of .env file:

```bash
DR_TRANSCRIBE_RELOAD="True"
DR_TRANSCRIBE_PORT="8000"
DR_TRANSCRIBE_ENVIRONMENT="dev"
```

You can read more about BaseSettings class here: https://pydantic-docs.helpmanual.io/usage/settings/

## Pre-commit

To install pre-commit simply run inside the shell:

```bash
pre-commit install
```

pre-commit is very useful to check your code before publishing it.
It's configured using .pre-commit-config.yaml file.

By default it runs:

-   black (formats your code);
-   mypy (validates types);
-   isort (sorts imports in all files);
-   flake8 (spots possible bugs);

You can read more about pre-commit here: https://pre-commit.com/

## Running tests

If you want to run it in docker, simply run:

```bash
docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . run --build --rm api pytest -vv .
docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . down
```

For running tests on your local machine.

2. Run the pytest.

```bash
pytest -vv .
```
