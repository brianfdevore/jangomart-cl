from aws_cdk import core
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_elasticloadbalancingv2 as elb
import aws_cdk.aws_autoscaling as autoscaling
import aws_cdk.aws_iam as awsiam
import aws_cdk.aws_codedeploy as codedeploy
import aws_cdk.aws_codepipeline as codepipeline
import aws_cdk.aws_codepipeline_actions as codepipeline_actions

ec2_type = "t2.micro"
key_name = "bdevore_rsa"  # Setup key_name for EC2 instance login 
linux_ami = ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
                                 edition=ec2.AmazonLinuxEdition.STANDARD,
                                 virtualization=ec2.AmazonLinuxVirt.HVM,
                                 storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
                                 )

with open("./user_data/user_data.sh") as f:
    user_data = f.read()


class CdkEC2Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # # Create Bastion
        # bastion = ec2.BastionHostLinux(self, "myBastion",
        #                                vpc=vpc,
        #                                subnet_selection=ec2.SubnetSelection(
        #                                subnet_type=ec2.SubnetType.PUBLIC),
        #                                instance_name="myBastionHostLinux",
        #                                instance_type=ec2.InstanceType(instance_type_identifier="t2.micro"))
        
        # # Setup key_name for EC2 instance login if you don't use Session Manager
        # # bastion.instance.instance.add_property_override("KeyName", key_name)

        # bastion.connections.allow_from_any_ipv4(
        #     ec2.Port.tcp(22), "Internet access SSH")

        # Create ALB
        alb = elb.ApplicationLoadBalancer(self, "jmALB",
                                          vpc=vpc,
                                          internet_facing=True,
                                          load_balancer_name="JangoMart-ALB"
                                          )
        
        # Configure ALB security groups/rules
        alb.connections.allow_from_any_ipv4(
            ec2.Port.tcp(80), "Internet access for ALB via port 80")
        listener = alb.add_listener("my80",
                                    port=80,
                                    open=True)
        
        # Create Autoscaling Group (initial config is with 2 EC2 hosts)
        self.asg = autoscaling.AutoScalingGroup(self, "jmASG",
                                                vpc=vpc,
                                                vpc_subnets=ec2.SubnetSelection(subnet_group_name="App-Private"),
                                                #associate_public_ip_address=True,
                                                #role=awsiam.IRole.role_name=["EC2InstanceRoleForCodeDeploy"], # <-- Not working, syntax error
                                                instance_type=ec2.InstanceType(instance_type_identifier=ec2_type),
                                                machine_image=linux_ami,
                                                key_name=key_name,
                                                user_data=ec2.UserData.custom(user_data),
                                                desired_capacity=2,
                                                min_capacity=2,
                                                max_capacity=2,                                                
                                                )

        # Set up security gruops/rules for ASG access
        self.asg.connections.allow_from(alb, ec2.Port.tcp(80), "JangoMart ALB access for port 80 of EC2 in JangoMart ASG")
        self.asg.connections.allow_from_any_ipv4(ec2.Port.tcp(22), "Allow SSH connection from anywhere (for demo only)")
        
        # Configure ALB listener and target group
        listener.add_targets("addTargetGroup",
                             port=80,
                             targets=[self.asg])


        ###############################
        ## CI/CD Configuration Below ##
        ###############################

        #Set up CodeDeploy
        codedeploy_application = codedeploy.ServerApplication(self, "CodeDeployApp",
                                                        application_name="JangoMartLoyaltyApp")

        deploymentgroup = codedeploy.ServerDeploymentGroup(self, "CodeDeployDeploymentGroup",
                                                        application=codedeploy_application,
                                                        auto_scaling_groups=[self.asg],
                                                        deployment_group_name="JangoMartASG",
                                                        #role="CodeDeployServiceRole", # <-- syntax error here
                                                        deployment_config=codedeploy.ServerDeploymentConfig.ALL_AT_ONCE)

        # #Create CodePipeline
        # pipeline = codepipeline.Pipeline(self, "CodePipeline",
        #                             pipeline_name="JangoMartPipeline",
        #                             #role="CodePipeline-Service-Role" # <-- syntax error here
        # )
        
        # source_output = codepipeline.Artifact()
        
        # #Set up source action for the Source stage of pipeline
        # source_action = codepipeline_actions.GitHubSourceAction(
        #         action_name="GitHub_Source",
        #         owner="brianfdevore",
        #         repo="jangomart-cl",
        #         oauth_token=core.SecretValue.secrets_manager("my-github-token"),
        #         output=source_output,
        #         #branch="master",
        #         trigger=codepipeline_actions.GitHubTrigger.WEBHOOK
        # )

        # #Set up Deploy action for Deploy stage of pipeline
        # deploy_action = codepipeline_actions.CodeDeployServerDeployAction(
        #         action_name="CodeDeploy",
        #         input=source_output,
        #         deployment_group=deploymentgroup
        # )

        # #Add the stages defined above to the pipeline
        # pipeline.add_stage(
        #         stage_name="Source",
        #         actions=[source_action]
        # )

        # pipeline.add_stage(
        #         stage_name="Deploy",
        #         actions=[deploy_action]
        # )

        #Output CFN ALB DNS Name to access web application
        core.CfnOutput(self, "ALBOutput",
                       value=alb.load_balancer_dns_name) 
