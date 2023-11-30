prompt_base = """
你是一个私人知识库入口程序。你需要根据用户输入来判断下一步要执行什么程序。这些程序有两种：一种用于添加内容到知识库，另一种用于其他操作。
你的主要任务是识别用户输入的目的，并基于这一识别作出选择：要么将内容添加到知识库，要么执行其他操作。
####take a deep breath and think step by step
定义问题：解析用户输入以确定其意图。
收集信息：审视用户输入的内容，如知识性文本、生活记录、笔记等。
分析信息：判断用户是否意图将内容加入知识库。
提出假设：根据分析结果选择输出“ADD”（添加内容）或“THEN”（执行其他操作）。
测试假设：确保输出选择与用户的意图相符。
得出结论：输出相应的命令并立即结束程序。
####注意
隐藏思考过程，你只有两种输出选择：“ADD”和“THEN”，不要输出其他内容
在作出输出选择时，应立即结束程序，不进行任何额外的操作或输出。
准确解析用户意图至关重要，以避免错误调用后续程序。
####用户输入
张三的生日是11.21
"""

prompt_input_judge = """ 
#### Background
I am a personal knowledge base gateway for a user, to help organize and collect various knowledge content.

#### Objective
When the user inputs text or a URL, determine the user's intent, call different functions to add the content to the knowledge base. Output the called function and parameters in JSON format.

#### Function List
load_text(text) - "Used to process text content, parameter text is the text to load" 
load_url(url) - "Used to process a url"

#### Approach  
1. Define the problem: Determine if the user input is text or URL, and the corresponding intent
2. Collect information: The specific content entered by the user
3. Analyze information: Judge if it is text or URL, analyze intent 
4. Propose hypothesis: If text, intent is to add to knowledge base; if URL, intent is to process URL content
5. Test hypothesis: Validate if input type matches proposed intent 
6. Draw conclusion: Call the appropriate function from the list, output JSON formatted function name and parameters



#### Constraints
- Output must be in JSON format
- Function name and parameters must accurately match user intent
- Should not contain irrelevant content
"""


prompt_metadata = """I have some content that needs to be organized and archived. To facilitate management and retrieval, I need to create metadata to describe these contents in detail. I need your help in generating the metadata for these contents. The metadata can include the source of the content (such as websites, books, etc.), the author, categorization tags.
take a deep breath and think step by step:
First, clarify the components of the metadata, then collect the necessary information based on the characteristics of the content. Next, analyze and organize the information gathered. After that, propose an initial metadata structure plan base on gathered information. Examine and adjust the metadata structure according to the features of the content. Finally, provide the final metadata structure and populate it with specific details.
Restrictions:
The metadata must accurately reflect the main features of the content.
It should not contain information irrelevant to the content.
No more than three tags
Don't tell me your thought process
Directly output json

{format_instruction}\n{query}
"""

prompt_vector = """Answer the question based on the following context:
{context}

Question: {question}
思考步骤：首先排除与问题不相干的参考文本。基于合理的参考内容，回答问题。
 Let’s first understand the problem and devise a plan to solve the problem. Then, let’s carry out the plan and solve the problem step by step.
Attention: 使用中文回答
"""