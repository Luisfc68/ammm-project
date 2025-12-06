from Heuristics.problem.utils import computeScheduleCombinations, computeSchedulesPerAutonomy

DAYS = 7
MIN_AUTONOMY = 2
MAX_AUTONOMY = 6
ALL_SCHEDULES = computeScheduleCombinations(DAYS)
SCHEDULES_PER_AUTONOMY = computeSchedulesPerAutonomy(ALL_SCHEDULES, DAYS, MIN_AUTONOMY, MAX_AUTONOMY)