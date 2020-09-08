import * as cdk from '@aws-cdk/core';
import { StackProps } from '@aws-cdk/core';
import { Function, Runtime, Code } from "@aws-cdk/aws-lambda"
import { LambdaIntegration, MethodLoggingLevel, RestApi } from "@aws-cdk/aws-apigateway"
import { Bucket, BlockPublicAccess} from "@aws-cdk/aws-s3"
import { StringParameter } from '@aws-cdk/aws-ssm';

export class OldDanteStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const bucket = new Bucket(this, this.stackName + "Bucket", {
      versioned: false,
      publicReadAccess: false,
      blockPublicAccess: BlockPublicAccess.BLOCK_ALL,
    });

    const lambda = new Function(this, this.stackName + "Lambda", {
      functionName: this.stackName + "Lambda",
      handler: "handler.lambda_handler",
      runtime: Runtime.PYTHON_3_7,
      code: Code.fromAsset('src/lambda.zip'),
      memorySize: 512,
      timeout: cdk.Duration.seconds(60),
      environment: {
        bucketName: bucket.bucketName
      }
    })
    bucket.grantRead(lambda)

    StringParameter.fromStringParameterName(this, 'SlackBotToken', '/olddante/slack/bot_token')
      .grantRead(lambda);

    StringParameter.fromStringParameterName(this, 'SlackSigningSecret', '/olddante/slack/signing_secret')
      .grantRead(lambda)


    const api = new RestApi(this, this.stackName + "RestApi", {
        deployOptions: {
            stageName: "prod",
            metricsEnabled: true,
            loggingLevel: MethodLoggingLevel.INFO,
            dataTraceEnabled: true,
        },
      })
    const integration = new LambdaIntegration(lambda, {})
    api.root.addMethod("GET", integration)
    const slack = api.root.addResource('slack');
    const events = slack.addResource('events')
    events.addMethod("POST", integration)
  }
}
