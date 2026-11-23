---
title: Marketplace template moves off App Runner
type: change
authors:
  - lava
created: 2026-07-16T16:14:09.462982Z
---

The AWS Marketplace CloudFormation template now deploys the platform UI as an
ECS Fargate service behind the existing gateway load balancer, using host-based
routing for `ui.<domain>`. Previously the UI ran on AWS App Runner, which is
closed to new customers since April 2026 and caused deployments into fresh AWS
accounts to fail.

Existing stacks are unaffected; the change applies to new deployments of the
template. The UI's security group is also tightened to only accept traffic
from the load balancer instead of the whole VPC.
