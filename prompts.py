# requirements.py

import os

def generate_requirements():
    # Define the required packages and their versions
    requirements = {
        "numpy": "^1.20",
        "pandas": "^1.3",
        "scikit-learn": "^0.24",
        "matplotlib": "^3.4",
        "seaborn": "^0.11"
    }

    # Create a requirements.txt file
    with open("requirements.txt", "w") as f:
        for package, version in requirements.items():
            f.write(f"{package} {version}\n")

    print("Requirements generated successfully.")

if __name__ == "__main__":
    generate_requirements()
