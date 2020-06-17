from setuptools import setup, find_packages

setup(
    author='Bryce Freshcorn',
    author_email='bcf4kv@gmail.com',
    description='Solution implementations for Q1.',
    name='question_one',
    packages=find_packages(include='question_one'),
    version=0.1,
    dist_dir='dist',
    zip_safe=True,
    install_requires=[
        'pandas',
        'tqdm'
    ] # Also, would include `openfda` dependency if published to pypi or a GitHub release
)