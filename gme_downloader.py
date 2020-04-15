import requests
from datetime import date

COOKIE_GMEITALIANO = "73121C41475ED92C082815C756EF486AEDB084515F184617CD3E736CBA2E1633BB5ED56855453D5599AA5CCFEC57CD70680B6541DA0654E94B6B5334DB04380FCBD154AA7B815603F909F96E2756D9E299D4F4F1AAB3B92694C27D3EF310D8D1AE0ADD7AD08C66B54A426D22068C1688CAB6B03B1483F67B2FA69202AEF21D22A7600AA867D1E101CD17A015061BA2A56250EF00DEF77F871FC486DA3EE2AB84"

class GMEDownloader:
    '''
    Downloads all kind of data from https://www.mercatoelettrico.org/
    '''

    def MGP_informazioni_preliminari(self, category : str, day : date):
        '''
        Downloads data from MGP/informazioni preliminari/category

        Parameters:
            category : str
                Must be one of the following: "StimeFabbisogno", "LimitiTransito", "PrezziConvenzionali"
            date : date
                Any date between 2009 circa and today, depends on the type of data.
        '''
        session = requests.Session()
        jar = requests.cookies.RequestsCookieJar()
        jar.set("GmeItaliano",COOKIE_GMEITALIANO)
        session.cookies = jar

        formatted_date = day.strftime("%Y%m%d")
        r = session.get('https://www.mercatoelettrico.org/It/WebServerDataStore/MGP_{}/{}MGP{}.xml'.format(category, formatted_date, category))
        print(r.text)

downloader = GMEDownloader()
downloader.MGP_informazioni_preliminari("StimeFabbisogno", date.today())