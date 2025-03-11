import json
import subprocess

from kubernetes_client_shell.exceptions import (
    ConfigMapNotFoundError,
    CommandExecutionError,
)


def get_configmap(namespace: str, name: str):
    cmd = ["kubectl", "get", "configmap", name, "-n", namespace, "-o", "json"]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        if "NotFound" in e.stderr:
            raise ConfigMapNotFoundError(
                f"ConfigMap '{name}' not found in namespace '{namespace}'"
            ) from e
        raise CommandExecutionError(
            f"Failed to get ConfigMap: {e.stderr}"
        ) from e
    except json.JSONDecodeError as e:
        raise CommandExecutionError(
            f"Failed to parse kubectl output: {e}"
        ) from e


def get_configmap_data(namespace: str, name: str):
    configmap = get_configmap(namespace, name)
    return configmap["data"]


def get_configmap_value(namespace: str, name: str, key: str):
    data = get_configmap_data(namespace, name)
    return data.get(key)
