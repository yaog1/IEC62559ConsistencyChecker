'''
Created on 14.11.2018
Contains all Classes for the representation of a Use Case described with the template of the IEC 62559 Methodology
@author: yasino
'''


class UcMetaData(object):

    """A metadata class for the UcSentence objects. Contains information about the exact position of the sentence in the Use Case template, the [UcSentence], the validity against the consistency rules and possible result messages
    """
    
    __section = ''
    __sequence= 0
    __element_number = 0
    __sentence_number = 0
    __validity = True
    __result_message = []
    __type = ''

    def __init__(self, section = '0.0', sequence = 0, element_number = 0, attribut_type = '', sentence_nr= 0):
        """Constructor - the sequence, element_number and sentence_number are optional, default values are 0
        
        Args:
            section (str): Use Case Template section number e.g. 4.1 
            sequence (int, optional): Sequence number, usefull if there are more than one tables of the same kind in the section (for e.g. in section 4.2)
            element_number (int, optional): The element number (row) in the section table
            attribut_[UcSentence] (str): The attribute [UcSentence] (collumn header) in the section table
            sentence_nr (int, optional): The sentence number e.g. 2nd sentence in the complete description
        """
        self.__section = section
        self.__sequence = sequence
        self.__element_number = element_number
        self.__sentence_number = sentence_nr
        self.__type = attribut_type
        self.__validity = True
        self.__result_message = []

    def get_section(self):
        """Get the template section number in which the specific UcSentence can be found
        
        Returns:
            str: UseCase Template section number (e.g. '4.1')
        """
        return self.__section


    def get_sequence(self):
        """Get the sequence number in which the UcSentence is nested
        
        Returns:
            int: Sequence number (index)
        """
        return self.__sequence


    def get_sentence_number(self):
        """Get the index of the UcSentence e.g. 0 if it is the first sentence of a text
        
        Returns:
            int: Sentence number (index)
        """
        return self.__sentence_number

    def get_element_number (self):
        """Get the row number in which this element in the section table can be found
        
        Returns:
            int: Element number (index)
        """
        return  self.__element_number

    def get_validity(self):
        """Get the validity state of the UcSentence.
        
        Returns:
            boolean: True if no violation of consistency rules happened; False if at least 1 violation of consistency rules exists
        """
        return self.__validity


    def get_result_message(self):
        """Get the result messages which contain the violated consistency rules
        
        Returns:
            [str]: empty OR result message if violation of consistency rules happened
        """
        return self.__result_message


    def get_type(self):
        """Get the type of the attribute in the Use Case template (collumn header) which is represented by the UcSentence 
        
        Returns:
            str: collumn header name in the section (get_section)
        """
        return self.__type

    def set_section(self, value):
        """Set the template section number in which the specific UcSentence can be found
        
        Args:
            value (str): section number (e.g '4.1')
        """
        self.__section = value


    def set_sequence(self, value):
        """Set the sequence number in which the UcSentence is nested
        
        Args:
            value (int): sequence number (index)
        """
        self.__sequence = value


    def set_sentence_number(self, value):
        """Set the index of the UcSentence e.g. 0 if it is the first sentence of a text
        
        Args:
            value (int): sentence number (index)
        """
        self.__sentence_number = value

    def set_element_number(self, value):
        """Set the row number in which this element in the section table can be found
        
        Args:
            value (int): element number (index)
        """
        self.__element_number = value

    def set_validity(self, value):
        """Set the validity state of the UcSentence.
        
        Args:
            value (boolean): True if no violation of consistency rules happened; False if at least 1 violation of consistency rules exists
        """
        self.__validity = value


    def set_result_message(self, value):
        """Set the result messages which contain the violated consistency rules
        
        Args:
            value ([str]): empty OR result message if violation of consistency rules happened
        """
        self.__result_message = value


    def set_type(self, value):
        """Get the [UcSentence] of the attribute in the Usecase template (collumn header) which is represented by the UcSentence
        
        Args:
            value (str): collumn header name
        """
        self.__type = value


class UcSentence(object):

    """Class representing a sentence in a Use Case, contains metadata about the position, type and state
    """
    
    __content = ''
    __meta_data = UcMetaData()

    def __init__(self, content = '', meta_data = UcMetaData()):
        """Constructor
        
        Args:
            content (str, optional): sentence content
            meta_data (UcMetaData): metadata object
        """
        self.__content = content
        self.__meta_data = meta_data

    def get_content(self):
        """Get the sentence content
        
        Returns:
            str: sentence content
        """
        return self.__content


    def get_meta_data(self):
        """Get the meta_data of the sentence
        
        Returns:
            UcMetaData: metadata object
        """
        return self.__meta_data



class NameOfUC_1_1(object):
    '''Class representing the Use Case section 1.1 - Name of Use Case 
    '''
    __id = []
    __domains = []
    __name = []

    def __init__(self, id, domains, name):
        """Summary
        
        Args:
            id ([UcSentence]): Use Case id
            domains ([UcSentence]): Domain of the Use Case
            name ([UcSentence]): Name of the Use Case
        """
        self.__id = id
        self.__domains = domains
        self.__name = name

    def get_id(self):
        """Get the Use Case Id
        
        Returns:
            [UcSentence]: Use Case ID
        """
        return self.__id


    def get_domains(self):
        """Get the Domains of the Use Case
        
        Returns:
            [UcSentence]: Use Case Domains
        """
        return self.__domains


    def get_name(self):
        """Get the name of the Use Case
        
        Returns:
            [UcSentence]: Name of the Use Case
        """
        return self.__name
    
    def get_all_attributes(self):
        """Get all attributes of this object in a single List containing the UcSentences
        
        Returns:
            [UcSentence]: All attributes of this object
        """
        return self.__id + self.__domains + self.__name

class VersionManagement_1_2(object):

    """Class representing the Use Case section 1.2 - Version Management
    """
    
    __version_number=[]
    __date = []
    __authors =[]
    __changes =[]
    __status = []
    
    def __init__(self, version_number, date, authors, changes, status):
        """Constructor
        
        Args:
            version_number ([UcSentence]): version number
            date ([UcSentence]): save date
            authors ([UcSentence]): Authors involved in this version
            changes ([UcSentence]): Changes made in this version
            status ([UcSentence]): Status e.g. Draft, Final
        """
        self.__version_number = version_number
        self.__date = date
        self.__authors = authors
        self.__changes = changes
        self.__status = status

    def get_version_number(self):
        """Get the version number
        
        Returns:
            [UcSentence]: version number
        """
        return self.__version_number


    def get_date(self):
        """Get the save date of this version
        
        Returns:
            [UcSentence]: date
        """
        return self.__date


    def get_authors(self):
        """Get the involved authors
        
        Returns:
            [UcSentence]: author names
        """
        return self.__authors


    def get_changes(self):
        """Get a description of the made changes
        
        Returns:
            [UcSentence]: change protocol
        """
        return self.__changes


    def get_status(self):
        """Get the status of this version
        
        Returns:
            [UcSentence]: status e.g. Draft, Final
        """
        return self.__status
    
    def get_all_attributes(self):
        """Get all attributes of this object in a single List containing the UcSentences
        
        Returns:
            [UcSentence]: All attributes of this object
        """
        return self.__version_number + self.__date + self.__authors + self.__changes + self.__status
    
class Objective_1_3(object):

    """Class representing a Objective in the Use Case section 1.3 - Scope and Objectives of Use Case
    """
    
    __name = []
    __description = []

    def __init__(self, name, desc):
        """Constructor
        
        Args:
            name ([UcSentence]): name of the Objective
            desc ([UcSentence]): description of the Objective
        """
        self.__name = name
        self.__description = desc

    def get_name(self):
        """Get the name of the Objective
        
        Returns:
            [UcSentence]: name
        """
        return self.__name


    def get_description(self):
        """Get the description of the Objective
        
        Returns:
            [UcSentence]: description
        """
        return self.__description
    
    def get_all_attributes(self):
        """Get all attributes of this object in a single List containing the UcSentences
        
        Returns:
            [UcSentence]: All attributes of this object
        """
        return self.__name + self.__description

class Scope_1_3(object):

    """Class representing the Use Case section 1.3 - Scope and Objectives of Use Case
    """
    
    __scope = []
    __objectives = []

    def __init__(self, scope, objectives):
        """Summary
        
        Args:
            scope ([UcSentence]): Scope description
            objectives ([Objective_1_3]): Objective objects
        """
        self.__scope = scope
        self.__objectives = objectives

    def get_scope(self):
        """Get the scope description of the Use Case
        
        Returns:
            [UcSentence]: scope of the use case
        """
        return self.__scope


    def get_objectives(self):
        """Get a list of Objectives of the Use Case
        
        Returns:
            [Objective_1_3]: list of Objective objects
        """
        return self.__objectives
    
    def get_all_attributes(self):
        """Get all attributes of this object in a single List containing the UcSentences
        
        Returns:
            [UcSentence]: All attributes of this object
        """
        return self.__scope

class Narrative_1_4(object):

    """Class representing the Use Case section 1.4 - Narrative of Use Case
    """
    
    __short_description = []
    __complete_description = []

    def __init__(self, short_desc, complete_desc):
        """Constructor
        
        Args:
            short_desc ([UcSentence]): Short Description of the Use Case
            complete_desc ([UcSentence]): Complete Description of the Use Case
        """
        self.__short_description = short_desc
        self.__complete_description = complete_desc

    def get_short_description(self):
        """Get the Short Description of the Use Case
        
        Returns:
            [UcSentence]: short description
        """
        return self.__short_description


    def get_complete_description(self):
        """Get the Complete Description of the Use Case
        
        Returns:
            [UcSentence]: complete description
        """
        return self.__complete_description
    
    def get_all_attributes(self):
        """Get all attributes of this object in a single List containing the UcSentences
        
        Returns:
            [UcSentence]: All attributes of this object
        """
        return self.__short_description + self.__complete_description


class Kpi_1_5(object):

    """Class representing a KPI of the Use Case section 1.5 - Key Performance Indicators (KPI)
    """
    
    __id = []
    __name = []
    __description = []
    __mentioned_objective = []


    def __init__(self, id = [], name = [], desc = [], objective = []):
        """Constructor
        
        Args:
            id ([UcSentence]): ID of the KPI
            name ([UcSentence]): Name of the KPI
            desc ([UcSentence]): Description of the KPI
            objective ([UcSentence]): Objective name mentioned in the KPI
        """
        self.__id = id
        self.__name = name
        self.__description = desc
        self.__mentioned_objective = objective

    def get_id(self):
        """Get the ID of the KPI
        
        Returns:
            [UcSentence]: ID of the KPI
        """
        return self.__id


    def get_name(self):
        """Get the Name of the KPI
        
        Returns:
            [UcSentence]: Name of the KPI
        """
        return self.__name


    def get_description(self):
        """Get the Description of the KPI
        
        Returns:
            [UcSentence]: Description of the KPI
        """
        return self.__description


    def get_mentioned_objective(self):
        """Get the Objective name mentioned in the KPI
        
        Returns:
            [UcSentence]: Objective name mentioned in the KPI
        """
        return self.__mentioned_objective

    def get_all_attributes(self):
        """Get all attributes of this object in a single List containing the UcSentences
        
        Returns:
            [UcSentence]: All attributes of this object
        """
        return self.__id + self.__name + self.__description + self.__mentioned_objective
#1.6
class UseCaseConditions_1_6(object):

    """Class representing a Condition contained in the Use Case section 1.6 - Use Case Conditions
    """
    
    __assumptions = []
    __prerequisites = []

    def __init__(self, assumptions, prerequisites):
        """Summary
        
        Args:
            assumptions ([UcSentence]): Assumption of the condition
            prerequisites ([UcSentence]): Prerequisites of the condition
        """
        self.__assumptions = assumptions
        self.__prerequisites = prerequisites

    def get_assumptions(self):
        """Get the Assumption of the condition
        
        Returns:
            [UcSentence]: Assumption of the condition
        """
        return self.__assumptions


    def get_prerequisites(self):
        """Get the Prerequisites of the condition
        
        Returns:
            [UcSentence]: Prerequisites of the condition
        """
        return self.__prerequisites
    
    def get_all_attributes(self):
        """Get all attributes of this object in a single List containing the UcSentences
        
        Returns:
            [UcSentence]: All attributes of this object
        """
        return self.__assumptions + self.__prerequisites

#1.7

class FurtherInformation_1_7 (object):

    """Class representing the Use Case section 1.7 - Further Information to the Use Case for Classiﬁcation/Mapping
    """
    
    __relation_to_other_uc = []
    __level_of_depth = []
    __prioritisation = []
    __generic_regional_national_relation = []
    __nature = []
    __further_keywords = []

    def __init__(self, relation_to_other_uc, level_of_depth, prioritisation, generic_regional_national_relation, nature, further_keywords):
        """Constructor
        
        Args:
            relation_to_other_uc ([UcSentence]): Relation to ohter Use Cases
            level_of_depth ([UcSentence]): Level of Depth of the Use Case
            prioritisation ([UcSentence]): Prioritisation of the Use Case
            generic_regional_national_relation ([UcSentence]): Generic of the Use Case
            nature ([UcSentence]): Nature of the Use Case
            further_keywords ([UcSentence]): Further Keywords describing the Use Case
        """
        self.__relation_to_other_uc = relation_to_other_uc
        self.__level_of_depth = level_of_depth
        self.__prioritisation = prioritisation
        self.__generic_regional_national_relation = generic_regional_national_relation
        self.__nature = nature
        self.__further_keywords = further_keywords

    def get_relation_to_other_uc(self):
        """Get the Relation to ohter Use Cases
        
        Returns:
            [UcSentence]: Relation to ohter Use Cases
        """
        return self.__relation_to_other_uc


    def get_level_of_depth(self):
        """Get the Level of Depth of the Use Case
        
        Returns:
            [UcSentence]: Level of Depth of the Use Case
        """
        return self.__level_of_depth


    def get_prioritisation(self):
        """Get the Prioritisation of the Use Case
        
        Returns:
            [UcSentence]: Prioritisation of the Use Case
        """
        return self.__prioritisation


    def get_generic_regional_national_relation(self):
        """Get the Generic of the Use Case
        
        Returns:
            [UcSentence]: Generic of the Use Case
        """
        return self.__generic_regional_national_relation


    def get_nature(self):
        """Get the Nature of the Use Case
        
        Returns:
            [UcSentence]: Nature of the Use Case
        """
        return self.__nature


    def get_further_keywords(self):
        """Get Further Keywords describing the Use Case
        
        Returns:
            [UcSentence]: Further Keywords describing the Use Case
        """
        return self.__further_keywords
    
    def get_all_attributes(self):
        """Get all attributes of this object in a single List containing the UcSentences
        
        Returns:
            [UcSentence]: All attributes of this object
        """
        return self.__relation_to_other_uc + self.__level_of_depth + self.__prioritisation + self.__generic_regional_national_relation + self.__nature + self.__further_keywords

# 1.8
class GeneralRemark_1_8(object):

    """Class representing a General Remark of the Use Case section 1.8 - General Remarks
    """
    
    __content = []

    def __init__(self, content = []):
        """Constructor
        
        Args:
            content ([UcSentence]): Content of the General Remark
        """
        self.__content = content

    def get_content(self):
        """Get the Content of the General Remark
        
        Returns:
            [UcSentence]: Content of the General Remark
        """
        return self.__content

    def get_all_attributes(self):
        """Get all attributes of this object in a single List containing the UcSentences
        
        Returns:
            [UcSentence]: All attributes of this object
        """
        return self.__content
#3.1

class Actor_3_1 (object):

    """Class representing a Actor of the Use Case section 3.1 - Actors
    """
    
    __actor_name =[]
    __actor_type = []
    __actor_description = []
    __further_info = []

    def __init__(self, actor_name, actor_type, actor_description, further_info):
        """Constructor
        
        Args:
            actor_name ([UcSentence]): Actor name
            actor_type ([UcSentence]): Actor type
            actor_description ([UcSentence]): Description of the actor
            further_info ([UcSentence]): Further information about the actor
        """
        self.__actor_name = actor_name
        self.__actor_type = actor_type
        self.__actor_description = actor_description
        self.__further_info = further_info

    def get_name(self):
        """Get the actor name
        
        Returns:
            [UcSentence]: Actor name
        """
        return self.__actor_name


    def get_type(self):
        """Get the actor type
        
        Returns:
            [UcSentence]: Actor type
        """
        return self.__actor_type


    def get_description(self):
        """Get the description of the actor
        
        Returns:
            [UcSentence]: Description pf the actor
        """
        return self.__actor_description


    def get_further_info(self):
        """Get further information about the actor
        
        Returns:
            [UcSentence]: Further information about the actor
        """
        return self.__further_info
    
    def get_all_attributes(self):
        """Get all attributes of this object in a single List containing the UcSentences
        
        Returns:
            [UcSentence]: All attributes of this object
        """
        return self.__actor_name + self.__actor_type + self.__actor_description + self.__further_info

# 3.1
class ActorGrouping_3_1 (object):

    """Class representing a Actor Grouping of the Use Case section 3.1 - Actors
    """
    
    __name = []
    __description = []
    __actors_objects = []

    def __init__(self, grouping_name, group_description, actors_objects):
        """Summary
        
        Args:
            grouping_name ([UcSentence]): Name of the Actor Grouping
            group_description ([UcSentence]): Description of the Actor Grouping
            actors_objects ([Actor_3_1]): Contained Actors of the Actor Grouping
        """
        self.__name = grouping_name
        self.__description = group_description
        self.__actors_objects = actors_objects

    def get_name(self):
        """Get the name of the Actor Grouping
        
        Returns:
            [UcSentence]: Name of the Actor Grouping
        """
        return self.__name


    def get_description(self):
        """Get the description of the Actor Grouping
        
        Returns:
            [UcSentence]: Description of the Actor Grouping
        """
        return self.__description


    def get_actors_objects(self):
        """Get the actor classified into this Actor Grouping
        
        Returns:
            [Actor_3_1]: Contained Actors of the Actor Grouping
        """
        return self.__actors_objects
    
    def get_all_attributes(self):
        """Get all attributes of this object in a single List containing the UcSentences
        
        Returns:
            [UcSentence]: All attributes of this object
        """
        return self.__name + self.__description

#3.2

class References_3_2(object):

    """Class representing a Reference of the Use Case section 3.2 - References
    """
    
    __name = []
    __type_x= []
    __reference = []
    __status = []
    __impact = []
    __origin = []
    __link = []

    def __init__(self, name, type_x, reference, status, impact, origin, link):
        """Constructor
        
        Args:
            name ([UcSentence]): Name of the Reference
            type_x ([UcSentence]): Type of the Reference
            reference ([UcSentence]): Reference
            status ([UcSentence]): Status
            impact ([UcSentence]): Impact
            origin ([UcSentence]): Origin
            link ([UcSentence]): Link
        """
        self.__name = name
        self.__type_x = type_x
        self.__reference = reference
        self.__status = status
        self.__impact = impact
        self.__origin = origin
        self.__link = link

    def get_name(self):
        """Get the name of the Reference
        
        Returns:
            [UcSentence]: Name of the Reference
        """
        return self.__name


    def get_type_x(self):
        """Get the type of the Reference
        
        Returns:
            [UcSentence]: Type of the Reference
        """
        return self.__type


    def get_reference(self):
        """Get the reference
        
        Returns:
            [UcSentence]: reference
        """
        return self.__reference


    def get_status(self):
        """Get the status
        
        Returns:
            [UcSentence]: Status
        """
        return self.__status


    def get_impact(self):
        """Get the impact
        
        Returns:
            [UcSentence]: Impact
        """
        return self.__impact


    def get_origin(self):
        """Get the origin
        
        Returns:
            [UcSentence]: Origin
        """
        return self.__origin


    def get_link(self):
        """Get the link to the reference
        
        Returns:
            [UcSentence]: Link
        """
        return self.__link
    
    def get_all_attributes(self):
        """Get all attributes of this object in a single List containing the UcSentences
        
        Returns:
            [UcSentence]: All attributes of this object
        """
        return self.__name +  self.__type_x +  self.__reference +  self.__status +  self.__impact +  self.__origin +  self.__link


#4.1
class Scenario_4_1(object):

    """Class representing a Scenario in the Use Case section 4.1 - Overview of Scenarios
    """
    
    __id= []
    __name = []
    __description = []
    __primary_actor = []
    __triggering_event = []
    __precondition = []
    __postcondition = []
    __steps = []

    def __init__(self, id, name, description, primary_actor, triggering_event, precondition, postcondition, steps = []):
        """Summary
        
        Args:
            id ([UcSentence]): Scenario ID
            name ([UcSentence]): Scenario name
            description ([UcSentence]): Description of the Scenario
            primary_actor ([UcSentence]): Primary Actor of the Scenario
            triggering_event ([UcSentence]): Triggering Event of the Scenario
            precondition ([UcSentence]): Precondition for the Scenario
            postcondition ([UcSentence]): Postcondition for the Scenario
            steps ([Steps_4_2], optional): Steps specifieng the 
        """
        self.__id = id
        self.__name = name
        self.__description = description
        self.__primary_actor = primary_actor
        self.__triggering_event = triggering_event
        self.__precondition = precondition
        self.__postcondition = postcondition
        self.__steps = steps

    def get_id(self):
        """Get the Scenario ID
        
        Returns:
            [UcSentence]: Scenario ID
        """
        return self.__id


    def get_name(self):
        """Get the name of the Scenario
        
        Returns:
            [UcSentence]: Scenario name
        """
        return self.__name


    def get_description(self):
        """Get the description of the Scenario
        
        Returns:
            [UcSentence]: Scenario Description
        """
        return self.__description


    def get_primary_actor(self):
        """Get the Primary Actor of the Scenario
        
        Returns:
            [UcSentence]: Primary Actor
        """
        return self.__primary_actor


    def get_triggering_event(self):
        """Get the Triggering Event of the Scenario
        
        Returns:
            [UcSentence]: Triggering Event
        """
        return self.__triggering_event


    def get_precondition(self):
        """Get the Precondition
        
        Returns:
            [UcSentence]: Precondition
        """
        return self.__precondition


    def get_postcondition(self):
        """Get the Postcondition
        
        Returns:
            [UcSentence]: Postcondition
        """
        return self.__postcondition


    def get_steps(self):
        """Get the Steps of the Scenario
        
        Returns:
            [UcSentence]: Scenario Steps
        """
        return self.__steps
    
    def get_all_attributes(self):
        """Get all attributes of this object in a single List containing the UcSentences
        
        Returns:
            [UcSentence]: All attributes of this object
        """
        return self.__id + self.__name + self.__description + self.__primary_actor + self.__triggering_event + self.__precondition + self.__postcondition


# 4.2
class Steps_4_2(object):

    """Class representing a Step of a Scenario in the Use Case section 4.2 - Steps – Scenarios
    """
    
    __number = []
    __event=[]
    __process_name = []
    __process_description = []
    __service = []
    __information_producer = []
    __information_receiver = []
    __inf_exchanged_id = []
    __requirements_ids = []

    def __init__(self, number, event, process_name, process_description, service, information_producer, information_receiver, inf_exchanged_id, requirements_ids):
        """Summary
        
        Args:
            number ([UcSentence]): Number of the Step
            event ([UcSentence]): Event of the Step
            process_name ([UcSentence]): Process name
            process_description ([UcSentence]): Description of the process
            service ([UcSentence]): Service of the Step
            information_producer ([UcSentence]): Information Producer of the exchanged Information Objects
            information_receiver ([UcSentence]): Information Receiver of the exchanged Infromation Objects
            inf_exchanged_id ([UcSentence]): IDs of exchanged Information Objects 
            requirements_ids ([UcSentence]): Requirements Category ID of the Requirements used in this Step
        """
        self.__number = number
        self.__event = event
        self.__process_name = process_name
        self.__process_description = process_description
        self.__service = service
        self.__information_producer = information_producer
        self.__information_receiver = information_receiver
        self.__inf_exchanged_id = inf_exchanged_id
        self.__requirements_ids = requirements_ids

    def get_number(self):
        """Number of the Step
        
        Returns:
            [UcSentence]: Step number
        """
        return self.__number


    def get_event(self):
        """Event of the Step
        
        Returns:
            [UcSentence]: Step Event
        """
        return self.__event


    def get_process_name(self):
        """Name of the Step process
        
        Returns:
            [UcSentence]: Step process name
        """
        return self.__process_name


    def get_process_description(self):
        """Description of the process Step
        
        Returns:
            [UcSentence]: Step process description
        """
        return self.__process_description


    def get_service(self):
        """Get the Step Service
        
        Returns:
            [UcSentence]: Step service
        """
        return self.__service


    def get_information_producer(self):
        """Get the Information Producer of the exchanged Information Objects
        
        Returns:
            [UcSentence]: Information Producer of the exchanged Information Objects
        """
        return self.__information_producer


    def get_information_receiver(self):
        """Get the Information Receiver of the exchanged Infromation Objects
        
        Returns:
            [UcSentence]: Information Receiver of the exchanged Infromation Objects
        """
        return self.__information_receiver


    def get_inf_exchanged_id(self):
        """Get the IDs of exchanged Information Objects
        
        Returns:
            [UcSentence]: IDs of exchanged Information Objects
        """
        return self.__inf_exchanged_id


    def get_requirements_ids(self):
        """Get the Requirements Category ID of the Requirements used in this Step
        
        Returns:
            [UcSentence]: Requirements Category ID of the Requirements used in this Step
        """
        return self.__requirements_ids
    
    def get_all_attributes(self):
        """Get all attributes of this object in a single List containing the UcSentences
        
        Returns:
            [UcSentence]: All attributes of this object
        """
        return self.__number + self.__event + self.__process_name + self.__process_description + self.__service + self.__information_producer + self.__information_receiver + self.__inf_exchanged_id + self.__requirements_ids


#5

class InformationExchanged_5(object):

    """Class representing a Information Object of the Use Case section 5 - Information Exchanged
    """
    
    __id = []
    __name = []
    __description = []
    __requirement_id = []

    def __init__(self, id, name, description, requirement_id):
        """Summary
        
        Args:
            id ([UcSentence]): ID of the Information Object
            name ([UcSentence]): Name of the Information Object
            description ([UcSentence]): Description of the Information Object
            requirement_id ([UcSentence]): Requirement Category ID of the requirement related to the Information Object  
        """
        self.__id = id
        self.__name = name
        self.__description = description
        self.__requirement_id = requirement_id

    def get_id(self):
        """Get the ID of the Information Object
        
        Returns:
            [UcSentence]: ID
        """
        return self.__id


    def get_name(self):
        """Get the Name of the Information Object
        
        Returns:
            [UcSentence]: Name
        """
        return self.__name


    def get_description(self):
        """Get the Description of the Information Object
        
        Returns:
            [UcSentence]: Description
        """
        return self.__description


    def get_requirement_id(self):
        """Get the Requirement Category ID related to the Information Object
        
        Returns:
            [UcSentence]: Requirement Category ID
        """
        return self.__requirement_id
    
    def get_all_attributes(self):
        """Get all attributes of this object in a single List containing the UcSentences
        
        Returns:
            [UcSentence]: All attributes of this object
        """
        return self.__id + self.__name + self.__description + self.__requirement_id

#6

class Requirement_6(object):

    """Class representing a Requirement of the Use Case section 6 - Requirements
    """
    
    __id= []
    __name =[]
    __description = []
    __category_id = []

    def __init__(self, id, name, description, category_id):
        """Constructor
        
        Args:
            id ([UcSentence]): Requirement ID
            name ([UcSentence]): Requirement Name
            description ([UcSentence]): Description of the Requirement
            category_id ([UcSentence]): Category ID
        """
        self.__id = id
        self.__name = name
        self.__description = description
        self.__category_id = category_id

    def get_id(self):
        """Get the ID of the Requirement
        
        Returns:
            [UcSentence]: Requirement ID
        """
        return self.__id


    def get_name(self):
        """Get the Name of the Requirement
        
        Returns:
            [UcSentence]: Name
        """
        return self.__name


    def get_description(self):
        """Get the Description of Requirement
        
        Returns:
            [UcSentence]: Description
        """
        return self.__description
    
    def get_category_id(self):
        """Get the Category ID of the Requriement
        
        Returns:
            [UcSentence]: Category ID
        """
        return self.__category_id
    
    def get_all_attributes(self):
        """Get all attributes of this object in a single List containing the UcSentences
        
        Returns:
            [UcSentence]: All attributes of this object
        """
        return self.__id + self.__name + self.__description + self.__category_id

class RequirementsCategory_6(object):

    """Class representing a Requirement Category of the Use Case section 6 - Requirements
    """
    
    __id = []
    __name = []
    __description = []
    __requirement_objects = []


    def __init__(self, category_id, category_name, category_description, requirement_objects):
        """Constructor
        
        Args:
            category_id ([UcSentence]): Category ID
            category_name ([UcSentence]): Category Name
            category_description ([UcSentence]): Description of the Category
            requirement_objects ([Requirement_6]): Requirement Objects contained in this Category
        """
        self.__id = category_id
        self.__name = category_name
        self.__description = category_description
        self.__requirement_objects = requirement_objects

    def get_id(self):
        """Get the ID of Requirement Category
        
        Returns:
            [UcSentence]: ID
        """
        return self.__id


    def get_name(self):
        """Get the Name of the Requirement Category
        
        Returns:
            [UcSentence]: Name
        """
        return self.__name


    def get_description(self):
        """Get the Description of the Requirement Category
        
        Returns:
            [UcSentence]: Description
        """
        return self.__description


    def get_requirement_objects(self):
        """Get the Requirement Objects contained in the Requirement Category
        
        Returns:
            [Requirement_6]: Requirement Objects
        """
        return self.__requirement_objects
    
    def get_all_attributes(self):
        """Get all attributes of this object in a single List containing the UcSentences
        
        Returns:
            [UcSentence]: All attributes of this object
        """
        return self.__id + self.__name + self.__description
    
    def set_requirement_objects(self,value):
        """Set the Requirement Objects of this Category
        
        Args:
            value ([Requirement_6]): List with Requirement Objects
        """
        self.__requirement_objects = value
#7
class CommonTermsAndDefinitions_7(object):

    """Class representing a entry of the Glossary described in the Use Case section 7 - Common Terms and Definitions
    """
    
    __term = []
    __definition = []

    def __init__(self, term, definition):
        """Summary
        
        Args:
            term ([UcSentence]): Term
            definition ([UcSentence]): Term Definition
        """
        self.__term = term
        self.__definition = definition

    def get_term(self):
        """Get the Term itself
        
        Returns:
            [UcSentence]: Term
        """
        return self.__term


    def get_definition(self):
        """Get Defintion of the Term
        
        Returns:
            [UcSentence]: Definition
        """
        return self.__definition
    
    def get_all_attributes(self):
        """Get all attributes of this object in a single List containing the UcSentences
        
        Returns:
            [UcSentence]: All attributes of this object
        """
        return self.__term + self.__definition

#8

class CustomInformation_8(object):

    """Class representing a Custom Information of the Use Case section 8 - Custom Information
    """
    
    __key = []
    __value = []
    __refers_to_section = []

    def __init__(self, key, value, refers_to_section):
        """Summary
        
        Args:
            key ([UcSentence]): Key
            value ([UcSentence]): Value
            refers_to_section ([UcSentence]): Section related to the Information
        """
        self.__key = key
        self.__value = value
        self.__refers_to_section = refers_to_section

    def get_key(self):
        """Get the Key of the Information
        
        Returns:
            [UcSentence]: Key
        """
        return self.__key


    def get_value(self):
        """Get the Value of the Information
        
        Returns:
            [UcSentence]: Value
        """
        return self.__value


    def get_refers_to_section(self):
        """Get the section related to Information
        
        Returns:
            [UcSentence]: Section
        """
        return self.__refers_to_section
    
    def get_all_attributes(self):
        """Get all attributes of this object in a single List containing the UcSentences
        
        Returns:
            [UcSentence]: All attributes of this object
        """
        return self.__key + self.__value

class UseCase(object):

    """Class representing a Use Case described with template of the IEC 62559 Methodology
    """
    
    __name_of_uc_1_1 = []
    __version_management_1_2 = []
    __scope_1_3 = []
    __objective_1_3 = []
    __narrative_1_4 = []
    __kpi_1_5 = []
    __usecase_conditions_1_6 = []
    __further_infos_1_7= []
    __general_remark_1_8 = []
    __actor_grouping_3_1 = []
    __actor_3_1 = []
    __references_3_2 = []
    __scenarios_4_1 = []
    __steps_4_2 = []
    __information_exchanged_5 = []
    __requirements_category_6 = []
    __requirements_6 = []
    __glossary_7 = []
    __custom_information_8 = []

    def __init__(self, name_of_uc_1_1, version_management_1_2, scope_1_3, objective_1_3, narrative_1_4, kpi_1_5, usecase_conditions_1_6, further_infos_1_7, general_remark_1_8, actor_grouping_3_1, actor_3_1, references_3_2, scenarios_4_1, steps_4_2, information_exchanged_5, requirements_category_6, requirements_6, glossary_7, custom_information_8 = []):
        """Summary
        
        Args:
            name_of_uc_1_1 ([NameOfUC_1_1]): Section 1.1
            version_management_1_2 ([VersionManagement_1_2]): Section 1.2
            scope_1_3 ([Scope_1_3]): Section 1.3
            objective_1_3 ([Objective_1_3]): Objectives of Section 1.3
            narrative_1_4 ([Narrative_1_4]): Section 1.4 
            kpi_1_5 ([Kpi_1_5]): Section  1.5
            usecase_conditions_1_6 ([UseCaseConditions_1_6]): Section 1.6
            further_infos_1_7 ([FurtherInformation_1_7]): Section 1.7
            general_remark_1_8 ([GeneralRemark_1_8]): Section 1.8
            actor_grouping_3_1 ([ActorGrouping_3_1]): Section 3.1
            actor_3_1 ([Actor_3_1]): Actor of Section 3.1
            references_3_2 ([References_3_2]): Section 3.2
            scenarios_4_1 ([Scenario_4_1]): Section 4.1
            steps_4_2 ([Steps_4_2]): Section 4.2
            information_exchanged_5 ([InformationExchanged_5]): Section 5
            requirements_category_6 ([RequirementsCategory_6]): Requirement Category Section 6
            requirements_6 ([Requirement_6]): Requirement of Section 6
            glossary_7 ([CommonTermsAndDefinitions_7]): Section 7
            custom_information_8 ([CustomInformation_8], optional): Section 8
        """
        self.__name_of_uc_1_1 = name_of_uc_1_1
        self.__version_management_1_2 = version_management_1_2
        self.__scope_1_3 = scope_1_3
        self.__objective_1_3 = objective_1_3
        self.__narrative_1_4 = narrative_1_4
        self.__kpi_1_5 = kpi_1_5
        self.__usecase_conditions_1_6 = usecase_conditions_1_6
        self.__further_infos_1_7 = further_infos_1_7
        self.__general_remark_1_8 = general_remark_1_8
        self.__actor_grouping_3_1 = actor_grouping_3_1
        self.__actor_3_1 = actor_3_1
        self.__references_3_2 = references_3_2
        self.__scenarios_4_1 = scenarios_4_1
        self.__steps_4_2 = steps_4_2
        self.__information_exchanged_5 = information_exchanged_5
        self.__requirements_category_6 = requirements_category_6
        self.__requirements_6 = requirements_6
        self.__glossary_7 = glossary_7
        self.__custom_information_8 = custom_information_8

    def get_name_of_uc_1_1(self):
        """Get a list with Section 1.1 objects
        
        Returns:
            [NameOfUC_1_1]: Section 1.1 objects
        """
        return self.__name_of_uc_1_1


    def get_version_management_1_2(self):
        """Get a list with Section 1.2 objects
        
        Returns:
            [VersionManagement_1_2]: Section 1.2 objects
        """
        return self.__version_management_1_2


    def get_scope_1_3(self):
        """Get a list with Section 1.3 objects
        
        Returns:
            [Scope_1_3]: Section 1.3 objects
        """
        return self.__scope_1_3


    def get_objective_1_3(self):
        """Get a list with Objectives of Section 1.3
        
        Returns:
            [Objective_1_3]: Objectives of Section 1.3
        """
        return self.__objective_1_3


    def get_narrative_1_4(self):
        """Get a list with Section 1.4 objects
        
        Returns:
            [Narrative_1_4]: Section 1.4 objects
        """
        return self.__narrative_1_4


    def get_kpi_1_5(self):
        """Get a list with Section 1.5 objects
        
        Returns:
            [Kpi_1_5]: Section 1.5 objects
        """
        return self.__kpi_1_5


    def get_usecase_conditions_1_6(self):
        """Get a list with Section 1.6 objects
        
        Returns:
            [UseCaseConditions_1_6]: Section 1.6 objects
        """
        return self.__usecase_conditions_1_6


    def get_further_infos_1_7(self):
        """Get a list with Section 1.7 objects
        
        Returns:
            [FurtherInformation_1_7]: Section 1.7 objects
        """
        return self.__further_infos_1_7


    def get_general_remark_1_8(self):
        """Get a list with Section 1.8 objects
        
        Returns:
            [GeneralRemark_1_8]: Section 1.8 objects
        """
        return self.__general_remark_1_8


    def get_actor_grouping_3_1(self):
        """Get a list with Section 3.1 objects
        
        Returns:
            [ActorGrouping_3_1]: Section 3.1 objects
        """
        return self.__actor_grouping_3_1


    def get_actor_3_1(self):
        """Get a list with Actor objects of Section 3.1
        
        Returns:
            [Actor_3_1]: Actor objects of Section 3.1
        """
        return self.__actor_3_1


    def get_references_3_2(self):
        """Get a list with Section 3.2 objects
        
        Returns:
            [UcSentence]: Section 3.2 objects
        """
        return self.__references_3_2


    def get_scenarios_4_1(self):
        """Get a list with Section 4.1 objects
        
        Returns:
            [UcSentence]: Section 4.1 objects
        """
        return self.__scenarios_4_1


    def get_steps_4_2(self):
        """Get a list with Section 4.2 objects
        
        Returns:
            [UcSentence]: Section 4.2 objects
        """
        return self.__steps_4_2


    def get_information_exchanged_5(self):
        """Get a list with Section 5 objects
        
        Returns:
            [UcSentence]: Section 5 objects
        """
        return self.__information_exchanged_5

    def get_requirements_category_6(self):
        """Get a list with Section 6 objects
        
        Returns:
            [UcSentence]: Section 6 objects
        """
        return self.__requirements_category_6
        
    def get_requirements_6(self):
        """Get a list with Section 6 objects
        
        Returns:
            [UcSentence]: Requirements objects contained in Section 6
        """
        return self.__requirements_6


    def get_glossary_7(self):
        """Get a list with Section 7 objects
        
        Returns:
            [UcSentence]: Section 7 objects
        """
        return self.__glossary_7


    def get_custom_information_8(self):
        """Get a list with Section 8 objects
        
        Returns:
            [UcSentence]: Section 8 objects
        """
        return self.__custom_information_8

    def get_all_attributes(self):
        """Get all attributes of this object in a single List containing the UcSentences
        
        Returns:
            [UcSentence]: All attributes of this object
        """
        return self.__name_of_uc_1_1 + self.__version_management_1_2 + self.__scope_1_3 + self.__objective_1_3 + self.__narrative_1_4 + self.__kpi_1_5 + self.__usecase_conditions_1_6 + self.__further_infos_1_7 + self.__general_remark_1_8 + self.__actor_grouping_3_1 + self.__actor_3_1 + self.__references_3_2 + self.__scenarios_4_1 + self.__steps_4_2 + self.__information_exchanged_5 + self.__requirements_category_6 + self.__requirements_6 + self.__glossary_7 + self.__custom_information_8 
