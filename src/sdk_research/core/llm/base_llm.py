from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List

class BaseLLM(ABC):
    """
    Minimal blueprint every scraper should implement.
    - Keeps a small, stable public interface
    - Allows dependency injection (llm clients, crawler)
    """

    def __init__(self, *, api_key, model_name, temperature, model_kwargs = None):
        self._api_key = api_key
        self._model_name = model_name
        self._temperature = temperature
        self._model_kwargs = model_kwargs

        # Properties
        self._name, self._version = None, None
        self._description = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def version(self) -> str:
        return self._version

    @property
    def description(self) -> str:
        return self._description