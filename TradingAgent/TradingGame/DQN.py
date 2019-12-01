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
				self.fc1 = nn.Linear(37, 10) # N_STATES = 37
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
				#print(actions_value)
				action = np.argmax(actions_value.detach().numpy())     # return the argmax
				#print(action)
				
				return action

def adviseAction(state, playDuration):

	if playDuration == 60:
		
		# 標準化狀態變數 (用來標準化的平均數和標準差和訓練模型時用的相同(元大台灣50 2018/10/1~2018/12/28的資料))
		mean_60 = [78.08233333333335,
							 78.62533333333336,
							 79.50137500000001,
							 82.18918055533335,
							 82.62382638916667,
							 82.62973263883332,
							 12980377.98000001,
							 13109216.493333336,
							 13206643.817499997,
							 11660427.317716666,
							 8858807.07171667,
							 7081260.138633332,
							 1020515286.423333,
							 1035102541.8933331,
							 1050930273.4950002,
							 946536519.1033334,
							 724577138.3333335,
							 580011900.4783331,
							 12554183.533333333,
							 77.74249999999999,
							 78.12083333333334,
							 77.2125,
							 77.705,
							 -0.16833333333333336]

		std_60 = [3.347774047549555,
							3.5098897643931917,
							3.6578117423652006,
							2.697304618316148,
							0.6889397930919128,
							0.491906247613929,
							8498635.787508653,
							6736829.7106598,
							5009781.5548914205,
							1970487.0188612188,
							985629.930601265,
							716543.232945966,
							689272671.449235,
							552116427.0513507,
							415147948.0241058,
							142978472.66348475,
							74133293.81544879,
							54598375.58218146,
							12060809.55864161,
							3.1843742567072204,
							3.1479249510074316,
							3.0872705431788217,
							3.0671952074620177,
							1.0851449433244387]

		state[:24] = [(a - b) / c for a, b, c in zip(state[:24], mean_60, std_60)]
		#print(state)

		#print(state)

		# 讀取60天的參數
		param = OrderedDict([('fc1.weight',
									tensor([[ 1.5322e-01,  2.4188e-02,  1.5392e-01,  3.8963e-02, -3.1396e-02,
														9.1942e-03,  1.2582e-01, -6.2924e-02,  4.7180e-02,  8.2196e-02,
														1.4104e-02, -3.3060e-02,  1.5208e-02, -1.3783e-02, -1.8774e-01,
													 -2.3123e-02,  5.7452e-02, -2.3748e-02, -8.5421e-02, -2.3326e-01,
													 -5.8038e-02, -1.2542e-01, -1.1739e-01,  5.9239e-02, -1.6203e-01,
													 -1.2483e-01,  1.8688e-02,  5.4656e-02, -1.0233e-01,  8.3958e-02,
													 -7.4056e-02,  1.1326e-01, -3.5667e-02, -5.7259e-03, -2.2609e-01,
													 -7.2624e-02, -1.1822e-01],
													[-4.1060e-02,  1.5698e-02,  8.8164e-02, -1.0116e-02,  7.5424e-02,
														1.4978e-01,  1.2131e-01,  3.6977e-05, -2.4113e-01,  7.5316e-02,
														5.8737e-02,  1.9495e-01, -1.1624e-02,  2.2562e-01, -2.3505e-02,
													 -9.6384e-02,  1.4830e-01, -1.5938e-01,  7.8304e-02, -3.1507e-03,
													 -6.4858e-02,  1.1895e-01,  1.1452e-01,  9.7040e-02, -1.0714e-01,
														1.5742e-02,  1.4446e-01, -7.6298e-03,  2.1599e-02, -1.6212e-01,
													 -5.7674e-02,  1.1677e-02,  1.4191e-01,  1.1417e-01, -4.3471e-02,
													 -2.4914e-01, -6.4292e-02],
													[-8.7433e-02,  7.0148e-02, -1.2103e-01,  1.9575e-01,  1.0677e-01,
														6.4755e-02, -9.3247e-02,  1.4631e-01, -1.0878e-02,  7.2910e-02,
													 -1.7150e-01,  1.4593e-01, -4.2898e-02, -9.0609e-02, -4.2441e-02,
													 -8.1579e-02,  2.2124e-01, -6.8133e-02,  5.5988e-02,  4.7118e-02,
													 -1.1513e-02, -9.5604e-02,  1.0690e-01, -1.0606e-01,  1.5968e-02,
													 -2.3845e-02,  1.7663e-01,  2.0720e-02, -4.7404e-03, -3.5509e-02,
													 -9.4794e-02,  3.6193e-02, -2.5124e-02,  2.7490e-03, -7.9768e-02,
														5.5889e-02,  1.1357e-01],
													[ 1.1828e-01,  3.3001e-02,  4.7555e-02,  6.9371e-03,  8.5813e-02,
														8.1696e-02,  3.9980e-02,  7.1452e-02, -1.3256e-01, -6.8281e-02,
														2.5093e-02, -8.0031e-02, -1.1384e-01,  1.1944e-01, -1.0625e-01,
														9.2641e-03, -1.6643e-01, -7.4301e-02,  7.2895e-02, -7.5442e-02,
													 -1.3307e-02,  7.0399e-02, -1.4779e-01,  4.5165e-02, -1.4099e-01,
														5.7763e-02,  1.0930e-01, -9.1685e-02,  1.5474e-01,  6.3540e-02,
													 -1.3877e-01, -1.8119e-02, -3.4178e-01,  5.1519e-02,  5.9171e-02,
														1.2116e-01,  1.6433e-01],
													[ 1.5155e-01,  2.3427e-01,  1.2725e-01, -4.1311e-02, -3.8627e-02,
													 -1.6031e-02, -2.5190e-01,  1.9576e-01, -6.3309e-02, -2.7657e-03,
														6.7794e-02, -2.2837e-02, -3.8720e-02, -1.0942e-01, -1.3620e-02,
														5.0649e-02,  8.2773e-02,  1.3372e-01,  6.1104e-03, -5.8228e-02,
														1.9699e-02, -2.2926e-02, -1.0193e-01, -8.4287e-02, -8.0621e-02,
													 -5.1378e-02, -6.1443e-03, -1.4627e-01, -3.7837e-02, -1.0639e-01,
														2.0356e-02, -3.8806e-02, -8.7133e-03, -6.5063e-02,  7.3272e-02,
													 -6.3943e-02,  4.0197e-02],
													[-5.2227e-02, -1.8807e-01, -1.9980e-01,  7.7133e-02, -9.9576e-02,
													 -1.5015e-02, -1.8682e-02, -7.5048e-03,  1.8004e-02,  9.4452e-02,
														3.2547e-01,  1.0386e-01,  6.1883e-02, -7.4505e-02, -7.1621e-02,
														3.1824e-02,  2.3149e-02,  4.7943e-02, -5.7806e-02,  2.9225e-01,
													 -1.9086e-02,  7.8964e-03, -3.4555e-02, -4.8283e-03, -2.1849e-02,
														1.7995e-02, -6.7868e-02, -6.4013e-04, -5.1951e-02, -1.5036e-02,
														1.2861e-01, -2.4174e-02, -3.8513e-04,  1.0036e-01,  1.5662e-01,
														1.2006e-01,  1.1838e-01],
													[ 1.2590e-02, -1.5780e-01,  1.3731e-01, -1.8119e-01,  1.2634e-01,
														1.3297e-01, -7.9034e-02, -1.2180e-02, -1.4576e-01,  8.7004e-02,
														2.1953e-02, -1.5834e-02, -1.3203e-01, -4.1521e-02,  1.2762e-02,
														2.7174e-01, -7.1389e-02, -3.1053e-02,  4.0638e-02, -3.2355e-02,
													 -2.7666e-02,  8.9429e-02, -9.4056e-03,  1.7152e-02,  5.8720e-02,
													 -1.0406e-01,  1.3550e-01,  3.9976e-02, -1.5170e-01,  2.9916e-02,
														1.4362e-02, -2.9273e-02, -1.6282e-01,  1.3996e-02,  6.7678e-02,
														6.5220e-02,  9.3763e-02],
													[ 1.1168e-01, -9.5421e-02,  2.2198e-02,  1.9799e-02,  4.6235e-02,
														4.8083e-02, -4.5960e-02, -5.8789e-02, -9.1042e-02,  1.1898e-01,
														7.3176e-02,  1.4141e-01, -5.6761e-03, -9.7338e-02, -2.7667e-02,
														6.9870e-02,  2.8904e-02, -7.7537e-02,  8.9832e-02, -9.8850e-02,
														7.6820e-02, -1.1032e-01, -1.4904e-01,  1.2636e-01,  1.7915e-01,
														1.4786e-01, -1.2387e-01,  1.9001e-02,  1.2061e-01, -8.7866e-02,
													 -3.3130e-02,  2.8067e-02,  1.4711e-01, -2.6198e-02, -4.4416e-02,
													 -1.4587e-01,  4.1374e-02],
													[-5.9457e-02,  4.7441e-02,  5.2893e-02, -2.7748e-02, -4.9680e-02,
													 -1.4477e-01,  1.3623e-01, -6.8444e-02,  2.5712e-02, -8.3544e-02,
														7.7373e-03,  1.2910e-01, -1.8443e-02,  9.6713e-03, -7.0700e-02,
														1.2392e-01, -2.1622e-02,  1.4252e-01,  6.0751e-02,  8.7998e-02,
													 -8.1518e-02,  6.7554e-02,  9.5034e-02,  4.4633e-02, -1.5101e-01,
														1.2905e-01, -1.5675e-02, -9.9116e-02, -1.5860e-01,  3.2651e-02,
													 -3.4156e-02,  4.1548e-02, -1.7429e-02, -2.1111e-01,  3.1819e-02,
													 -1.2679e-03,  4.7344e-02],
													[ 1.1730e-01,  3.9499e-02,  9.9938e-03, -1.6620e-01, -4.9935e-02,
														5.9727e-02, -6.1575e-02,  8.6934e-02,  2.7100e-02, -3.7920e-02,
													 -4.1871e-02,  1.9420e-02, -1.0620e-01,  8.6566e-02, -2.6362e-02,
													 -1.3917e-01, -3.8775e-02,  1.0477e-01,  1.6333e-01, -1.0756e-01,
														8.1010e-02,  7.3704e-02, -7.5876e-02,  1.0265e-02, -5.6799e-02,
													 -2.1570e-02,  1.1815e-02,  6.9901e-02, -6.3735e-02,  4.4083e-02,
														8.0857e-02, -1.5380e-02,  2.1207e-01,  1.3929e-01, -4.8520e-02,
													 -1.0641e-01, -2.0237e-03]])),
								 ('fc1.bias',
									tensor([-0.0350, -0.0379, -0.0300,  0.0661, -0.0616, -0.0990, -0.0510, -0.0720,
													 0.1259,  0.1047])),
								 ('out.weight',
									tensor([[ 0.0395, -0.0374, -0.1781, -0.0830,  0.0026,  0.1110, -0.2572,  0.1891,
														0.0269,  0.1039],
													[ 0.0078,  0.0051,  0.0348,  0.0163, -0.0622,  0.1525,  0.0978,  0.0659,
													 -0.0409,  0.0251]])),
								 ('out.bias', tensor([0.2799, 0.1376]))])
					
	elif playDuration == 240:

		# 標準化狀態變數 (用來標準化的平均數和標準差和訓練模型時用的相同(元大台灣50 2018/1/2~2018/12/28的資料))

		mean_240 = [79.42135135135139,
								79.72108108108108,
								80.24050675675677,
								82.42286036013516,
								82.68012387418918,
								82.0539611485135,
								11537589.789189195,
								11487967.02702703,
								11549561.317567565,
								10138967.630810812,
								7868577.8842972955,
								6448618.183972973,
								913809474.6999998,
								912162208.0270268,
								922540087.4256757,
								824468010.8864865,
								644253770.8013514,
								526401241.5472971,
								11215215.027027028,
								79.15608108108107,
								79.53918918918922,
								78.67162162162163,
								79.14729729729731,
								-0.11689189189189189]

		std_240 = [4.212543995729547,
							4.007139456454291,
							3.7021746658961185,
							2.4739819955514677,
							0.6368319303483394,
							1.2915998469623724,
							8216028.703668517,
							6944954.947685839,
							5681301.2581617525,
							3634270.761978022,
							2246682.1990809734,
							1467613.2219774378,
							658928976.1350849,
							559644435.928114,
							459874420.3677312,
							285232307.9555328,
							180255601.3700861,
							122058910.03669365,
							11210836.724297745,
							4.195667634291995,
							4.184751103630128,
							4.194484972393595,
							4.161811808196272,
							1.0080931758355647]

		state[:24] = [(a - b) / c for a, b, c in zip(state[:24], mean_240, std_240)]

		#print(state)

		# 讀取240天的參數
		param = OrderedDict([('fc1.weight',
									tensor([[-0.1223, -0.0203, -0.0836, -0.1756, -0.0195,  0.0189, -0.0250,  0.0164,
														0.0482, -0.0331, -0.1414,  0.1711,  0.1655,  0.0156, -0.1196, -0.0583,
													 -0.0857,  0.1118, -0.0231, -0.0594, -0.0237, -0.0849, -0.0045, -0.0165,
													 -0.0225,  0.0461,  0.1495,  0.2344,  0.2640,  0.0912,  0.0293,  0.0161,
														0.1400, -0.1136,  0.0411,  0.0593,  0.0965],
													[-0.1384,  0.1893, -0.0700,  0.2508, -0.1443,  0.1592,  0.0462, -0.0924,
													 -0.0708, -0.1140,  0.1248,  0.0393,  0.0515, -0.0226,  0.1532,  0.0300,
													 -0.1540, -0.0630, -0.0048,  0.0429, -0.1125, -0.1226, -0.0291,  0.0206,
														0.0752,  0.0178, -0.0150, -0.0891, -0.0571, -0.1155,  0.0260, -0.1989,
													 -0.0913, -0.0736, -0.0072,  0.0804, -0.0431],
													[-0.0117,  0.1883,  0.0398,  0.0233,  0.2568,  0.1128,  0.0613,  0.0175,
														0.0884, -0.0758,  0.0755,  0.0734,  0.1245, -0.1029, -0.0211,  0.1369,
														0.1108,  0.1223,  0.1718, -0.1189, -0.0752,  0.0082, -0.0204,  0.0870,
														0.0115,  0.0222, -0.0212,  0.1725,  0.0624,  0.0020, -0.0615,  0.0400,
														0.0057,  0.0452,  0.1536, -0.1144,  0.0085],
													[-0.0650,  0.1083,  0.0485,  0.0075,  0.0454, -0.0632, -0.0291,  0.2430,
													 -0.0922, -0.0360,  0.0272,  0.0102,  0.1452,  0.1056, -0.0300,  0.1156,
														0.0082,  0.0393, -0.0096, -0.0722,  0.0602, -0.1343, -0.1814, -0.0078,
													 -0.0194, -0.1736, -0.0576,  0.0655,  0.0339, -0.0550, -0.0044,  0.0061,
													 -0.0603, -0.2017, -0.1160,  0.1552,  0.0890],
													[-0.0312,  0.0825, -0.0626, -0.0133,  0.0080,  0.1319,  0.0012, -0.1286,
														0.0074, -0.0349, -0.0381,  0.0241, -0.0693,  0.0255,  0.0581, -0.0276,
													 -0.1739, -0.0379,  0.0118,  0.0282,  0.0512,  0.0204, -0.1772,  0.1180,
													 -0.0862,  0.1602,  0.0496,  0.1008, -0.0204, -0.0864,  0.1400,  0.1968,
														0.0274, -0.0838,  0.0279,  0.0676,  0.1014],
													[ 0.0221, -0.0516,  0.0654, -0.0009,  0.0016, -0.0351, -0.0534, -0.0474,
													 -0.0178, -0.1026, -0.0350, -0.0432, -0.2249,  0.0281, -0.1334,  0.1014,
													 -0.0320,  0.0315,  0.0109, -0.0757, -0.1258,  0.0343,  0.1390, -0.0027,
														0.0877,  0.1536,  0.0443, -0.3280,  0.0321, -0.0610, -0.1923,  0.0888,
													 -0.1727, -0.2037,  0.1504, -0.0260, -0.1104],
													[ 0.0872, -0.0910,  0.0404,  0.0835, -0.2086, -0.2251,  0.0668, -0.0016,
														0.1652, -0.0448,  0.0059, -0.0425, -0.1078, -0.0280,  0.0619, -0.0937,
													 -0.2407, -0.0320,  0.0960,  0.1075, -0.0776, -0.0537,  0.0560,  0.0519,
													 -0.0943,  0.0200, -0.0259,  0.1516, -0.0295, -0.0467, -0.0684, -0.0321,
														0.1154,  0.0084,  0.0828, -0.0397, -0.0702],
													[ 0.1614, -0.0034, -0.1421,  0.0750,  0.0960, -0.0230, -0.0507,  0.0444,
													 -0.0567, -0.0032,  0.1937,  0.0227,  0.1174,  0.0084,  0.0183, -0.0216,
													 -0.1129,  0.1492,  0.1017,  0.0669, -0.0970, -0.0546, -0.1127,  0.0665,
													 -0.0073,  0.0454, -0.0829,  0.0042, -0.0866, -0.1343, -0.0635,  0.0323,
														0.1264, -0.0811,  0.0598, -0.0811,  0.0101],
													[-0.0929, -0.0764, -0.0042,  0.0755,  0.0529, -0.1298,  0.0346, -0.0257,
														0.0254,  0.2163, -0.0190, -0.1050, -0.1848,  0.1243, -0.0854,  0.1475,
														0.0470, -0.0348,  0.0078,  0.0767,  0.0258,  0.0524,  0.2513,  0.0071,
														0.0365, -0.0738, -0.0148,  0.0836, -0.0292,  0.0783,  0.1065,  0.1375,
														0.3071, -0.0340,  0.0215, -0.0385,  0.1180],
													[ 0.1109,  0.0953,  0.0317, -0.1599, -0.1314, -0.2302, -0.1324, -0.0311,
													 -0.0596,  0.0235, -0.1847, -0.0515, -0.0711, -0.0572,  0.0342, -0.1562,
													 -0.1387, -0.1094,  0.0145, -0.0431, -0.0326, -0.0726,  0.1009,  0.0493,
													 -0.1102,  0.1577,  0.0777,  0.0578,  0.1002, -0.0261,  0.1558,  0.0968,
													 -0.0762,  0.0007, -0.0911,  0.1939, -0.0693]])),
								 ('fc1.bias',
									tensor([-0.0564, -0.0265, -0.0785, -0.1046, -0.0497, -0.0483, -0.1557, -0.1415,
													-0.1682, -0.0453])),
								 ('out.weight',
									tensor([[-0.0721,  0.0547, -0.0723, -0.0017,  0.0360,  0.0547,  0.0463,  0.1299,
													 -0.0284, -0.0707],
													[-0.0480,  0.2418, -0.1218, -0.0245,  0.0482,  0.0808,  0.0682,  0.1428,
														0.0041, -0.0963]])),
								 ('out.bias', tensor([0.0349, 0.0206]))])

	#abs_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'params_top50Return_Linear.pkl')
	#param_list50 = torch.load('params_top50Return_Linear.pkl')
	#param_list50 = torch.load('abs_path')

	"""
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
	"""


	ddqn = Net()
	ddqn.load_state_dict(param)
	action = ddqn.choose_action(state)
	return action
	
def makeDecision(position, action):
	#print(position, action)
	if position == 0:
		if action == 0:
			decision = '等待'
		else:
			decision = '買入'
	else:
		if action == 0:
			decision = '持有'
		else:
			decision = '賣出'
	#print(decision)
	return decision