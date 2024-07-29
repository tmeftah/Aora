# %%
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma

#%%
llm = ChatOllama(model="llama3",temperature=0)


# %%
answer = ResponseSchema(name="answer", description="The answer to the question")
question = ResponseSchema(name="question", description="The question asked")
response_schema = [question,answer]

output_parser = StructuredOutputParser.from_response_schemas(response_schema)

instruct = output_parser.get_format_instructions()

# %%
template = ChatPromptTemplate.from_template("""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are an Math assistant, you only answer Maths questions and nothing else. {instruct}. If you do not know how to answer please only say see Documentation.<|eot_id|><|start_header_id|>user<|end_header_id|>
{input}<|eot_id|><|start_header_id|>assistant<|end_header_id|>""")


# %%
math = """What is Langchain?"""
prompt = template.format_messages(input=math,instruct=instruct)


# %%
response = llm.invoke(prompt)
# %%
