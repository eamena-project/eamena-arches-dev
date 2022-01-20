"""
Automated or semi-automated functions to audit the quality of heritage resources (HR).
By convention, the recording quality of a HR is the ratio between completed and empty fields (eg. Archaeological Assessment, Condition Assessment).

"""

def hr_rec_qual(graph_layout, hr):
    """
    Evaluate the quality of recording of a single HR. Returns a dataframe with two rows:
        - the first row shows the total of completed fields in each super-category for the HR record
        - the second row shows the total of fields in each super-category
    This dataframe is used in 
    
    :param graph_layout: A dictionnary with the key as super-category, and names of categories in a list 
    :param hr: The UUID of a single HR
    
    :type graph_layout: dict
    :type hr: str
    
    :return: A dataframe
    
    :Example:
        >>> graph_layout = {'Archaeological Assessment':['Cultural Period Belief', 
                                                         'Related Geoarchaeology/Palaeolandscape',
                                                         'Overall Site Morphology Type',
                                                         'Site Feature Assignment',
                                                         'Archaeological Timespace',
                                                         'Archaeological Certainty Observation',
                                                         'Material',
                                                         'Measurements'],
                            'Condition Assessment':['Recommendation Plan',
                                                    'Condition State',
                                                    'Detailed Condition Assessments']
                            }
        >>> hr = '61897f0f-cf2a-42ad-9213-d2258d2fd8d7'
        >>> hr_recq = hr_rec_qual(graph_layout, hr)
        >>> hr_recq
        +----+------------------------------+------------------------+
        |    | Archaeological Assessment    |  Condition Assessment  |
        |----+------------------------------+------------------------|
        |  0 |                            4 |                      1 |
        |  1 |                            8 |                      3 | 
        +----+------------------------------+------------------------+

    """
    pass
    return None

def hr_rec_qual_grad(hr_recq):
    """
    Plot a radar chart (ie, spider chart) showing the recording quality of a HR.
    ex: https://knowhow.visual-paradigm.com/openapi/radar-chart/
    """
    pass
    return None
