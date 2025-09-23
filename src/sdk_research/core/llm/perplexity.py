from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_perplexity import ChatPerplexity
from src.sdk_research.core.llm.base_llm import BaseLLM

class PerplexityLLM(BaseLLM):

    def __init__(self, api_key, model_name, temperature, model_kwargs = None):
        self._api_key = api_key
        self._model_name = model_name
        self._temperature = temperature
        self._model_kwargs = model_kwargs

        if self._model_kwargs is None:
            model_kwargs = {}
            # self._llm = ChatPerplexity(api_key=self._api_key,
            #                            temperature=self._temperature,
            #                           model=self._model_name,
            #                           model_kwargs=model_kwargs)
            self._llm = ChatGoogleGenerativeAI(
                api_key=self._api_key,
                model="gemini-2.5-flash",
                temperature=0,
            )

        # Properties
        self._name, self._version = "Perplexity", "NA"
        self._description = "Perplexity LLM."

    @property
    def llm(self):
        return self._llm