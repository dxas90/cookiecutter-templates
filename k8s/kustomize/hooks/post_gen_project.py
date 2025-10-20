#!/usr/bin/env python3
"""
Post-generation hook for processing environment file and updating ConfigMap and Secret YAML files
"""
import os
import yaml
import base64

def load_env_file(env_file_path):
    """Load environment variables from a KEY=VALUE file"""
    env_vars = {}

    if not env_file_path or not os.path.exists(env_file_path):
        return env_vars

    try:
        with open(env_file_path, 'r') as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue

                # Parse KEY=VALUE format
                if '=' in line:
                    key, value = line.split('=', 1)
                    # Remove quotes if present
                    value = value.strip('"\'')
                    env_vars[key.strip()] = value
    except Exception as e:
        print(f"Warning: Could not parse env file {env_file_path}: {e}")

    return env_vars

def classify_env_vars(env_vars):
    """Classify environment variables into config and secrets based on naming"""
    config_vars = {}
    secret_vars = {}

    secret_keywords = ['password', 'secret', 'key', 'token', 'credential', 'auth']

    for key, value in env_vars.items():
        key_lower = key.lower()
        if any(keyword in key_lower for keyword in secret_keywords):
            secret_vars[key] = value
        else:
            config_vars[key] = value

    return config_vars, secret_vars

def update_configmap(config_vars):
    """Update the ConfigMap YAML file with configuration variables"""
    configmap_path = 'base/configmap.yaml'

    if not os.path.exists(configmap_path):
        print(f"Warning: {configmap_path} not found")
        return

    try:
        # Load existing configmap.yaml
        with open(configmap_path, 'r') as f:
            content = f.read()

        # Find the data section and add variables
        lines = content.split('\n')
        data_section_found = False
        new_lines = []

        for line in lines:
            new_lines.append(line)
            if line.strip() == 'data:':
                data_section_found = True
                # Add new config variables
                for key, value in config_vars.items():
                    new_lines.append(f'  {key}: "{value}"')

        if data_section_found:
            # Write back to configmap.yaml
            with open(configmap_path, 'w') as f:
                f.write('\n'.join(new_lines))
            print(f"Successfully added {len(config_vars)} configuration variables to ConfigMap")
        else:
            print("Warning: Could not find data section in ConfigMap")

    except Exception as e:
        print(f"Error updating ConfigMap: {e}")

def update_secret(secret_vars):
    """Update the Secret YAML file with secret variables"""
    secret_path = 'base/secret.yaml'

    if not os.path.exists(secret_path):
        print(f"Warning: {secret_path} not found")
        return

    try:
        # Load existing secret.yaml
        with open(secret_path, 'r') as f:
            content = f.read()

        # Find the stringData section and add variables
        lines = content.split('\n')
        stringdata_section_found = False
        new_lines = []

        for line in lines:
            new_lines.append(line)
            if line.strip() == 'stringData:':
                stringdata_section_found = True
                # Add new secret variables
                for key, value in secret_vars.items():
                    new_lines.append(f'  {key}: "{value}"')

        if stringdata_section_found:
            # Write back to secret.yaml
            with open(secret_path, 'w') as f:
                f.write('\n'.join(new_lines))
            print(f"Successfully added {len(secret_vars)} secret variables to Secret")
        else:
            print("Warning: Could not find stringData section in Secret")

    except Exception as e:
        print(f"Error updating Secret: {e}")

def cleanup_conditional_files():
    """Remove files that are conditionally included but not needed"""

    # Get the configuration values from cookiecutter context
    import json

    try:
        with open('.cookiecutter_context.json', 'r') as f:
            context = json.load(f)
        cookiecutter_vars = context.get('cookiecutter', {})
    except (FileNotFoundError, json.JSONDecodeError):
        # Fallback to default values if context file not found
        cookiecutter_vars = {}

    persistence_enabled = str(cookiecutter_vars.get('persistence_enabled', 'false')).lower() == 'true'
    httproute_enabled = str(cookiecutter_vars.get('httproute_enabled', 'false')).lower() == 'true'
    autoscaling_enabled = str(cookiecutter_vars.get('autoscaling_enabled', 'false')).lower() == 'true'
    serviceaccount_enabled = str(cookiecutter_vars.get('serviceaccount_enabled', 'false')).lower() == 'true'
    networkpolicy_enabled = str(cookiecutter_vars.get('networkpolicy_enabled', 'false')).lower() == 'true'
    poddisruptionbudget_enabled = str(cookiecutter_vars.get('poddisruptionbudget_enabled', 'false')).lower() == 'true'

    # List of conditional files and their conditions
    conditional_files = [
        ('base/pvc.yaml', not persistence_enabled),
        ('base/httproute.yaml', not httproute_enabled),
        ('base/hpa.yaml', not autoscaling_enabled),
        ('base/serviceaccount.yaml', not serviceaccount_enabled),
        ('base/networkpolicy.yaml', not networkpolicy_enabled),
        ('base/poddisruptionbudget.yaml', not poddisruptionbudget_enabled),
    ]

    # Remove files that start with template conditionals (they weren't processed)
    for file_path, should_remove in conditional_files:
        if should_remove and os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    # If file starts with template conditionals and ends with endif, remove it
                    template_start = '{' + '% '
                    template_end = ' %' + '}'
                    if content.strip().startswith(template_start) and content.strip().endswith(template_end):
                        # Check if the content between conditional statements is empty or only whitespace
                        lines = content.strip().split('\n')
                        if len(lines) <= 2:  # Only has conditional start and end tags
                            os.remove(file_path)
                            print(f"Removed empty conditional file: {file_path}")
            except Exception as e:
                print(f"Warning: Could not process {file_path}: {e}")

def main():
    # Get the env file path from cookiecutter context
    import json

    # Read the cookiecutter context
    try:
        with open('.cookiecutter_context.json', 'r') as f:
            context = json.load(f)
        env_file_path = context.get('cookiecutter', {}).get('env_file_path', '')
    except (FileNotFoundError, json.JSONDecodeError):
        # Fallback to empty string if context file not found
        env_file_path = ''

    # Clean up any quotes or whitespace that might be introduced
    env_file_path = env_file_path.strip().strip('"').strip("'")

    if env_file_path and env_file_path != "None" and env_file_path != "null":
        print(f"Processing environment file: {env_file_path}")
        env_vars = load_env_file(env_file_path)

        if env_vars:
            config_vars, secret_vars = classify_env_vars(env_vars)

            if config_vars:
                update_configmap(config_vars)
                print(f"Configuration variables: {list(config_vars.keys())}")

            if secret_vars:
                update_secret(secret_vars)
                print(f"Secret variables: {list(secret_vars.keys())}")
        else:
            print("No environment variables found in file")
    else:
        print("No environment file specified")

    # Clean up conditional files
    cleanup_conditional_files()

    print("Kustomize template generation completed!")

if __name__ == '__main__':
    main()
