'''
Created on 15.11.2018

@author: yasino
'''
from DocumentPreparation import DocumentPreparation
from TestCriteria import TestCriteria
from TextMiningService import TmService

if __name__ == '__main__':
    print('hello world')
    
# define filepath to the targeted use case XML
input_output_path = 'D:/cchecker/'

filepath = input_output_path + 'SmartTL.xml'
#filepath = input_output_path + 'VPP02.xml'
#filepath = input_output_path + 'VPP09.xml'
filepath2 = input_output_path + 'rule15.xml'


# prepare the sourcefile and create usecase objects 
uc1 = DocumentPreparation().create_usecase_62559(filepath)
uc2 = DocumentPreparation().create_usecase_62559(filepath2)

# create a textmining service object
ts1 = TmService(input_output_path, 'test_the_code')

# create a testcriteria object, execute rule checks
tc1 = TestCriteria(ts1)

uc1 = tc1.check_rule_1(uc1)
uc1 = tc1.check_rule_2(uc1)
uc1 = tc1.check_rule_3(uc1)
uc1 = tc1.check_rule_4(uc1)
uc1 = tc1.check_rule_5(uc1)
uc1 = tc1.check_rule_6(uc1)
uc1 = tc1.check_rule_7(uc1)
uc1 = tc1.check_rule_8(uc1)
uc1 = tc1.check_rule_9(uc1)
uc1 = tc1.check_rule_10(uc1)
uc1 = tc1.check_rule_11(uc1)
uc1 = tc1.check_rule_12(uc1)
uc1 = tc1.check_rule_13(uc1)
uc1 = tc1.check_rule_14(uc1)
uc1 = tc1.check_rule_15(uc1, uc2)
uc1 = tc1.check_rule_16(uc1)
uc1 = tc1.check_rule_17(uc1)
uc1 = tc1.check_rule_18(uc1)
uc1 = tc1.check_rule_19(uc1)
uc1 = tc1.check_rule_20(uc1)
