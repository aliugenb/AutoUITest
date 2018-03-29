# -*- coding:utf-8 -*-
import os,sys

class FileHandle:
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
                                                fileNames.append(os.path.join(path, filename))
                return fileNames
                                        
        def getlogInfo(self,filename):
                #logfile='/Users/nali/gitlab/uiautotest/Android/LOG/20180105144105_log.txt'
                table_contens = []        
                        
                for lines in open(filename):
                        line = lines.strip().encode('utf-8')
                        r = line.strip().split(' - ',2)
                        '''
                        for i in range(len(r)):
                                print r[i]
                        '''

                        caseName_ex = r[1].split('.',1)
                        caseName = caseName_ex[0]
                        #print "用例名："+ caseName
                        
                        moduleName_ex =caseName_ex[0]
                        moduleName = moduleName_ex.split('_', 1)[0]
                        #print "模块名："+ moduleName
                                                
                        subModuleName_ex = r[2].split(' ',1)
                        subModuleName = subModuleName_ex[0][1:len(subModuleName_ex[0])-1]
                        #print "子模块名："+ subModuleName
                                                                                          
                        testResult_ex = subModuleName_ex[1].split(":",1)
                        testResult = testResult_ex[0]
                        #print "测试结果："+ testResult
                                                
                        comment = testResult_ex[1]
                        #print "备注："+ comment   
                        
                        dict = {'caseNames': caseName, 'moduleNames': moduleName,'subModuleNames': subModuleName, 'testResults': testResult,'comments': comment}
                        table_contens.append(dict)
                '''
                for i in range(len(table_contens)):
                        print table_contens[i]['caseNames']
                        print table_contens[i]['moduleNames']
                        print table_contens[i]['subModuleNames']
                        print table_contens[i]['testResults']                        
                        print table_contens[i]['comments']
                        print "*********"
                '''                        
                return table_contens                    
        
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
        
def writeToHtml(filename, htmlTag, tagContents):
        f = open(filename,'a')
        f.write('<'+htmlTag+'>'+tagContents+'</'+htmlTag+'>')
        
def writeHtmlHead(filename):
        f = open(filename,'a')
        f.write('<head><title>Test 喜马拉雅FM-Android-UI自动化测试报告</title></head>')
        f.write('<meta charset="UTF-8">')       
        f.write('<h1 align="center"><b>喜马拉雅FM-Android-UI自动化测试报告</b></h1>')
        
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
        
def writeTestDetail(filename, table_contens):
        f = open(filename,'a')
        f.write('<table border="1" class="dataframe">') 
        f.write('<thead><tr style="text-align: center;"><th>用例名</th><th>模块名</th><th>子模块名</th><th>测试结果</th><th>备注</th></tr>')  
        for i in range(len(table_contens)):
                f.write('<tr style="text-align: center;">')
                f.write('<th>'+ table_contens[i]['caseNames']+'</th>')
                f.write('<th>'+ table_contens[i]['moduleNames']+'</th>')
                f.write('<th>'+ table_contens[i]['subModuleNames']+'</th>')
                f.write('<th>'+ table_contens[i]['testResults']+'</th>')
                f.write('<th>'+ table_contens[i]['comments']+'</th>')
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
        
        #root = '/Users/nali/gitlab/uiautotest/Android/LOG'
        root='/home/leo/workspace/jenkinsworkspace/workspace/Android_UI_Test/uiautotest/Android/LOG'
        tempHtmlname = os.path.join(root, 'test.html')
        
        h = Handler()
        deviceName = h.getDeviceName()
        platformVersion = h.getPlatformVersion()
        deviceId = h.getDeviceId()
              
        fd = FileHandle()
        projectInfo = fd.getProjectInfo(root)
        fileNames = fd.getLogFiles(root)
        if (len(fileNames) >=1):
                filename = fileNames[0]
                testTime = fd.getLogTime(filename) 
                table_contens = fd.getlogInfo(filename)
        
                #写test.html文件信息
                writeHtmlHead(tempHtmlname)
                writeAppInfo(tempHtmlname,projectInfo[0], projectInfo[1], projectInfo[2])
                writeDeviceInfo(tempHtmlname, deviceName, platformVersion, deviceId)
                writeTestResult(tempHtmlname,testTime[0], testTime[1])
                writeTestDetail(tempHtmlname, table_contens)
        
                #已测试开始时间重命名test.html
                renameHtmlFile(root, testTime)
                
        else:
                print "ERROR：没有找到文件或读取文件失败"
                
                
                
        
        
        
        
        
        
        
        
       
        
        
        
   