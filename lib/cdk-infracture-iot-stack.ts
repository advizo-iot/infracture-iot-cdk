import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { stackReactIot } from './stack/stackReactIot';


export class CdkInfractureIotStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const stackAdvizoIot = stackReactIot(this); 

  }
}
