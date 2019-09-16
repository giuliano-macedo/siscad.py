import setuptools
setuptools.setup(
	name='siscad-test',
	license='GPLv3',
	version='0.0.4',
	author="Giuliano Oliveira De Macedo",
	author_email="giuliano.llpinokio@gmail.com",
	description="Module for siscad.ufms.br",
	long_description=open("README.md").read(),
	download_url="https://github.com/llpinokio/siscad.py/archive/v0.0.1.tar.gz",
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