# Helm Chart Cookiecutter Template

This cookiecutter template generates a production-ready Helm chart with comprehensive Kubernetes resource definitions and optional testing capabilities.

**Repository**: [https://github.com/dxas90/cookiecutter-templates.git](https://github.com/dxas90/cookiecutter-templates.git)

## Features

- **Complete Kubernetes resources**: Deployment, Service, ConfigMap, Secret, HTTPRoute (Gateway API), HPA, PVC, and more
- **Gateway API support**: Modern HTTPRoute resources instead of traditional Ingress
- **Environment variable support**: Automatic processing of `.env` files
- **Security best practices**: Security contexts, service accounts, network policies
- **Testing framework**: Includes `helm-unittest` test suites
- **Flexible configuration**: Extensive customization options via `cookiecutter.json`
- **Template safety**: Helm Go-templates are properly wrapped to avoid conflicts with Jinja2

## Quick Start

### Generate a Chart

```bash
# Interactive mode
cookiecutter https://github.com/dxas90/cookiecutter-templates.git --directory=k8s/chart

# Non-interactive with defaults
cookiecutter https://github.com/dxas90/cookiecutter-templates.git --directory=k8s/chart --no-input --output-dir generated

# With custom values
cookiecutter https://github.com/dxas90/cookiecutter-templates.git --directory=k8s/chart --no-input \
  chart_name=my-app \
  image_repository=my-registry/my-app \
  httproute_enabled=true
```

### Using Environment Files

Automatically include environment variables in your chart:

```bash
# Create an environment file
cat > my-app.env << EOF
DATABASE_URL=postgresql://user:pass@localhost/db
API_KEY=your-secret-api-key
DEBUG=true
LOG_LEVEL=info
EOF

# Generate chart with environment file
cookiecutter https://github.com/dxas90/cookiecutter-templates.git --directory=k8s/chart --no-input \
  env_file_path=my-app.env \
  chart_name=my-app
```

Environment variables are automatically:
- Added to `values.yaml` under `env.variables`
- Included in the Kubernetes Secret (base64 encoded)
- Available for use in deployments

## Configuration Options

Key configuration parameters in `cookiecutter.json`:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `chart_name` | Name of the Helm chart | "learn" |
| `chart_version` | Chart version | "0.1.0" |
| `app_version` | Application version | "v0.0.12" |
| `image_repository` | Docker image repository | "dxas90/learn" |
| `replicaCount` | Number of pod replicas | 1 |
| `service_type` | Kubernetes service type | "ClusterIP" |
| `httproute_enabled` | Enable HTTPRoute resource | false |
| `httproute_gateway_name` | Gateway name to attach to | "gateway" |
| `httproute_gateway_namespace` | Gateway namespace | "gateway-system" |
| `httproute_hostname` | Hostname for HTTPRoute | "example.local" |
| `persistence_enabled` | Enable persistent storage | false |
| `autoscaling_enabled` | Enable horizontal pod autoscaler | false |
| `resources_limits_*` | CPU and memory limits | "1m", "56Mi" |

See `cookiecutter.json` for the complete list of configuration options.

## Prerequisites

### Gateway API Support

This template uses HTTPRoute from the Kubernetes Gateway API instead of traditional Ingress resources. To use HTTPRoute features, you need:

1. **Gateway API CRDs installed** in your cluster:
   ```bash
   kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.0.0/standard-install.yaml
   ```

2. **A Gateway controller** (e.g., Istio, Envoy Gateway, NGINX Gateway, etc.)

3. **A Gateway resource** deployed in your cluster that the HTTPRoute can attach to.

Example Gateway resource:
```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: gateway
  namespace: gateway-system
spec:
  gatewayClassName: istio  # or your gateway class
  listeners:
  - name: http
    port: 80
    protocol: HTTP
```

## Testing

The template includes comprehensive test suites using `helm-unittest`.

### Install helm-unittest

```bash
helm plugin install https://github.com/helm-unittest/helm-unittest || true
```

### Run Tests

```bash
# Generate a chart first
cookiecutter https://github.com/dxas90/cookiecutter-templates.git --directory=k8s/chart --no-input --output-dir generated

# Run tests
CHART_DIR=$(ls -d generated/* | head -n1)
helm unittest "$CHART_DIR" -f 'tests/unittest/*_test.yaml'
```

### Update Snapshots

If you intentionally change templates and need to update test snapshots:

```bash
helm unittest "$CHART_DIR" -f 'tests/unittest/*_test.yaml' -u
```

Snapshot files are stored under `tests/__snapshot__/` and should be committed to version control.

## Template Structure

```
{{cookiecutter.chart_name}}/
├── Chart.yaml                    # Chart metadata
├── values.yaml                   # Default configuration values
└── templates/
    ├── _helpers.tpl              # Template helpers
    ├── deployment.yaml           # Application deployment
    ├── service.yaml              # Service definition
    ├── configmap.yaml            # Configuration data
    ├── secret.yaml               # Secret data
    ├── serviceaccount.yaml       # Service account
    ├── httproute.yaml            # HTTPRoute configuration (Gateway API)
    ├── hpa.yaml                  # Horizontal pod autoscaler
    ├── pvc.yaml                  # Persistent volume claim
    ├── networkpolicy.yaml        # Network policies
    ├── poddisruptionbudget.yaml  # Pod disruption budget
    └── NOTES.txt                 # Post-install notes
```

## Best Practices

### Template Safety
- Helm Go-templates (`{{ .Values.foo }}`) are wrapped in Jinja2 raw blocks to prevent conflicts
- After generation, standard Helm commands work normally (`helm template`, `helm install`)

### Security
- Security contexts are enabled by default
- Network policies can be enabled for network isolation
- Secrets are properly base64 encoded

### Resource Management
- Resource limits and requests are configurable
- Horizontal pod autoscaling is available
- Pod disruption budgets for high availability

## Environment File Format

```bash
# Comments are supported
KEY1=value1
KEY2="value with spaces"
SECRET_KEY=sensitive-value
DEBUG=true
```

## Deployment

After generating your chart:

```bash
# Install the chart
helm install my-release ./my-chart

# Upgrade the chart
helm upgrade my-release ./my-chart

# Template and review
helm template my-release ./my-chart
```

## Notes

- If you modify templates, ensure Helm Go-template syntax is properly wrapped in Jinja2 raw blocks
- Test files are included as examples - customize them based on your specific requirements
- The post-generation hook automatically processes environment files and updates chart values
