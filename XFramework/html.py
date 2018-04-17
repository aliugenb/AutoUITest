# -*- coding:utf-8 -*-
import os,sys
import chardet
from dateutil import parser

class LogFileHandle():
    
    def  getLogTime(self,logfile):
        #logfile='/Users/nali/Documents/Task/20180105144105_log.txt'
        count = -1
        for count, line in enumerate(open(logfile,'rU')):
            pass
        count +=1
        #print count
    
        with open(logfile, 'r') as f:
            first_line = f.readline().split(",",1)[0]
            if count == 1:
                last_line = first_line
            else:
                off = -50
                while True:
                    f.seek(off, 2)
                    lines = f.readlines()
                    if len(lines)>=2:
                        last_line = lines[-1].split(",",1)[0]
                        break   
                    off *= 2             
        return first_line, last_line 
    
    def getProjectInfo(self, root): 
        projectInfo = []
        g=os.walk(root)
        for path, dir, filelist in g:
            for filename in filelist:
                if filename.endswith('txt'):
                    if filename == 'project.txt':
                        projectPath=os.path.join(path,filename)
                        #print projectPath
                        for line in open(projectPath):
                            projectInfo.append(line.split('\n',1)[0])

                    else:
                        pass
            projectName = projectInfo[0]
            versionBranch = projectInfo[1]
            jenkinsAddress = projectInfo[2]
            return projectInfo
    
    def getLogFiles(self,root):
        fileNames = []
        g=os.walk(root)
        for path, dir, filelist in g:
            for filename in filelist:
                if filename.endswith('txt'):
                    if filename == 'project.txt':
                        pass        
                    else:
                        print '找到log文件'
                        fileNames.append(os.path.join(path, filename))
        return fileNames    
   
    def getModuleTestTime(self, logfile):
        # 得到日志文件中每个子模块的测试时间
        # 如 other--个人页--aa
        #    other--个人页--bb
        # 结果：个人页的测试开始时间，结束时间
        startTimes=[]
        endTimes=[]        
        for lines in open(logfile):
            line = lines.strip().encode('utf-8')
            if 'Test Start...' in line:
                starttime = line.strip().split(',',2)[0]
                #print  starttime
                startTimes.append(starttime)
            elif 'Test End...' in line:
                endtime = line.strip().split(',',2)[0] 
                #print endtime
                endTimes.append(starttime) 
        if len(startTimes) == len(endTimes):
            return startTimes, endTimes
        else: 
            pass
        
    def getTesttimeLine(self, logfile):
        # 得到日志文件中每个子模块的测试开始，结束行数
        # 目的：保证后续精确批评到测试子模块的测试内容
        count = 0
        startLineCount = []
        endLineCount = []        
        for lines in open(logfile):
            line = lines.strip().encode('utf-8')
            if 'ERROR:' in line:
                pass
            else:
                if 'Test Start...' in line:
                     #starttime = line.strip().split(',',2)[0]
                     #print  starttime
                    startLineCount.append(count)
                elif 'Test End...' in line:
                     #endtime = line.strip().split(',',2)[0] 
                     #print endtime
                    endLineCount.append(count) 
                count = count +1
        return startLineCount, endLineCount
             
    def getModulesSplitContents(self, logfile):
        # 对模块内容进行处理:分离，开始行，结束行
        # 处理异常行，置换内容为' ZERO'
        # 得到begin行，zero行，测试内容行，end行
        tempContents = [] 
        contentS = []
        for lines in open(logfile):
            line = lines.strip().encode('utf-8')
    
            if 'Test Start...' in line:
                #starttime = line.strip().split(',',2)[0]                
                tempContents.append(' begin')
                
            elif 'Test End...' in line:
                #endtime = line.strip().split(',',2)[0]
                tempContents.append(' end')
                
            else:
                contents = line.strip().split('>',1)[1]
                tempContents.append(contents)
                
        for i in range(len(tempContents)-1):
            if "ERROR" in tempContents[i]:                               
                #print mTotalContents[i].split(':',1)[1]
                tempContents[i+1]=tempContents[i+1]+'(Error:'+tempContents[i].split(':',1)[1]+')'
                tempContents[i]=' ZERO' 
                
        return tempContents
    
    def getModulesSplitTimestamps(self, logfile):
        # 对模块内容进行处理:分离，开始行，结束行
        # 处理异常行，置换内容为' ZERO'
        # 得到begin行，zero行，测试内容行，end行
        tempTimes = [] 
        timeS = []
        for lines in open(logfile):
            line = lines.strip().encode('utf-8')
            
            if 'ERROR:' in line:
                pass            
            elif 'Test Start...' in line:
                starttimestamp = line.strip().split(',',1)[0]                
                tempTimes.append(starttimestamp)
                
            elif 'Test End...' in line:
                endtimestamp = line.strip().split(',',1)[0]
                tempTimes.append(endtimestamp)
            
            else:
                moduleTimestamp = line.strip().split(',', 1)[0]
                tempTimes.append(moduleTimestamp)
        return tempTimes
    
class Handler:
    
        def getDeviceName(self):
                """
                获取手机名字
                """
                command = 'adb shell getprop ro.product.model'
                deviceName = os.popen(command).read().strip()
                if deviceName == '':
                        print '获取手机名称失败'
                        raise RuntimeError
                return deviceName
                  
        def getPlatformVersion(self):
                """
                获取平台版本
                """
                command = 'adb shell getprop ro.build.version.release'
                platformVersion = os.popen(command).read().strip()
                if platformVersion == '':
                        print '获取手机名称失败'
                        raise RuntimeError
                return platformVersion
        
        def getDeviceId(self):
                """
                获取设备id
                """
                command = 'adb devices'
                #deviceIdInfo 得到devices命令
                deviceIdSourceInfo=os.popen(command).read().strip()
                # 得到第二行后的信息
                deviceIdInfo=deviceIdSourceInfo.split('\n',2)[1]
                # 得到设备号
                deviceId=deviceIdInfo.split('\t',1)[0]
                if deviceId == '':
                        print '获取设备id失败'
                        raise RuntimeError
                return deviceId
       
def getModulesContents(tempContents):
    #得到log中所有模块到内容
    #即，去掉begin行， zero行， end行
    modulesContents = []
    for i in range(len(tempContents)):
        if  'begin'  in tempContents[i] or 'ZERO'  in tempContents[i] or 'end' in tempContents[i]:
            pass
        else:
            modulesContents.append(tempContents[i])
    return modulesContents

def getDurtime(starttime, endtime):
    
    begintime = parser.parse(starttime)
    endtime = parser.parse(endtime)
    day_sector = (endtime - begintime).days
    seconds_sector = (endtime - begintime).seconds
    hour_sector = seconds_sector/3600
    minute_sector = (seconds_sector%3600)/60
    second_sector = (seconds_sector%3600)%60
    #print minute_sector, second_sector
    
    if day_sector != 0 :            
        durtime = str(day_sector)+'天'
    else:
        durtime = ''
        
    if hour_sector != 0 :
        durtime = durtime + str(minute_sector)+'时'
    else:
        durtime = durtime
        
    if minute_sector != 0:
        durtime = durtime + str(minute_sector)+'分'
    else:
        durtime = durtime
        
    if seconds_sector != 0:
        durtime = durtime+str(second_sector)+'秒'
    else:
        durtime = durtime
   
    return durtime

def getModuleTimestamps(slines,  elines, tempTimes):
    caseTestDur = []
    caseTestDurs = []
    for i in range(len(slines)):
        temp2Times = []
        caseTestDur = []
        for j in range(slines[i], elines[i]): 
            temp2Times.append(tempTimes[j]) 
        #print i,len(temp2Times), temp2Times
            
        for k in range(len(temp2Times)-1):            
            durtime = getDurtime(temp2Times[k], temp2Times[k+1])
            #print k, durtime
            caseTestDur.append(durtime)
        '''
        for x in range(len(caseTestDur)):
            print i,x, caseTestDur[x]'''
            
        caseTestDurs.extend(caseTestDur)
    
    return caseTestDurs


def getModuleContents(slines, elines,tempContents):
    #如：other--个人页--aa
    #得到子模块(如个人页)的测试内容
    moduleContents=[]
    for i in range(len(slines)):
        temp2Contents=[]
        for j in range(slines[i], elines[i]): 
            temp2Contents.append(tempContents[j])  
        moduleContents.append(temp2Contents)
    return moduleContents

def writeToHtml(filename, htmlTag, tagContents):
    f = open(filename,'a')
    f.write('<'+htmlTag+'>'+tagContents+'</'+htmlTag+'>')

def writeHtmlHead(filename):
    f = open(filename,'a')
    f.write('<head><title>Test 喜马拉雅FM-Android-UI自动化测试报告V2.0</title></head>')
    f.write('<meta charset="UTF-8">')       
    f.write('<h1 align="center"><b>喜马拉雅FM-Android-UI自动化测试报告v2.0</b></h1>')

def writeAppInfo(filename, projectName, versionBranch, jenkinsAddress):
    f = open(filename,'a')
    f.write('<font style="color: green"><b>App版本信息</b></font>')
    f.write('<hr>')
    f.write('<table>')
    f.write('<tr align="left"><th>项目名称：'+projectName+'</th></tr>')
    f.write('<tr align="left"><th>版本分支：'+versionBranch+'</th></tr>')
    f.write('<tr align="left"><th>jenkins测试项目地址：<a  href="'+ jenkinsAddress + '"target = _blank >'+jenkinsAddress+'</a></th></tr>')
    f.write('</table>')
    f.write('<br/>')
    f.write('<br/>')

def writeDeviceInfo(filename, deviceName, platformVersion, deviceId):
    f = open(filename,'a')
    f.write('<font style="color: green"><b>设备信息</b></font>')
    f.write('<hr>')
    f.write('<table>')
    f.write('<tr align="left"><th>设备名称：'+deviceName+'</th></tr>')
    f.write('<tr align="left"><th>Android版本：'+platformVersion+'</th></tr>')
    f.write('<tr align="left"><th>DevicesId：'+deviceId+'</th></tr>')
    f.write('</table>')
    f.write('<br/>')
    f.write('<br/>')

def writeTestResult(filename, startTime, endTime, durTime="60min"):
    durTime = getDurtime(startTime, endTime)
    f = open(filename,'a')
    f.write('<font style="color: green"><b>设备信息</b></font>')
    f.write('<hr>')
    f.write('<table>')
    f.write('<tr align="left"><th>测试开始时间：'+startTime+'</th></tr>')
    f.write('<tr align="left"><th>测试结束时间：'+endTime+'</th></tr>')
    f.write('<tr align="left"><th>测试持续时间：'+durTime+'</th></tr>')
    f.write('</table>')
    f.write('<br/>')
    f.write('<br/>')

def writeTestDetail(filename, modulesContents):
    for i in range(len(modulesContents)):
        modulesContents[i]= modulesContents[i].strip().split(':', 1)[1]
     
    f = open(filename,'a')
    #f.write('<table border="1" class="dataframe">') 
    f.write('<table width="100%" border="1"  class="dataframe">') 
    f.write('<thead><tr style="text-align: center;background: #ccc"><th>测试耗时</th><th>用例名</th><th>模块名</th><th>子模块名</th><th>测试结果</th><th>备注</th><th>失败截图</th><th>重要日志</th>')  
    for i in range(len(zip(caseTestDurs,  modulesContents))):
        modulesContents[i]= modulesContents[i].strip().split('-', 2)
    
        testresultComment=modulesContents[i][2].strip().split(':',1)[1]
        if '(' in testresultComment:
            testresult = testresultComment.split('(',1)[0]
            comment = testresultComment.split('(',1)[1][:-1]
            f.write('<tr style="text-align:center; color:#FF0000;">')
            f.write('<th>'+caseTestDurs[i] +'</th>')
            f.write('<th>'+modulesContents[i][0] +'</th>')
            f.write('<th>'+modulesContents[i][1] +'</th>')
            f.write('<th>'+ modulesContents[i][2].strip().split(':',1)[0]+'</th>')             
            f.write('<th >'+ testresult+'</th>')
            f.write('<th >'+ comment +'</th>')
            f.write('<th>'+' '+'</th>')
            f.write('<th>'+' '+'</th>')
            f.write('</tr>')                
        else:
            f.write('<tr style="text-align: center;">')
            f.write('<th>'+caseTestDurs[i] +'</th>')
            f.write('<th>'+modulesContents[i][0] +'</th>')
            f.write('<th>'+modulesContents[i][1] +'</th>')
            f.write('<th>'+ modulesContents[i][2].strip().split(':',1)[0]+'</th>')             
            f.write('<th>'+ modulesContents[i][2].strip().split(':',1)[1]+'</th>')
            f.write('<th>'+' '+'</th>')
            f.write('<th>'+' '+'</th>')
            f.write('<th>'+' '+'</th>')
        f.write('</tr>')                
    f.write('</table>')
    
def renameHtmlFile(root, testTime):
    testTime1 = testTime[0].replace('-','')
    testTime2 = testTime1.replace(' ','_')
    testTimes = testTime2.replace(':','')        
    src = os.path.join(root, 'test.html')
    dst = os.path.join(root, testTimes+'.html')
    #print src
    #print dst
    os.rename(src, dst)
           
if __name__=="__main__":
    #root='/home/leo/workspace/jenkinsworkspace/workspace/Android_NewUI_Test/Newuiautotest/Android/LOG'
    #root='/Users/nali/gitlab/Newuiautotest/Android/LOG'
    root1= os.path.abspath('..')
    root = root1+'/Android/LOG'
    print 'root:', root
    tempHtmlname = os.path.join(root, 'test.html')
    print tempHtmlname
          
    lfh = LogFileHandle()
    
    # 得到log.txt文件
    #filename='/Users/nali/gitlab/Newuiautotest/Android/LOG/total_log.txt'
    filename = lfh.getLogFiles(root)
    if len(filename)==0:
        print "ERROR:不存在log文件"
    else:  
        print filename
        filename = filename[0]    
    
    #得到模块的测试开始时间，结束时间
    stimes =  lfh.getModuleTestTime(filename)[0]
    etimes = lfh.getModuleTestTime(filename)[1]
    
    #得到模块的测试开始时间行，结束时间行 
    slines = lfh.getTesttimeLine(filename)[0]
    elines = lfh.getTesttimeLine(filename)[1]
    
    #得到模块的测试内容
    tempContents = lfh.getModulesSplitContents(filename)
    modulesContents = getModulesContents(tempContents)
    
    #单个测试case测试时间
    tempTimestamps = lfh.getModulesSplitTimestamps(filename)
    #单个测试case测试耗时
    caseTestDurs = getModuleTimestamps(slines, elines, tempTimestamps)
    
    #得到测试项目信息
    projectInfo = lfh.getProjectInfo(root)
            
    h = Handler()
    deviceName = h.getDeviceName()
    platformVersion = h.getPlatformVersion()
    deviceId = h.getDeviceId()
    
    
    testTime = lfh.getLogTime(filename) 

    #写test.html文件信息
    writeHtmlHead(tempHtmlname)
    writeAppInfo(tempHtmlname,projectInfo[0], projectInfo[1], projectInfo[2])
    writeDeviceInfo(tempHtmlname, deviceName, platformVersion, deviceId)
    writeTestResult(tempHtmlname,testTime[0], testTime[1])
    writeTestDetail(tempHtmlname, modulesContents)

    #已测试开始时间重命名test.html
    #renameHtmlFile(root, testTime)
    
