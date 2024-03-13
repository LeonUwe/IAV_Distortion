class DriverController:

    speedRequest = 0
    laneChangeRequest = 0

    def __init__(self):
        self.speedRequest = 0
        self.laneChangeRequest = 0
        return

    def request_speed_change(self, uuid, value):
        self.speedRequest = value
        return

    def request_lane_change(self, uuid, value):
        if value == "left":
            laneChangeRequest = 1

        elif value == "right":
            laneChangeRequest = -1

        else:
            laneChangeRequest = 0
        return

    def request_lights_on(self, uuid):
        return
    
    def request_lights_off(self, uuid):
        return