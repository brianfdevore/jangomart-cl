import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="jangomart_cl",
    version="0.0.1",

    description="A CDK Python app which defines and provisions AWS cloud resources and configuration necessary for the JangoMart Customer Loyalty application.",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Brian F. DeVore",

    package_dir={"": "jangomart_cl"},
    packages=setuptools.find_packages(where="jangomart_cl"),

    install_requires=[
        "aws-cdk.core==1.47.0",
        "aws-cdk.aws_iam==1.47.0",
        "aws-cdk.aws_ec2==1.47.0",
        "aws-cdk.aws_route53==1.47.0",
        "aws-cdk.aws_cloudfront==1.47.0",
        "aws-cdk.aws_elasticloadbalancingv2==1.47.0",
        "aws-cdk.aws_autoscaling==1.47.0",
        "aws-cdk.aws_s3==1.47.0",
        "aws-cdk.aws_efs==1.47.0",
        "aws-cdk.aws_rds==1.47.0",
        "aws-cdk.aws_elasticache==1.47.0",
        "aws-cdk.aws_codedeploy==1.47.0",
        "aws-cdk.aws_codepipeline==1.47.0",
        "aws-cdk.aws_codepipeline_actions==1.47.0"
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: Apache Software License",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
