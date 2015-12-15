'''There are some necessary common functions here
'''
import random

def genEvent(dict):
    '''Generates random event from dictionary.
    :param dict: dictionaty event --> probability.
    Event must be hashable.
    :returns: Event.
    '''
    points = [0]
    cur = 0
    for event in dict.keys():
        cur += dict[event]
        points.append(cur)
    i = random.random()
    for p in range(1,len(points)):
        if points[p-1] <= i < points[p]:
            return dict.keys()[p-1]