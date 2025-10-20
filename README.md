# Kubernetes Deployment Templates

A collection of production-ready cookiecutter templates for Kubernetes application deployment using both Helm and Kustomize.

**Repository**: [https://github.com/dxas90/cookiecutter-templates.git](https://github.com/dxas90/cookiecutter-templates.git)
**Shorthand**: `gh:dxas90/cookiecutter-templates`

## Overview

This repository provides two comprehensive cookiecutter templates for deploying applications to Kubernetes:

- **Helm Chart Template** (`k8s/chart/`) - Traditional Helm-based deployments
- **Kustomize Template** (`k8s/kustomize/`) - Native Kubernetes configuration management

Both templates include modern best practices, security configurations, multi-environment support, and extensive customization options.

## Installation

### Prerequisites

- Python 3.6+
- cookiecutter
- kubectl (for Kustomize)
- helm (for Helm charts)

### Install Cookiecutter

```bash
pip install cookiecutter
# or
pipx install cookiecutter
```

### Repository Access

All examples in this documentation use the GitHub shorthand syntax:
```bash
gh:dxas90/cookiecutter-templates
```

This is equivalent to:
```bash
https://github.com/dxas90/cookiecutter-templates.git
```

## Templates

### 🎡 Helm Chart Template

Located in `k8s/chart/`

**Features:**
- Complete Helm chart with all common Kubernetes resources
- Environment variable processing from `.env` files
- helm-unittest test suites included
- Security best practices built-in
- Flexible resource management
- Template safety (proper Jinja2/Go-template separation)

**Quick Start:**
```bash
# Generate a new Helm chart
cookiecutter gh:dxas90/cookiecutter-templates --directory=k8s/chart --no-input \
  chart_name=my-app \
  image_repository=my-registry/my-app

# With environment file
cookiecutter gh:dxas90/cookiecutter-templates --directory=k8s/chart --no-input \
  env_file_path=my-app.env
```

### 🔧 Kustomize Template

Located in `k8s/kustomize/`

**Features:**
- Multi-environment overlays (dev/staging/prod)
- Automatic environment variable classification
- Conditional resource generation
- Post-generation automation
- Native kubectl integration
- GitOps-friendly structure

**Quick Start:**
```bash
# Generate a new Kustomize configuration
cookiecutter gh:dxas90/cookiecutter-templates --directory=k8s/kustomize --no-input \
  app_name=my-app \
  image_repository=my-registry/my-app

# With environment file
cookiecutter gh:dxas90/cookiecutter-templates --directory=k8s/kustomize --no-input \
  env_file_path=my-app.env
```

## Comparison

| Feature | Helm Chart | Kustomize |
|---------|------------|-----------|
| **Templating** | Go templates with values | Overlay-based patches |
| **Dependencies** | Helm CLI required | kubectl built-in |
| **Learning Curve** | Steeper (template syntax) | Moderate (YAML patches) |
| **Environments** | Multiple values files | Overlay directories |
| **Package Management** | Helm repositories | Git repositories |
| **Rollback** | Built-in (`helm rollback`) | Manual (`kubectl apply`) |
| **Validation** | `helm lint`, `helm template` | `kubectl kustomize` |
| **Testing** | helm-unittest | Manual validation |
| **Gateway API** | HTTPRoute support | HTTPRoute support |

## Common Features

Both templates include:

### 📦 Kubernetes Resources
- **Deployment** - Application workload
- **Service** - Network access
- **ConfigMap** - Configuration data
- **Secret** - Sensitive data
- **ServiceAccount** - Pod identity
- **HTTPRoute** - HTTP routing (Gateway API)
- **HPA** - Auto-scaling
- **PVC** - Persistent storage
- **NetworkPolicy** - Network security
- **PodDisruptionBudget** - High availability

### 🔒 Security Features
- Security contexts (non-root, read-only filesystem)
- Network policies for traffic isolation
- Proper secret handling and base64 encoding
- RBAC with service accounts
- Pod security standards compliance

### 📊 Resource Management
- CPU and memory limits/requests
- Horizontal pod autoscaling
- Persistent volume claims
- Storage class configuration
- Resource quotas and limits

### 🌍 Multi-Environment Support
- **Development**: Lower resources, debug settings
- **Staging**: Production-like configuration
- **Production**: Full resources, security hardening

### 🔄 Health Checks
- Liveness probes for application health
- Readiness probes for traffic routing
- Startup probes for slow applications
- Configurable probe parameters

## Environment File Support

Both templates support environment files in KEY=VALUE format:

```bash
# Configuration values
app_name=my-application
image_repository=my-registry/my-app
image_tag=v1.0.0
replicaCount=3

# Resource settings
resources_limits_cpu=100m
resources_limits_memory=256Mi

# Feature toggles
httproute_enabled=true
autoscaling_enabled=true
persistence_enabled=true

# Environment variables (automatically classified)
DATABASE_URL=postgresql://db:5432/myapp
API_SECRET_KEY=your-secret-key
LOG_LEVEL=info
DEBUG=false
```

Variables containing keywords like `PASSWORD`, `SECRET`, `KEY`, `TOKEN` are automatically placed in Secrets, while others go to ConfigMaps.

## Gateway API Support

Both templates now use **HTTPRoute** from the Kubernetes Gateway API instead of traditional Ingress resources. This provides:

- **Better traffic management**: More advanced routing capabilities
- **Protocol support**: HTTP/2, gRPC, and future protocols
- **Vendor neutrality**: Standardized across different ingress controllers
- **Enhanced security**: Built-in support for advanced authentication and authorization

### Gateway API Requirements

To use HTTPRoute features, your cluster needs:

1. **Gateway API CRDs**:
   ```bash
   kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.4.0/standard-install.yaml
   ```

2. **Gateway controller** (choose one):
   - Istio Gateway
   - Envoy Gateway
   - NGINX Gateway Fabric
   - Kong Gateway
   - HAProxy Ingress

3. **Gateway resource** deployed in your cluster that HTTPRoutes can attach to

## Prerequisites

### Common Requirements
- Python 3.6+
- cookiecutter
- kubectl

```bash
pip install cookiecutter
```

### Helm Template Additional Requirements
- Helm 3.x
- helm-unittest plugin (for testing)

```bash
# Install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Install helm-unittest plugin
helm plugin install https://github.com/helm-unittest/helm-unittest
```

### Kustomize Template Additional Requirements
- kubectl with Kustomize support (1.14+)
- OR standalone kustomize

```bash
# Kustomize is built into kubectl 1.14+
kubectl version

# Or install standalone kustomize
curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh" | bash
```

## Usage Examples

### Basic Usage

```bash
# Helm chart
cookiecutter gh:dxas90/cookiecutter-templates --directory=k8s/chart

# Kustomize
cookiecutter gh:dxas90/cookiecutter-templates --directory=k8s/kustomize
```

### Non-interactive with Custom Values

```bash
# Helm chart
cookiecutter gh:dxas90/cookiecutter-templates --directory=k8s/chart --no-input \
  chart_name=my-web-app \
  image_repository=myorg/web-app \
  image_tag=v1.2.3 \
  httproute_enabled=true \
  autoscaling_enabled=true

# Kustomize
cookiecutter gh:dxas90/cookiecutter-templates --directory=k8s/kustomize --no-input \
  app_name=my-web-app \
  image_repository=myorg/web-app \
  image_tag=v1.2.3 \
  httproute_enabled=true \
  autoscaling_enabled=true
```

### With Environment Files

```bash
# Create environment file
cat > web-app.env << EOF
# App settings
chart_name=my-web-app
app_name=my-web-app
image_repository=myorg/web-app
image_tag=v1.2.3
replicaCount=3

# Features
httproute_enabled=true
autoscaling_enabled=true
persistence_enabled=true

# Environment variables
DATABASE_URL=postgresql://db:5432/webapp
REDIS_URL=redis://redis:6379
API_SECRET_KEY=your-secret-key
LOG_LEVEL=info
EOF

# Helm
cookiecutter gh:dxas90/cookiecutter-templates --directory=k8s/chart --no-input env_file_path=web-app.env

# Kustomize
cookiecutter gh:dxas90/cookiecutter-templates --directory=k8s/kustomize --no-input env_file_path=web-app.env
```

## Deployment

### Helm Deployment

```bash
# Generate chart
cookiecutter gh:dxas90/cookiecutter-templates --directory=k8s/chart --no-input chart_name=my-app

# Deploy
helm install my-app ./my-app

# Upgrade
helm upgrade my-app ./my-app

# Rollback
helm rollback my-app 1
```

### Kustomize Deployment

```bash
# Generate configuration
cookiecutter gh:dxas90/cookiecutter-templates --directory=k8s/kustomize --no-input app_name=my-app

# Deploy to environments
kubectl apply -k my-app/overlays/dev
kubectl apply -k my-app/overlays/staging
kubectl apply -k my-app/overlays/prod

# Preview changes
kubectl kustomize my-app/overlays/prod
```

## Testing

### Helm Charts

```bash
# Lint chart
helm lint ./my-app

# Template and validate
helm template my-app ./my-app

# Run unit tests
helm unittest ./my-app -f 'tests/unittest/*_test.yaml'
```

### Kustomize

```bash
# Validate YAML
kubectl kustomize my-app/overlays/dev | kubectl apply --dry-run=client -f -

# Validate all environments
for env in dev staging prod; do
  echo "Validating $env..."
  kubectl kustomize my-app/overlays/$env | kubectl apply --dry-run=client -f -
done
```

## Best Practices

### Security
- Always run containers as non-root users
- Use read-only root filesystems where possible
- Enable network policies in production
- Regularly rotate secrets and keys
- Use service accounts with minimal permissions

### Resource Management
- Set appropriate resource limits and requests
- Use horizontal pod autoscaling for variable workloads
- Configure pod disruption budgets for high availability
- Monitor resource usage and adjust limits accordingly

### Operations
- Use health checks for all applications
- Implement proper logging and monitoring
- Use GitOps for configuration management
- Test deployments in staging before production
- Document all configuration changes

### Environment Management
- Keep environment-specific configurations minimal
- Use secrets for sensitive data
- Validate configurations before deployment
- Use consistent labeling across environments

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with both templates
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Check the template-specific README files
- Review the example configurations
- Open an issue for bugs or feature requests

## Roadmap

- [ ] ArgoCD application templates
- [ ] Flux deployment configurations
- [ ] Istio service mesh integration
- [ ] Monitoring and observability templates
- [ ] CI/CD pipeline templates
