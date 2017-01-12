import requests,pickle
from bs4 import BeautifulSoup
from model import db,users


def get_session(username, password):
    passw=str(password)
    user =str(username)
    head={'UserID': user ,'UserPassword': passw, 'pswdStatus': 'strong', 'DummyVar': ''}
    url = 'http://puya.birjandut.ir/gateway/UserInterim.php'
    page = requests.post(url, data=head)
    s = requests.Session()
    response = s.post(url, data=head)
    return requests.utils.dict_from_cookiejar(s.cookies)
    
def grade(session):
    num = requests.get('http://puya.birjandut.ir/educ/educfac/stuShowEducationalLogFromGradeList.php',cookies=session)
    page = num.text
    soup = BeautifulSoup(page,'html')
    row = soup.find_all('tr')
    ##### row ok
    report=[]
    for r in row:
        #print r.contents
        soup = BeautifulSoup(str(r),'lxml')
        table = soup.find_all('td')
        one_row=[]
        #print table
        for x in table:
            one_row.append(x.string)
            #print "\n\n"
        report.append(one_row)
    return report
def save(username,md5,chat_id):
    #on start!
    temp = users.query.filter_by(chat_id = chat_id).first()
    if temp is not None and chat_id == temp.chat_id :
        temp.username= username
        temp.md5=md5
        db.session.commit()
    if temp is None:
        new_user = users(username,md5,chat_id)
        db.session.add(new_user)
        db.session.commit()


def startid(chat_id):
    if users.query.filter_by(chat_id = chat_id).first() is None :
        new_user = users('','',chat_id)
        db.session.add(new_user)
        db.session.commit()

def grade_HTML(report):
    html=''
    for row in report:
        if row is not None:
            for cell in row:
                if cell is not None:
                    html = html+'\n'+''+cell+'\n'
            html = html + '-------------'
    html = html + '\n Developed By @Cyanogen_ir \n BenYamin Salimi \n Github: BenYaminSalimi \ '
    return html


    
    
