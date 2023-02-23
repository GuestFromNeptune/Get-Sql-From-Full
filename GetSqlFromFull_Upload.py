# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 16:08:20 2023

@author: YuanYi
"""

import sqlparse

strDir = r'C:\\<YOUR DIR WHERE INPUT>\\'
outDir = r'C:\\<YOUR DIR TO OUTPUT>\\'

#fullsqlFile = r'sz_tab_cre.sql'
fullsqlFile = r'sz_idx_cre.sql'
#outTblnameListFile = r'out_tab_list.txt'
outTblnameListFile = r'out_idx_list.txt'
outStatementFile = r'out_statement.sql'
srcFilterTblListFile = r'failureIndex20230215.txt'   #also as failure file list

#Read from FailedRecordFile and insert into a list
#Read from FullTableCreationFile 
#   if the Table was in Failure Record, then put the creation statement into a New File!

with open(strDir + fullsqlFile, mode = 'rt', encoding='utf-8') as ftbl:
    dataFromFullSqlFile = ftbl.read()
    
    oTblnmListFile_fh = open(outDir + outTblnameListFile, "wt")
    rTblSrcFltrTblList_fh = open(outDir + srcFilterTblListFile, mode = 'rt')
    oStatmntFile_fh = open(outDir + outStatementFile, mode = "wt", encoding='utf-8')
    
    lines = rTblSrcFltrTblList_fh.readlines()
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
                    oTblnmListFile_fh.write(iToken.value+"\n")
                    oStatmntFile_fh.write(str(iStatement))
                break
    
    oTblnmListFile_fh.close()
    rTblSrcFltrTblList_fh.close()
    oStatmntFile_fh.close()
