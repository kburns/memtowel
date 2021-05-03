import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="memtowel",
    version="0.0.1",
    author="Keaton J. Burns",
    author_email="keaton.burns@gmail.com",
    description="A small parallel memory tracker.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kburns/memtowel",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
)