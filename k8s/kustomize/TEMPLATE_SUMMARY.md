# Kustomize Template Features

This document outlines the key features and capabilities of the Kustomize cookiecutter template.

## Template Capabilities

### Resource Types Supported

The template generates the following Kubernetes resources:

- **Deployment**: Application workload with configurable replicas, resources, and security contexts
- **Service**: ClusterIP, NodePort, or LoadBalancer service types
- **ConfigMap**: Non-sensitive configuration data
- **Secret**: Sensitive configuration data (passwords, keys, tokens)
- **ServiceAccount**: Identity for pods with optional RBAC
- **PersistentVolumeClaim**: Storage for stateful applications
- **HTTPRoute**: HTTP routing with Gateway API support
- **HorizontalPodAutoscaler**: Automatic scaling based on CPU/memory
- **NetworkPolicy**: Network isolation and security
- **PodDisruptionBudget**: High availability during updates

### Environment Management

#### Base Configuration
- Shared resources and common configuration
- Default values and standard Kubernetes manifests
- Template helpers and common labels

#### Environment Overlays

**Development (`overlays/dev/`)**
- Reduced resource requirements (CPU: 10m, Memory: 64Mi)
- Debug logging enabled
- Single replica for cost efficiency
- Development-specific hostnames (dev.example.com)
- Relaxed security for easier debugging

**Staging (`overlays/staging/`)**
- Production-like resource allocation (CPU: 50m, Memory: 256Mi)
- Multiple replicas for testing high availability
- Staging-specific hostnames (staging.example.com)
- Performance monitoring enabled
- Optional TLS configuration

**Production (`overlays/prod/`)**
- Full resource allocation (CPU: 100m, Memory: 512Mi)
- High availability with multiple replicas
- Production domains with TLS
- Strict security policies
- Pod disruption budgets
- Network policies enabled

### Configuration Features

#### Environment Variables
- **Automatic classification**: Variables containing keywords like PASSWORD, SECRET, KEY, TOKEN are placed in Secrets
- **ConfigMap variables**: Non-sensitive configuration goes to ConfigMaps
- **Environment file support**: KEY=VALUE format with automatic processing

#### Resource Management
- **CPU/Memory limits and requests**: Configurable per environment
- **Storage**: Optional persistent volumes with configurable size and storage class
- **Scaling**: Manual replica count and automatic horizontal scaling

#### Security
- **Security contexts**: Non-root user, read-only filesystem options
- **Service accounts**: Optional dedicated service accounts
- **Network policies**: Ingress/egress traffic control
- **Secrets management**: Automatic base64 encoding

#### Health Checks
- **Liveness probes**: Application health monitoring
- **Readiness probes**: Traffic routing readiness
- **Configurable endpoints**: Custom health check paths and ports
- **Startup probes**: Support for slow-starting applications

#### Networking
- **Service types**: ClusterIP, NodePort, LoadBalancer
- **HTTPRoute**: HTTP routing with Gateway API support
- **Gateway integration**: Modern traffic management with parentRefs
- **Port configuration**: Flexible service and container port mapping

### Advanced Features

#### Init Containers
- Optional init containers for setup tasks
- Configurable resources and security contexts
- Common use cases: database migrations, file preparation

#### Labels and Annotations
- Standard Kubernetes recommended labels
- Environment-specific labels
- Custom labels for team/owner identification
- Annotations for monitoring and tooling integration

#### Conditional Resources
Resources can be enabled/disabled based on configuration:
- PersistentVolumeClaim (persistence_enabled)
- HTTPRoute (httproute_enabled)
- HorizontalPodAutoscaler (autoscaling_enabled)
- ServiceAccount (serviceaccount_enabled)
- NetworkPolicy (networkpolicy_enabled)
- PodDisruptionBudget (poddisruptionbudget_enabled)

### Post-Generation Processing

The included hook script (`hooks/post_gen_project.py`) provides:

1. **Environment file processing**
   - Parses KEY=VALUE format files
   - Classifies variables as config or secrets
   - Updates YAML manifests automatically

2. **Resource cleanup**
   - Removes disabled resources
   - Cleans up unused files
   - Validates configuration consistency

3. **Documentation generation**
   - Creates deployment instructions
   - Provides environment-specific examples
   - Generates validation commands

### Best Practices Included

#### Security
- Non-root security contexts by default
- Read-only root filesystem options
- Network policies for traffic isolation
- Proper secret handling

#### Reliability
- Resource limits prevent resource exhaustion
- Health checks ensure traffic routing to healthy pods
- Pod disruption budgets maintain availability during updates
- Init containers handle dependencies

#### Operations
- Comprehensive labeling for monitoring and management
- Environment-specific configurations
- Structured logging configuration
- Monitoring and observability hooks

### Usage Patterns

#### GitOps Integration
The template structure supports GitOps workflows:
- Base configurations in version control
- Environment-specific overlays
- Clear separation of concerns
- Automated deployment pipelines

#### Development Workflow
1. Generate template with development defaults
2. Customize base configuration
3. Add environment-specific overrides
4. Test in development environment
5. Promote through staging to production

#### Multi-Environment Deployment
```bash
# Deploy to each environment
kubectl apply -k overlays/dev
kubectl apply -k overlays/staging
kubectl apply -k overlays/prod
```

This template provides a comprehensive foundation for Kubernetes application deployment with modern best practices and operational requirements built-in.
