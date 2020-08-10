from aws_cdk import core
import aws_cdk.aws_codedeploy as codedeploy
import aws_cdk.aws_codepipeline as codepipeline
import aws_cdk.aws_codepipeline_actions as codepipeline_actions

class CdkCICDStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, asg, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        #Set up CodeDeploy
        codedeploy_application = codedeploy.ServerApplication(self, "CodeDeployApp",
                                                        application_name="JangoMartLoyaltyApp")

        deploymentgroup = codedeploy.ServerDeploymentGroup(self, "CodeDeployDeploymentGroup",
                                                        application=codedeploy_application,
                                                        auto_scaling_groups=[asg],
                                                        deployment_group_name="JangoMartASG",
                                                        #role="CodeDeployServiceRole", # <-- syntax error here
                                                        deployment_config=codedeploy.ServerDeploymentConfig.ALL_AT_ONCE)

        #Create the pipeline
        pipeline = codepipeline.Pipeline(self, "CodePipeline",
                                    pipeline_name="JangoMartPipeline",
                                    #role="CodePipeline-Service-Role" # <-- syntax error here
        )
        
        source_output = codepipeline.Artifact()
        
        #Set up Source stage
        source_action = codepipeline_actions.GitHubSourceAction(
                action_name="GitHub_Source",
                owner="brianfdevore",
                repo="jangomart-cl",
                oauth_token=core.SecretValue.secrets_manager("my-github-token"),
                #oauth_token=secretsmanager.Secret.from_secret_attributes(self, "ImportedSecret", secret_arn="arn:aws:secretsmanager:us-east-1:446451421466:secret:GitHub_JangoMart_Repo_Access_Token-t3S4dj"),
                output=source_output,
                branch="master",
                trigger=codepipeline_actions.GitHubTrigger.POLL
        )

        #Set up Deploy stage
        deploy_action = codepipeline_actions.CodeDeployServerDeployAction(
                action_name="CodeDeploy",
                input=source_output,
                deployment_group=deploymentgroup
        )


        #Add the stages defined above to the pipeline
        pipeline.add_stage(
                stage_name="Source",
                actions=[source_action]
        )

        pipeline.add_stage(
                stage_name="Deploy",
                actions=[deploy_action]
        )