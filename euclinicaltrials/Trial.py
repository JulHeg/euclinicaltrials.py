from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Type
import requests
from bs4 import BeautifulSoup
from . import CTIS, Document
import pandas as pd



class Trial:
    EUCTNUMBER: str
    __soup_full_cache: BeautifulSoup
    __soup_results_cache: BeautifulSoup
    __soup_summary_cache: BeautifulSoup
    
    def __init__(self, EUCTNUMBER:str) -> None:
        self.EUCTNUMBER = EUCTNUMBER
        self.__soup_full_cache = None
        self.__soup_results_cache = None
        self.__soup_summary_cache = None

    
    def __soup_full(self):
        if self.__soup_full_cache is None:
            URL = CTIS.BASE_URI + '/view-clinical-trial?p_p_id=emactview_WAR_emactpublicportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_emactview_WAR_emactpublicportlet_number=' + self.EUCTNUMBER + '&_emactview_WAR_emactpublicportlet__facesViewIdRender=%2FWEB-INF%2Fviews%2Fview%2Ftabs%2FfullInformation.xhtml'
            page = requests.get(URL)
            self.__soup_full_cache = BeautifulSoup(page.content, "html.parser")
        return self.__soup_full_cache

    
    def __soup_results(self):
        if self.__soup_results_cache is None:
            URL = CTIS.BASE_URI + '/view-clinical-trial?p_p_id=emactview_WAR_emactpublicportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_emactview_WAR_emactpublicportlet_number=' + self.EUCTNUMBER + '&_emactview_WAR_emactpublicportlet__facesViewIdRender=%2FWEB-INF%2Fviews%2Fview%2Ftabs%2FtrialResults.xhtml'
            page = requests.get(URL)
            self.__soup_results_cache = BeautifulSoup(page.content, "html.parser")
        return self.__soup_results_cache

    
    def __soup_summary(self):
        if self.__soup_summary_cache is None:
            URL = CTIS.BASE_URI + '/view-clinical-trial?p_p_id=emactview_WAR_emactpublicportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_emactview_WAR_emactpublicportlet_number=' + self.EUCTNUMBER + '&_emactview_WAR_emactpublicportlet__facesViewIdRender=%2FWEB-INF%2Fviews%2Fview%2Ftabs%2Fsummary.xhtml'
            page = requests.get(URL)
            self.__soup_summary_cache = BeautifulSoup(page.content, "html.parser")
        return self.__soup_summary_cache
    
    def overall_trial_status_table(self) -> pd.core.frame.DataFrame:
        '''
        Returns a pandas dataframe of the overall trial status table (the big one on the Summary tab)
        '''
        trialStatusInfoDataTable = self.__soup_summary().find(id='trialStatusInfoDataTableId')
        df = pd.read_html(str(trialStatusInfoDataTable))[0]
        df.columns = df.columns.droplevel(level=0)
        return df
    
    
    def member_states_concerned(self) -> List[str]:
        return list(self.overall_trial_status_table()['Member state'])
    
    def documents_part_1(self) -> List[Type[Document]]:
        '''
        Returns a list of all documents attached trial specific information (Part I).
        '''
        attached_documents = []
        productsDetails_tab = self.__soup_full().find(id='productsDetails')
        trial_document_table = productsDetails_tab.next_sibling.next_sibling.next_sibling.next_sibling.table
        return CTIS.parse_documents_table(trial_document_table)
    
    
    def __country_accordions(self) -> List[Type[BeautifulSoup]]:
        trialStatusInfoDataTable = self.__soup_full().find(id='countrySpecificDetailsInfoAccordionId')
        separated = CTIS.separate_accordion_sections(trialStatusInfoDataTable)
        new_keys = {k.split("-")[0].strip(): v for k, v in separated.items()}
        return new_keys
    
    
    def documents_part_2(self) -> Dict[str, List[Type[Document]]]:
        '''
        Returns a dictionary of all documents attached country specific details (Part II). The key is the country name, and the value is a list of documents attached.
        '''
        country_accordion = self.__country_accordions()
        attached_documents= {}
        for country in country_accordion:
            docs = country_accordion[country].find(string='All Documents')
            table = docs.parent.find_next('table')
            attached_documents[country] = CTIS.parse_documents_table(table)
        return attached_documents
    
    
    def planned_subjects_by_country(self) -> Dict[str, List[Type[Document]]]:
        '''
        Returns a dictionary of all documents attached country specific details (Part II). The key is the country name, and the value is a list of documents attached.
        '''
        country_accordion = self.__country_accordions()
        subjects= {}
        for country in country_accordion:
            span = country_accordion[country].select('span[id$=subjectId]')[0]
            subjects[country] = int(span.contents[0])
        return subjects

    
    def total_planned_subjects(self) -> int:
        '''
        Returns the total number of planned subjects.
        '''
        return sum(self.planned_subjects_by_country().values())

    # Now for some properties that come neatly labeled
    
    def scope(self) -> str:
        trial_scope = CTIS.get_content_by_id(self.__soup_full(), "_emactview_WAR_emactpublicportlet_:mainFormID:trialScopeId")
        return trial_scope

    
    def sponsor(self) -> str:
        '''
        This only returns the sponsor name. More information is on the website, but can also be retrieved from the EMA's SPOR database. That one does have an API!
        '''
        sponsor = CTIS.get_content_by_id(self.__soup_summary(), "_emactview_WAR_emactpublicportlet_:mainFormID:trialInfoSponsorId")
        return sponsor

    
    def conditions(self) -> str:
        conditions = CTIS.get_content_by_id(self.__soup_summary(), "_emactview_WAR_emactpublicportlet_:mainFormID:trialInfoConditionsId")
        return conditions

    
    def population_type(self) -> str:
        population_type = CTIS.get_content_by_id(self.__soup_summary(), "_emactview_WAR_emactpublicportlet_:mainFormID:trialInfoVulnerablePopulationsId")
        return population_type

    
    def description(self) -> str:
        description = CTIS.get_content_by_id(self.__soup_summary(), "_emactview_WAR_emactpublicportlet_:ctPublicViewHeaderFornId:trialDescriptionId")
        return description

    
    def therapeutic_area(self) -> str:
        therapeutic_area = CTIS.get_content_by_id(self.__soup_summary(), "_emactview_WAR_emactpublicportlet_:mainFormID:trialInfoTherapeuticAreaId")
        return therapeutic_area

    
    def phase(self) -> str:
        phase = CTIS.get_content_by_id(self.__soup_summary(), "_emactview_WAR_emactpublicportlet_:mainFormID:trialInfoTrialPhaseId")
        return phase

    
    def is_low_intervention(self) -> bool:
        is_low_intervention = CTIS.get_content_by_id(self.__soup_summary(), "_emactview_WAR_emactpublicportlet_:mainFormID:trialInfoLowInterStudyLabelNoId")
        return CTIS.yes_no_to_boolean(is_low_intervention)

    
    def is_transition_trial(self) -> bool:
        is_transition_trial = CTIS.get_content_by_id(self.__soup_summary(), "_emactview_WAR_emactpublicportlet_:mainFormID:isTransitionedLabelNoId")
        return CTIS.yes_no_to_boolean(is_transition_trial)

    
    def is_medical_device(self) -> bool:
        is_medical_device = CTIS.get_content_by_id(self.__soup_summary(), "_emactview_WAR_emactpublicportlet_:mainFormID:trialInfoMedicalDeviceLabelNoId")
        return CTIS.yes_no_to_boolean(is_medical_device)

    
    def first_submitted_date(self) -> datetime.date:
        first_submitted_date = CTIS.get_content_by_id(self.__soup_summary(), "_emactview_WAR_emactpublicportlet_:mainFormID:trialInfoFirstSumbittedId")
        return CTIS.parse_CTIS_date(first_submitted_date)

    
    def last_update_date(self) -> datetime.date:
        last_update_date = CTIS.get_content_by_id(self.__soup_summary(), "_emactview_WAR_emactpublicportlet_:mainFormID:trialInfoLastUpdatedId")
        return CTIS.parse_CTIS_date(last_update_date)

    
    def link(self) -> str:
        '''
        This is a link to open the underlying webpage.
        '''
        # It's just the link to the summary page for convenience
        return CTIS.BASE_URI + '/view-clinical-trial?p_p_id=emactview_WAR_emactpublicportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_emactview_WAR_emactpublicportlet_number=' + self.EUCTNUMBER + '&_emactview_WAR_emactpublicportlet__facesViewIdRender=%2FWEB-INF%2Fviews%2Fview%2Ftabs%2Fsummary.xhtml'

    
    def full_zip_download_link(self) -> str:
        '''
        This is a link to download the full zip file. For bigger trials, this can take more than a minute.
        '''
        request_URL = CTIS.BASE_URI + '/download-clinical-trial?p_p_id=emactdownload_WAR_emactpublicportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1&p_p_col_count=1&_emactdownload_WAR_emactpublicportlet_cmd=downloadCT&_emactdownload_WAR_emactpublicportlet_number=' + self.EUCTNUMBER + '&_emactdownload_WAR_emactpublicportlet_number=2022-500137-89-00&_emactdownload_WAR_emactpublicportlet_backURL=/view-clinical-trial?p_p_id=emactview_WAR_emactpublicportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_emactview_WAR_emactpublicportlet_number=2022-500137-89-00&_emactview_WAR_emactpublicportlet__facesViewIdRender=%2FWEB-INF%2Fviews%2Fview%2Ftabs%2FfullInformation.xhtml&_emactdownload_WAR_emactpublicportlet_backURL=/view-clinical-trial?p_p_id=emactview_WAR_emactpublicportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_emactview_WAR_emactpublicportlet_number=2022-500137-89-00&_emactview_WAR_emactpublicportlet__facesViewIdRender=%2FWEB-INF%2Fviews%2Fview%2Ftabs%2FfullInformation.xhtml&_emactdownload_WAR_emactpublicportlet_downloadOptions={%22ctid%22:137,%22ctNumber%22:%222022-500137-89-00%22,%22includeSummary%22:1,%22includeFullTrial%22:1,%22includeEvents%22:0,%22includeResults%22:0,%22includeCorrectiveMeasures%22:0,%22includeInspectionRecords%22:0,%22includeDocuments%22:1,%22includedApplications%22:[]}'
        response = requests.get(request_URL)
        assert response.status_code == 200
        return response.text

    
    def is_protocol_published(self) -> bool:
        '''
        Returns True if the trial has a full protocol published, False otherwise.
        '''
        return any(doc.is_published_protocol() for doc in self.documents_part_1())