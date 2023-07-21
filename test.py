import array
import argparse
import ast
import json

import msrest
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod

# python test.py --device_id Cobot --method_name MoveJControlCommand --position_array "[-3.14, -0.5, 0.5, -.5, -.5, .5]"

parser = argparse.ArgumentParser(description="Process command-line arguments.")

iothub_connection_str = "HostName=100638182IotHub.azure-devices.net;SharedAccessKeyName=service;SharedAccessKey" \
                        "=lvHQWwVYdyhxjOpxKzwp39EDJnQyWmklEd73eMCcG8U="

parser.add_argument("--device_id", type=str, help="The device ID.")
parser.add_argument("--method_name", type=str, help="The method name.")
parser.add_argument("--payload", type=str, help="List of positions as json object.")

args = parser.parse_args()

device_id = args.device_id
method_name = args.method_name
payload = args.payload

try:
    # Create IoTHubRegistryManager
    iothub_registry_manager = IoTHubRegistryManager.from_connection_string(iothub_connection_str)

    # Get device twin
    twin = iothub_registry_manager.get_twin(device_id)
    print("The device twin is: ")
    print("")
    print(twin)
    print("")

    # Print the device's model ID
    additional_props = twin.additional_properties
    if "modelId" in additional_props:
        print("The Model ID for this device is:")
        print(additional_props["modelId"])
        print("")

    # invoke device method
    device_method = CloudToDeviceMethod(method_name=method_name, payload=payload)
    iothub_registry_manager.invoke_device_method(device_id, device_method)
    print("The device method has been successfully invoked")
    print("")

    # Set registry manager object to `None` so all open files get closed
    iothub_registry_manager = None

except msrest.exceptions.HttpOperationError as ex:
    print("HttpOperationError error {0}".format(ex.response.text))
except Exception as ex:
    print("Unexpected error {0}".format(ex))
except KeyboardInterrupt:
    print("{} stopped".format(__file__))
finally:
    print("{} finished".format(__file__))
