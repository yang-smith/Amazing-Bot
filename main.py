
from prase import parse_bookmarks
from price import calculate_price
from prompts import prompt_vector
from utils import choose_bookmarks_file
from loader import get_loader
from vector_db import show_search, db_init, docs_add, token_count
import logging
from restruct import restruct
# 配置日志记录
logging.basicConfig(filename='errors.log', level=logging.ERROR)


def main():
    vectorstore = db_init()
    # splits = restruct()
    if(True):
        # vectorstore.add_documents(splits)
        # vectorstore.persist()
        from langchain.prompts import ChatPromptTemplate
        from langchain.chat_models import ChatOpenAI
        from langchain.schema.output_parser import StrOutputParser
        from langchain.schema.runnable import RunnablePassthrough
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


if __name__ == '__main__':
    main()
