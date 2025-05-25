from setuptools import setup, find_packages

setup(
    name="unit-converter",
    version="1.0.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    
    # Runtime dependencies (empty for standard library)
    install_requires=[],  
    
    # Test dependencies
    extras_require={
        "test": [
            "pytest>=8.2.2",
            "pytest-cov>=4.1.0",
        ]
    },
    
    entry_points={
        "console_scripts": ["unit-converter=unit_converter:main"]
    }
)