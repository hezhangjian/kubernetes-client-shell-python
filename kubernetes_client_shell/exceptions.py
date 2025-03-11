"""Exceptions for kubernetes client shell operations."""


class KubernetesClientError(Exception):
    """Base exception for kubernetes client shell operations."""
    pass


class ConfigMapNotFoundError(KubernetesClientError):
    """Raised when a configmap is not found."""
    pass


class ServiceNotFoundError(KubernetesClientError):
    """Raised when a service is not found."""
    pass


class CommandExecutionError(KubernetesClientError):
    """Raised when a kubectl command fails to execute."""
    pass
