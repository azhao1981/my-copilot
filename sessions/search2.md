
1. 首先是查询重构的核心代码：

```python
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from bing_search import BingSearchAPI  # 假设这是Bing搜索的API包装

class CustomSearchAgent:
    def __init__(self, openai_api_key, bing_api_key):
        self.llm = OpenAI(api_key=openai_api_key)
        self.search_client = BingSearchAPI(bing_api_key)
        
        # 查询重构的prompt模板
        self.query_reformulation_template = """
        作为一个搜索专家，你需要将用户的问题转换为有效的搜索关键词。
        
        用户问题: {question}
        
        请生成2-3个最优的搜索查询词组。要求：
        1. 提取核心概念和关键实体
        2. 移除不必要的词语
        3. 考虑同义词和相关术语
        4. 确保查询词具有足够的特异性
        
        仅输出搜索词，每行一个，不要其他解释。
        """
        
        self.query_prompt = PromptTemplate(
            input_variables=["question"],
            template=self.query_reformulation_template
        )

    def reformulate_query(self, user_question):
        """将用户问题转换为搜索关键词"""
        # 使用LLM生成搜索词
        search_queries = self.llm(self.query_prompt.format(question=user_question))
        # 分割成列表
        return [q.strip() for q in search_queries.split('\n') if q.strip()]

    def search(self, user_question):
        """执行搜索流程"""
        # 1. 重构查询
        search_queries = self.reformulate_query(user_question)
        
        # 2. 执行多个搜索并合并结果
        all_results = []
        for query in search_queries:
            results = self.search_client.search(query, count=5)
            all_results.extend(results)
            
        # 3. 结果去重和排序
        unique_results = self._deduplicate_results(all_results)
        
        return unique_results

    def _deduplicate_results(self, results):
        """去除重复的搜索结果"""
        seen_urls = set()
        unique_results = []
        
        for result in results:
            if result['url'] not in seen_urls:
                seen_urls.add(result['url'])
                unique_results.append(result)
                
        return unique_results
```

2. 使用示例：

```python
# 初始化agent
agent = CustomSearchAgent(
    openai_api_key="your-openai-key",
    bing_api_key="your-bing-key"
)

# 测试查询
question = "Python中如何实现多线程编程？"
results = agent.search(question)

# 打印结果
for result in results:
    print(f"Title: {result['title']}")
    print(f"URL: {result['url']}")
    print(f"Snippet: {result['snippet']}")
    print("---")
```

关键点说明：

1. 查询重构的核心是精心设计的prompt，它指导LLM将用户问题转换为有效的搜索关键词。

2. prompt设计考虑了以下几个关键因素：
   - 提取核心概念
   - 移除冗余词语
   - 生成多个查询变体
   - 保持查询的特异性

3. 实现中的关键技术点：
   - 使用LLM进行查询理解和重构
   - 执行多个搜索查询以提高召回率
   - 结果去重和排序确保质量
   - 模块化设计便于扩展和维护

4. 可以根据需要优化的方向：
   - 改进prompt模板以获得更好的搜索词
   - 添加结果排序算法
   - 实现更复杂的结果聚合策略
   - 添加缓存机制提高性能
   - 实现错误处理和重试机制

这个实现方案的优点是：
- 不依赖LangChain的工具和代理
- 实现简单直接，容易理解和修改
- 可以根据具体需求灵活扩展
- 通过LLM实现智能查询重构