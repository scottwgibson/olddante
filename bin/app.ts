#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { OldDanteStack } from '../lib/olddante-stack';

const envEU  = { region: 'eu-central-1' };

const app = new cdk.App();
new OldDanteStack(app, 'OldDante', { env: envEU });
