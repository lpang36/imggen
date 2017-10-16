from setuptools import setup

setup(
	name='imggen',
	version='0.1',
	description='A Python module to automatically generate images by overlaying foreground images on background images. Intended to facilitate training for computer vision algorithms.',
	author='Lawrence Pang',
	install_requires=[
		'opencv-python',
		'numpy',
		'tqdm'
	],
)