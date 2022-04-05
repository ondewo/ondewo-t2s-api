import setuptools

long_description = ""
# with open("README.md", "r") as f:
#     long_description = f.read()

with open("grpc_config_server/requirements.txt") as f:
    requires = f.read().splitlines()

setuptools.setup(
    name="ONDEWO text-to-speech server",
    version="3.1.3",
    author="Ondewo GbmH",
    author_email="info@ondewo.com",
    description="Server for managing Text-To-Speech services",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/ondewo/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">=3.0.1",
    install_requires=requires,
)
