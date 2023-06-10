from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ko_re',
    version='0.0.1',
    description='regex for Korean - Being free from ord/chr in Hangeul analysis.',
    author='ilotoki0804',
    author_email='ilotoki0804@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/ilotoki0804/ko_re',
    install_requires=[],
    packages=find_packages(exclude=[]),
    keywords=['re', 'regex', 'korean regex', 'regular expression', '정규표현식', 'hangeul', 'hangul', 'hangeul analysis'],
    python_requires='>=3.8',
    package_data={},
    zip_safe=False,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'TOPIC :: SOFTWARE DEVELOPMENT :: LOCALIZATION',
        'TOPIC :: TEXT PROCESSING',
        'TOPIC :: TEXT PROCESSING :: LINGUISTIC',
        'INTENDED AUDIENCE :: RELIGION',
        'NATURAL LANGUAGE :: KOREAN'
    ],
)