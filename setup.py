#!/usr/bin/env python3
from os.path import join, abspath, dirname
from setuptools import setup
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


def required(requirements_file):
    """Read a requirements file, stripping comments and blank lines."""
    with open(HERE / requirements_file) as f:
        requirements = f.read().splitlines()
    return [pkg.strip() for pkg in requirements
            if pkg.strip() and not pkg.strip().startswith("#")]


PLUGIN_ENTRY_POINT = 'ovos-tts-plugin-azure = ovos_tts_plugin_azure:AzureTTSPlugin'
setup(
    name='ovos_tts_plugin_azure',
    version='0.1.1',
    description='A tts plugin for OpenVoiceOS, using Azure Cognitive Services',
    long_description=README,
    long_description_content_type="text/markdown",
    url='http://github.com/dalgwen/ovos-tts-plugin-azure',
    author='Gwendal Roulleau',
    author_email='private@private.org',
    license='Apache-2.0',
    packages=['ovos_tts_plugin_azure'],
    install_requires=required("requirements.txt"),
    extras_require={"test": ["ovoscope[tts]", "pytest"]},
    zip_safe=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='mycroft plugin tts',
    entry_points={'mycroft.plugin.tts': PLUGIN_ENTRY_POINT}
)
