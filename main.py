
from prase import parse_bookmarks
from price import calculate_price
from prompts import prompt_vector
from utils import choose_bookmarks_file
from loader import get_loader
from vector_db import show_search, db_init, docs_add, token_count
import logging
from restruct import restruct
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
# 配置日志记录
logging.basicConfig(filename='errors.log', level=logging.ERROR)


def db_test():
    vectorstore = db_init()
    # splits = restruct()
    if(True):
        # vectorstore.add_documents(splits)
        # vectorstore.persist()

        model = ChatOpenAI(model="gpt-3.5-turbo")
        prompt = ChatPromptTemplate.from_template(prompt_vector)

        counts = token_count(prompt_vector)
        price = calculate_price('gpt-3.5-turbo', counts, True)
        print("token_count:"+ str(counts) + "   price:"+ str(price))

        chain = prompt | model
        while True:
            question = input("Enter your question (or 'exit' to quit): ")
            if question.lower() == 'exit':
                break

            result_str = show_search(query=question, db=vectorstore)
            print("Robot say:")
            for s in chain.stream({"context": result_str, "question": question}):
                print(s.content, end="")

def parse():
    from langchain.output_parsers import PydanticOutputParser
    from pydantic import BaseModel, Field, validator
    from prompts import prompt_metadata
    model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    prompt_metadata = str(prompt_metadata)
    class output(BaseModel):
        content: str = Field(description="Contains the main text of the document. This should include the full body of the text to be stored, such as an article, a book chapter, or any other substantial piece of writing.")
        metadata: dict = Field(description="Stores additional information about the page content")
    parser = PydanticOutputParser(pydantic_object=output)
    prompt = PromptTemplate(
        template=prompt_metadata,
        input_variables=["query"],
        partial_variables={"format_instruction": parser.get_format_instructions()},
    )
    # print(prompt)
    # print(parser.get_format_instructions())
    chain = prompt | model
    while True:
        question = input("Enter your question (or 'exit' to quit): ")
        if question.lower() == 'exit':
            break

        print("Robot say:")
        robot_out = ''
        for s in chain.stream({"query": question}):
            print(s.content, end="")
            robot_out+=s.content
        from restruct import restruct_collect
        import json
        splits = restruct_collect(json.loads(robot_out))
        print(splits)


def main():
    from prompts import prompt_input_judge
    model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    prompt = ChatPromptTemplate.from_messages( [ 
        (
            "system",
            prompt_input_judge,
        ),
        ("human", "{human_input}"),
    ])
    chain = prompt | model
    while True:
        question = input("Enter your question (or 'exit' to quit): ")
        if question.lower() == 'exit':
            break

        print("Robot say:")
        for s in chain.stream({"human_input": question}):
            print(s.content, end="")


if __name__ == '__main__':
    # main()
    parse()
