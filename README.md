# GIGA BOT

## Description

A brief description of your Discord bot project.

## Commands

The bot supports the following commands:

- `/price <symbol> <token_address>`: Fetches the current price of a cryptocurrency. Replace `<symbol>` with the symbol of the cryptocurrency and `<token_address>` with the token address of the cryptocurrency. This command is implemented in the [`price`](gigabot/bot/bot_setup.py) function.

- `/price-cron <symbol> <token_address> <minute> <hour>`: Fetches the current price of a cryptocurrency periodically. Replace `<symbol>` with the symbol of the cryptocurrency, `<token_address>` with the token address of the cryptocurrency, `<minute>` with the minute interval, and `<hour>` with the hour interval. This command is implemented in the [`price_cron`](gigabot/bot/bot_setup.py) function.

## Deployment

To deploy the GIGA BOT into a Kubernetes cluster using the Helm chart, follow these steps:

1. Clone the repository: `git clone https://github.com/your-username/your-repo.git`
2. Change directory to the Helm chart: `cd helm-charts/gigabot-server`
3. Customize the Helm chart values in `values.yaml` according to your requirements.
4. Install the Helm chart: `helm install gigabot .`
5. Verify that the deployment was successful: `kubectl get pods`
6. If necessary, update the Helm chart values and upgrade the deployment: `helm upgrade gigabot .`
7. To uninstall the deployment, run: `helm uninstall gigabot`

## Usage

1. Create a new Discord bot on the [Discord Developer Portal](https://discord.com/developers/applications).
2. Copy the bot token and paste it in the `.env` file.
3. Customize the bot's behavior by modifying the code in `main.py`.
4. Start the bot: `poetry run python -m gigabot.main`


## Deployment with ArgoCD
To deploy the GIGA BOT using ArgoCD, follow these steps:

1. Create a new release by updating the image tag in the `values.yaml` file of the Helm chart.
2. Push the updated release to your Git repository.
3. Open the ArgoCD web interface.
4. Sync the project by selecting the appropriate Git repository and target revision.
5. ArgoCD will automatically deploy the updated version of the GIGA BOT to your Kubernetes cluster.

Note: Make sure to update the image tag in the `values.yaml` file before pushing the release to ensure that the latest version of the bot is deployed.

## License

This project is close source.