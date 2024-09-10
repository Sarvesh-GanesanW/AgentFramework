import json
import requests
from termcolor import colored
from prompts import (
    coding_planning_agent_prompt,
    coding_integration_agent_prompt,
    coding_testing_agent_prompt,
    coding_documentation_agent_prompt,
    coding_optimization_agent_prompt,
    feedback_prompt  
)
from config_loader import load_config
from language_detector import detect_language
from execution_manager import execute_code, run_tests
from file_manager import save_code
from search_manager import SearchManager
from logger_config import setup_logging
import os
import time

class CoderAgent:
    def __init__(self, model, model_tool, model_qa, model_endpoint, planning_agent_prompt, integration_agent_prompt, testing_agent_prompt, documentation_agent_prompt, optimization_agent_prompt, verbose=False, iterations=1, max_retries=3, retry_delay=5):
        load_config('config.yaml')
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.url = model_endpoint
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        self.temperature = 0
        self.max_tokens = 1000
        self.model = model
        self.model_tool = model_tool
        self.model_qa = model_qa
        self.planning_agent_prompt = planning_agent_prompt
        self.integration_agent_prompt = integration_agent_prompt
        self.testing_agent_prompt = testing_agent_prompt
        self.documentation_agent_prompt = documentation_agent_prompt
        self.optimization_agent_prompt = optimization_agent_prompt
        self.feedback_prompt = feedback_prompt
        self.verbose = verbose
        self.iterations = iterations
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.search = SearchManager(self.model_qa)

        # Set up logging
        self.logger = setup_logging(verbose=self.verbose)

    def make_request(self, data):
        retries = 0
        while retries < self.max_retries:
            try:
                payload = {
                    "model": self.model,
                    "prompt": data['prompt'],
                    "stream": True 
                }
                response = requests.post(self.url, headers=self.headers, json=payload, stream=True, timeout=180)
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Request failed: {e}")
                self.logger.error(f"Request URL: {self.url}")
                self.logger.error(f"Request Headers: {self.headers}")
                self.logger.error(f"Request Payload: {payload}")
                retries += 1
                time.sleep(self.retry_delay)
        self.logger.error("Max retries exceeded. Aborting request.")
        return None

    def parse_ndjson(self, response_text):
        responses = []
        for line in response_text.splitlines():
            if line:
                try:
                    data = json.loads(line)
                    if 'response' in data:
                        responses.append(data['response'])
                except json.JSONDecodeError as e:
                    self.logger.error(f"JSON Decode Error: {e}")
                    continue
        return ''.join(responses)

    def extract_code(self, content):
        code_block = []
        in_code_block = False
        for line in content.splitlines():
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                code_block.append(line)
        return "\n".join(code_block)

    def generate_plan(self, query, languages):
        system_prompt = self.planning_agent_prompt.format(query=query, languages=",".join(languages))

        data = {
            "model": self.model,
            "prompt": system_prompt,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stop": None
        }

        response = self.make_request(data)
        if response is None:
            return None

        if self.verbose:
            self.logger.info(f"Response Status Code: {response.status_code}")
            self.logger.info(f"Response Headers:\n{response.headers}")
            self.logger.info(f"Raw Response Content (first 500 chars):\n{response.text[:500]}")

        plan = self.parse_ndjson(response.text)
        if self.verbose:
            self.logger.info(f"Generated Plan:\n{plan}")
        return plan

    def generate_code(self, plan, languages):
        system_prompt = self.integration_agent_prompt.format(plan=plan, languages=",".join(languages))

        data = {
            "model": self.model_tool,
            "prompt": system_prompt,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stop": None
        }

        response = self.make_request(data)
        if response is None:
            return None

        if self.verbose:
            self.logger.info(f"Response Status Code: {response.status_code}")
            self.logger.info(f"Response Headers:\n{response.headers}")
            self.logger.info(f"Raw Response Content (first 500 chars):\n{response.text[:500]}")
        
        content = self.parse_ndjson(response.text)
        code = self.extract_code(content)
        if self.verbose:
            self.logger.info(f"Generated Code:\n{code}")
        return code

    def generate_tests(self, plan, code, languages):
        system_prompt = self.testing_agent_prompt.format(plan=plan, code=code, languages=",".join(languages))

        data = {
            "model": self.model_tool,
            "prompt": system_prompt,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stop": None
        }

        response = self.make_request(data)
        if response is None:
            return None

        if self.verbose:
            self.logger.info(f"Response Status Code: {response.status_code}")
            self.logger.info(f"Response Headers:\n{response.headers}")
            self.logger.info(f"Raw Response Content (first 500 chars):\n{response.text[:500]}")
        
        content = self.parse_ndjson(response.text)
        tests = self.extract_code(content)
        if self.verbose:
            self.logger.info(f"Generated Tests:\n{tests}")
        return tests

    def generate_documentation(self, code, languages):
        system_prompt = self.documentation_agent_prompt.format(code=code, languages=",".join(languages))

        data = {
            "model": self.model_tool,
            "prompt": system_prompt,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stop": None
        }

        response = self.make_request(data)
        if response is None:
            return None

        if self.verbose:
            self.logger.info(f"Response Status Code: {response.status_code}")
            self.logger.info(f"Response Headers:\n{response.headers}")
            self.logger.info(f"Raw Response Content (first 500 chars):\n{response.text[:500]}")
        
        content = self.parse_ndjson(response.text)
        documented_code = self.extract_code(content)
        if self.verbose:
            self.logger.info(f"Generated Documentation:\n{documented_code}")
        return documented_code

    def optimize_code(self, code, languages):
        system_prompt = self.optimization_agent_prompt.format(code=code, languages=",".join(languages))

        data = {
            "model": self.model_tool,
            "prompt": system_prompt,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stop": None
        }

        response = self.make_request(data)
        if response is None:
            return None

        if self.verbose:
            self.logger.info(f"Response Status Code: {response.status_code}")
            self.logger.info(f"Response Headers:\n{response.headers}")
            self.logger.info(f"Raw Response Content (first 500 chars):\n{response.text[:500]}")
        
        content = self.parse_ndjson(response.text)
        optimized_code = self.extract_code(content)
        if self.verbose:
            self.logger.info(f"Optimized Code:\n{optimized_code}")
        return optimized_code

    def fetch_code_reference(self, query):
        self.logger.info(f"Fetching code reference for query: {query}")
        # Replace with actual logic to fetch code references
        return "Example code reference"

    def collect_feedback(self, code, tests, primary_language):
        print("Generated Code:")
        print(colored(code, 'green'))
        print("\nGenerated Tests:")
        print(colored(tests, 'green'))
        feedback = input("\nPlease provide feedback on the generated code and tests (or press Enter to accept): ")
        return feedback

    def refine_code_with_feedback(self, code, feedback, languages):
        system_prompt = feedback_prompt.format(code=code, feedback=feedback, languages=",".join(languages))

        data = {
            "model": self.model_tool,
            "prompt": system_prompt,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stop": None
        }

        response = self.make_request(data)
        if response is None:
            return None

        content = self.parse_ndjson(response.text)
        refined_code = self.extract_code(content)
        return refined_code

    def execute(self):
        # Mapping of programming languages to file extensions
        language_extensions = {
            'python': 'py',
            'javascript': 'js',
            'html': 'html',
            'css': 'css',
            'java': 'java',
            'c++': 'cpp',
            'c#': 'cs',
            'ruby': 'rb',
            'go': 'go',
            'php': 'php',
            # Add more mappings as needed
        }

        for i in range(self.iterations):
            query = input("Enter your coding query: ")
            
            detected_language = detect_language(query)

            if detected_language:
                languages = [detected_language]
            else:
                languages = input("Enter the programming languages (comma-separated, e.g., python,javascript,html): ").strip().lower().split(',')

            # Ensure primary_language is defined
            primary_language = languages[0]

            # Step 1: Generate Plan
            plan = self.generate_plan(query, languages)
            if plan is None:
                self.logger.error("Failed to generate plan. Aborting execution.")
                continue

            # Step 2: Generate Code based on Plan
            code = self.generate_code(plan, languages)
            if code is None:
                self.logger.error("Failed to generate code. Aborting execution.")
                continue

            # Step 3: Generate Tests for the Code
            tests = self.generate_tests(plan, code, languages)
            if tests is None:
                self.logger.error("Failed to generate tests. Aborting execution.")
                continue

            # Collect user feedback and refine code
            feedback = self.collect_feedback(code, tests, primary_language)
            if feedback:
                refined_code = self.refine_code_with_feedback(code, feedback, languages)
                if refined_code:
                    code = refined_code
                    tests = self.generate_tests(plan, code, languages)

            # Step 4: Document the Code
            documented_code = self.generate_documentation(code, languages)
            if documented_code is None:
                self.logger.error("Failed to generate documentation. Aborting execution.")
                continue

            # Step 5: Optimize the Code
            optimized_code = self.optimize_code(documented_code, languages)
            if optimized_code is None:
                self.logger.error("Failed to optimize code. Aborting execution.")
                continue

            # Filename for final code
            filename = input("Enter the filename (without extension) for the final code: ")
            extension = language_extensions.get(primary_language, 'txt')  # Default to 'txt' if language is not mapped
            filepath = f"{filename}.{extension}"

            # Loop until all tests pass
            all_tests_passed = False
            while not all_tests_passed:
                # Save the optimized code to a temporary file for testing
                temp_code_filepath = "temp_generated_code.py"
                save_code(optimized_code, temp_code_filepath, self.verbose)

                # Run the tests
                test_results = run_tests(optimized_code, tests, primary_language, self.verbose)

                # Check if all tests passed
                all_tests_passed = test_results == 0  # Assuming run_tests returns 0 if all tests pass

                if not all_tests_passed:
                    # If tests failed, regenerate the code
                    code = self.generate_code(plan, languages)
                    if code is None:
                        self.logger.error("Failed to regenerate code. Aborting execution.")
                        break
                    tests = self.generate_tests(plan, code, languages)
                    if tests is None:
                        self.logger.error("Failed to regenerate tests. Aborting execution.")
                        break
                    documented_code = self.generate_documentation(code, languages)
                    if documented_code is None:
                        self.logger.error("Failed to regenerate documentation. Aborting execution.")
                        break
                    optimized_code = self.optimize_code(documented_code, languages)
                    if optimized_code is None:
                        self.logger.error("Failed to re-optimize code. Aborting execution.")
                        break

            # Save the final version of the code
            save_code(optimized_code, filepath, self.verbose)

            # Step 8: Execute the Generated Code
            execute_code(filepath, primary_language, self.verbose)

            # Step 10: Clean up temporary files
            temp_files = [temp_code_filepath, "test_generated_code.py"]
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.remove(temp_file)

            # Example of fetching a code reference
            reference_query = query
            reference = self.fetch_code_reference(reference_query)
            print(reference)




    


if __name__ == '__main__':
    model = "llama3.1:8b"
    model_tool = "llama3.1:8b"
    model_qa = "llama3.1:8b"
    model_endpoint = 'http://localhost:11434/api/generate'
    stop = None
    server = 'ollama'

    agent = CoderAgent(
        model=model,
        model_tool=model_tool,
        model_qa=model_qa,
        model_endpoint=model_endpoint,
        planning_agent_prompt=coding_planning_agent_prompt,
        integration_agent_prompt=coding_integration_agent_prompt,
        testing_agent_prompt=coding_testing_agent_prompt,
        documentation_agent_prompt=coding_documentation_agent_prompt,
        optimization_agent_prompt=coding_optimization_agent_prompt,
        verbose=True,
        iterations=3
    )
    agent.execute()


