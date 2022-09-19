# Hydrangea Bot

The open-source and forever free Discord bot for all your roleplaying needs.

## Setting up

The Python development environment is managed by [Poetry](https://python-poetry.org/) with automated formatting, syntax checking, and test execution performed via [pre-commit](https://pre-commit.com/). After cloning the repository, setting up the software development environment is easy.

```
pip install poetry
poetry install
poetry run pre-commit install
```

Finally, you can start the Discord bot.

```
poetry run python -m hydrangeabot
```

## Planned features

- Rolling and roll macros
- Customizable character sheets with system templates
- Rulebooks for systems
- Highly configurable
