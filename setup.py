from setuptools import setup, find_namespace_packages

setup(
    name="email-validator",
    version="1.0.0",
    packages=find_namespace_packages(include=["src", "src.*"]),
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn==0.24.0",
        "pydantic==2.5.2",
        "python-multipart==0.0.6",
        "email-validator==2.1.0.post1",
        "aiofiles==23.2.1",
        "aiohttp==3.9.1",
        "aiosmtplib==2.0.2",
        "dnspython==2.4.2",
        "tld==0.13",
        "whois==0.9.27",
        "python-Levenshtein==0.23.0",
        "disposable-email-domains==0.0.82",
        "numpy==1.26.4",
        "pandas==2.1.3",
        "matplotlib==3.8.2",
        "seaborn==0.13.0",
        "pytest==7.4.3",
        "PyQt6==6.5.2",
        "qt-material==2.14",
        "openpyxl==3.1.2",
        "xlrd==2.0.1"
    ],
    package_dir={"": "."}
)