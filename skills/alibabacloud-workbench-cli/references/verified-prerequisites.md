# Local prerequisite supplement

This is a local verification note, not an original file from the vendor ZIP.

- Confirm server product, region, instance ID and OS. This skill targets ECS; do not assume Simple Application Server is compatible. Current official docs support Linux targets, although the local CLI is cross-platform.
- Check existing CLI and credential configuration before requesting new credentials. Print only presence/mode/region, never key values. Keep secrets out of group chat. Skill installation does not install the CLI or authenticate Alibaba Cloud.
- Confirm Cloud Assistant is installed and healthy before connecting. Do not install or restart it merely as a diagnostic step without the relevant authorization.
- The live official policy adds `ecs-workbench:EndSessions`, used for session close and automatic cleanup, to the vendor package's action list. First-use service-linked-role creation must be restricted to `workbench.ecs.aliyuncs.com`. Restrict instance ARNs only for actions that support resource-level authorization.
- The official guide states first connection automatically adds an internal TCP 22 security-group rule for source `100.104.0.0/16`. Check existing rules and scope approval before connecting; do not describe first connection as necessarily read-only, and never substitute public SSH exposure.
- The local computer needs Alibaba Cloud API/WebSocket connectivity; file transfer additionally requires the instance to reach its regional internal OSS endpoint.

Official sources:
- https://help.aliyun.com/en/ecs/user-guide/install-and-configure-workbench-cli-credentials
- https://help.aliyun.com/en/ecs/user-guide/connect-to-an-instance-through-workbench-cli
