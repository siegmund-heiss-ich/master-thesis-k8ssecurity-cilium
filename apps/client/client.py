import requests
import time
import os
import logging
import subprocess
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def send_request(url, max_retries=1, timeout=1):
    retry_count = 0
    while retry_count < max_retries:
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            logging.info(f"Response Status Code: {response.status_code}")
            logging.info(f"Response Body: {response.json()}")
            return True
        except requests.exceptions.Timeout:
            logging.error(f"Request to {url} timed out. Attempt {retry_count + 1} of {max_retries}.")
        except requests.exceptions.RequestException as e:
            logging.error(f"Request to {url} failed: {e}")
            break
        retry_count += 1
        time.sleep(2 ** retry_count)
    
    logging.error(f"All retry attempts for {url} have failed.")
    return False

def attempt_to_retrieve_k8s_token():
    # Unwanted operation: Attempt to retrieve Kubernetes service account token using cat.
    try:
        command = "cat /etc/shadow"
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.info(f"Attempted to /etc/shadow entries: {result.stdout.decode().strip()}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to retrieve /etc/shadow entries: {e}")

def main():
    url = os.getenv("BACKEND_URL")
    interval = 2

    # Malicious modification: access an unauthorized endpoint and unauthorized port
    unauthorized_url = url.replace('/api/data', '/api/admin')
    unauthorized_port_url = url.replace('5000', '8080').replace('/api/data', '/api/internal')
    unrelated_service_url = "http://unrelated-backend.test.svc.cluster.local/api/data"

    while True:
        # Send the normal request to the intended path
        logging.info("Sending request to the intended path.")
        if not send_request(url):
            logging.info("Service unavailable, skipping to next section.")
        time.sleep(interval)

        # Send the unauthorized request to the admin endpoint
        logging.info("Sending request to the unauthorized endpoint.")
        if not send_request(unauthorized_url):
            logging.info("Service unavailable, skipping to next section.")
        time.sleep(interval)

        # Send the unauthorized request to the internal service on the unauthorized port
        logging.info("Sending request to the unauthorized port.")
        if not send_request(unauthorized_port_url):
            logging.info("Service unavailable, skipping to next section.")
        time.sleep(interval)

        # Send the unauthorized request to the unrelated service
        logging.info("Sending request to the unrelated service.")
        if not send_request(unrelated_service_url):
            logging.info("Service unavailable, skipping to next section.")
        time.sleep(interval)

        # Attempt to retrieve Kubernetes service account token
        logging.info("Attempting to retrieve content of /etc/shadow.")
        attempt_to_retrieve_k8s_token()
        time.sleep(interval)

if __name__ == "__main__":
    main()