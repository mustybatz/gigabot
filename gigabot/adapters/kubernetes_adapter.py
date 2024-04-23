# file: gigabot/adapters/kubernetes_adapter.py

from kubernetes import client, config
from kubernetes.client.rest import ApiException

class KubernetesAdapter:
    """
    A class to manage interactions with the Kubernetes API, specifically for creating and deleting cron jobs.
    """

    def __init__(self):
        """
        Initializes the adapter by setting up the API access configuration. This setup is designed to be run
        within a Kubernetes cluster.
        """
        # Uncomment the following line for local development with a kubeconfig file:
        # config.load_kube_config()
        config.load_incluster_config()

    def create_cron_job(self, namespace, name, hours, minutes, image, env_vars, secret_name, image_pull_secret=None):
        """
        Creates a Kubernetes CronJob resource within a specified namespace with provided environment variables and secrets.

        Args:
            namespace (str): The namespace in which the CronJob will be created.
            name (str): The name of the CronJob resource.
            hours (int): The hour at which the job should run (24-hour format).
            minutes (int): The minute at which the job should run.
            image (str): The Docker image to use for the CronJob.
            env_vars (dict): A dictionary of environment variables to pass to the container.
            secret_name (str): The name of the Kubernetes secret to use for sensitive environment variables.
            image_pull_secret (str): Optional. The name of the Kubernetes imagePullSecrets to use for pulling the docker image.

        Creates a CronJob that runs at the specified hour and minute, using the provided image and environment configuration.
        """
        batch_v1beta1 = client.BatchV1beta1Api()

        # Construct the schedule string from hours and minutes
        schedule = f"{minutes} {hours} * * *"

        # Setup environment variables from static values
        env_list = [
            client.V1EnvVar(name="COINMARKETCAP_URL", value=env_vars["COINMARKETCAP_URL"]),
            client.V1EnvVar(name="DISCORD_WEBHOOK", value=env_vars["DISCORD_WEBHOOK"]),
        ]

        # Setup environment variables sourced from secrets
        env_from_secrets = [
            client.V1EnvVar(
                name="DISCORD_TOKEN",
                value_from=client.V1EnvVarSource(
                    secret_key_ref=client.V1SecretKeySelector(
                        name=secret_name,
                        key="discord_token"
                    )
                )
            ),
            client.V1EnvVar(
                name="COINMARKETCAP_TOKEN",
                value_from=client.V1EnvVarSource(
                    secret_key_ref=client.V1SecretKeySelector(
                        name=secret_name,
                        key="coinmarketcap_token"
                    )
                )
            ),
        ]

        # Combine all environment settings
        env_list.extend(env_from_secrets)

        container = client.V1Container(
            name=name,
            image=image,
            env=env_list,
            image_pull_policy="Always"
        )

        # Add imagePullSecrets if provided
        image_pull_secrets = [client.V1LocalObjectReference(name=image_pull_secret)] if image_pull_secret else None

        # Define the Job spec
        job_spec = client.V1JobSpec(
            template=client.V1PodTemplateSpec(
                spec=client.V1PodSpec(
                    restart_policy='OnFailure',
                    containers=[container],
                    image_pull_secrets=image_pull_secrets  # Set image pull secrets here
                )
            )
        )

        # Define the CronJob spec
        cron_job_spec = client.V1beta1CronJobSpec(
            schedule=schedule,
            job_template=client.V1beta1JobTemplateSpec(
                spec=job_spec
            )
        )

        # Create the CronJob
        cron_job = client.V1beta1CronJob(
            api_version="batch/v1beta1",
            kind="CronJob",
            metadata=client.V1ObjectMeta(name=name),
            spec=cron_job_spec
        )

        try:
            api_response = batch_v1beta1.create_namespaced_cron_job(namespace, cron_job)
            print(f"CronJob created. status='{str(api_response.status)}'")
        except ApiException as e:
            print(f"An error occurred: {str(e)}")

    def delete_cron_job(self, namespace, name):
        """
        Deletes a CronJob from a specified Kubernetes namespace.

        Args:
            namespace (str): The namespace from which to delete the CronJob.
            name (str): The name of the CronJob to delete.
        """
        batch_v1beta1 = client.BatchV1beta1Api()
        try:
            api_response = batch_v1beta1.delete_namespaced_cron_job(
                name,
                namespace,
                client.V1DeleteOptions()
            )
            print(f"CronJob deleted. status='{str(api_response.status)}'")
        except ApiException as e:
            print(f"An error occurred: {str(e)}")

    def list_cron_jobs(self, namespace):
        """
        Lists all cronjobs in a specified Kubernetes namespace.

        Args:
            namespace (str): The namespace from which to list the CronJobs.

        Returns:
            list: A list of cronjobs in the specified namespace.
        """
        batch_v1beta1 = client.BatchV1beta1Api()
        try:
            cron_jobs = batch_v1beta1.list_namespaced_cron_job(namespace)
            for job in cron_jobs.items:
                print(f"CronJob Name: {job.metadata.name}")
            return cron_jobs.items
        except ApiException as e:
            print(f"Failed to list cronjobs: {str(e)}")
            return []
