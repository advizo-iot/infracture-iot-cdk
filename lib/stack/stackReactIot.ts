import { Stack,RemovalPolicy,CfnOutput } from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as glue from 'aws-cdk-lib/aws-glue';
import { Role, ServicePrincipal, ManagedPolicy,Effect,PolicyStatement } from 'aws-cdk-lib/aws-iam';
import { Fn, Duration } from 'aws-cdk-lib';
import path = require('path');
import { Function, Runtime, Code, LayerVersion, Architecture } from 'aws-cdk-lib/aws-lambda';

export const stackReactIot = (scope: Stack) => {

  ////////////////////////////////////////////////////////////////////////////////////////
  /////////////////////////////////    CREATE AWS ROLE   /////////////////////////////////
  ////////////////////////////////////////////////////////////////////////////////////////

  const iotReactFireRole = new Role(scope, 'iotReactFireRole', {
    assumedBy: new ServicePrincipal('s3.amazonaws.com'),
    roleName: 'iotReactFireRole',
  });

  iotReactFireRole.addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName('AmazonS3FullAccess'));

  ////////////////////////////////////////////////////////////////////////////////////////
  ////////////////////////////////    CREATE BUCKETS S3    ///////////////////////////////
  ////////////////////////////////////////////////////////////////////////////////////////
  
  const advizoIOTResources = new s3.Bucket(scope, 'advizoIOTResources', {
    versioned: false,
    bucketName: 'advizo-iot-fire-resources',
    publicReadAccess: false,
    blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
    removalPolicy: RemovalPolicy.DESTROY
  });

  ////////////////////////////////////////////////////////////////////////////////////////
  ////////////////////////////////////////////////////////////////////////////////////////

  const loginIotApp = new Function(scope, 'loginIotApp', {
    runtime: Runtime.PYTHON_3_9, 
    handler: 'main.lambda_handler',
    code: Code.fromAsset(path.join(__dirname, './lambda/loginIotApp')),
    functionName: 'loginIotApp',
    timeout: Duration.minutes(10),
    role: iotReactFireRole,
  });

}