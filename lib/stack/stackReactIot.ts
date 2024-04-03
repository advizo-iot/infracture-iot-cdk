import { Stack,RemovalPolicy,CfnOutput } from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as glue from 'aws-cdk-lib/aws-glue';
import { Role, ServicePrincipal, ManagedPolicy,Effect,PolicyStatement } from 'aws-cdk-lib/aws-iam';
import { Fn, Duration } from 'aws-cdk-lib';
import path = require('path');
import { Function, Runtime, Code, LayerVersion, Architecture } from 'aws-cdk-lib/aws-lambda';
import { RestApi, LambdaIntegration,Cors ,MethodLoggingLevel} from 'aws-cdk-lib/aws-apigateway';

export const stackReactIot = (scope: Stack) => {

  ////////////////////////////////////////////////////////////////////////////////////////
  /////////////////////////////////    CREATE AWS ROLE   /////////////////////////////////
  ////////////////////////////////////////////////////////////////////////////////////////

  const iotReactFireRole = new Role(scope, 'iotReactFireRole', {
    assumedBy: new ServicePrincipal('lambda.amazonaws.com'),
    roleName: 'iotReactFireRole',
  });

  iotReactFireRole.addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName('AmazonS3FullAccess'));
  iotReactFireRole.addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName('AWSLambda_FullAccess'));
  iotReactFireRole.addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName('AmazonAthenaFullAccess'));

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
  ////////////////////////////        CREATE AWS LAMBDAS       ///////////////////////////
  ////////////////////////////////////////////////////////////////////////////////////////

  const apiIotAdvizo = new Function(scope, 'apiIotAdvizo', {
    runtime: Runtime.PYTHON_3_9, 
    handler: 'main.lambda_handler',
    code: Code.fromAsset(path.join(__dirname, './lambda')),
    functionName: 'apiIotAdvizo',
    timeout: Duration.minutes(10),
    role: iotReactFireRole,
  });

  ////////////////////////////////////////////////////////////////////////////////////////
  //////////////////////////////      CREATE AWS APIS      ///////////////////////////////
  ////////////////////////////////////////////////////////////////////////////////////////

  const apiAdvizoIot = new RestApi(scope, `apiAdvizoIot`, {
    restApiName: `iot-advizo-api`,
    deployOptions: {
      metricsEnabled: true,
      loggingLevel: MethodLoggingLevel.INFO, 
      dataTraceEnabled: true,
    },
    cloudWatchRole: true,
    defaultCorsPreflightOptions: {
      allowOrigins: Cors.ALL_ORIGINS,
      allowMethods: ["OPTIONS", "GET", "POST", "PUT", "PATCH", "DELETE"],
      allowHeaders: Cors.DEFAULT_HEADERS, 
    },
  });

  ////////////////////////////////////////////////////////////////////////////////////////
  ///////////////////////////      CREATE RESOURCES APIS      ////////////////////////////
  ////////////////////////////////////////////////////////////////////////////////////////

  const createloginIotApp = new LambdaIntegration(apiIotAdvizo, 
    {allowTestInvoke: false,});

  ////////////////////////////////////////////////////////////////////////////////////////
  /////////////////////////////      CREATE METHOD APIS     //////////////////////////////
  ////////////////////////////////////////////////////////////////////////////////////////

  const resourcePostpushmessageIot = apiAdvizoIot.root.addResource("apiIotAdvizo");
    resourcePostpushmessageIot.addMethod("POST", createloginIotApp); 


  
}