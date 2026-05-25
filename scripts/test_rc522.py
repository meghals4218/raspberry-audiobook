from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

print("Tap NFC tag...")

try:
    while True:
        tag_id, text = reader.read()

        print(f"Tag ID: {tag_id}")
        print(f"Text: {text}")

except KeyboardInterrupt:
    print("Exiting...")