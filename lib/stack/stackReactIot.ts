import { Stack,RemovalPolicy,CfnOutput } from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as glue from 'aws-cdk-lib/aws-glue';
import { Role, ServicePrincipal, ManagedPolicy,Effect,PolicyStatement } from 'aws-cdk-lib/aws-iam';

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

}