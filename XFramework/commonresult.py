#-*- coding:utf-8 -*- 
import os, sys, platform
import requests,json



def getResultPath(filename='result.txt'):
    '''
    获取Result生成路径和文件名
    '''
    #设置结果生成路径
    targetPath = os.path.realpath(sys.argv[0])
    #print(targetPath)
    if 'XFramework' in targetPath:
        targetPath = targetPath.split('XFramework')
        if 'Windows' in platform.system():
            targetPath = targetPath[0] + 'Android\\LOG\\'
        else:
            targetPath = targetPath[0] + r'Android/LOG/'
    else:
        print('路径中不存在，XFramework, 请检查路径')
        raise IOError
    
    logFile = targetPath + filename
    return logFile

resultPath = getResultPath()
#统计一次构建执行的用例情况
#with open(r'result.txt', 'r') as inFile:
with open(resultPath, 'r') as inFile:
	data = inFile.readlines()
	testsRun = []
	successful = []
	failures = []
	errors = []
	skipped = []
	i = 0
	for line in data:
		if (i%6 == 1):
			#print(int(line.split(':')[1].split('\n')[0]))
			testsRun.append(int(line.split(':')[1].split('\n')[0]))
		elif (i%6 == 2):
			successful.append(int(line.split(':')[1].split('\n')[0]))
		elif (i%6 == 3):
			failures.append(int(line.split(':')[1].split('\n')[0]))
		elif (i%6 == 4):
			errors.append(int(line.split(':')[1].split('\n')[0]))
		elif (i%6 == 5):
			skipped.append(int(line.split(':')[1].split('\n')[0]))
		i += 1
	
#将统计结果追加写到文本中
#with open(r'result.txt', 'a+') as wf:
with open(resultPath, 'a+') as wf:
	#print('testsRunTotal:'+str(sum(testsRun))+' '+'successfulTotal:'+str(sum(successful))+' '+'failuresTotal:'+str(sum(failures))+' '+'errorsTotal:'+str(sum(errors))+' '+'skippedTotal:'+str(sum(skipped))+'\n')
	wf.write('testsRunTotal:'+str(sum(testsRun))+' '+'successfulTotal:'+str(sum(successful))+' '+'failuresTotal:'+str(sum(failures))+' '+'errorsTotal:'+str(sum(errors))+' '+'skippedTotal:'+str(sum(skipped))+'\n')

#发送钉钉消息
with open(resultPath, 'r') as readFile:
	read =''
	while True:  
	    line = readFile.readline() 
	    if not line: 
	        break 
	    read = line 
	#print(read)  

url = 'https://oapi.dingtalk.com/robot/send?access_token=4f97966c1fff6608904a19caf1e9750e205c901acd2a0738a70217ad2359fc8c'##定义http请求的地址，即1
headers = {'Content-Type': "application/json"}
pagrem={
	"msgtype": "link",
	"link": {
		"text": read,
		"title": "Android _UI测试报告",
		"picUrl": "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1494415057918&di=60c2f6f58b464649e234bc4c1419e737&imgtype=0&src=http%3A%2F%2Fwww.ran10.com%2Fckfinder%2Fuserfiles%2Fimages%2Fximalaya.jpg", 
		"messageUrl": "http://192.168.62.26:8080/view/UITest/job/Android_UI_Test/227/"
	}
}
f=requests.post(url,data=json.dumps(pagrem),headers=headers)


