# -*- coding: utf-8 -*-
"""
Created on Fri May 12 09:18:59 2023

@author: YuanYi
"""

#%%
#sector of importion
import os
import argparse

#import pandas as pd
#import sqlite3

import sqlparse
#%%
#parse arguments
parser = argparse.ArgumentParser()
parser.description='From the full SQL statements [fullSQLFile], find the statements of the TABLE/INDEX which was listed in [srcFilterTblListFile], \
    output to [outStatementFile] for the next execution in SQL client, and output to [outTblnameListFile] for comparation and evaluation.'
#parser.add_argument("-a", "--inputA", help="this is parameter a", dest="argA", type=int, default="0")

parser.add_argument("-D", "--DirOfFullSQLFile", help="this parameter is to indicate the \
                    working directory of fullSQLFile, which by default will be the one containing this .py file. Mostantly the fullSQLFile will not move.", \
                        dest = "dirFullSQLFile", type=str, default=os.getcwd())
    
parser.add_argument("-W", "--WorkDir", help="this parameter is to appoint the directory that contains [srcFilterTblListFile], [outStatementFile] \
                    and [outTblnameListFile]. Current dir of this .py file by default.", \
                            dest="workDir", \
                        type = str , default=os.getcwd())

parser.add_argument("-F", "--fullSQLFile", help="this parameter is to appoint the full SQL File which contains all the statements to create TABLE, INDECES or \
                    other entries. 'sz_tab_cre.sql' by DEFAULT.", dest='fullSQLFile' , \
                        type = str , default='sz_tab_cre.sql')
    
parser.add_argument("-S", "--srcFailedListFile", help="this parameter is to appoint \
                    the file containing list of last failed created TABLES or Indeces, according which to picked out statements out from [fullSQLFile]. 'failed.txt' by default.", \
                         dest="srcFailedList", type = str , default='failedList.txt')
    
parser.add_argument("-O", "--OutputStatemensFile", help="this parameter is to appoint \
                    the OUTPUT file containing the statements which were picked out and would used to try for the next time. 'out_statement.sql' by default.", \
                        dest="outputStatemensFile", type = str, default = 'out_statement.sql')

parser.add_argument("-L", "--OutputListFile", help="this parameter is to appoint \
                    the output TABLE/INDECES list file name, which will be used to evluate the operaion of the Programme. 'out_name_list.txt' by default.", \
                        dest="outputListFile", type = str, default = 'out_name_list.txt')
args = parser.parse_args()

#print("parameter A is :",args.argA)

print("parameter D 全量创建语句所在目录 is :", args.dirFullSQLFile)
print("parameter W 输入失败文件和输出创建等文件目录 is :", args.workDir)
print("parameter F 全量创建语句文件 is :", args.fullSQLFile)

print("parameter S 输入的上次创建失败文件清单 is :", args.srcFailedList)
print("parameter O 输出的创建语句文件 is :", args.outputStatemensFile)
print("parameter L 输出的创建实体名列表文件 is :", args.outputListFile)
#%%

with open(args.dirFullSQLFile +'\\' + args.fullSQLFile, mode = 'rt', encoding='utf-8') as fFullSQLFile:
    dataFromFullSqlFile = fFullSQLFile.read()
    
    outputListFile_fh = open(args.workDir +'\\' + args.outputListFile, "wt")
    srcFailedList_fh = open(args.workDir + '\\' + args.srcFailedList, mode = 'rt')
    oStatmntFile_fh = open(args.workDir + '\\' + args.outputStatemensFile, mode = "wt", encoding='utf-8')
    
    lines = srcFailedList_fh.readlines()
    newLine = []
    #for line in flist.readlines():
    for line in lines:
        line = line.strip('\n')
        newLine.append(line.strip('\n'))
        
    statements = sqlparse.parse(dataFromFullSqlFile)
    for iStatement in statements:
        print("\r")
        print("================")
        print("Statement get_type():" ,iStatement.get_type())
        #print("iStatement:", iStatement.tokens)
        print("\r")
        for iToken in iStatement.tokens:
            #print("\t type of:", type(iToken),"\t token value:", iToken.value,"\t token ttype:", iToken.ttype)
            if type(iToken) == sqlparse.sql.Identifier:
                print("\t type of:", type(iToken),"\t token value:", iToken.value,"\t token ttype:", iToken.ttype)
                print("IDENDIFIER IS HERE!")
                if iToken.value in newLine:
                    print("!!!!!FOUND in SOURCE! put into OUTPUT NAME LIST!!!!!!")
                    outputListFile_fh.write(iToken.value+"\n")
                    oStatmntFile_fh.write(str(iStatement))
                break
    
    outputListFile_fh.close()
    srcFailedList_fh.close()
    oStatmntFile_fh.close()
    
    fFullSQLFile.close()