
This project was done as part of a job interview to demonstrate presentation, design, architecture, and engineering skills.

The documents in the "docs" folder are .odp (Open Document Format) formatted downloads from the Google Docs (2) and Google Slides (1)
documents.  To access these documents directly in Google Drive (recommended), please use the link below:

https://drive.google.com/drive/folders/1bfQ6naaM2jEgvMbc1W_0IuyEAcmnBOAG?usp=sharing

This project is a CDK application which spins up a portion of the core architecture for the JangoMart Customer Loyalty application, which
includes VPC and networking, subnets, NAT Gateway, ALB, ASG, and EC2.

In its current state, running the "cdk deploy * " command will deploy 2 stacks (cdk-vpc, cdk-ec2) and provide as output the public DNS
for the ALB.  2 t2.micro EC2 instances (Amazon Linux 2 base AMI) will be provisioned, but will run the bootstrap scripts (see the "user_data" folder) to install packages and configure the application, which is a simple PHP website with just 1 page (see index.php for the source code).

Additionally, CodeDeploy agents are installed to enable automated deployment in a CI/CD pipeline (CodePipeline).

Note that in order to use this, you will need to manually edit the IAM policy document associated with the EC2 role which is defined and provisioned in the CDK deployment.  You need to allow the EC2 instances to access all buckets ("*" in the resources section).

Run "cdk destroy * " when done to delete all resources.



# Below is the default CDK README.md documentation text

# Welcome to your CDK Python project!

You should explore the contents of this project. It demonstrates a CDK app with an instance of a stack (`jangomart_cl_stack`)
which contains an Amazon SQS queue that is subscribed to an Amazon SNS topic.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization process also creates
a virtualenv within this project, stored under the .env directory.  To create the virtualenv
it assumes that there is a `python3` executable in your path with access to the `venv` package.
If for any reason the automatic creation of the virtualenv fails, you can create the virtualenv
manually once the init process completes.

To manually create a virtualenv on MacOS and Linux:

```
$ python -m venv .env
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .env/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .env\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

You can now begin exploring the source code, contained in the hello directory.
There is also a very trivial test included that can be run like this:

```
$ pytest
```

To add additional dependencies, for example other CDK libraries, just add to
your requirements.txt file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
