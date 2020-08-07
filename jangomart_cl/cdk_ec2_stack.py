from aws_cdk import core
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_elasticloadbalancingv2 as elb
import aws_cdk.aws_autoscaling as autoscaling

ec2_type = "t2.micro"
key_name = "bdevore_rsa"  # Setup key_name for EC2 instance login 
linux_ami = ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
                                 edition=ec2.AmazonLinuxEdition.STANDARD,
                                 virtualization=ec2.AmazonLinuxVirt.HVM,
                                 storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
                                 )  # Indicate your AMI, no need a specific id in the region
with open("./user_data/user_data.sh") as f:
    user_data = f.read()


class CdkEC2Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # # Create Bastion
        # bastion = ec2.BastionHostLinux(self, "myBastion",
        #                                vpc=vpc,
        #                                subnet_selection=ec2.SubnetSelection(
        #                                    subnet_type=ec2.SubnetType.PUBLIC),
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
        alb.connections.allow_from_any_ipv4(
            ec2.Port.tcp(80), "Internet access for ALB via port 80")
        listener = alb.add_listener("my80",
                                    port=80,
                                    open=True)
        
        # Create Autoscaling Group with fixed 2*EC2 hosts
        self.asg = autoscaling.AutoScalingGroup(self, "jmASG",
                                                vpc=vpc,
                                                vpc_subnets=ec2.SubnetSelection(subnet_group_name="App-Private"),
                                                #associate_public_ip_address=True,
                                                instance_type=ec2.InstanceType(instance_type_identifier=ec2_type),
                                                machine_image=linux_ami,
                                                key_name=key_name,
                                                user_data=ec2.UserData.custom(user_data),
                                                desired_capacity=2,
                                                min_capacity=2,
                                                max_capacity=2,
                                                # block_devices=[
                                                #     autoscaling.BlockDevice(
                                                #         device_name="/dev/xvda",
                                                #         volume=autoscaling.BlockDeviceVolume.ebs(
                                                #             volume_type=autoscaling.EbsDeviceVolumeType.GP2,
                                                #             volume_size=12,
                                                #             delete_on_termination=True
                                                #         )),
                                                #     autoscaling.BlockDevice(
                                                #         device_name="/dev/sdb",
                                                #         volume=autoscaling.BlockDeviceVolume.ebs(
                                                #             volume_size=20)
                                                #         # 20GB, with default volume_type gp2
                                                #     )
                                                # ]
                                                )

        self.asg.connections.allow_from(alb, ec2.Port.tcp(80), "JangoMart ALB access for port 80 of EC2 in JangoMart ASG")
        self.asg.connections.allow_from_any_ipv4(ec2.Port.tcp(22), "Allow SSH connection from anywhere (for demo only)")
        listener.add_targets("addTargetGroup",
                             port=80,
                             targets=[self.asg])

        core.CfnOutput(self, "Output",
                       value=alb.load_balancer_dns_name)