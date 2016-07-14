# -*- coding: UTF-8 -*-
import pymysql
import sys
import  os
import re

#Connect the databse
conn = pymysql.connect(host='192.168.1.249', user='root', passwd='root', db='tj', charset='utf8')
cur = conn.cursor()

#change the current folder
def SouguoDir(path):

    items=[]
    for o in os.listdir(path):
        item={}
        item['foodname']=re.sub("-?[1-9]\d*","",o)
        item['foodname']=item['foodname'].decode('gbk').encode('utf-8')
        nextfilepath=path+"/%s" % o
        nextfilename=os.listdir(nextfilepath)
        if not nextfilename:
            print u'文件夹为空'
            item['foodpic']='empty'
        else:
            item['foodpic']=nextfilename[0]
        item['foodpath']=nextfilepath+"/%s" % item['foodpic']

        items.append(item)

    return items # return the items apply function  openImage

def openImage(items,jishu,writedir):

    for it in items:
        print it['foodname']
        print it['foodpath']
        try:
            #用读文件模式打开图片
            fin = open(it['foodpath'],'rb')
            #将文本读入img对象中
            img = fin.read()
            #关闭文件
            #print '正常读取文件 %s' % img
            fin.close()
        except IOError, e:
            #如果出错，打印错误信息
            print "Error %d: %s" % (e.args[0],e.args[1])

        try:
            #链接mysql，获取对象

            insert_sql="""INSERT into tj_food VALUES (%s,%s)"""
            args=(it['foodname'],pymysql.Binary(img))
            cur.execute(insert_sql,args)

            #提交数据
            conn.commit()
            #提交之后，再关闭cursor和链接


        except pymysql.Error, e:
            #若出现异常，打印信息
            print "Error %d: %s" % (e.args[0],e.args[1])

        #暂时不需要从数据库取出图片数据了
        # cur.execute("SELECT foodjpg FROM tj_food limit 1")
        # d = cur.fetchone()[0]
        # cur.close()
        # conn.commit()
        write_path="%s/%s.jpg" % (writedir,it['foodname'])
        write_path=unicode(write_path,'utf8')
        f = open(write_path,'wb')
        f.write(pymysql.Binary(img))
        f.close()
        jishu+=1

#以菜品文件夹命名，将第一张图片提取到items并保存好
MyItems=SouguoDir('e:/caipin')
jpg_count=1
#执行添加并将菜品写入到内置的目录
openImage(MyItems,jpg_count,'d:/caicai')
conn.close()


# import pymysql
#
# class BlobDataTestor:
#     def __init__ (self):
#         self.conn = pymysql.connect(host='192.168.1.249', user='root', passwd='root', db='tj', charset='utf8')
#
#     def __del__ (self):
#         try:
#             self.conn.close()
#         except :
#             pass
#
#
#     def closedb(self):
#         self.conn.close()
#
#     def setup(self):
#         cursor = self.conn.cursor()
#         cursor.execute( """
#             CREATE TABLE IF NOT EXISTS `Dem_Picture` (
#             `ID` int(11) NOT NULL auto_increment,
#             `PicData` mediumblob,
#             PRIMARY KEY (`ID`)
#             ) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=4 ;
#             """)
#
#
#
#     def teardown(self):
#         cursor = self.conn.cursor()
#         try:
#             cursor.execute( "Drop Table Dem_Picture" )
#         except:
#             pass
#         # self.conn.commit()
#
#     def testRWBlobData(self):
#     # 读取源图片数据
#         path="E:/caipin/22黄焖鸡/111.jpg"
#         mypath=unicode(path,'utf8')
#         f = open( mypath , "rb" )
#         b = f.read()
#         f.close()
#
#     # 将图片数据写入表
#         cursor = self.conn.cursor()
#         cursor.execute( "INSERT INTO Dem_Picture (PicData) VALUES (%s)" , (pymysql.Binary(b)))
#     # self.conn.commit()
#
#     # 读取表内图片数据，并写入硬盘文件
#         cursor.execute( "SELECT PicData FROM Dem_Picture ORDER BY ID DESC limit 1" )
#         d = cursor.fetchone()[0]
#         cursor.close()
#
#         f = open( "d:/22.jpg" , "wb" )
#         f.write(d)
#         f.close()
#
# # 下面一句的作用是：运行本程序文件时执行什么操作
# if __name__ == "__main__":
#
#     test = BlobDataTestor()
#
#     try:
#         test.setup()
#         test.testRWBlobData()
#         test.teardown()
#     finally:
#         test.closedb()
#
#
#



