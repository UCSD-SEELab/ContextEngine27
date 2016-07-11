import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '../python'))
sys.path.insert(1, os.path.join(sys.path[0], '../python/LinSVM'))
from LinSVM import LinSVM
from ContextEngineBase import Complexity
comp = Complexity.firstOrder
obj = LinSVM(comp, 2, 0, [0, 0], {})
obj.addSingleObservation([0,0],0)
obj.addSingleObservation([1,1],1)
obj.train()
obj.printO()
