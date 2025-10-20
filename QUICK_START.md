# Quick Start Guide

## Repository

**GitHub**: [https://github.com/dxas90/cookiecutter-templates.git](https://github.com/dxas90/cookiecutter-templates.git)
**Shorthand**: `gh:dxas90/cookiecutter-templates`

## Prerequisites

```bash
# Install cookiecutter
pip install cookiecutter

# Install Gateway API CRDs (for HTTPRoute support)
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.4.0/standard-install.yaml
```

## Basic Usage

### Helm Chart

```bash
# Generate Helm chart
cookiecutter gh:dxas90/cookiecutter-templates --directory=k8s/chart
```

### Kustomize

```bash
# Generate Kustomize configuration
cookiecutter gh:dxas90/cookiecutter-templates --directory=k8s/kustomize
```

## Non-Interactive Examples

### Helm with HTTPRoute

```bash
cookiecutter gh:dxas90/cookiecutter-templates --directory=k8s/chart --no-input \
  chart_name=my-app \
  image_repository=myorg/my-app \
  httproute_enabled=true \
  httproute_hostname=my-app.example.com
```

### Kustomize with HTTPRoute

```bash
cookiecutter gh:dxas90/cookiecutter-templates --directory=k8s/kustomize --no-input \
  app_name=my-app \
  image_repository=myorg/my-app \
  httproute_enabled=true \
  httproute_hostname=my-app.example.com
```

## Deployment

### Helm

```bash
cd my-app
helm install my-app . --namespace my-namespace --create-namespace
```

### Kustomize

```bash
cd my-app
kubectl apply -k overlays/dev    # Development
kubectl apply -k overlays/staging # Staging
kubectl apply -k overlays/prod   # Production
```

## More Information

- [Full Documentation](README.md)
- [Gateway API Migration Guide](GATEWAY_API_MIGRATION.md)
- [Helm Chart Details](k8s/chart/README.md)
- [Kustomize Details](k8s/kustomize/README.md)
