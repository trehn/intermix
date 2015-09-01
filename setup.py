try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name="intermix",
    version="0.1.0",
    description="HTML5 canvas output for Python applications",
    long_description="Intermix is a library that provides Python applications with a real-time API to draw in an HTML5 canvas served by the builtin web server",
    author="Torsten Rehn",
    author_email="torsten@rehn.email",
    license="ISC",
    url="https://github.com/trehn/intermix",
    keywords=["HTML5", "canvas", "GUI", "draw", "output"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        "aiohttp >= 0.17.3",
        "mako >=  1.0.2",
    ],
    py_modules=['intermix'],
    data_files=[
        (".", "intermix_client.html"),
    ],
)
