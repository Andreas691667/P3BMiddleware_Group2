import json

def encode_message(msg_type, sender_id, msg_id, msg_payload):
    """Encode the message
    msg_type: The type of the message
    sender_id: The id of the sender
    msg_payload: The payload of the message
    Returns the message in json format"""
    msg = {
        "MSG_TYPE": msg_type,
        "SENDER_ID": sender_id,
        "MESSAGE_ID": msg_id,
        "MSG_PAYLOAD": msg_payload
    }
    return json.dumps(msg)

def decode_message(msg):
    """Decode the message
    msg: The message to decode in json format
    Returns the message type, sender id and message payload"""
    msg_json = json.loads(msg)
    msg_type = msg_json["MSG_TYPE"]
    sender_id = msg_json["SENDER_ID"]
    msg_id = msg_json["MESSAGE_ID"]
    msg_payload = msg_json["MSG_PAYLOAD"]
    return msg_type, sender_id, msg_id, msg_payload
