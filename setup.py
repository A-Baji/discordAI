import setuptools
import pathlib
import discordai as package
import sys

min_py_version = (3, 8)

if sys.version_info < min_py_version:
    sys.exit(
        "DiscordAI is only supported for Python {}.{} or higher".format(*min_py_version)
    )

here = pathlib.Path(__file__).parent.resolve()
with open(pathlib.Path(here, "requirements.txt")) as f:
    requirements = [r for r in f.read().splitlines()]

setuptools.setup(
    name=package.__name__,
    version=package.__version__,
    author="Adib Baji",
    author_email="bidabaji@gmail.com",
    description="A discord bot package that utilizes openAI to create custom AI models out of your chat history",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/A-Baji/discordAI",
    packages=setuptools.find_packages(exclude=["tests*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            f"{package.__name__}={package.__name__}.command_line:{package.__name__}"
        ],
    },
    include_package_data=True,
    install_requires=requirements.append("git+https://github.com/A-Baji/discordAI-modelizer.git"),
    python_requires="~={}.{}".format(*min_py_version),
)
