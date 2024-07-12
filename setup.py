import setuptools
import pathlib
import discordai as package
import sys

min_py_version = (3, 9)

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
    author_email="bidabaji@gmail.com",
    description="A Discord bot driver package that utilizes OpenAI to create custom AI models out of your Discord chat history",
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
            f"{package.__name__}={package.__name__}.command_line.command_line:{package.__name__}"
        ],
    },
    include_package_data=True,
    install_requires=requirements,
    python_requires="~={}.{}".format(*min_py_version),
)
