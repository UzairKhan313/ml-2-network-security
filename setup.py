from setuptools import setup, find_packages
from typing import List


def get_requirements() -> List[str]:
    requirement_list: List[str] = []
    try:
        with open("requirements.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                if requirement and requirement != "-e .":
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print(f"Error: requirements.txt not found.")
    return requirement_list


print("get_requirements:", get_requirements())


setup(
    name="network_security",
    version="0.1.0",
    author="Uzair Khan",
    author_email="uzairkhaan2003@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(),
)
