# XBOW Code Review Agents

This directory contains agent definitions for automated code review, documentation generation, and quality assurance.

## Agent Types

### 1. Documentation Agent
- **Purpose**: Auto-generate and update documentation
- **Triggers**: Code changes, new features
- **Tasks**: Update docs, generate API references

### 2. Security Review Agent
- **Purpose**: Review code for security vulnerabilities
- **Triggers**: Pull requests, commits
- **Tasks**: Security audit, compliance checks

### 3. Performance Analysis Agent
- **Purpose**: Monitor and analyze performance metrics
- **Triggers**: Scan completion, test runs
- **Tasks**: Profile code, identify bottlenecks

### 4. Test Coverage Agent
- **Purpose**: Ensure adequate test coverage
- **Triggers**: Code changes
- **Tasks**: Generate coverage reports, suggest tests

### 5. Dependency Agent
- **Purpose**: Manage and audit dependencies
- **Triggers**: Version updates, security alerts
- **Tasks**: Update requirements, audit packages

---

## Agent Configuration Files

Each agent should have a configuration file in JSON format:

```json
{
  "agent_name": "string",
  "description": "string",
  "version": "string",
  "enabled": boolean,
  "trigger_events": ["string"],
  "tasks": ["string"],
  "schedule": "cron_expression"
}
```

### Example: documentation-agent.json

```json
{
  "agent_name": "documentation-agent",
  "description": "Automatically generates and updates documentation",
  "version": "1.0.0",
  "enabled": true,
  "trigger_events": ["push", "release", "new_module"],
  "tasks": [
    "generate_api_docs",
    "update_architecture_docs",
    "generate_examples"
  ],
  "schedule": "0 2 * * *"
}
```

---

## Agent Directory Structure

Each agent should have:
- `<agent_name>.json` - Configuration
- `<agent_name>_rules.yml` - Processing rules
- `<agent_name>_templates/` - Template files if applicable

