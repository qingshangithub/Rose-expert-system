#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import chardet
from data_base import DataBase
from knowledge_base import KnowledgeBase
from conclusion_base import ConclusionBase

#初始化数据库，插入用户数据
DataBase = DataBase()
KnowledgeBase = KnowledgeBase()
CnclsBase = ConclusionBase()
KnowledgeBase.insert()

def reason(form):

	msymptom = [form.biti.data*1, form.bisai.data*2, form.fashao.data*3 , form.toutong.data*4 ,
				 form.jirousuantong.data*5 , form.kesou.data*6 ]
	mallegy = [form.wmhjgm.data*1 , form.dyxajfgm.data*2 , form.ymsfgm.data*3]

	while 0 in msymptom:
		msymptom.remove(0)
	while 0 in mallegy:
		mallegy.remove(0)
	print msymptom
	print mallegy


	DataBase.clear()
	CnclsBase.clear()
	DataBase.ask(msymptom,mallegy)
	DataBase.insert()

	# 推理
	while DataBase.newdatanum()>0:
		print "newdata还有数据条数：" + str(DataBase.newdatanum())
		fact = DataBase.pickone();	#取出一个事实，进行推理
		for i in range(KnowledgeBase.num()):
			rule = KnowledgeBase.pickone(i);
			if rule[0]==fact[0]:
				print "get conclusion:"+rule[1]
				#可信度计算
				fea_fact = float(fact[1])
				fea_rule = float(rule[2])
				fea_concl = fea_rule*max(0,fea_fact)
				#结论归纳
				if rule[1].encode('UTF-8') in ConclusionBase.param:
					# 如果是一个结论
					# print "put into conclusion"
					CnclsBase.putone((rule[1],fea_concl))#放入结论库
				else:
					#如果是一个推论
					# print "put into newdata"
					DataBase.nputone((rule[1],fea_concl))#放入一个推论
		#删除已使用的事实
		DataBase.ndeleteone(fact)
	#把结论总结一下（之前的推理对同一个结论得出不同的可信度）
	for j in ConclusionBase.param:
		kind = CnclsBase.pickkind(j)
		if len(kind)==0:
			break;
		else:
			tmp = float(kind[0][2])
			for i in range(len(kind)-1):
				nex = float(kind[i+1][2])
				if tmp*nex<0:
					tmp = (tmp+nex)/(1-min(abs(tmp),abs(nex)))
				elif (tmp<0 and nex<0):
					tmp = tmp+nex+tmp*nex
				else:
					tmp = tmp+nex-tmp*nex
			CnclsBase.deletekind(kind[0][1])
			CnclsBase.putone((kind[0][1],tmp))

	# 打印结论，并解释
	for i in range(CnclsBase.num()):	#对所有结论检查一遍
		clu = CnclsBase.pickone(i);		
		for j in CnclsBase.interpretor:	#对每个结论，检查所有解释字段，以找到匹配的字段
			if j[0].decode('UTF-8')==clu:	#结论匹配
				print 'conclusion matched'
				print clu
				symptoms = []
				for symptom in j[1:len(j)]:
					if DataBase.checksymptom(symptom):
						symptoms.append(symptom)
				CnclsBase.update((clu,symptoms))
	string = CnclsBase.show()
	return string
