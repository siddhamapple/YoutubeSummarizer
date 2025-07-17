from setuptools import setup,find_packages
from typing import List
HYPEN_E_DOT='-e .'


def get_requirements(file_path:str)->List[str]:
    requirments=[]
    with open (file_path) as file_obj:
        requirments=file_obj.readlines()
        requirments=[req.replace("\n", "")  for req in requirments]

        if HYPEN_E_DOT in requirments:
            requirments.remove(HYPEN_E_DOT)

    return requirments


setup(
    name="YoutubeSummarizer",
    version="0.0.1",
    description="Summarize or ask any queries form a youtube video",
    author="Siddham Jain",
    author_email="siddhamjainn@gmail.com",
    package_dir={"": "src"},  
    packages=find_packages(where="src"),
    install_requires=get_requirements("requirements.txt"),
    python_requires=">=3.8",   

)