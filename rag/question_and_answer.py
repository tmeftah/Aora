# %%
import json
from langchain_community.llms.ollama import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.callbacks.tracers import ConsoleCallbackHandler
from langchain_core.runnables import RunnablePassthrough


def create_llm():
    llm = Ollama(model="llama3", temperature=0)

    # %%
    template = """
    Text: {text}
    Given the above text, it is your job to create {number} questions and their answers.
    Make sure that questions are not repeated and check all the questions to be conforming to the text as well.
    """

    prompt = PromptTemplate(
        input_variables=["text", "number"],
        template=template,
    )

    chain = {"text": RunnablePassthrough(), "number": RunnablePassthrough()
             } | prompt | llm | StrOutputParser()
    return chain


def resp(message, number: int,  history):

    chain = create_llm()

    # yield chain.invoke({"question": message})
    yield chain.invoke({
        "text": message,
        "number": number
    }, config={'callbacks': [ConsoleCallbackHandler()]})


if __name__ == "__main__":
    import gradio as gr

    gr.Interface(fn=resp,
                 inputs=[gr.TextArea(lines=3, label="Text"), gr.Number(
                     minimum=1, maximum=10, value=3, label="Anzahl der Fragen")],
                 outputs=gr.TextArea(),
                 title="K-Averroes",).launch()
