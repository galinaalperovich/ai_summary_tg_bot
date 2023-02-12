from setuptools import setup, find_packages

setup(
    name="summary_bot",
    version="0.0.1",
    description="A package for generating summaries for URL served via Telegram bot",
    url="https://github.com/galinaalperovich/summary_bot",
    author="Galina Alperovich",
    author_email="galya.alperovich@gmail.com",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
