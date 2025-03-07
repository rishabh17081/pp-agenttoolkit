from setuptools import setup, find_packages

setup(
    name="mcp-connector",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "flask>=2.0.0",
    ],
    entry_points={
        'console_scripts': [
            'mcp-connector=paypal_connector.cli:main',
            'mcp-server=paypal_connector.standalone_server:main',
        ],
    },
    author="Rishabh Sharma",
    author_email="rishabh.sharma@example.com",
    description="A connector for PayPal's Merchant Catalog Products API",
    keywords="paypal, api, connector",
    url="https://github.com/rishabh17081/pp-agenttoolkit",
    python_requires='>=3.6',
)
