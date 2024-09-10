# coding_planning_agent_prompt: This prompt serves as a foundation for planning a software development project.
coding_planning_agent_prompt = """
You are a highly skilled software development assistant. Your primary objective is to assist in planning a software development project.

User Query: {query}
Programming Languages: {languages}

The project plan should include the following essential components:

1.  A clear and concise **project objective**: Define the purpose, goals, and deliverables of the project.
2.  **Detailed project steps**: Outline the necessary tasks, milestones, and timelines to achieve the project objectives.
3.  **Project considerations and prerequisites**: Identify any critical factors, dependencies, or requirements that must be addressed before commencing the project.

Please provide a detailed plan based on these specifications.
"""

# coding_integration_agent_prompt: This prompt guides the generation of code for integration purposes.
coding_integration_agent_prompt = """
Based on the provided project plan:
{plan}

Generate high-quality code in the following programming languages: {languages}. Ensure the code is:

*   Clean and properly formatted
*   Free from installation commands like 'pip install'
*   Ready to execute without further modification

Dependencies should be handled separately and not included in the generated code. Always use real URLs for placeholders, as they may return actual answers during testing.
"""

# coding_testing_agent_prompt: This prompt facilitates the creation of tests for the provided code.
coding_testing_agent_prompt = """
Based on the project plan:
{plan}

And the following code:
{code}

Generate comprehensive tests in the specified programming languages: {languages}. Ensure the tests are:

*   Clean and properly formatted
*   Free from installation commands like 'pip install'
*   Ready to execute without further modification

Dependencies should be handled separately and not included in the generated tests.
"""

# coding_documentation_agent_prompt: This prompt enables the generation of documentation for the provided code.
coding_documentation_agent_prompt = """
Based on the following code:
{code}

Generate high-quality documentation in the specified programming languages: {languages}. Ensure the documentation is:

*   Clean and properly formatted
*   Free from installation commands like 'pip install'
*   Clear and easy to understand

The generated documentation should provide a comprehensive overview of the code, its functionality, and any relevant details.
"""

# coding_optimization_agent_prompt: This prompt facilitates code optimization for improved performance and efficiency.
coding_optimization_agent_prompt = """
Based on the following code:
{code}

Optimize the provided code in the specified programming languages: {languages}. Ensure the optimized code is:

*   Clean and properly formatted
*   Free from installation commands like 'pip install'
*   Efficient and easy to read

The optimized code should be designed to improve performance, reduce complexity, and enhance overall maintainability.
"""

# feedback_prompt: This prompt enables refinement of the generated code based on user-provided feedback.
feedback_prompt = """
The user has provided valuable feedback on the generated code and tests. Here is the original code:
{code}

And here is the user's feedback:
{feedback}

Please refine the code based on this feedback, ensuring it is corrected and improved according to the user's suggestions. Additionally, generate updated tests to verify the new code. Ensure the refined code and tests are:

*   Clean and properly formatted
*   Free from installation commands like 'pip install'
*   Ready to execute without further modification

Dependencies should be handled separately and not included in the generated code or tests.
"""
