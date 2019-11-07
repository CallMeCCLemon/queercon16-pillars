from distutils.core import setup


packages = []

with open("requirements.txt", 'r') as requirements:
    for requirement in requirements:
        packages.append(requirement)

setup(
    name="Queercon16-Pillars",
    version=1.0,
    description="Queercon 16 Pillars Drivers",
    author="Queercon",
    url="https://github.com/CallMeCCLemon/queercon16-pillars",
    install_requires=packages
)
