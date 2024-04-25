from kubernetes import client, config
from kubernetes.client.rest import ApiException

class KubernetesAdapter:
    """
    A class to manage interactions with the Kubernetes API, specifically for creating, deleting, editing, and listing Deployments and Cron Jobs.
    """

    def __init__(self):
        """
        Initializes the adapter by setting up the API access configuration. This setup is designed to be run
        within a Kubernetes cluster.
        """
        config.load_incluster_config()

    def create_deployment(
        self,
        namespace,
        name,
        image,
        env_vars,
        secret_name,
        replicas=1,
        image_pull_secret=None,
    ):
        """
        Creates a Kubernetes Deployment within a specified namespace with provided environment variables and secrets.

        Args:
            namespace (str): The namespace in which to create the deployment.
            name (str): The name of the deployment.
            image (str): The Docker image to use for the deployment.
            env_vars (dict): Dictionary of environment variables to set in the pod.
            secret_name (str): The name of the Kubernetes secret to use for sensitive environment variables.
            replicas (int): The number of replicas for the deployment.
            image_pull_secret (str, optional): The name of the Kubernetes imagePullSecrets to use for pulling the docker image.
        """
        apps_v1 = client.AppsV1Api()

        # Setup environment variables from static values and secrets
        env_list = [
            client.V1EnvVar(name=key, value=value)
            for key, value in env_vars.items()
            if key not in ["DISCORD_TOKEN", "COINMARKETCAP_TOKEN"]
        ] + [
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

        # Define the container spec
        container = client.V1Container(
            name=name, image=image, env=env_list, image_pull_policy="Always"
        )

        # Define the pod template spec
        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"app": name}),
            spec=client.V1PodSpec(
                containers=[container],
                image_pull_secrets=(
                    [client.V1LocalObjectReference(name=image_pull_secret)]
                    if image_pull_secret
                    else None
                ),
            ),
        )

        # Define the deployment spec
        deployment_spec = client.V1DeploymentSpec(
            replicas=replicas,
            selector=client.V1LabelSelector(match_labels={"app": name}),
            template=template,
        )

        # Create the deployment object
        deployment = client.V1Deployment(
            api_version="apps/v1",
            kind="Deployment",
            metadata=client.V1ObjectMeta(name=name),
            spec=deployment_spec,
        )

        try:
            api_response = apps_v1.create_namespaced_deployment(namespace, deployment)
            print(f"Deployment created. status='{api_response.status}'")
        except ApiException as e:
            print(f"An error occurred: {str(e)}")


    def list_deployments(self, namespace):
        apps_v1 = client.AppsV1Api()
        try:
            deployments = apps_v1.list_namespaced_deployment(namespace)
            for deployment in deployments.items:
                print(f"Deployment Name: {deployment.metadata.name}")
            return deployments.items
        except ApiException as e:
            print(f"Failed to list deployments: {str(e)}")
            return []

    def delete_deployment(self, namespace, name):
        apps_v1 = client.AppsV1Api()
        try:
            api_response = apps_v1.delete_namespaced_deployment(name, namespace)
            print(f"Deployment deleted. status='{api_response.status}'")
        except ApiException as e:
            print(f"An error occurred: {str(e)}")

    def update_deployment(self, namespace, name, image=None, env_vars=None, replicas=None):
        apps_v1 = client.AppsV1Api()
        deployment = apps_v1.read_namespaced_deployment(name, namespace)
        if image:
            deployment.spec.template.spec.containers[0].image = image
        if env_vars:
            deployment.spec.template.spec.containers[0].env = self._create_env_list(env_vars, deployment.spec.template.spec.containers[0].env[0].value_from.secret_key_ref.name)
        if replicas is not None:
            deployment.spec.replicas = replicas
        try:
            api_response = apps_v1.patch_namespaced_deployment(name, namespace, deployment)
            print(f"Deployment updated. status='{api_response.status}'")
        except ApiException as e:
            print(f"An error occurred: {str(e)}")

    def _create_env_list(self, env_vars, secret_name):
        """Helper method to create a list of environment variables."""
        env_list = [client.V1EnvVar(name=key, value=env_vars[key]) for key in env_vars if key not in ["DISCORD_TOKEN", "COINMARKETCAP_TOKEN"]]
        env_list.append(client.V1EnvVar(name="DISCORD_TOKEN", value_from=client.V1EnvVarSource(secret_key_ref=client.V1SecretKeySelector(name=secret_name, key="discord_token"))))
        env_list.append(client.V1EnvVar(name="COINMARKETCAP_TOKEN", value_from=client.V1EnvVarSource(secret_key_ref=client.V1SecretKeySelector(name=secret_name, key="coinmarketcap_token"))))
        return env_list

    # Existing methods for CronJobs...

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
