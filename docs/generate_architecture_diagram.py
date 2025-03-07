from diagrams import Diagram, Cluster
from diagrams.azure.compute import KubernetesServices
from diagrams.azure.devops import ContainerRegistry
from diagrams.azure.network import VirtualNetworks, Subnets
from diagrams.azure.general import ResourceGroups
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.analytics import OpenTelemetry

with Diagram("Giglet Architecture", show=False, filename="giglet-architecture", outformat="png"):
    with Cluster("Azure Cloud"):
        rg = ResourceGroups("giglet-rg")
        acr = ContainerRegistry("giglet-acr")

        with Cluster("Virtual Network"):
            vnet = VirtualNetworks("giglet-vnet")
            subnet = Subnets("aks-subnet")

            with Cluster("Kubernetes (AKS)"):
                job_service = KubernetesServices("Job Service")
                user_service = KubernetesServices("User Service")
                payment_service = KubernetesServices("Payment Service")
                notification_service = KubernetesServices("Notification Service")

            vnet >> subnet >> [job_service, user_service, payment_service, notification_service]

        otel = OpenTelemetry("OpenTelemetry Collector")
        prom = Prometheus("Prometheus")
        grafana = Grafana("Grafana")

        job_service >> otel
        payment_service >> otel
        notification_service >> otel
        user_service >> otel

        otel >> prom
        prom >> grafana

        rg >> acr
        rg >> vnet