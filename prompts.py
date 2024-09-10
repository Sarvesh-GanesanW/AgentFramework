coding_planning_agent_prompt = """
You are a highly skilled software development assistant. Your task is to help plan a software development project. Based on the user's query and the programming languages specified, generate a detailed plan for the project.

User Query: {query}
Programming Languages: {languages}

The plan should include the following:
1. A clear objective of the project.
2. Detailed steps to achieve the objective.
3. Any considerations or prerequisites needed for the project.
"""

coding_integration_agent_prompt = """
Based on the plan:
{plan}

Generate the code in the following languages: {languages}. Ensure the code is clean, properly indented, and does not include any installation commands like 'pip install'. Pay special attention to correct indentation, as it is crucial for the code to run properly. The code should be ready to execute without further modification. Dependencies should be handled separately and not included in the generated code. Always use real urls for placeholders, because while testing it may return actual answers.
"""

coding_testing_agent_prompt = """
Based on the plan:
{plan}

And the following code:
{code}

Generate the tests for the code in the following languages: {languages}. Ensure the tests are clean, properly indented, and do not include any installation commands like 'pip install'. The tests should be ready to execute without further modification. Dependencies should be handled separately and not included in the generated tests.
"""

coding_documentation_agent_prompt = """
Based on the following code:
{code}

Generate the documentation in the following languages: {languages}. Ensure the documentation is clean, properly formatted, and does not include any installation commands like 'pip install'. The documentation should be clear and easy to understand.
"""

coding_optimization_agent_prompt = """
Based on the following code:
{code}

Optimize the code in the following languages: {languages}. Ensure the optimized code is clean, properly indented, and does not include any installation commands like 'pip install'. The optimized code should be efficient and easy to read.
"""

feedback_prompt = """
The user has provided feedback on the generated code and tests. Here is the original code:
{code}

And here is the user's feedback:
{feedback}

Please refine the code based on this feedback. Ensure the code is corrected and improved based on the user's suggestions. Additionally, generate updated tests to verify the new code. Ensure the refined code and tests are clean, properly indented, and do not include any installation commands like 'pip install'. Dependencies should be handled separately and not included in the generated code or tests.
"""
