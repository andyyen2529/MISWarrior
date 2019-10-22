import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.nn.functional as F
import numpy as np
import statistics
from copy import deepcopy
import os
from collections import OrderedDict
import torch.tensor as tensor

class Net(nn.Module):
    '''
        建立現實網路(Target Net)及估計網路(Eval Net)
    '''
    def __init__(self, ):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(8, 10) # N_STATES = 8
        self.fc1.weight.data.normal_(0, 0.1)   # initialization
        self.out = nn.Linear(10, 2) # N_ACTIONS = 2
        self.out.weight.data.normal_(0, 0.1)   # initialization

    def forward(self, x):
        x = self.fc1(x)
        x = F.relu(x)
        actions_value = self.out(x)
        return actions_value
    
    def choose_action(self, x):
        x = torch.unsqueeze(torch.FloatTensor(x), 0)
        actions_value = self.forward(x)
        action = np.argmax(actions_value.detach().numpy())     # return the argmax
        
        return action

def adviseAction(state):
	#abs_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'params_top50Return_Linear.pkl')
	#param_list50 = torch.load('params_top50Return_Linear.pkl')
	#param_list50 = torch.load('abs_path')
	param = OrderedDict([('fc1.weight',
              tensor([[ 0.1158, -0.0988,  0.0720,  0.2408,  0.0421, -0.1349, -0.0247, -0.0283],
                      [ 0.0687, -0.0295, -0.1720, -0.1260, -0.3383, -0.1223, -0.0508,  0.0681],
                      [-0.0600, -0.0783,  0.0301, -0.0246, -0.1391,  0.1548,  0.0292, -0.1311],
                      [-0.0360, -0.0857,  0.0505,  0.2222, -0.1010, -0.1674,  0.0695, -0.1696],
                      [-0.0989,  0.0587, -0.0901, -0.0404, -0.0952,  0.1623,  0.0679,  0.0023],
                      [-0.1824,  0.0544, -0.1328,  0.1459, -0.1539, -0.0407,  0.0618,  0.0925],
                      [-0.0017,  0.1142, -0.2593, -0.0378,  0.1240,  0.2351,  0.2373,  0.0864],
                      [ 0.0843,  0.1238, -0.1252, -0.1437, -0.0084,  0.1250, -0.0294,  0.0134],
                      [-0.0741, -0.0639,  0.0489, -0.0714, -0.1792,  0.0922,  0.0653,  0.0888],
                      [ 0.0849, -0.0864,  0.0608,  0.2027, -0.1749, -0.1271, -0.1926, -0.0327]])),
             ('fc1.bias',
              tensor([ 0.1649, -0.2401, -0.1918,  0.3311, -0.1392,  0.0695, -0.1101, -0.2536,
                      -0.3651, -0.3548])),
             ('out.weight',
              tensor([[ 0.1298,  0.0655, -0.0123,  0.1892, -0.1207,  0.2288, -0.0091, -0.0593,
                        0.0410,  0.0045],
                      [-0.0851,  0.1379, -0.0819,  0.0264, -0.0631,  0.0217,  0.0781,  0.0360,
                        0.0648,  0.0026]])),
             ('out.bias', tensor([-0.1241, -0.0462]))])
	ddqn = Net()
	ddqn.load_state_dict(param)
	action = ddqn.choose_action(state)
	return action
	
def makeDecision(position, action):
	if position == 0:
		if action == 0:
			decision = '等待'
		else:
			decision = '買入'
	else:
		if action == 0:
			decision = '繼續持有'
		else:
			decision = '賣出'
	return decision