#!/usr/bin/env python
#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from feature import DataBase
from rul import KnowledgeBase
from result import ConclusionBase
from flask import Flask
from flask import render_template
from flask import request
#初始化数据库，插入用户数据
DataBase = DataBase()
KnowledgeBase = KnowledgeBase()
CnclsBase = ConclusionBase()
KnowledgeBase.clear()
KnowledgeBase.create()
KnowledgeBase.insert()

def reason(form):

	# mye = [form.e1.data, form.e2.data, form.e3.data , form.e4.data ,
	# 			 form.e5.data , form.e6.data ,form.e7.data]
	#mye中暂时是bool值
	mye = form
	for i in range(len(mye)):
		if mye[i]:
			mye[i] = 1
		else:
			mye[i] = 0
	print mye  #用于检测

	DataBase.clear()
	CnclsBase.clear()
	DataBase.create()
	CnclsBase.create()
	DataBase.insert(mye)

	# 推理
	while DataBase.newdatanum()>0:
		print "newdata还有数据条数：" + str(DataBase.newdatanum())
		fact = DataBase.pickone()	#取出一个事实，进行推理
		print fact
		for i in range(KnowledgeBase.num()):
			rule = KnowledgeBase.pickone(i)
			if rule[0] == fact[0]:
				print "get conclusion:"+rule[1]
				#可信度计算
				fea_fact = float(fact[1])
				fea_rule = float(rule[2])
				fea_concl = fea_rule*max(0,fea_fact)
				#结论归纳
				if rule[1] in ConclusionBase.param:
					# 如果是一个结论
					# print "put into conclusion"
					CnclsBase.putone((rule[1],fea_concl))#放入结论库
					print 1
				else:
					#如果是一个推论
					# print "put into newdata"
					DataBase.nputone((rule[1],fea_concl))#放入一个推论
					print 2
		#删除已使用的事实
		DataBase.ndeleteone(fact)
	#把结论总结一下（之前的推理对同一个结论得出不同的可信度）
	for j in ConclusionBase.param:
		kind = CnclsBase.pickkind(j)
		print kind
		if len(kind)==0:
			break
		# elif len(kind)==1:
		# 	break
		else:
			tmp = float(kind[0][2])
			if len(kind) > 1:
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

	fin = CnclsBase.getcon()
	fin = list(fin)

	for item in fin:
		fin[fin.index(item)] = list(item)
	print fin

	for i in range(len(fin)):
		for j in CnclsBase.interpretor:
			if fin[i][1] == j[0]:
				for eb in j[1:len(j)]:
					if DataBase.checksymptom(eb):
						fin[i].append(eb)

	return fin

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
	if request.method == 'POST':
		tmpList=[]
		xingtai = request.form['xingtai']
		tmpList.append(xingtai)
		picixingtai = request.form['picixingtai']
		tmpList.append(picixingtai)
		picidaxiao = request.form['picidaxiao']
		tmpList.append(picidaxiao)
		huageng = request.form['huageng']
		tmpList.append(huageng)
		picirongmao = request.form['picirongmao']
		tmpList.append(picirongmao)
		guoshi = request.form['guoshi']
		tmpList.append(guoshi)
		epian = request.form['epian']
		tmpList.append(epian)
		boolList=[0,0,0,0,0,0,0]
		for i in range(len(tmpList)):
			if tmpList[i].encode("utf-8")=="是":
				boolList[i]=1
			else:
				pass
		output = reason(boolList)
		print 'hh'
		print tmpList
		print boolList
		print output
		muxue=['','','']
		dicCondition={'asgm':"矮生灌木",'sshdspc':"散生或成对皮刺",'pcdxbd':"皮刺大小不等",'hgzl':"花梗直立",'gsbqx':"果实扁球形",'epqy':"萼片全缘",'pcbrm':"皮刺被绒毛"};
		dicFlower={'fgqw':"法国蔷薇",'xssj':"香水月季",'mg':"玫瑰"};
		for i in range(len(output)):
			output[i][2]=str(output[i][2])
			output[i][1]=dicFlower[output[i][1].encode('utf8')]#.encode('gbk')
			if len(output[i])-3>0:
				for j in range(len(output[i])-3):
					output[i][j+3]=dicCondition[output[i][j+3].encode('utf8')]#.encode('gbk')
			else:
				pass
			output[i][0]=' '
			muxue[i]=' '.join(output[i])
		print output
		finalresult='\n'.join(muxue)
		return render_template('index.html',muxue=finalresult)
	else:
		return render_template('index.html')
	#return 'hello'

def main():
	app.debug=True
	app.run(host='0.0.0.0')
	# form=[0,1,1,1,0,0,1] #只调试使用
	# output = reason(form)

	# for i in range(len(output)):
	# print output

if __name__ == '__main__':
	main()