import setuptools
setuptools.setup(
	 name='siscad',
	 license='GPLv3',
	 version='0.0.1',
	 author="Giuliano Oliveira De Macedo",
	 author_email="giuliano.llpinokio@gmail.com",
	 description="Module for siscad.ufms.br",
	 long_description=open("README.md").read(),
	 long_description_content_type="text/markdown",
	 keywords=["web-scraping"],
	 url="https://github.com/llpinokio/siscad.py",
	 packages=["siscad"],
	 install_requires=open("requirements.txt").read().split(),
	 classifiers=[
		 "Programming Language :: Python :: 3",
		 "License :: OSI Approved :: GPLv3 License",
		 "Operating System :: OS Independent",
	 ],
 )