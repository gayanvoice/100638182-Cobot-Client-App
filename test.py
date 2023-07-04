import os
import msrest
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod

iothub_connection_str = "HostName=100638182IotHub.azure-devices.net;SharedAccessKeyName=service;SharedAccessKey=lvHQWwVYdyhxjOpxKzwp39EDJnQyWmklEd73eMCcG8U="
device_id = "Wrist3"
method_name = "startIotCommand"
# method_name = "stopIotCommand"
method_payload = "hello world"

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
    device_method = CloudToDeviceMethod(method_name=method_name, payload=method_payload)
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