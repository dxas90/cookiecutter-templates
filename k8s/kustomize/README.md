# Kustomize Cookiecutter Template

This cookiecutter template generates a comprehensive Kustomize configuration for Kubernetes applications with multi-environment support and best practices built-in.

**Repository**: [https://github.com/dxas90/cookiecutter-templates.git](https://github.com/dxas90/cookiecutter-templates.git)
**Shorthand**: `gh:dxas90/cookiecutter-templates --directory=k8s/kustomize`

## Features

- **Multi-environment support**: Dev, staging, and production overlays
- **Comprehensive resources**: Deployment, Service, ConfigMap, Secret, HTTPRoute, HPA, PVC, and more
- **Environment variable processing**: Automatic classification of config vs secrets
- **Security best practices**: Security contexts, service accounts, network policies
- **Resource management**: CPU/memory limits, autoscaling, pod disruption budgets
- **Conditional resources**: Enable/disable features based on configuration
- **Post-generation automation**: Environment file processing and cleanup

## Prerequisites

- Python 3.6+
- cookiecutter
- kubectl with Kustomize support (or standalone kustomize)
- **Gateway API support** for HTTPRoute resources

```bash
pip install cookiecutter

# Install Gateway API CRDs
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.4.0/standard-install.yaml
```

### Gateway API Requirements

This template uses HTTPRoute from the Kubernetes Gateway API. You need:
1. Gateway API CRDs installed (see command above)
2. A Gateway controller (Istio, Envoy Gateway, NGINX Gateway, etc.)
3. A Gateway resource deployed that HTTPRoutes can attach to

## Quick Start

### Generate a Kustomize Configuration

```bash
# Interactive mode
cookiecutter gh:dxas90/cookiecutter-templates --directory=k8s/kustomize

# Non-interactive with defaults
cookiecutter gh:dxas90/cookiecutter-templates --directory=k8s/kustomize --no-input

# With custom values
cookiecutter gh:dxas90/cookiecutter-templates --directory=k8s/kustomize --no-input \
  app_name=my-app \
  image_repository=my-registry/my-app \
  httproute_enabled=true \
  autoscaling_enabled=true
```

### Using Environment Files

You can provide configuration values and environment variables via an environment file:

```bash
# Create configuration file
cat > my-app.env << EOF
# Application settings
app_name=my-application
image_repository=my-registry/my-app
image_tag=v1.0.0
replicaCount=3

# Enable features
httproute_enabled=true
autoscaling_enabled=true
persistence_enabled=true

# Environment variables (will be classified automatically)
DATABASE_URL=postgresql://db:5432/myapp
API_SECRET_KEY=your-secret-key
LOG_LEVEL=info
DEBUG=false
EOF

# Generate with environment file
cookiecutter gh:dxas90/cookiecutter-templates --directory=k8s/kustomize --no-input env_file_path=my-app.env
```

Environment variables are automatically classified:
- **ConfigMap**: Non-sensitive configuration (LOG_LEVEL, DEBUG)
- **Secret**: Sensitive data containing keywords like KEY, SECRET, PASSWORD, TOKEN

## Configuration Options

Key parameters in `cookiecutter.json`:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `app_name` | Application name | "learn" |
| `app_version` | Application version | "v0.0.12" |
| `image_repository` | Docker image repository | "dxas90/learn" |
| `image_tag` | Image tag | "latest" |
| `replicaCount` | Number of replicas | 1 |
| `service_type` | Service type | "ClusterIP" |
| `httproute_enabled` | Enable HTTPRoute | false |
| `httproute_gateway_name` | Gateway name to attach to | "gateway" |
| `httproute_gateway_namespace` | Gateway namespace | "gateway-system" |
| `httproute_hostname` | Hostname for HTTPRoute | "example.local" |
| `persistence_enabled` | Enable persistent storage | true |
| `autoscaling_enabled` | Enable HPA | false |
| `networkpolicy_enabled` | Enable network policies | true |
| `serviceaccount_enabled` | Enable service account | true |

### Resource Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `resources_limits_cpu` | CPU limit | "25m" |
| `resources_limits_memory` | Memory limit | "263M" |
| `resources_requests_cpu` | CPU request | "25m" |
| `resources_requests_memory` | Memory request | "263M" |

### Ingress Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `ingress_host` | Ingress hostname | "example.local" |
| `ingress_tls_enabled` | Enable TLS | false |

### Autoscaling Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `autoscaling_minReplicas` | Minimum replicas | 1 |
| `autoscaling_maxReplicas` | Maximum replicas | 100 |
| `autoscaling_targetCPUUtilizationPercentage` | CPU target | 80 |

## Generated Structure

```
{{cookiecutter.app_name}}/
├── kustomization.yaml              # Main Kustomize configuration
├── NOTES.txt                       # Usage instructions
├── base/                           # Base Kubernetes manifests
│   ├── kustomization.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── serviceaccount.yaml
│   ├── pvc.yaml
│   ├── httproute.yaml
│   ├── hpa.yaml
│   ├── networkpolicy.yaml
│   └── poddisruptionbudget.yaml
└── overlays/                       # Environment-specific configurations
    ├── dev/
    │   ├── kustomization.yaml
    │   ├── deployment-patch.yaml
    │   └── httproute-patch.yaml
    ├── staging/
    │   ├── kustomization.yaml
    │   ├── deployment-patch.yaml
    │   └── httproute-patch.yaml
    └── prod/
        ├── kustomization.yaml
        ├── deployment-patch.yaml
        └── httproute-patch.yaml
```

## Environment Overlays

### Development (`overlays/dev/`)
- Lower resource requirements
- Debug logging enabled
- Development subdomain (dev.example.com)
- Relaxed security settings

### Staging (`overlays/staging/`)
- Production-like settings
- Staging subdomain (staging.example.com)
- Optional TLS configuration
- Performance monitoring enabled

### Production (`overlays/prod/`)
- Full resource allocation
- Production domain
- TLS with cert-manager integration
- Strict security policies
- High availability settings

## Deployment

Deploy to different environments using kubectl with Kustomize:

```bash
# Development
kubectl apply -k my-app/overlays/dev

# Staging
kubectl apply -k my-app/overlays/staging

# Production
kubectl apply -k my-app/overlays/prod
```

## Validation

Preview the rendered manifests before applying:

```bash
# Build and preview
kustomize build my-app/overlays/dev

# Or with kubectl
kubectl kustomize my-app/overlays/dev
```

## Post-Generation Processing

The template includes a post-generation hook (`hooks/post_gen_project.py`) that:

1. **Processes environment files**: Parses KEY=VALUE format files
2. **Classifies variables**: Automatically determines ConfigMap vs Secret placement
3. **Updates manifests**: Injects variables into appropriate YAML files
4. **Removes unused resources**: Deletes disabled features (based on `*_enabled` flags)
5. **Provides completion summary**: Shows next steps and deployment commands

## Environment File Format

```bash
# Configuration values (non-sensitive)
LOG_LEVEL=info
DEBUG=false
MAX_CONNECTIONS=100

# Secrets (automatically detected by keywords)
DATABASE_PASSWORD=secretvalue
API_SECRET_KEY=your-secret-key
JWT_TOKEN=your-jwt-token

# Mixed configuration
DATABASE_URL=postgresql://user:password@db:5432/app
REDIS_URL=redis://redis:6379
```

Variables containing keywords like `PASSWORD`, `SECRET`, `KEY`, `TOKEN` are automatically placed in Secrets, while others go to ConfigMaps.

## Customization

After generation, you can:

1. **Modify resource limits** based on your application requirements
2. **Add environment-specific variables** to overlay patches
3. **Configure ingress hostnames** and TLS certificates
4. **Adjust autoscaling parameters** for your workload
5. **Enable additional security policies** as needed

## Best Practices

- **Resource Management**: Set appropriate CPU/memory limits for your application
- **Security**: Enable network policies and security contexts in production
- **High Availability**: Use pod disruption budgets and multiple replicas
- **Monitoring**: Configure health checks and resource monitoring
- **Environment Separation**: Use different overlays for different environments

## Comparison with Helm

| Feature | Kustomize | Helm |
|---------|-----------|------|
| **Templating** | Overlay-based | Go templates |
| **Dependencies** | None (kubectl built-in) | Helm CLI required |
| **Configuration** | Environment files + patches | values.yaml |
| **Environments** | Overlay directories | Multiple values files |
| **Learning Curve** | Moderate | Steeper |

Choose Kustomize if you prefer:
- Native kubectl integration
- Simpler overlay-based approach
- No additional tooling requirements
- Declarative configuration management
