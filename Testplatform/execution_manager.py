import subprocess
import importlib.util
import logging
from file_manager import save_code


logger = logging.getLogger(__name__)


def install_dependencies(dependencies):
    for dependency in dependencies:
        try:
            subprocess.run(["pip", "install", dependency], check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install {dependency}: {e}")

def extract_dependencies(code):
    # A simple heuristic to find 'pip install' lines and extract package names
    dependencies = []
    for line in code.splitlines():
        if line.startswith("pip install"):
            parts = line.split()
            dependencies.extend(parts[2:])  # Extract package names after 'pip install'
    return dependencies

def correct_indentation(code):
    lines = code.splitlines()
    corrected_lines = []
    indentation_level = 0
    for line in lines:
        stripped_line = line.lstrip()
        if stripped_line.startswith('except') or stripped_line.startswith('elif') or stripped_line.startswith('else'):
            indentation_level -= 1
        corrected_lines.append('    ' * indentation_level + stripped_line)
        if stripped_line.endswith(':'):
            indentation_level += 1
    return '\n'.join(corrected_lines)

def execute_code(filepath, language, verbose=False):
    if not filepath:
        logger.error("No code file path provided; skipping code execution.")
        return

    if language in ["html", "css"]:
        logger.info(f"{language.upper()} code generated and saved to {filepath}. Please open it in a web browser to view.")
        return

    try:
        if language == "python":
            subprocess.run(["python", filepath], check=True)
        elif language == "javascript":
            subprocess.run(["node", filepath], check=True)
        elif language == "java":
            subprocess.run(["javac", filepath], check=True)
            subprocess.run(["java", filepath], check=True)
        elif language == "csharp":
            subprocess.run(["csc", filepath], check=True)
            subprocess.run(["mono", f"{filepath}.exe"], check=True)
        elif language == "c":
            subprocess.run(["gcc", filepath, "-o", filepath], check=True)
            subprocess.run([f"./{filepath}"], check=True)
        elif language == "cpp":
            subprocess.run(["g++", filepath, "-o", filepath], check=True)
            subprocess.run([f"./{filepath}"], check=True)
        # Add more languages as needed
    except subprocess.CalledProcessError as e:
        logger.error(f"Execution Error: {e}")

def run_tests(code, tests, language, verbose=False):
    if language in ["html", "css"]:
        logger.info(f"Skipping tests for non-executable language: {language.upper()}")
        return 0  # Return 0 indicating all tests passed (since there are no tests to run)

    if language == "python":
        code_filename = "temp_generated_code"
        code_filepath = f"{code_filename}.py"
        test_filepath = "test_generated_code.py"

        # Extract and install dependencies
        dependencies = extract_dependencies(code)
        if dependencies:
            install_dependencies(dependencies)
        
        # Clean the code from 'pip install' lines and correct indentation
        cleaned_code = "\n".join([line for line in code.splitlines() if not line.startswith("pip install")])
        cleaned_code = correct_indentation(cleaned_code)
        
        # Save the cleaned code to a file
        save_code(cleaned_code, code_filepath, verbose)

        spec = importlib.util.spec_from_file_location(code_filename, code_filepath)
        generated_module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(generated_module)
        except ModuleNotFoundError as e:
            logger.error(f"ModuleNotFoundError: {e}. Attempting to install the missing module.")
            subprocess.run(["pip", "install", e.name], check=True)
            spec.loader.exec_module(generated_module)

        test_code = f"""
import unittest
from {code_filename} import *

{tests}

if __name__ == "__main__":
    unittest.main()
"""
        # Save the test code to a file
        save_code(test_code, test_filepath, verbose)

        try:
            result = subprocess.run(["python", test_filepath], check=True)
            return result.returncode  # Return the return code from the test run
        except subprocess.CalledProcessError as e:
            logger.error(f"Test Execution Error: {e}")
            return e.returncode  # Return the return code from the failed test run
