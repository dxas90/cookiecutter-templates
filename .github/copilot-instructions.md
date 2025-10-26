# AI Coding Agent Instructions

This repository provides production-ready **cookiecutter templates** for Kubernetes deployments using **Helm** and **Kustomize**. Focus on template generation patterns, not end-user Kubernetes deployment.

## Architecture Overview

**Dual Template System**: Two independent cookiecutter templates with feature parity:
- `k8s/chart/` - Helm chart template with Go template syntax (wrapped in `{%- raw -%}` blocks)
- `k8s/kustomize/` - Kustomize template with direct YAML + Jinja2 conditionals

**Critical Pattern**: Templates use **Jinja2 for cookiecutter** and **Go templates for Helm**. Never mix syntaxes.

## Key Components

### Template Structure
```
{{cookiecutter.chart_name}}/          # Helm output directory
{{cookiecutter.app_name}}/            # Kustomize output directory
  base/                               # Base Kustomize resources
  overlays/dev|staging|prod/          # Environment-specific patches
```

### Post-Generation Hooks
- `hooks/post_gen_project.py` - Processes environment files and updates configurations
- **Critical**: Read cookiecutter context from `.cookiecutter_context.json`, NOT template variables
- Environment variables automatically classified: `*SECRET*|*PASSWORD*|*KEY*|*TOKEN*` → Secrets, others → ConfigMaps

### Configuration Files
- `cookiecutter.json` - Template parameters with defaults
- `example.env` - Sample environment file showing KEY=VALUE format
- Both templates support `env_file_path` parameter for batch configuration

## Developer Workflows

### Template Generation Testing
```bash
# Test Helm template
pipx run cookiecutter ./k8s/chart --no-input --output-dir /tmp/test-helm

# Test Kustomize template
pipx run cookiecutter ./k8s/kustomize --no-input --output-dir /tmp/test-kustomize

# Test with environment file
cookiecutter ./k8s/chart --no-input env_file_path=example.env
```

### Template Validation
```bash
# Helm validation
helm lint /tmp/test-helm/learn
helm template test /tmp/test-helm/learn

# Kustomize validation
kubectl kustomize /tmp/test-kustomize/learn/overlays/prod
```

## Project-Specific Patterns

### Jinja2 Template Safety
- **Always wrap Go templates**: `{%- raw -%}...{% endraw %}` in Helm templates
- **Conditional resources**: Use `{% if cookiecutter.feature_enabled == 'true' %}` for optional components
- **Environment variables**: Automatic classification in post-generation hooks

### Gateway API Migration
- **HTTPRoute over Ingress**: All templates use Gateway API v1 HTTPRoute
- **Conditional inclusion**: `httproute_enabled` parameter controls HTTPRoute resource generation
- **Gateway references**: Templates expect existing Gateway resources (`httproute_gateway_name`)

### Common Resources Feature
- **Shared secrets/settings**: `common_secret_enabled` and `common_settings_enabled` parameters
- **envFrom blocks**: Conditional inclusion of common ConfigMaps and Secrets
- **Naming convention**: `common-secrets`, `common-settings` as default names

### Resource Conditionals
- **PVC mounting**: Only mount when `persistence.enabled=true` to avoid pod scheduling failures
- **Feature toggles**: Most resources are conditional based on `*_enabled` parameters
- **Multi-environment**: Kustomize overlays patch base resources for dev/staging/prod

## Integration Points

### Environment File Processing
```python
# In post_gen_project.py - read context correctly
with open('.cookiecutter_context.json', 'r') as f:
    context = json.load(f)
env_file_path = context.get('cookiecutter', {}).get('env_file_path')
```

### Template Dependencies
- **Helm**: Go template helpers in `_helpers.tpl`
- **Kustomize**: Strategic merge patches for environment customization
- **Both**: Common resource structure with different templating approaches

### External Dependencies
- **Gateway API CRDs**: Required for HTTPRoute functionality
- **cookiecutter**: Python package for template generation
- **Optional**: helm-unittest for Helm chart testing

## Critical Debugging

### Template Generation Failures
1. **Check Jinja syntax**: Ensure proper `{% if %}` conditions
2. **Verify context access**: Use `.cookiecutter_context.json` in hooks
3. **Test conditionals**: Verify boolean parameter comparisons (`== 'true'`)

### Resource Mounting Issues
- **PVC errors**: Always check `persistence.enabled` before mounting volumes
- **Common resources**: Verify `*_enabled` flags match actual resource existence

When working with these templates, always test both Helm and Kustomize outputs and verify the generated YAML is valid for the target Kubernetes version.
