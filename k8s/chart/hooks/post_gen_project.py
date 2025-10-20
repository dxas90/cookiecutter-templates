#!/usr/bin/env python3
"""
Post-generation hook for processing environment file and updating values.yaml
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

def update_values_yaml(env_vars):
    """Update the values.yaml file with environment variables"""
    values_path = 'values.yaml'

    if not os.path.exists(values_path):
        print(f"Warning: {values_path} not found")
        return

    try:
        # Load existing values.yaml
        with open(values_path, 'r') as f:
            values = yaml.safe_load(f)

        # Ensure env section exists
        if 'env' not in values:
            values['env'] = {}
        if 'variables' not in values['env']:
            values['env']['variables'] = {}

        # Add environment variables
        values['env']['variables'].update(env_vars)

        # Write back to values.yaml
        with open(values_path, 'w') as f:
            yaml.dump(values, f, default_flow_style=False, indent=2)

        print(f"Successfully added {len(env_vars)} environment variables to values.yaml")

    except Exception as e:
        print(f"Error updating values.yaml: {e}")

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

    if env_file_path:
        print(f"Processing environment file: {env_file_path}")
        env_vars = load_env_file(env_file_path)

        if env_vars:
            update_values_yaml(env_vars)
            print(f"Environment variables loaded: {list(env_vars.keys())}")
        else:
            print("No environment variables found in file")
    else:
        print("No environment file specified")

if __name__ == '__main__':
    main()
