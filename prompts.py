

prompt_vector = """Answer the question based on the following context:
{context}

Question: {question}
思考步骤：首先排除与问题不相干的参考文本。基于合理的参考内容，回答问题。
 Let’s first understand the problem and devise a plan to solve the problem. Then, let’s carry out the plan and solve the problem step by step.
Attention: 使用中文回答
"""