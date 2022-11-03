import requests
from pytz import timezone
from bs4 import BeautifulSoup, element
import re
from datetime import datetime
from .Document import Document

BASE_URI = "https://euclinicaltrials.eu"

def __get_all_trials_search_content(view_state:str, jsessionid:str, page:int = 1):
    # This code was generated with [harreplay](https://github.com/gtzampanakis/harreplay), worked really neatly! The request is changed with the page number, the ViewState, and the JSESSIONID from the first page.
    response = requests.post(
        BASE_URI + '/search-for-clinical-trials?p_p_id=emactsearch_WAR_emactpublicportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1&p_p_col_count=1&_emactsearch_WAR_emactpublicportlet__jsfBridgeAjax=true&_emactsearch_WAR_emactpublicportlet__facesViewIdResource=%2FWEB-INF%2Fviews%2Fsearch%2Ftabs%2FsearchResults.xhtml',

        headers={'Host': 'euclinicaltrials.eu', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0', 'Accept': '*/*', 'Accept-Language': 'en,de;q=0.7,en-US;q=0.3', 'Accept-Encoding': 'gzip, deflate, br', 'Referer': 'https://euclinicaltrials.eu/search-for-clinical-trials?p_p_id=emactsearch_WAR_emactpublicportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_emactsearch_WAR_emactpublicportlet__facesViewIdRender=%2FWEB-INF%2Fviews%2Fsearch%2Ftabs%2FsearchResults.xhtml', 'Faces-Request': 'partial/ajax', 'Content-type': 'application/x-www-form-urlencoded;charset=UTF-8', 'Origin': 'https://euclinicaltrials.eu', 'Connection': 'keep-alive', 'Cookie': 'COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=en_GB; accepted_cookie=true; JSESSIONID=' + jsessionid, 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache'},

        data='_emactsearch_WAR_emactpublicportlet_%3AmainFormID=_emactsearch_WAR_emactpublicportlet_%3AmainFormID&javax.faces.encodedURL=https%3A%2F%2Feuclinicaltrials.eu%2Fsearch-for-clinical-trials%3Fp_p_id%3Demactsearch_WAR_emactpublicportlet%26p_p_lifecycle%3D2%26p_p_state%3Dnormal%26p_p_mode%3Dview%26p_p_cacheability%3DcacheLevelPage%26p_p_col_id%3Dcolumn-1%26p_p_col_count%3D1%26_emactsearch_WAR_emactpublicportlet__jsfBridgeAjax%3Dtrue%26_emactsearch_WAR_emactpublicportlet__facesViewIdResource%3D%252FWEB-INF%252Fviews%252Fsearch%252Ftabs%252FsearchResults.xhtml&_emactsearch_WAR_emactpublicportlet_%3AmainFormID%3Aj_idt34=decisionDate&_emactsearch_WAR_emactpublicportlet_%3AmainFormID%3Aj_idt37=DESC&_emactsearch_WAR_emactpublicportlet_%3AmainFormID%3AtrialSearchResultsDataTableId_selectedRowIndexes=&_emactsearch_WAR_emactpublicportlet_%3AmainFormID%3AsearchResultRowsPerPageId=20&javax.faces.ViewState=' + view_state + '&javax.faces.source=_emactsearch_WAR_emactpublicportlet_%3AmainFormID%3AtrialSearchResultsPaginatorId&javax.faces.partial.event=click&javax.faces.partial.execute=_emactsearch_WAR_emactpublicportlet_%3AmainFormID%3AtrialSearchResultsPaginatorId%20_emactsearch_WAR_emactpublicportlet_%3AmainFormID%3AtrialSearchResultsPaginatorId&javax.faces.partial.render=_emactsearch_WAR_emactpublicportlet_%3AmainFormID%3AtrialSearchResultsPaginatorId%20_emactsearch_WAR_emactpublicportlet_%3AmainFormID%3AtrialSearchResultsDataTableId&_emactsearch_WAR_emactpublicportlet_%3AmainFormID%3AtrialSearchResultsPaginatorId_paginatorAction=' + str(page) + '&javax.faces.behavior.event=action&javax.faces.partial.ajax=true',
    )
    return response.content.decode('utf-8')

def is_unavailable() -> bool:
    '''
    Checks if the CTIS reports being current unavailable, for example for maintenance.
    '''
    response = requests.get(BASE_URI + "/website-outages-and-system-releases")
    assert response.status_code == 200
    response = response.text
    return "CTIS public portal is temporarily unavailable" in response

def is_maintenace_window(time: datetime = datetime.now()) -> bool:
    '''
    Checks whether time is during the regularly scheduled maintenance windows. if no argument time is given checks the current time.

    The windows (as per https://euclinicaltrials.eu/website-outages-and-system-releases) are:

    Each Tuesday and Thursday: 18:00 to 21:00 Amsterdam time
    Each first Saturday of the month, from 10:00 to 14:00 Amsterdam time
    '''
    amsterdam_timezone = timezone("Europe/Amsterdam")
    time = time.astimezone(amsterdam_timezone)
    if time.weekday() == 1 or time.weekday() == 3:
        # Tuesday or Thursday
        if 18 <= time.hour < 21:
            return True
    elif time.weekday() == 6 and time.day <= 7:
        # Saturday
        if 10 <= time.hour < 14:
            return True
    return False

def get_all_trial_numbers() -> list[str]:
    '''
    This method returns the ids of all trials in the database.
    '''
    # Open the search page to get the number of trials and the ViewState and JSESSIONID we need to access them
    URL = BASE_URI + '/search-for-clinical-trials?p_p_id=emactsearch_WAR_emactpublicportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_emactsearch_WAR_emactpublicportlet__facesViewIdRender=%2FWEB-INF%2Fviews%2Fsearch%2Ftabs%2FsearchResults.xhtml'
    response = requests.get(URL)
    page1 = response.content.decode('utf-8')
    results_count_matches = re.findall('>\d* results found</span>', page1)
    assert len(results_count_matches) == 1
    results_count = int(re.sub('\D', '', results_count_matches[0]))
    soup_search = BeautifulSoup(page1, "html.parser")
    view_state = soup_search.find(id='_emactsearch_WAR_emactpublicportlet_:javax.faces.ViewState:0').attrs['value']
    request_headers = response.headers['Set-Cookie'].split(';')
    for header in request_headers:
        if 'JSESSIONID' in header:
            jsessionid = header.split('=')[1]
            break

    numbers = set()
    for i in range(1,(results_count-1)//20+2):
        page = __get_all_trials_search_content(view_state=view_state,jsessionid=jsessionid, page=i)
        new_numbers = set(re.findall('2\d\d\d-\d\d\d\d\d\d-\d\d-\d\d',page))
        numbers |= new_numbers
    return list(numbers)

def get_content_by_id(soup: type[BeautifulSoup], id: str) -> str:
    res1 = soup.find(id=id).getText().strip()
    return res1

def yes_no_to_boolean(x: str) -> bool:
    if x == "Yes":
        return True
    elif x == "No":
        return False
    else:
        raise ValueError("Unexpected value: " + x)

def parse_CTIS_date(x: str) -> type[datetime.date]:
    '''
    Dates on CTIS website have the form dd/mm/yyyy
    '''
    return datetime.strptime(x, '%d/%m/%Y').date()

def parse_documents_table(table: type[BeautifulSoup]):
    attached_documents = []
    try:
        trial_document_table_body = table.find(name="tbody")
        for row in trial_document_table_body.children:
            children = list(row.children)
            assert len(children) == 3
            if children[0].a is not None:
                document_url = children[0].a['href']
                document_name = children[0].a.span.getText().strip()
            else:
                document_url = None
                document_name = children[0].getText().strip()
            document_file_type = children[1].getText().strip()
            document_document_type = children[2].getText().strip()
            document = Document(url = document_url, title = document_name, filetype = document_file_type, documenttype = document_document_type)
            attached_documents.append(document)
    except Exception as e:
        attached_documents = []
        #TODO: Currently this catches both exceptions and when no documents are attached. But it should only catch the latter to fail fast.
    return attached_documents

def separate_accordion_sections(soup: type[BeautifulSoup]) -> dict[str, type[BeautifulSoup]]:
    '''
    Separate accordion sections as a dictionary of section name and section content
    '''
    accordion_sections = {}
    for heading in soup.children:
        if heading.name != "h3":
            continue
        section_name = heading.getText().strip()
        section_content = heading.nextSibling.nextSibling
        accordion_sections[section_name] = section_content
    return accordion_sections