def handle(send_cb: callable, input_m: str) -> bool:
    if input_m != '@Skynet Skynet':
        return False
    send_cb('Hello')
    return True
