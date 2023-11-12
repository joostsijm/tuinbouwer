#!/usr/bin/env python3
import os

import aws_cdk
import aws_cdk.aws_apprunner_alpha as apprunner
from constructs import Construct


class TuinbouwerCdkStack(aws_cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        apprunner.Service(self, "service",
            source=apprunner.Source.from_ecr(
                image_configuration=apprunner.ImageConfiguration(port=8000),
                repository=aws_cdk.aws_ecr.Repository.from_repository_name(self, "tuinbouwer", "tuinbouwer"),
                tag_or_digest="latest"
            )
        )


aws_app = aws_cdk.App()
TuinbouwerCdkStack(aws_app, "TuinbouwerCdkStack")
aws_app.synth()
