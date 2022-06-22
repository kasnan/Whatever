
class PID:
    Kp_val = 0.0
    Kd_val = 0.0
    Ki_val = 0.0
    TargetVelo = 0.0

    #initializer
    def __init__(self):
        self.Kp_val = 100
        self.Kd_val = 0.5
        self.Ki_val = 0.5
        self.TargetVelo = 80.0

    #getter
    def getKp(self):
        return self.Kp_val
    def getKd(self):
        return self.Kd_val
    def getKi(self):
        return self.Ki_val
    def getTarget(self):
        return self.TargetVelo

    #setter
    def set(self, Kp, Kd, Ki):
        self.Kp_val = Kp
        self.Kd_val = Kd
        self.Ki_val = Ki
    def setKp(self, Kp):
        self.Kp_val = Kp
    def setKd(self, Kd):
        self.Kd_val = Kd
    def setKi(self, Ki):
        self.Ki_val = Ki

    def setTarget(self, target):
        self.TargetVelo = target

    #feedback



