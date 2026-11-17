# AI-for-All

AI-for-All is a NetworkBuster integration repository containing local Gemini, telemetry, machine-to-machine, orbital dashboard, and administration examples.

## Public landing page

Open `index.html`, or publish this repository through GitHub Pages. It links to the integrated LunaRecycle launchpad and administration documentation.

## Included areas

- `networkbuster-session-20260405-data/networkbuster-session-20260405-data/webapp` — Flask Gemini/network dashboard experiment
- `leins/pages/documentation-main/usbnb-main/admin/smoke` — M2M telemetry, SSH, SAT-GPU, and command demos

## Security

The examples are local development tooling. Configure all credentials through environment variables and never commit real API keys, SSH passwords, or service-account credentials.

Required optional variables include:

- `GEMINI_API_KEY`
- `NETWORKBUSTER_API_KEY`

Do not expose SSH or machine-control endpoints to the public internet.
