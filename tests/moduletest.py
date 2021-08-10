import torch
import sys
from torch import nn
sys.path.append("../")
import dump_percepnet
from dump_percepnet import printVector
class PercepNet(nn.Module):
    def __init__(self, input_dim=70):
        super(PercepNet, self).__init__()
        
        self.fc = nn.Sequential(nn.Linear(2, 3), nn.Sigmoid())
        self.conv1 = nn.Sequential(nn.Conv1d(2, 3, 3, stride=1, padding=1), nn.Sigmoid())
        self.gru1 = nn.GRU(2, 3, 1, batch_first=True)
        self.gru1.bias_ih_l0.data.fill_(0)
        self.gru1.bias_hh_l0.data.fill_(0)
if __name__ == '__main__':
    model = PercepNet()

    cfile = 'nnet_data_test.h'

    f = open(cfile, 'w')

    f.write('/*This file is automatically generated from a Pytorch model*/\n\n')
    f.write('#ifdef HAVE_CONFIG_H\n#include "config.h"\n#endif\n\n#include "nnet.h"\n//#include "nnet_data.h"\n\n')

    testdataset = [torch.Tensor([0.5,0.5]),torch.zeros([1,2,3])+0.5,torch.zeros([1,3,2])+0.5]
    for children, testdata in zip(model.named_children(),testdataset):
        name, module = children
        module.dump_data(f, name)
        output = module(testdata)
        if isinstance(output, tuple) :
            output = output[0]
        if len(output.size())>2:
            output = torch.transpose(output, 1, 2)
        if isinstance(module,nn.GRU):
            output = torch.transpose(output, 1, 2)
        printVector(f, output, name+"_output")
    
    
    #f.write('extern const struct RNNModel percepnet_model_orig = {\n')
    #for name, module in model.named_children():
    #        f.write('    &{},\n'.format(name))
    #f.write('};\n')
    
