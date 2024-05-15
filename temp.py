import time
import subprocess
import boto3

# Initialize AWS Kinesis client
kinesis_client = boto3.client('kinesis')

def get_internal_temperature():
    temp_output = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True, text=True)
    temp_str = temp_output.stdout
    temp_value = float(temp_str.split('=')[1].split("'")[0])
    return temp_value

if __name__ == "__main__":
    while True:
        # Get internal temperature
        temperature = get_internal_temperature()

        # Put temperature data into Kinesis stream
        response = kinesis_client.put_record(
            StreamName='pi-temp-stream',
            Data=str(temperature),
            PartitionKey='1'
        )

        print(f"Temperature data sent to Kinesis: {temperature}°C")

        # Wait for a specified interval (e.g., 1 minute)
        time.sleep(10)  # Sleep for 60 seconds before sending the next reading
