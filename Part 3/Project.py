import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)


class Inspector1:
    def __init__(self):
        self.wait_time = 0  # accumulative wait time for inspector1
        self.sp = np.loadtxt('sp1.txt')
        self.number = 0

    def generate(self):
        """Generate one time needed to inspect a component C1"""
        self.number += 1 if self.number + 1 <= len(self.sp) else 0
        return self.sp[self.number - 1]

    def whichtosend(self, W1, W2, W3):
        """Decide which workstation to send the component"""
        if W1.buffer["C1"] <= min(W2.buffer["C1"], W3.buffer["C1"]):
            return W1
        else:
            return W2 if W2.buffer["C1"] <= W3.buffer["C1"] else W3

    def component(self):
        """Show ID"""
        return 'C1'


class Workstation1:
    def __init__(self):
        self.__name__ = 'W1'
        self.buffer = {"C1": 0}  # number of components in the buffer
        self.dealTime = 0  # accumulative time
        self.ws = np.loadtxt('ws1.txt')  # number of outputs totally
        self.number = 0  # number of outputs totally
        self.isWorking = False  # if the workstation is in working condition
        self.idleTime = 0
        self.startIdle = 0

    def generate(self):
        """Generate one time needed to finish a product"""
        self.number += 1 if self.number + 1 < len(self.ws) else 0
        self.buffer['C1'] -= 1
        self.isWorking = True
        return self.ws[self.number - 1]

    def canWork(self):
        """If the Workstation can work now"""
        return self.buffer["C1"] > 0


class Inspector2:
    def __init__(self):
        self.time = 0  # time needed to inspect a component
        self.wait_time = 0  # accumulative wait time for inspector1
        self.sp22 = np.loadtxt('sp2.txt')
        self.sp23 = np.loadtxt('sp3.txt')
        self.number22 = 0
        self.number23 = 0
        self.which = True

    def generate(self):
        """Decide which component to be inspected"""
        return self.generate22() if np.random.randint(2) else self.generate23()

    def generate22(self):
        """Generate one time needed to inspect a component C2"""
        self.number22 += 1 if self.number22 + 1 <= len(self.sp22) else 0
        self.which = True
        return self.sp22[self.number22 - 1]

    def generate23(self):
        """Generate one time needed to inspect a component C3"""
        self.number23 += 1 if self.number23 + 1 <= len(self.sp23) else 0
        self.which = False
        return self.sp23[self.number23 - 1]

    def whichtosend(self, W1, W2, W3):
        """Decide which Workstation to send"""
        return W2 if self.which else W3

    def component(self):
        """Which component to send"""
        return "C2" if self.which else "C3"


class Workstation2:
    def __init__(self):
        self.__name__ = 'W2'
        self.buffer = {"C1": 0, "C2": 0}
        self.deal_time = 0  # accumulative time
        self.ws = np.loadtxt('ws2.txt')
        self.number = 0  # number of outputs totally
        self.isWorking = False
        self.idleTime = 0
        self.startIdle = 0

    def generate(self):
        """Generate one time needed to finish a product P2"""
        self.number += 1 if self.number + 1 < len(self.ws) else 0
        self.buffer["C1"] -= 1
        self.buffer["C2"] -= 1
        self.isWorking = True
        return self.ws[self.number - 1]

    def canWork(self):
        """If the Workstation can work now"""
        return self.buffer["C1"] > 0 and self.buffer["C2"] > 0


class Workstation3:
    def __init__(self):
        self.__name__ = 'W3'
        self.buffer = {"C1": 0, "C3": 0}
        self.deal_time = 0  # accumulative time
        self.ws = np.loadtxt('ws3.txt')
        self.number = 0  # number of outputs totally
        self.isWorking = False
        self.idleTime = 0
        self.startIdle = 0

    def generate(self):
        """Generate one time needed to finish a product P3"""
        self.number += 1 if self.number + 1 < len(self.ws) else 0
        self.buffer['C1'] -= 1
        self.buffer['C3'] -= 1
        self.isWorking = True
        return self.ws[self.number - 1]

    def canWork(self):
        """If the work station can work now"""
        return self.buffer["C1"] > 0 and self.buffer["C3"] > 0


def queue_diagram(Buffer, name):
    res = [buffer for buffer in Buffer if buffer[-1] == name]

    res.sort()
    x = [a[0] for a in res]
    y = [a[1] for a in res]

    total = 0
    for i in range(len(x) - 1):
        total += (x[i + 1] - x[i]) * y[i]

    average = [total / x[-1] for _ in range(len(x))]
    print(average[0], 189 / x[-1], total / 189)

    plt.step(x, y, where='post')
    plt.plot(x, average, 'r')
    print(len(res))
    # plt.show()


if __name__ == '__main__':
    worldTime = 0
    I1 = Inspector1()
    I2 = Inspector2()
    W1 = Workstation1()
    W2 = Workstation2()
    W3 = Workstation3()
    idleStart = 0
    idleEnd = 0

    Buffer = [[0, W1.buffer['C1'], 'W1_C1'], [0, W2.buffer['C1'], 'W2_C1'],
              [0, W2.buffer['C2'], 'W2_C2'], [0, W3.buffer['C1'], 'W3_C1'],
              [0, W3.buffer['C3'], 'W3_C3']]
    # Buffer = [World_time, which_buffer, buffer_name]

    eventList = [[worldTime + I1.generate(), I1.whichtosend(W1, W2, W3), I1.component(), 'receive'],
                 [worldTime + I2.generate(), I2.whichtosend(W1, W2, W3), I2.component(), 'receive']]
    # format: [time, objective, component, activity]
    # initialize the environment

    while eventList:
        eventList.sort()
        event = eventList.pop(0)
        # take out the nearest event from event list
        worldTime = event[0]
        generator = I1 if event[2] == 'C1' else I2

        if event[-1] == 'receive':
            if event[1].buffer[event[2]] <= 1:
                # if the buffer has room to admit the component
                event[1].buffer[event[2]] += 1
                Buffer.append([worldTime, event[1].buffer[event[2]], event[1].__name__ + '_' + event[2]])
                if not event[1].isWorking and event[1].canWork():
                    # the work station has ingredients to produce
                    time = worldTime + event[1].generate()
                    eventList.append([time, event[1], '', 'output'])
                    Buffer.append([time, event[1].buffer[event[2]], event[1].__name__ + '_' + event[2]])
                    event[1].idleTime += worldTime - event[1].startIdle
                if generator == I1 and generator.number >= 300:
                    continue
                if generator == I2 and (generator.number22 >= 300 or generator.number23 >= 300):
                    continue
                eventList.append(
                    [worldTime + generator.generate(), generator.whichtosend(W1, W2, W3), generator.component(),
                     'receive'])
            else:
                # no room for this component, it has to wait for room to settle down
                k = False
                for eve in eventList:
                    if eve[-1] == 'output' and eve[1] == event[1]:
                        eventList.append([eve[0] + 0.001, event[1], event[2], 'receive'])
                        k = True
                        break
                if not k and len(eventList):
                    eventList.append([eventList[0][0] + 0.001, event[1], event[2], 'receive'])
        elif event[-1] == 'output':
            # output the product
            event[1].isWorking = False
            event[1].startIdle = worldTime
            if event[1].canWork():
                eventList.append([worldTime + event[1].generate(), event[1], '', 'output'])
                event[1].idleTime += worldTime - event[1].startIdle

    print(worldTime, W1.number, W2.number, W3.number, W1.idleTime, W2.idleTime, W3.idleTime)
    print(np.mean(W1.ws))
    queue_diagram(Buffer, 'W1_C1')
