import can
import random

def simulate_can_message():
    
    data = [random.randint(0, 255) for i in range(12)]
    msg = can.Message(arbitration_id=0xc0ffee, data=data, is_extended_id=True)
    return msg

def parse_can_message(message):
   
    roll = int.from_bytes(message.data[0:2], 'big')
    pitch = int.from_bytes(message.data[2:4], 'big')
    yaw = int.from_bytes(message.data[4:6], 'big')
    surge = int.from_bytes(message.data[6:8], 'big')
    sway = int.from_bytes(message.data[8:10], 'big')
    heave = int.from_bytes(message.data[10:12], 'big')

    return {
        "roll": roll,
        "pitch": pitch,
        "yaw": yaw,
        "surge": surge,
        "sway": sway,
        "heave": heave
    }

def receive_can_message():
 
    message = simulate_can_message()
    
    return parse_can_message(message)
