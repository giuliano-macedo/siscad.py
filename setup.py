from setuptools import setup, find_packages
from pathlib import Path

version = Path("./siscad/_version.py").read_text().strip()
setup(
    name="siscad",
    license="GPLv3",
    version=version,
    author="Giuliano Oliveira De Macedo",
    author_email="giuliano.llpinokio@gmail.com",
    description="Module for siscad.ufms.br",
    long_description=Path("README.md").read_text(),
    download_url=f"https://github.com/llpinokio/siscad.py/archive/v{version}.tar.gz",
    long_description_content_type="text/markdown",
    keywords=["web-scraping"],
    url="https://github.com/llpinokio/siscad.py",
    packages=find_packages(),
    install_requires=Path("requirements.txt").read_text().split(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
