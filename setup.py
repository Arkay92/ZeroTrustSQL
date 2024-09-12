from setuptools import setup, find_packages

setup(
    name='ZeroTrustSQL',
    version='0.1.0',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'lightphe',
        'pycryptodome',
        # Add other dependencies here
    ],
    entry_points={
        'console_scripts': [
            'zerotrustsql = src.main:main',  # if you have a main entry point
        ],
    },
    description='A fully encrypted database solution with SQL-like operations and Zero-Knowledge Proofs.',
    author='Robert McMenemy',
    url='https://github.com/Arkay92/ZeroTrustSQL',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
