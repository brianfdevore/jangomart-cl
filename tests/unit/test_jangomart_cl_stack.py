import json
import pytest

from aws_cdk import core
from jangomart-cl.jangomart_cl_stack import JangomartClStack


def get_template():
    app = core.App()
    JangomartClStack(app, "jangomart-cl")
    return json.dumps(app.synth().get_stack("jangomart-cl").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
