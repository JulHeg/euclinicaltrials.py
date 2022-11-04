from dataclasses import dataclass
from typing import Literal

@dataclass
class Document:
    url: str
    title: str
    filetype: Literal['',
                    'PDF',
                    'DOCX',
                    'DOC']
    documenttype: Literal['Agreement from another sponsor (for publication)',
                    'Authorisation of manufacturing and import (for publication)',
                    'Auxiliary Medicinal Product Dossier (for publication)',
                    'Compliance with Regulation (EU) 2016/679 (for publication)',
                    'Compliance with national requirements on Data Protection (for publication)',
                    'Compliance with use of Biological samples (for publication)',
                    'Content labelling of the IMPs (for publication)',
                    'Cover letter (for publication)',
                    'Data Safety Monitoring Board Charter (for publication)',
                    'Investigational Medicinal Product Dossier: Safety and Efficacy (for publication)',
                    'Investigator Brochure (for publication)',
                    'Investigator CV (for publication)',
                    'Low Intervention Justification (for publication)',
                    'Modification Description (for publication)',
                    'PIP opinion (for publication)',
                    'Proof of insurance (for publication)',
                    'Proof of payment (for publication)',
                    'Protocol (for publication)',
                    'QP GMP certification (for publication)',
                    'Recruitment arrangements (for publication)',
                    'Simplified IMPD: Safety and Efficacy (for publication)',
                    'Study design (for publication)',
                    'Subject information and informed consent form (for publication)',
                    'Suitability of the clinical trial sites facilities (for publication)',
                    'Suitability of the investigator (for publication)',
                    'Summary of Product Characteristics (SmPC) (for publication)',
                    'Summary of scientific advice (for publication)',
                    'Synopsis of the protocol (for publication)']
    
    def is_published_protocol(self) -> bool:
        '''
        Returns True if the document is a full protocol that has been published, False otherwise.
        '''
        return self.filetype == "Protocol (for publication)" and self.url is not None