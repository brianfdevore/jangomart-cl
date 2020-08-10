#!/usr/bin/env python3

from aws_cdk import core
from jangomart_cl.cdk_vpc_stack import CdkVPCStack
from jangomart_cl.cdk_ec2_stack import CdkEC2Stack
#from jangomart_cl.cdk_cicd_stack import CdkCICDStack

app = core.App()

vpc_stack = CdkVPCStack(app, "cdk-vpc", env={'region': 'us-east-1'})
ec2_stack = CdkEC2Stack(app, "cdk-ec2", vpc=vpc_stack.vpc, env={'region': 'us-east-1'})
#cicd_stack = CdkCICDStack(app, "cdk-cicd", asg=ec2_stack.asg, env={'region': 'us-east-1'})

app.synth()
