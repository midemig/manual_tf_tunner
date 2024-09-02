from setuptools import find_packages, setup

package_name = 'manual_tf_tunner'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='migueldm',
    maintainer_email='midemig@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'manual_tf_tunner_node = manual_tf_tunner.manual_tf_tunner_node:main'
        ],
    },
)
