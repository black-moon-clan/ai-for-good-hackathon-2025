from brainbase_labs import BrainbaseLabs
import os

# SDK @ https://pypi.org/project/brainbase-labs/
# docs (SDK) @ https://docs.usebrainbase.com/sdk/
# docs (API) @ https://docs.usebrainbase.com/api-reference/overview
# based guide @ https://docs.usebrainbase.com/based-crash-course
# VS Code extension @ https://marketplace.visualstudio.com/items?itemName=BrainbaseLabsInc.brainbase-based

bb = BrainbaseLabs(api_key=os.getenv("BB_API_KEY"))

twilio_integration = bb.team.integrations.twilio.create(
    account_sid=os.getenv("TWILIO_ACCOUNT_SID"),
    auth_token=os.getenv("TWILIO_AUTH_TOKEN")
)

raw_phone_number = "+18333916030"

# phone_number = bb.team.assets.register_phone_number(
#     phone_number=raw_phone_number,
#     integration_id=twilio_integration.id
# )

worker = bb.workers.create(name="My Shift Booker", description="A shift booking assistant", status="active")

flow = bb.workers.flows.create(
    worker_id=worker.id,
    name="Shift Booker",
    path="./shift_booker/shift_booker.based",
    label="v1"
)

voice_deployment = bb.workers.deployments.voice.create(
    worker_id=worker.id,
    name="Shift Booker Voice Deployment",
    flow_id=flow.id,
    phone_number=raw_phone_number,
    config={}
)

if voice_deployment:
    print(f"Successfully deployed shift booking assistant to {voice_deployment.phone_number}")
else:
    print("Failed to deploy shift booking assistant")