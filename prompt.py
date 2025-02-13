GENERATE_QA_PROMPT = """Given the user context:

${context}  

<Instructions>
    - You are a Professor in marine engines and their control systems. Your task is to setup at least 5 question-answer pairs for an upcoming technical examination given the context information and not prior knowledge.
    - The questions should be diverse in nature across the document. Restrict the questions to the context information provided.
    - Try to design questions that have paragraph-length answers.
    - Take a deep breath.
    - Think first and then extract the information.
</Instructions>    

Given below is XML that describes the information to extract from the query and the tags to extract it into.

${output_schema}

Return a valid JSON object (no other text is necessary), where the key of the field in JSON is the `name` attribute of the corresponding XML, and the value is of the type specified by the corresponding XML's tag. The JSON MUST conform to the XML format, including any types and format requests e.g. requests for lists, objects and specific types. Be correct and concise.
You are allowed to return an JSON object with an empty sensor's list if no information can be extracted from the query.

Here are examples of simple (XML, JSON) pairs that show the expected behavior:
- `<![CDATA[<string name='foo' format='two-words lower-case' />`]]> => `{'foo': 'example one'}`
- `<![CDATA[<list name='bar'><string format='upper-case' /></list>]]>` => `{"bar": ['STRING ONE', 'STRING TWO', etc.]}`
- `<![CDATA[<object name='baz'><string name="foo" format="capitalize two-words" /><integer name="index" format="1-indexed" /></object>]]>` => `{'baz': {'foo': 'Some String', 'index': 1}}`

Follow the following format:
<thought>your thoughts go here</thought>
<json>valid JSON in format [{"query": question, "pos":answer}, ...]</json>

Assistant: <thought>
"""