import time
import os

while True:
    os.system("python -m scripts.fetch_crypto_data")
    
    print("Data updated successfully")
    
    # Wait 60 seconds
    time.sleep(60)