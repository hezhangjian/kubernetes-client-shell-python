from dataclasses import dataclass
import json
import subprocess

from kubernetes_client_shell.exceptions import (
    ServiceNotFoundError,
    CommandExecutionError,
)


@dataclass
class ServiceSpec:
    clusterIP: str


@dataclass
class Service:
    spec: ServiceSpec


def get_service(namespace: str, name: str) -> Service:
    cmd = ["kubectl", "get", "configmap", name, "-n", namespace, "-o", "json"]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        data = json.loads(result.stdout)
        return Service(**data)
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
