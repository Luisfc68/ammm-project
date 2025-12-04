
def computeScheduleCombinations(size):
    result = []
    for mask in range(2**size):
        combination = [(mask >> i) & 1 for i in range(size)]
        result.append(combination)
    return result

def isValidSchedule(schedule, size, autonomy):
    if not any(schedule): return False
    if all(schedule): return 2 <= len(schedule) <= autonomy
    blocks = []

    for i in range(size):
        if schedule[i] == 1 and schedule[i - 1] == 0: # block start
            blockLength = 0
            j = i
            while schedule[j] == 1:
                blockLength += 1
                j = (j + 1) % size # the modulo is to be able to continue if block includes the end and the start of the week
            blocks.append(blockLength)
    if not blocks: return False
    return all(2 <= b <= autonomy for b in blocks)

def computeCrossingDayPairs(crossings, days):
    return {(a, b) for a in range(1, crossings + 1) for b in range(1, days + 1)}

def computeSchedulesPerAutonomy(allSchedules, scheduleSize, minAutonomy, maxAutonomy):
    result = {} # autonomy => schedules
    for a in range(minAutonomy, maxAutonomy + 1):
        result[a] = list(filter(lambda x: isValidSchedule(x, scheduleSize, a), allSchedules))
    return result