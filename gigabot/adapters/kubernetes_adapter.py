from kubernetes import client, config
from kubernetes.client.rest import ApiException


class KubernetesAdapter:
    """
    A class to manage interactions with the Kubernetes API, specifically for creating, deleting, and listing cron jobs.
    """

    def __init__(self):
        """
        Initializes the adapter by setting up the API access configuration. This setup is designed to be run
        within a Kubernetes cluster.
        """
        # Uncomment the following line for local development with a kubeconfig file:
        # config.load_kube_config()
        config.load_incluster_config()

    def create_cron_job(
        self,
        namespace,
        name,
        hours,
        minutes,
        image,
        env_vars,
        secret_name,
        image_pull_secret=None,
    ):
        """
        Creates a Kubernetes CronJob resource within a specified namespace with provided environment variables and secrets.
        """
        batch_v1 = client.BatchV1Api()

        # Construct the schedule string from hours and minutes
        if hours == 0:
            schedule = f"*/{minutes} * * * *"
        else:
            schedule = f"{minutes} */{hours} * * *"

        # Setup environment variables from static values and secrets
        env_list = [
            client.V1EnvVar(
                name="COINMARKETCAP_URL", value=env_vars["COINMARKETCAP_URL"]
            ),
            client.V1EnvVar(name="DISCORD_WEBHOOK", value=env_vars["DISCORD_WEBHOOK"]),
            client.V1EnvVar(name="SYMBOL", value=env_vars["SYMBOL"]),
            client.V1EnvVar(
                name="DISCORD_TOKEN",
                value_from=client.V1EnvVarSource(
                    secret_key_ref=client.V1SecretKeySelector(
                        name=secret_name, key="discord_token"
                    )
                ),
            ),
            client.V1EnvVar(
                name="COINMARKETCAP_TOKEN",
                value_from=client.V1EnvVarSource(
                    secret_key_ref=client.V1SecretKeySelector(
                        name=secret_name, key="coinmarketcap_token"
                    )
                ),
            ),
        ]

        container = client.V1Container(
            name=name, image=image, env=env_list, image_pull_policy="Always"
        )

        # Add imagePullSecrets if provided
        image_pull_secrets = (
            [client.V1LocalObjectReference(name=image_pull_secret)]
            if image_pull_secret
            else None
        )

        # Define the Job spec
        job_spec = client.V1JobSpec(
            template=client.V1PodTemplateSpec(
                spec=client.V1PodSpec(
                    restart_policy="OnFailure",
                    containers=[container],
                    image_pull_secrets=image_pull_secrets,
                )
            )
        )

        # Define the CronJob spec using V1CronJobSpec which now replaces V1beta1CronJobSpec
        cron_job_spec = client.V1CronJobSpec(
            schedule=schedule, job_template=client.V1JobTemplateSpec(spec=job_spec)
        )

        # Create the CronJob using V1CronJob which now replaces V1beta1CronJob
        cron_job = client.V1CronJob(
            api_version="batch/v1",
            kind="CronJob",
            metadata=client.V1ObjectMeta(name=name),
            spec=cron_job_spec,
        )

        try:
            api_response = batch_v1.create_namespaced_cron_job(namespace, cron_job)
            print(f"CronJob created. status='{str(api_response.status)}'")
        except ApiException as e:
            print(f"An error occurred: {str(e)}")

    def delete_cron_job(self, namespace, name):
        """
        Deletes a CronJob from a specified Kubernetes namespace.
        """
        batch_v1 = client.BatchV1Api()
        try:
            api_response = batch_v1.delete_namespaced_cron_job(name, namespace)
            print(f"CronJob deleted. status='{str(api_response.status)}'")
        except ApiException as e:
            print(f"An error occurred: {str(e)}")

    def list_cron_jobs(self, namespace):
        """
        Lists all cronjobs in a specified Kubernetes namespace.
        """
        batch_v1 = client.BatchV1Api()
        try:
            cron_jobs = batch_v1.list_namespaced_cron_job(namespace)
            for job in cron_jobs.items:
                print(f"CronJob Name: {job.metadata.name}")
            return cron_jobs.items
        except ApiException as e:
            print(f"Failed to list cronjobs: {str(e)}")
            return []
