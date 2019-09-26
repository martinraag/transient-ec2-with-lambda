from setuptools import setup, find_packages

setup(
    name="pie",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["boto3==1.9.108"],
    entry_points="""
        [console_scripts]
        pie=pie.pie:main
    """,
)
