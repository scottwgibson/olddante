import { expect as expectCDK, matchTemplate, MatchStyle } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import * as App from '../lib/olddante-stack';

test('Empty Stack', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new App.OldDanteStack(app, 'MyTestStack');
    // THEN
    expectCDK(stack).to(matchTemplate({
      "Resources": {}
    }, MatchStyle.EXACT))
});
