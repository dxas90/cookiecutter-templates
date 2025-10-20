# Gateway API Migration Summary

## Overview

Successfully migrated both Helm and Kustomize templates from traditional Ingress resources to HTTPRoute from the Kubernetes Gateway API.

## Changes Made

### 🎡 Helm Chart Template (`k8s/chart/`)

#### Files Modified:
- **`templates/ingress.yaml` → `templates/httproute.yaml`**
  - Replaced Ingress API with HTTPRoute (gateway.networking.k8s.io/v1)
  - Added support for parentRefs, hostnames, matches, and backendRefs
  - Maintained flexibility with configurable gateway references

- **`values.yaml`**
  - Replaced `ingress:` section with `httproute:` configuration
  - Added gateway name, namespace, and hostname settings
  - Maintained backward compatibility for service port references

- **`cookiecutter.json`**
  - Replaced `ingress_enabled` with `httproute_enabled`
  - Added `httproute_gateway_name`, `httproute_gateway_namespace`, `httproute_hostname`
  - Updated default values to be Gateway API compliant

### 🔧 Kustomize Template (`k8s/kustomize/`)

#### Files Modified:
- **`base/ingress.yaml` → `base/httproute.yaml`**
  - Converted to HTTPRoute with parentRefs and hostnames
  - Simplified configuration removing Traefik-specific annotations
  - Added Gateway API standard structure

- **Overlay patches**:
  - **`overlays/dev/ingress-patch.yaml` → `httproute-patch.yaml`**
    - Dev subdomain: `{app_name}-dev.{hostname}`
  - **`overlays/staging/ingress-patch.yaml` → `httproute-patch.yaml`**
    - Staging subdomain: `{app_name}-staging.{hostname}`
  - **`overlays/prod/ingress-patch.yaml` → `httproute-patch.yaml`**
    - Production hostname: `{hostname}`

- **Kustomization files**:
  - **`base/kustomization.yaml`**: Updated resource reference from `ingress.yaml` to `httproute.yaml`
  - **Overlay kustomizations**: Updated patch references to `httproute-patch.yaml`

- **`cookiecutter.json`**
  - Replaced ingress settings with HTTPRoute equivalents
  - Removed TLS-specific settings (handled at Gateway level)
  - Added gateway configuration options

### 📚 Documentation Updates

#### All README files updated to reflect Gateway API usage:
- **Prerequisites sections**: Added Gateway API CRD installation instructions
- **Configuration tables**: Replaced ingress parameters with HTTPRoute equivalents
- **Template structures**: Updated file listings to show `httproute.yaml`
- **Examples**: Changed all examples from `ingress_enabled` to `httproute_enabled`

#### Main project README (`README.md`):
- Added comprehensive Gateway API support section
- Updated comparison table to include Gateway API support
- Added gateway controller options and requirements
- Updated all example commands and configurations

## New Configuration Options

### Helm Chart (`cookiecutter.json`)
```json
"httproute_enabled": false,
"httproute_gateway_name": "gateway",
"httproute_gateway_namespace": "gateway-system",
"httproute_hostname": "example.local"
```

### Kustomize (`cookiecutter.json`)
```json
"httproute_enabled": false,
"httproute_gateway_name": "gateway",
"httproute_gateway_namespace": "gateway-system",
"httproute_hostname": "example.local"
```

## Gateway API Benefits

### Advantages over Ingress:
1. **Better traffic management**: More advanced routing capabilities
2. **Protocol support**: HTTP/2, gRPC, and future protocols
3. **Vendor neutrality**: Standardized across different ingress controllers
4. **Enhanced security**: Built-in support for advanced authentication and authorization
5. **Future-proof**: Actively developed as the next-generation ingress standard

### HTTPRoute Features Used:
- **parentRefs**: Attach to specific Gateway resources
- **hostnames**: Define which hostnames the route responds to
- **matches**: Path-based routing with PathPrefix matching
- **backendRefs**: Route to specific services with port configuration

## Prerequisites for Users

### Required Infrastructure:
1. **Gateway API CRDs installed**:
   ```bash
   kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.0.0/standard-install.yaml
   ```

2. **Gateway controller** (one of):
   - Istio Gateway
   - Envoy Gateway
   - NGINX Gateway Fabric
   - Kong Gateway
   - HAProxy Ingress

3. **Gateway resource** deployed that HTTPRoutes can attach to:
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

## Migration Impact

### Breaking Changes:
- Configuration parameter names changed from `ingress_*` to `httproute_*`
- File names changed from `ingress.yaml` to `httproute.yaml`
- Requires Gateway API CRDs and Gateway controller

### Backward Compatibility:
- All other functionality remains unchanged
- Environment variable processing works the same
- Resource management and security features unchanged
- Multi-environment support maintained

## Environment-Specific Behavior

### Development
- Hostname: `{app_name}-dev.{httproute_hostname}`
- Basic HTTP routing

### Staging
- Hostname: `{app_name}-staging.{httproute_hostname}`
- Production-like configuration

### Production
- Hostname: `{httproute_hostname}`
- Full production settings

## Usage Examples

### Generate with HTTPRoute enabled:
```bash
# Helm
cookiecutter https://github.com/dxas90/cookiecutter-templates.git --directory=k8s/chart --no-input \
  chart_name=my-app \
  httproute_enabled=true \
  httproute_hostname=my-app.example.com

# Kustomize
cookiecutter https://github.com/dxas90/cookiecutter-templates.git --directory=k8s/kustomize --no-input \
  app_name=my-app \
  httproute_enabled=true \
  httproute_hostname=my-app.example.com
```

The migration maintains all existing functionality while providing modern, standardized HTTP routing through the Kubernetes Gateway API.
