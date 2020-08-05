#!/usr/bin/env python3

from aws_cdk import core

from jangomart_cl.jangomart_cl_stack import JangomartClStack


app = core.App()
JangomartClStack(app, "jangomart-cl", env={'region': 'us-west-2'})

app.synth()
