import setuptools
import os
import ast
here = os.path.abspath(os.path.dirname(__file__))
exec(next(iter(open(os.path.join(here,"siscad","__init__.py"))))) #exec first line of init, get __version__
setuptools.setup(
	name='siscad',
	license='GPLv3',
	version=__version__,
	author="Giuliano Oliveira De Macedo",
	author_email="giuliano.llpinokio@gmail.com",
	description="Module for siscad.ufms.br",
	long_description=open("README.md").read(),
	download_url=f"https://github.com/llpinokio/siscad.py/archive/v{__version__}.tar.gz",
	long_description_content_type="text/markdown",
	keywords=["web-scraping"],
	url="https://github.com/llpinokio/siscad.py",
	packages=setuptools.find_packages(),
	install_requires=open("requirements.txt").read().split(),
	classifiers=[
		"Development Status :: 4 - Beta",
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
		"Operating System :: OS Independent",
	 ],
 )