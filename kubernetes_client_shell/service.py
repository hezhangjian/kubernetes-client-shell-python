from dataclasses import dataclass
import json
import subprocess

from kubernetes_client_shell.exceptions import (
    ServiceNotFoundError,
    CommandExecutionError,
)

def get_service(namespace: str, name: str) -> dict:
    cmd = ["kubectl", "get", "service", name, "-n", namespace, "-o", "json"]

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
            raise ServiceNotFoundError(
                f"Service '{name}' not found in namespace '{namespace}'"
            ) from e
        raise CommandExecutionError(
            f"Failed to get ConfigMap: {e.stderr}"
        ) from e
    except json.JSONDecodeError as e:
        raise CommandExecutionError(
            f"Failed to parse kubectl output: {e}"
        ) from e
