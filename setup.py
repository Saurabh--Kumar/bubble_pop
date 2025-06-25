from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bubble-pop",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A fun bubble popping game using computer vision",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/bubble_pop",
    packages=find_packages(),
    package_data={
        'bubble_pop': ['assets/sounds/*.wav'],
    },
    install_requires=[
        'opencv-python>=4.5.0',
        'mediapipe>=0.8.9',
        'numpy>=1.19.5',
        'pygame>=2.0.1',
        'screeninfo>=0.8.1',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'bubble-pop=bubble_pop.main:main',
        ],
    },
)
