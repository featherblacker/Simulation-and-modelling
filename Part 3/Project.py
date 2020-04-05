import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)

TIME_END = 3467.462
ADDRESS = './Replication 10'
ALGORITHM = 'altered'


class Inspector1:
    def __init__(self):
        self.wait_time = 0  # accumulative wait time for inspector1
        self.sp = np.loadtxt(ADDRESS + '/sp1.txt')
        self.number = 0

    def generate(self):
        """Generate one time needed to inspect a component C1"""
        self.number += 1 if self.number + 1 <= len(self.sp) else 0
        return self.sp[self.number - 1]

    def whichtosend(self, W1, W2, W3, algorithm):
        """Decide which algorithm to use and which workstation to send the component"""
        if algorithm == "origin":
            if W1.buffer["C1"] <= min(W2.buffer["C1"], W3.buffer["C1"]):
                return W1
            else:
                return W2 if W2.buffer["C1"] <= W3.buffer["C1"] else W3
        else:
            if W2.buffer["C1"] <= min(W3.buffer["C1"], W1.buffer["C1"]):
                return W2
            else:
                return W3 if W3.buffer["C1"] <= W1.buffer["C1"] else W1

    def component(self):
        """Show ID"""
        return 'C1'

    def info(self, ):
        print('inspector 1 mean time {:.3f}'.format(np.mean(self.sp[:300])))
        print('inspector 1 idle time {:.3f}'.format((TIME_END - np.sum(self.sp[:300])) / TIME_END))


class Workstation1:
    def __init__(self):
        self.buffer = {"C1": 0}  # number of components in the buffer
        self.dealTime = 0  # accumulative time
        self.ws = np.loadtxt(ADDRESS + '/ws1.txt')  # number of outputs totally
        self.number = 0  # number of outputs totally
        self.isWorking = False  # if the workstation is in working condition
        self.idleTime = 0
        self.startIdle = 0
        self.bufferRecord = [[0, 0, 'C1']]

    def generate(self):
        """Generate one time needed to finish a product"""
        self.number += 1 if self.number + 1 < len(self.ws) else 0
        return self.ws[self.number - 1]

    def canWork(self):
        """If the Workstation can work now"""
        return self.buffer["C1"] > 0

    def bufferChange(self, time, change, component='C1'):
        if change == "add":
            self.buffer[component] += 1
            self.bufferRecord.append([time, self.buffer[component], component])
        else:
            for item in self.buffer:
                self.buffer[item] -= 1
                self.bufferRecord.append([time, self.buffer[item], item])

    def plot(self, component='C1'):
        result = self.bufferRecord
        result.sort()
        res = []
        i = 0
        while i < len(result) - 1:
            if result[i][0] == result[i + 1][0]:
                i += 2
                continue
            if result[i][0] - 0.001 <= TIME_END:
                res.append(result[i])
                i += 1
            else:
                break

        x = [a[0] for a in res]
        y = [a[1] for a in res]
        total = 0
        for i in range(len(x) - 1):
            total += (x[i + 1] - x[i]) * y[i]

        average = [total / x[-1] for _ in range(len(x))]
        print('Workstation 1 mean number of {} in line: {:.3f}, mean waiting time: {:.3f}'.format(component, average[0],
                                                                                                  total / 122))

        plt.step(x, y, where='post')
        plt.hlines(average[0], x[0], x[-1], 'r')
        # print(len(res))

    def output(self):
        print('Number of output of Workstation 1: {}'.format(W1.number))
        print('Idle time ratio of Workstation 1: {:.3f}'.format((TIME_END - sum(self.ws[:122])) / TIME_END))


class Inspector2:
    def __init__(self):
        self.time = 0  # time needed to inspect a component
        self.wait_time = 0  # accumulative wait time for inspector1
        self.sp22 = np.loadtxt(ADDRESS + '/sp2.txt')
        self.sp23 = np.loadtxt(ADDRESS + '/sp3.txt')
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

    def whichtosend(self, W1, W2, W3, algorithm=ALGORITHM):
        """Decide which Workstation to send"""
        return W2 if self.which else W3

    def component(self):
        """Which component to send"""
        return "C2" if self.which else "C3"

    def info(self):
        print('inspector 2 mean time {:.3f}'.format(np.mean(list(self.sp22[:95]) + list(self.sp23[:82]))))
        print('inspector 2 idle time {:.3f}'.format(
            (TIME_END - sum(list(self.sp22[:95]) + list(self.sp23[:82]))) / TIME_END))


class Workstation2:
    def __init__(self):
        self.buffer = {"C1": 0, "C2": 0}
        self.deal_time = 0  # accumulative time
        self.ws = np.loadtxt(ADDRESS + '/ws2.txt')
        self.number = 0  # number of outputs totally
        self.isWorking = False
        self.idleTime = 0
        self.startIdle = 0
        self.bufferRecord = [[0, 0, 'C1'], [0, 0, 'C2']]

    def generate(self):
        """Generate one time needed to finish a product P2"""
        self.number += 1 if self.number + 1 < len(self.ws) else 0
        return self.ws[self.number - 1]

    def canWork(self):
        """If the Workstation can work now"""
        return self.buffer["C1"] > 0 and self.buffer["C2"] > 0

    def bufferChange(self, time, change, component='C1'):
        if change == "add":
            self.buffer[component] += 1
            self.bufferRecord.append([time, self.buffer[component], component])
        else:
            for item in self.buffer:
                self.buffer[item] -= 1
                self.bufferRecord.append([time, self.buffer[item], item])

    def plot(self, component='C1'):
        result = []
        for item in self.bufferRecord:
            if item[-1] == component and item[0] - 0.001 <= TIME_END:
                result.append(item)
        result.sort()
        res = []
        i = 0
        while i < len(result) - 1:
            if result[i][0] == result[i + 1][0]:
                i += 2
                continue
            res.append(result[i])
            i += 1

        x = [a[0] for a in res]
        y = [a[1] for a in res]
        total = 0
        for i in range(len(x) - 1):
            total += (x[i + 1] - x[i]) * y[i]

        if x[-1] == 0:
            average = [0]
        else:
            average = [total / x[-1] for _ in range(len(x))]
        print('Workstation 2 mean number of {} in line: {:.3f}, mean waiting time: {:.3f}'.format(component, average[0],
                                                                                                  total / 95))
        plt.step(x, y, where='post')
        plt.hlines(average[0], x[0], x[-1], 'r')
        # print(len(res))

    def output(self):
        print('Number of output of Workstation 2: {}'.format(W2.number))
        print('Idle time ratio of Workstation 2: {:.3f}'.format((TIME_END - sum(self.ws[:95])) / TIME_END))


class Workstation3:
    def __init__(self):
        self.buffer = {"C1": 0, "C3": 0}
        self.deal_time = 0  # accumulative time
        self.ws = np.loadtxt(ADDRESS + '/ws3.txt')
        self.number = 0  # number of outputs totally
        self.isWorking = False
        self.idleTime = 0
        self.startIdle = 0
        self.bufferRecord = [[0, 0, 'C1'], [0, 0, 'C3']]

    def generate(self):
        """Generate one time needed to finish a product P3"""
        self.number += 1 if self.number + 1 < len(self.ws) else 0
        return self.ws[self.number - 1]

    def canWork(self):
        """If the work station can work now"""
        return self.buffer["C1"] > 0 and self.buffer["C3"] > 0

    def bufferChange(self, time, change, component='C1'):
        if change == "add":
            self.buffer[component] += 1
            self.bufferRecord.append([time, self.buffer[component], component])
        else:
            for item in self.buffer:
                self.buffer[item] -= 1
                self.bufferRecord.append([time, self.buffer[item], item])

    def plot(self, component='C1'):
        result = []
        for item in self.bufferRecord:
            if item[-1] == component and item[0] - 0.001 <= TIME_END:
                result.append(item)
        result.sort()
        res = []
        i = 0
        while i < len(result) - 1:
            if result[i][0] == result[i + 1][0]:
                i += 2
                continue
            res.append(result[i])
            i += 1

        x = [a[0] for a in res]
        y = [a[1] for a in res]
        total = 0
        for i in range(len(x) - 1):
            total += (x[i + 1] - x[i]) * y[i]

        if x[-1] == 0:
            average = [0]
        else:
            average = [total / x[-1] for _ in range(len(x))]
        print('Workstation 3 mean number of {} in line: {:.3f}, mean waiting time: {:.3f}'.format(component, average[0],
                                                                                                  total / 82))
        plt.step(x, y, where='post')
        plt.hlines(average[0], x[0], x[-1], 'r')
        # print(len(res))

    def output(self):
        print('Number of output of Workstation 3: {}'.format(W3.number))
        print('Idle time ratio of Workstation 3: {:.3f}'.format((TIME_END - sum(self.ws[:82])) / TIME_END))


if __name__ == '__main__':
    worldTime = 0
    I1 = Inspector1()
    I2 = Inspector2()
    W1 = Workstation1()
    W2 = Workstation2()
    W3 = Workstation3()
    idleStart = 0
    idleEnd = 0

    # Buffer = [World_time, which_buffer, buffer_name]

    eventList = [[worldTime + I1.generate(), I1.whichtosend(W1, W2, W3, ALGORITHM), I1.component(), 'receive'],
                 [worldTime + I2.generate(), I2.whichtosend(W1, W2, W3, ALGORITHM), I2.component(), 'receive']]
    # format: [time, objective, component, activity]
    # initialize the environment

    while eventList:
        eventList.sort(key=lambda x: x[0])
        event = eventList.pop(0)
        # take out the nearest event from event list
        worldTime = event[0]
        generator = I1 if event[2] == 'C1' else I2

        if event[-1] == 'receive':
            if event[1].buffer[event[2]] <= 1:

                # if the buffer has room to admit the component
                event[1].bufferChange(worldTime, "add", event[2])
                if not event[1].isWorking and event[1].canWork():
                    # the work station has ingredients to produce
                    event[1].isWorking = True
                    event[1].bufferChange(worldTime, "pop")
                    eventList.append([worldTime + event[1].generate(), event[1], '', 'output'])
                    event[1].idleTime += worldTime - event[1].startIdle
                if (generator == I1 and generator.number >= 300) or (
                        generator == I2 and (generator.number22 >= 300 or generator.number23 >= 300)):
                    continue
                eventList.append(
                    [worldTime + generator.generate(), generator.whichtosend(W1, W2, W3, ALGORITHM), generator.component(),
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
                event[1].isWorking = True
                event[1].bufferChange(worldTime, "pop")
                eventList.append([worldTime + event[1].generate(), event[1], '', 'output'])
                event[1].idleTime += worldTime - event[1].startIdle

        print('{:.3f}'.format(worldTime), W1.number, W2.number, W3.number, W1.buffer['C1'], W2.buffer['C1'], W2.buffer['C2'], W3.buffer['C1'], W3.buffer['C3'])
    print(I1.info(), I2.info(), W1.plot('C1'), W2.plot('C1'), W2.plot('C2'), W3.plot('C1'), W3.plot('C3'), W1.output(),
          W2.output(), W3.output())
    # plt.show()
