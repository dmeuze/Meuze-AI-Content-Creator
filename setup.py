from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tmz_content_creator",
    version="0.1.1",
    author="Meuze",
    author_email="dirksmaurits@gmail.com",
    description="An AI-powered content creation tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dmeuze/Meuze-AI-Content-Creator",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "flask>=3.1.0",
        "python-dotenv>=1.1.0",
        "openai>=1.75.0",
    ],
    entry_points={
        "console_scripts": [
            "tmz-content-creator=tmz_content_creator.run:app",
        ],
    },
) 