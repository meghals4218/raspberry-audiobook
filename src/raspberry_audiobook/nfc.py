class NFCReader:
    def read_uid(self) -> str:
        raise NotImplementedError


class MockNFCReader(NFCReader):
    def read_uid(self) -> str:
        return input("Enter fake NFC UID: ").strip().upper()


class RC522Reader(NFCReader):
    def __init__(self):
        from mfrc522 import SimpleMFRC522
        self.reader = SimpleMFRC522()

    def read_uid(self) -> str:
        tag_id, _ = self.reader.read()
        return str(tag_id).upper()