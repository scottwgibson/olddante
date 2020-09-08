import { expect as expectCDK, matchTemplate, MatchStyle } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import * as App from '../lib/olddante-stack';
import { SynthUtils } from '@aws-cdk/assert';

test('Empty Stack', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new App.OldDanteStack(app, 'MyTestStack');
    // THEN
    expect(SynthUtils.toCloudFormation(stack)).toMatchSnapshot();
});
