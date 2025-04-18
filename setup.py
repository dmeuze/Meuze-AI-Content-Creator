from setuptools import setup, find_packages

setup(
    name="tmz_content_creator",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
        "python-dotenv",
        "openai",
    ],
) 