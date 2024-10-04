from setuptools import setup, find_packages

setup(
    name='vectortoapple',  
    version='0.1.3', 
    packages=find_packages(), 
    install_requires=[
        'cairosvg',
        'Pillow',
        'tqdm',
    ],
    entry_points={
        'console_scripts': [
            'vectortoapple = vectortoapple.convert:main',  
        ],
    },
    author='Ginder Singh',
    author_email='ginderksingh@gmail.com',
    description='Convert Android vector drawable XML files to Apple\'s Asset Catalog format',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Ginder-Singh/vectortoapple', 
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License', 
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6', 
)