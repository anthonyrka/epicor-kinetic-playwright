from setuptools import setup, find_packages


setup(
    name="epicor-kinetic-playwright",
    version="0.1.0",
    description="Python + Playwright test harness for Epicor Kinetic customizations",
    author="Ryan Kirkish",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
