import setuptools

setuptools.setup(
    name="videocap",
    py_modules=["videocap"],
    entry_points={"console_scripts": ["videocap=videocap:main"]},
    install_requires=["opencv-python"],
)
