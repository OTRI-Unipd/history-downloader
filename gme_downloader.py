import requests
from datetime import date


class GMEDownloader:
    '''
    Downloads all kind of data from https://www.mercatoelettrico.org/
    '''

    DICTIONARY = { "categories" :[
        {
            "name" : "MGP",
            "types" : [
                "StimeFabbisogno",
                "LimitiTransito",
                "PrezziConvenzionali",
                "Quantita",
                "Liquidita",
                "Transiti",
                "Fabbisogno",
                "OfferteIntegrativeGrtn"
                "Prezzi",
                "MarketCoupling"
            ]
        },
        {
            "name" : "MI1",
            "types" : [
                "LimitiTransito",
                "PrezziConvenzionali",
                "Prezzi",
                "Quantita"
            ]
        },
        {
            "name" : "MI2",
            "types" : [
                "LimitiTransito",
                "PrezziConvenzionali",
                "Prezzi",
                "Quantita"
            ]
        },
        {
            "name" : "MI3",
            "types" : [
                "LimitiTransito",
                "PrezziConvenzionali",
                "Prezzi",
                "Quantita"
            ]
        },
        {
            "name" : "MI4",
            "types" : [
                "LimitiTransito",
                "PrezziConvenzionali",
                "Prezzi",
                "Quantita"
            ]
        },
        {
            "name" : "MI5",
            "types" : [
                "LimitiTransito",
                "PrezziConvenzionali",
                "Prezzi",
                "Quantita"
            ]
        },
        {
            "name" : "MI6",
            "types" : [
                "LimitiTransito",
                "PrezziConvenzionali",
                "Prezzi",
                "Quantita"
            ]
        },
        {
            "name" : "MI7",
            "types" : [
                "LimitiTransito",
                "PrezziConvenzionali",
                "Prezzi",
                "Quantita"
            ]
        }
    ]}

    def get_MGP(self, req_type: str, day: date):
        '''
        Downloads data from MGP

        Parameters:
            req_type : str
                Could be one of the following: "StimeFabbisogno", "LimitiTransito", "PrezziConvenzionali", "Quantita", "Liquidita", "Transiti", "Fabbisogno", "OfferteIntegrativeGrtn"
                "Prezzi", "MarketCoupling"
            date : date
                Any date between 2009 circa and today, depends on the type of data.
        Raises:
            ValueError when required data could not be retrieved (wrong date or req_type)
        '''
        return self.get_data("MGP",req_type, day)

    def get_MI(self, number : int, req_type : str, day : date):
        '''
        Downloads data from MI-number (1 to 7)

        Parameters:
            req_type : str
                Must be one of the following: "LimitiTransito", "PrezziConvenzionali", "Prezzi", "Quantita"
            date : date
                Any date between 2009 circa and today, depends on the type of data.
        Raises:
            ValueError when required data could not be retrieved (wrong date or req_type)
        '''
        return self.get_data("MI{}".format(number), req_type, day)

    def get_data(self, category: str, req_type: str, day: date):
        '''
        Prepares request with necessary cookies and post data to bypass required conditions.

        Parameters:
            category : str
                Could be "MGP" or "MI1" to "MI7".
            req_type : str
                Depends on the category, could be "Prezzi" or "Quantita" or "Fabbisogno" and more.
            day : date
                Any date between 2009 circa and today, depends on category and date.
        Raises:
            ValueError when required data could not be retrieved (wrong date, category or req_type)
        '''
        session = requests.Session()
        post_data = {
            '__VIEWSTATE': '/wEPDwULLTIwNTEyNDQzNzQPZBYCZg9kFgICAw9kFgJmD2QWBAIMD2QWAmYPZBYCZg9kFgICCQ8PZBYCHgpvbmtleXByZXNzBRxyZXR1cm4gaW52aWFQV0QodGhpcyxldmVudCk7ZAIVD2QWAgIBDw8WAh4NT25DbGllbnRDbGljawUmamF2YXNjcmlwdDp3aW5kb3cub3BlbignP3N0YW1wYT10cnVlJylkZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WBQUMY3RsMDAkSW1hZ2UxBRJjdGwwMCRJbWFnZUJ1dHRvbjEFIGN0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkc3RhbXBhBSRjdGwwMCRDb250ZW50UGxhY2VIb2xkZXIxJENCQWNjZXR0bzEFJGN0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkQ0JBY2NldHRvMvV5e94ExnpHUcybAr1bPdOOHxYDHpQG7fgAyUlbfpUy',
            # '__VIEWSTATEGENERATOR' : 'BD5243C0',
            # '__PREVIOUSPAGE' : 'cZ9asoMdEhcsdMTrKLddyuDgUqrpgV44mkItwJfPMdC5pTBV2YSxs8G-heXd_cSe0LgJT2dUbmEwn5EAxW2CKqwwsuEEvSwkj_TDS8XqtiFWyG906u2-XjhdXsqvVULm0',
            '__EVENTVALIDATION': '/wEdABN5QfIZ0Z09c70NXWGRJiGpcS/s8I39AyxLz4tn+AkBiEW+okpiqwYG+B4aTa9o+s43drX32rKpFiwqoHxZnWEOD4zZrxX92uOlyIx1SyGTQmV8haT0EfVomfKCKov4HgnZl/Xwcz7QqxVnz+OmFVuWzNBM98trssXld5dD73vgQX4H/0z/058uP3NmytG8PXozrkfQ7SmiPGgdsZPdEEV8g/gu4+zhSeI0ttI2ADLh/wU7Nz/6FKjnm2sSszw4FMr8VEDvc+zuMc1oKpjHdCosjDu35o5CUn6umW4JNpE1p4raaQaFnXKaLuO1sKRm4e9ZUwtJIYRkZxZmb4HmgHR6ltkgVwReXnm+EHOYvXjKP0Sd1PBpsO2hEyKj10xH8juA+rwVNruExpEBEKBupGsoUlq8qqob2Hte6ABdfJHWar0vp/uG8tjo+1et9YAPjLg=',
            # 'ctl00$tbTitolo': 'cerca nel sito',
            # 'ctl00$UserName': '',
            # 'ctl00$Password': '',
            'ctl00$ContentPlaceHolder1$CBAccetto1': 'on',
            'ctl00$ContentPlaceHolder1$CBAccetto2': 'on',
            'ctl00$ContentPlaceHolder1$Button1': 'Accetto',
        }
        formatted_date = day.strftime("%Y%m%d")
        url = "https://www.mercatoelettrico.org/It/Tools/Accessodati.aspx?ReturnUrl=/It/WebServerDataStore/{}_{}/{}{}{}.xml".format(
            category, req_type, formatted_date, category, req_type)
        response = session.post(url, data=post_data)
        if(response.status_code == 200):
            return response.text
        raise ValueError("Required value could not be found ({}, {}, {})".format(category, req_type, day))


downloader = GMEDownloader()
print(downloader.get_MGP("StimeFabbisogno", date(2020,4,17)))
