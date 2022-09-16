"""Setup file"""

import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="tuinbouwer_sensor",
    version="0.1.0",
    author="Joost Sijm",
    author_email="joostsijm@gmail.com",
    description="Tuinbouw sensor",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://git.craftbroec.nl/tuinbouwer/tuinbouwer_sensor",
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        "requests",
        "python-dotenv",
        "apscheduler",
        "Adafruit_Python_DHT",
    ],
    entry_points = {
        'console_scripts': ['tuinbouwer_sensor=tuinbouwer_sensor.__main__:main'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
