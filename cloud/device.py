import json
from azure.iot.device import Message, MethodResponse
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device.aio import ProvisioningDeviceClient
import logging


class Device:

    def __init__(self, model_id, provisioning_host, id_scope, registration_id, symmetric_key):
        self.model_id = model_id
        self.provisioning_host = provisioning_host
        self.id_scope = id_scope
        self.registration_id = registration_id
        self.symmetric_key = symmetric_key
        self.iot_hub_device_client = None
        self.registration_result = None

    async def create_iot_hub_device_client(self):
        self.registration_result = await self.register_provisioning_device_client()

        if self.registration_result.status == "assigned":
            logging.info("device.create_iot_hub_device_client:registration_result.status={status} "
                         "registration_result.registration_state.assigned_hub={registration_state_assigned_hub} "
                         "self.registration_result.registration_state.device_id={registration_state_device_id}"
                         .format(status=self.registration_result.status,
                                 registration_state_assigned_hub=self
                                 .registration_result.registration_state.assigned_hub,
                                 registration_state_device_id=self.registration_result.registration_state.device_id))

            self.iot_hub_device_client = IoTHubDeviceClient.create_from_symmetric_key(
                symmetric_key=self.symmetric_key,
                hostname=self.registration_result.registration_state.assigned_hub,
                device_id=self.registration_result.registration_state.device_id,
                product_info=self.model_id,
            )
            return self.iot_hub_device_client
        else:
            logging.error("device.create_iot_hub_device_client:Could not provision device. Aborting Plug and Play "
                          "device connection.")

    async def register_provisioning_device_client(self):
        provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
            provisioning_host=self.provisioning_host,
            registration_id=self.registration_id,
            id_scope=self.id_scope,
            symmetric_key=self.symmetric_key,
        )
        provisioning_device_client.provisioning_payload = {"modelId": self.model_id}
        return await provisioning_device_client.register()

    async def execute_command_listener(self, method_name, user_command_handler, create_user_response_handler):
        while True:
            if method_name:
                command_name = method_name
            else:
                command_name = None

            command_request = await self.iot_hub_device_client.receive_method_request(command_name)
            logging.info("device.create_iot_hub_device_client:payload={payload}"
                         .format(payload=command_request.payload))

            values = {}
            if not command_request.payload:
                logging.info("device.create_iot_hub_device_client:No payload")
            else:
                values = command_request.payload

            await user_command_handler(values)

            response_status = 200
            response_payload = create_user_response_handler(values)

            command_response = MethodResponse.create_from_method_request(
                command_request, response_status, response_payload
            )

            try:
                await self.iot_hub_device_client.send_method_response(command_response)
            except Exception as ex:
                logging.error("device.create_iot_hub_device_client:Responding to the {command} command failed "
                              "error={error}"
                              .format(command=method_name, error=ex))

    async def execute_property_listener(self):
        ignore_keys = ["__t", "$version"]
        while True:
            patch = await self.iot_hub_device_client.receive_twin_desired_properties_patch()

            logging.info("device.create_iot_hub_device_client:Desired properties patch was {patch}"
                         .format(patch=patch))

            version = patch["$version"]
            prop_dict = {}

            for prop_name, prop_value in patch.items():
                if prop_name in ignore_keys:
                    continue
                else:
                    prop_dict[prop_name] = {
                        "ac": 200,
                        "ad": "Successfully executed patch",
                        "av": version,
                        "value": prop_value,
                    }

            await self.iot_hub_device_client.patch_twin_reported_properties(prop_dict)

    async def send_telemetry(self, telemetry):
        message = Message(json.dumps(telemetry))
        message.content_encoding = "utf-8"
        message.content_type = "application/json"
        logging.info("device.send_telemetry:telemetry={telemetry}"
                     .format(telemetry=telemetry))
        await self.iot_hub_device_client.send_message(message)
