"""Setup file"""

import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="tuinbouwer_server_api",
    version="0.1.0",
    author="Joost Sijm",
    author_email="joostsijm@gmail.com",
    description="Tuinbouw server API",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://git.craftbroec.nl/tuinbouwer/tuinbouwer_server_api",
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        "flask",
        "python-dotenv",
        "flask-sqlalchemy",
        "flask-apscheduler",
    ],
    entry_points = {
        'console_scripts': ['tuinbouwer_server_api=tuinbouwer_server_api.__main__:main'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
