

# Node Restart API Setup

This project uses Docker Compose to deploy three services:
1. **node_restarter**: A service that handles restarting nodes via a REST API.
2. **ip_sender**: A service that sends IP addresses to a specified endpoint.
3. **ngrok-node-restart-setup**: An Ngrok service to expose the `ip_sender` service to the internet.

## Services

### 1. `node_restarter`
This service is responsible for restarting nodes via a REST API. It listens on port `6000`.

- **Build context**: `./tapo-restart-api/`
- **Exposed port**: `6000:6000`
- **Environment Variables**:
  - `TB_API_USERNAME`: Your ThingsBoard API username.
  - `TB_API_PASSWORD`: Your ThingsBoard API password.

### 2. `ip_sender`
This service sends the IP address to an endpoint and listens on port `6001`.

- **Build context**: `./node-restart/`
- **Exposed port**: `6001:6001`
- **Volumes**:
  - Maps the `./node-restart/` directory to `/app` inside the container.

### 3. `ngrok-node-restart-setup`
This service uses Ngrok to expose the `ip_sender` service to the internet.

- **Image**: `ngrok/ngrok:latest`
- **Environment Variables**:
  - `NGROK_AUTHTOKEN`: Your Ngrok authentication token.
  - `NGROK_REGION`: The Ngrok region (default: `us`).
- **Exposed port**: `4042:4040` (Ngrok Admin interface on host port `4042`).
- **Command**: Exposes the `ip_sender` service to the internet via Ngrok.

## Requirements

- **Docker**: Ensure that Docker is installed on your machine.
- **Docker Compose**: This setup requires Docker Compose to orchestrate the services.

## Setup

### 1. Clone the Repository
Clone the repository containing this Docker Compose configuration.

```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Build and Start the Services

Run the following command to build and start all services:

```bash
docker-compose up --build
```

This command will:
- Build and start the `node_restarter` service.
- Build and start the `ip_sender` service.
- Start the `ngrok-node-restart-setup` service.

### 3. Access the Services
- `node_restarter`: Available at `http://localhost:6000`.
- `ip_sender`: Available at `http://localhost:6001`.
- **Ngrok**: You can access the Ngrok admin interface at `http://localhost:4042`, and the exposed endpoint at `http://separately-champion-bulldog.ngrok-free.app`.

## Environment Variables

Ensure the following environment variables are set in the `docker-compose.yml` file or your `.env` file:
- `TB_API_USERNAME`: Your ThingsBoard API username.
- `TB_API_PASSWORD`: Your ThingsBoard API password.
- `NGROK_AUTHTOKEN`: Your Ngrok authentication token.
- `NGROK_REGION`: The Ngrok region (`us` by default).

## Networks

All services are connected to the same Docker network (`my-node-restart-network`), ensuring they can communicate with each other.

## Troubleshooting

If you encounter any issues, check the logs of the individual services:

```bash
docker-compose logs <service-name>
```

For example, to view logs for `node_restarter`:

```bash
docker-compose logs node_restarter
```

### Restarting Services

To restart any service, use the following command:

```bash
docker-compose restart <service-name>
```

### Stopping Services

To stop all services:

```bash
docker-compose down
```

---

