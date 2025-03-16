import os

from dotenv import load_dotenv
from brainbase_labs import BrainbaseLabs

# SDK @ https://pypi.org/project/brainbase-labs/
# docs (SDK) @ https://docs.usebrainbase.com/sdk/
# docs (API) @ https://docs.usebrainbase.com/api-reference/overview
# based guide @ https://docs.usebrainbase.com/based-crash-course
# VS Code extension @ https://marketplace.visualstudio.com/items?itemName=BrainbaseLabsInc.brainbase-based

load_dotenv()

brainbase_client = BrainbaseLabs(api_key=os.getenv("BRAINBASE_API_KEY"))

# twilio_integration = brainbase_client.team.integrations.twilio.create(
#     account_sid=os.getenv("TWILIO_ACCOUNT_SID"),
#     auth_token=os.getenv("TWILIO_AUTH_TOKEN")
# )

raw_phone_number = os.getenv("TWILIO_PHONE_NUMBER")

# phone_number = brainbase_client.team.assets.register_phone_number(
#     phone_number=raw_phone_number,
#     integration_id=twilio_integration.id
# )

worker = brainbase_client.workers.create(name=os.getenv("BRAINBASE_WORKER_NAME"), description=os.getenv("BRAINBASE_WORKER_DESCRIPTION"), status="active")

flow = brainbase_client.workers.flows.create(
    worker_id=worker.id,
    name=os.getenv("BRAINBASE_FLOW_NAME"),
    path="./rit_client_survey.based", # path=os.getenv("BRAINBASE_FLOW_SCRIPT_PATH")
    label=os.getenv("BRAINBASE_FLOW_LABEL"),
    validate=False
)

voice_deployment = brainbase_client.workers.deployments.voice.create(
    worker_id=worker.id,
    name=os.getenv("BRAINBASE_VOICE_DEPLOYMENT_NAME"),
    flow_id=flow.id,
    phone_number=raw_phone_number,
    config={}
)

if voice_deployment:
    print(f"Successfully deployed {os.getenv("BRAINBASE_VOICE_DEPLOYMENT_NAME")} to {voice_deployment.phone_number}")
else:
    print(f"Failed to deploy {BRAINBASE_VOICE_DEPLOYMENT_NAME}")
