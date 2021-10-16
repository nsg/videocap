import setuptools

setuptools.setup(
    name="analyzer",
    py_modules=["analyzer", "utils"],
    entry_points={"console_scripts": ["analyzer=analyzer:main"]},
    install_requires=["opencv-python"],
)
