from setuptools import find_packages,setup
from typing import List


HYPHEN_E_DOT="-e ."
def getrequirements(path:str)->List[str]:
    requirements=[]
    with open(path) as file:
        requirements=file.readlines()
        [req.replace("\n","") for req in requirements]
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    return requirements

setup(
    name='mlproject',
    version ='0.0.1',
    author='Paras',
    author_email='parasji014@gmail.com',
    packages=find_packages(),
    install_requires=getrequirements("requirements.txt")
)