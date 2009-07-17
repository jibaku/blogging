from distutils.core import setup
 
setup(
    name = "blogging",
    version = "0.2",
    author = "Fabien Schwob",
    author_email = "fabien@x-phuture.com",
    description = "Yet another django blogging app",
    long_description = "Yet another django blogging app",
    license = "BSD",
    url = "https://hg.jibaku.net/modules/blogging/",
    packages = [
        "blogging",
    ],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ]
)