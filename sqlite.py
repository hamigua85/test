# -*- coding:utf-8 -*- 
import sqlite3

def queryDB(path, openid):
    DB = sqlite3.connect(path)
    cur = DB.cursor()
    result = cur.execute("SELECT * FROM UserInfo WHERE OpenId = '%s'" %str(openid))
    result = cur.fetchall()
    DB.close()
    return result

def insertDataInDB(path,data):
    DB = sqlite3.connect(path)
    cur = DB.cursor()
    try:
        result = cur.execute("select * from UserInfo where OpenId = '%s'" %str(data.source))
        result = cur.fetchall()
        if len(result) == 0:
            result = cur.execute("insert into UserInfo values (?,?,?,?)", [str(data.source),'','',''])
    except Exception , e:
        pass
    DB.commit()
    DB.close()

def updataDataInDB(path,openid,username,address,phonenumber,sn):
    DB = sqlite3.connect(path)
    cur = DB.cursor()
    try:
        result = cur.execute("select * from UserInfo where OpenId = '%s'" %str(openid))
        result = cur.fetchall()
        if len(result) == 1:
            if username != None:
                result = cur.execute("UPDATE UserInfo set UserName=? WHERE OpenId = ?",(username,openid))
            if address != None:
                result = cur.execute("UPDATE UserInfo set Address=? WHERE OpenId = ?",(address,openid))
            if phonenumber != None:
                result = cur.execute("UPDATE UserInfo set PhoneNum=? WHERE OpenId = ?",(phonenumber,openid))
            if sn != None:
                result = cur.execute("UPDATE UserInfo set SN=? WHERE OpenId = ?",(sn,openid))
    except Exception , e:
        DB.close()
        return False
    DB.commit()
    DB.close()
    return True


def queryOpenID(path,sn):
    DB = sqlite3.connect(path)
    cur = DB.cursor()
    try:
        result = cur.execute("select * from UserInfo where SN = '%s'" %str(sn))
        result = cur.fetchall()
        if len(result) >= 1:
            DB.close()
            return result
    except Exception , e:
        print e
        DB.close()
        return None
    DB.close()
    return None
