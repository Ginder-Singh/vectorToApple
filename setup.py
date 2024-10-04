from setuptools import setup, find_packages

setup(
    name='vectortoapple',  # Replace with your tool's name
    version='0.1.0',  # Version of your tool
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=[
        'cairosvg',
        'Pillow',
        'tqdm',
    ],
    entry_points={
        'console_scripts': [
            'vectortoapple = vectortoapple.convert:main',  # Replace with your main function
        ],
    },
    author='Ginder Singh',
    author_email='ginderksingh@gmail.com',
    description='Convert Android vector drawable XML files to Apple\'s Asset Catalog format',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Ginder-Singh/vectortoapple',  # Replace with your repository URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Change if using a different license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify the Python version required
)