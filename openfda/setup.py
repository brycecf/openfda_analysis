from setuptools import setup, find_packages

setup(
    author='Bryce Freshcorn',
    author_email='bcf4kv@gmail.com',
    description='CLI for pulling OpenFDA data.',
    entry_points={
        'console_scripts': [
            'openfda = openfda.cli:main'
        ]
    },
    name='openfda',
    packages=find_packages(include='openfda'),
    version=0.1,
    dist_dir='dist',
    zip_safe=True,
    install_requires=[
        'click',
        'fire',
        'requests'
    ]
)