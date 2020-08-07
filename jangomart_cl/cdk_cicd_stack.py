from aws_cdk import core
import aws_cdk.aws_codedeploy as codedeploy
import aws_cdk.aws_codepipeline as codepipeline
import aws_cdk.aws_codepipeline_actions as cpactions

class CdkCICDStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

    #TODO...