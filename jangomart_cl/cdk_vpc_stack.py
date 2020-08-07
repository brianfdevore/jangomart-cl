from aws_cdk import core
import aws_cdk.aws_ec2 as ec2

class CdkVPCStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

    #Create production VPC
        self.vpc = ec2.Vpc(self, "VPC-JM",
            cidr="10.0.0.0/16",
            max_azs=2,
            #Configuration below will create 3 subnet groups in 2 AZs = 6 subnets
            subnet_configuration=[
            ec2.SubnetConfiguration(
                subnet_type=ec2.SubnetType.PUBLIC,
                name="Bastion",
                cidr_mask=24           
            ),
            ec2.SubnetConfiguration(
                subnet_type=ec2.SubnetType.PRIVATE,
                name="App-Private",
                cidr_mask=24           
            ),
            ec2.SubnetConfiguration(
                subnet_type=ec2.SubnetType.ISOLATED,
                name="DB-Private",
                cidr_mask=24
            )],
            nat_gateway_provider=ec2.NatProvider.gateway(),
            nat_gateways=1,
            )

        core.CfnOutput(self, "Output",
                       value=self.vpc.vpc_id)
        
    #End VPC creation



       
