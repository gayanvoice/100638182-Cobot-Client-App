import argparse
import msrest
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod

iothub_connection_str = "HostName=100638182IotHub.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=O" \
                        "/fpHPDkS+5/oU/Ob5v7fx8YahD0oUeesLTmLIXLkGw="

parser = argparse.ArgumentParser()
parser.add_argument("--device", help="Specify the device id")
parser.add_argument("--method", help="Specify the method name")
parser.add_argument("--payload", help="Specify the method name")
args = parser.parse_args()

model = args.device
command = args.method

try:
    iot_hub_registry_manager = IoTHubRegistryManager.from_connection_string(iothub_connection_str)
    twin = iot_hub_registry_manager.get_twin(args.device)
    print("The device twin is: ")
    print("")
    print(twin)
    print("")

    additional_props = twin.additional_properties
    if "modelId" in additional_props:
        print("The Model ID for this device is:")
        print(additional_props["modelId"])
        print("")

    if args.payload == "default":
        input_array = [
            [-0.12, -0.43, 0.14, 0, 3.11, 0.14],
            [-0.22, -0.71, 0.21, 0, 3.11, 0.24],
            [-0.82, -0.81, 0.31, 0, 3.21, 0.34],
            [-0.62, -0.91, 0.41, 0, 3.31, 0.54]
        ]
        cloud_to_device_method = CloudToDeviceMethod(method_name=args.method, payload=input_array)
        iot_hub_registry_manager.invoke_device_method(args.device, cloud_to_device_method)
        print("The device method has been successfully invoked")
        print("")

        iot_hub_registry_manager = None
    else:
        cloud_to_device_method = CloudToDeviceMethod(method_name=args.method, payload=args.payload)
        iot_hub_registry_manager.invoke_device_method(args.device, cloud_to_device_method)
        print("The device method has been successfully invoked")
        print("")

except msrest.exceptions.HttpOperationError as ex:
    print("HttpOperationError error {0}".format(ex.response.text))
except Exception as ex:
    print("Unexpected error {0}".format(ex))
except KeyboardInterrupt:
    print("{} stopped".format(__file__))
finally:
    print("{} finished".format(__file__))
