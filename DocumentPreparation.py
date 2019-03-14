'''
Created on 14.11.2018

@author: yasino
'''
import xml.etree.ElementTree as ET
import nltk
from nltk.corpus import stopwords
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.stem import WordNetLemmatizer
import unicodedata
import re

from UseCase62559 import UseCase, Narrative_1_4, Objective_1_3, Scope_1_3, Kpi_1_5,\
    UcSentence, UcMetaData, FurtherInformation_1_7, GeneralRemark_1_8,\
    ActorGrouping_3_1, Actor_3_1, References_3_2, Scenario_4_1, Steps_4_2,\
    InformationExchanged_5, Requirement_6, RequirementsCategory_6,\
    CommonTermsAndDefinitions_7, CustomInformation_8, UseCaseConditions_1_6,\
    VersionManagement_1_2, NameOfUC_1_1    

class DocumentPreparation(object):

    """Implementation of the Document Preparation step of the Text Mining Process
    """
    __sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
	
    '''
    classdocs
    '''
    
    def _import_file (self, filepath):
        """Import a xml file, representing a usecase
        
        Args:
            filepath (str): filepath to a xml representing a Use Case IEC 62559 Methodology
        
        Returns:
            TYPE: Root element of the xml file tree
        """
        tree = ET.parse(filepath)
        root = tree.getroot()
        return root
    
    def _remove_html_tags(self, text):
        """Remove HTML Tags in text
        
        Args:
            text (str): text
            attribute_type (str): Attribute Type e.g. 'Requirements(IDs)'
        
        Returns:
            str: text
        """
        return re.compile(r'<[^>]+>').sub('', text)
    
    def _remove_punctuation(self, sentences, attribute_type):
        """Remove Punctations in sentences, but only in some cases related to the attribute_type
        
        Args:
            sentences ([str]): Sentences
            attribute_type (str): Attribute Type e.g. 'Requirements(IDs)'
        
        Returns:
            [str]: Sentences
        """
        #Remove punctuation from list of tokenized words
        new_sentences = []
        # Only remove the punctations which were added self added in some sections
        if (attribute_type == 'Inf. exchanged (IDs)' or attribute_type == 'Requirements (IDs)' or attribute_type =='Req. ID'):
            for sentence in sentences:
                words = nltk.word_tokenize(sentence)
                new_words = []
                # remove punctation just in special cases defined by attribute_type
                for word in words:
                    new_word = re.sub(r'[^\w\s]', '', word)
                    if new_word != '':
                        new_words.append(new_word)
                new_sentences.append(TreebankWordDetokenizer().detokenize(new_words))
            return new_sentences
        else:
            return sentences 
            
    def _remove_non_ascii(self, sentences):
        """remove non ASCII chars and run function _the remove_html_tag
        
        Args:
            sentences ([str]): Sentences
        """
    ##Remove non-ASCII characters
        new_sentences = []
        for sentence in sentences:
            #remove ascii    
            new_sentence = unicodedata.normalize('NFKD', sentence).encode('ascii', 'ignore').decode('utf-8', 'ignore')
            new_sentences.append(new_sentence)
        return new_sentences
    
    def _to_lowercase(self, sentences):
        """Convert all characters to lowercase
        
        Args:
            sentences ([str]): List of sentences in lowercase
        """
    ##
        new_sentences = []
        for sentence in sentences:
            new_sentence = sentence.lower()
            new_sentences.append(new_sentence)
        return new_sentences
    
    def _filter_stopwords(self, sentences):
        """Remove stop words in a list of sentences
        
        Args:
            sentences ([str]): List of sentences without stopwords
        """
        new_sentences = []
        for sentence in sentences:
            new_words = []
            words = nltk.word_tokenize(sentence)
            for word in words:
                if word not in stopwords.words('english'):
                    new_words.append(word)
            new_sentences.append(TreebankWordDetokenizer().detokenize(new_words))
        return new_sentences    
        
    def _get_pos(self, tag):
        """Get a Pos for the lemmatization process
        
        Args:
            tag (str): Tag returned from function nltk.pos_tag
        
        Returns:
            str: Pos for the lemmatization process
        """
        if tag.startswith('J'):   ## adjective
            return 'a'
        elif tag.startswith('V'):  ## verb
            return 'v'
        elif tag.startswith('N'):  ## noun
            return 'n'
        elif tag.startswith('R'):  ## adverb
            return 'r'
        else:
            return ''    
    
    def _lemmatize_sentence(self, sentences):
        """Lemmatize senctences
        
        Args:
            sentences ([str]): List of sentences
        
        Returns:
            [str]: List of sentences
        """
        lemmatizer = WordNetLemmatizer()
        new_sentences = []
        for sentence in sentences:
            new_words = []
            words = nltk.word_tokenize(sentence)            
            ## need to use tokens for pos_tags
            pos_tags = nltk.pos_tag(words) 
            for i in range(len(words)):
                ## for any tags other than adj, verb, noun, adverb use default lemmatization
                if self._get_pos(pos_tags[i][1]) == '':
                    lemma = lemmatizer.lemmatize(words[i])
                ## default lemmatizer not working for adverb so manaully code to remove end 'ly' of adverb
                elif self._get_pos(pos_tags[i][1]) == 'r' and words[i].endswith('ly'):
                    lemma = words[i].replace('ly','')
                ## for adj, verb and noun
                ## explicitly pass POS tagger so that lemmatization is correct and efficient
                else:
                    lemma = lemmatizer.lemmatize(words[i], pos=self._get_pos(pos_tags[i][1]))    
                
                new_words.append(lemma)
            new_sentences.append(TreebankWordDetokenizer().detokenize(new_words))
        return new_sentences  
    
    def _preparation(self, text, section, sequence, element, attribute_type):
        """Summary
        
        Args:
            text (str): A unprepared text
            section (str): Use Case section, origin of the text
            sequence (int): Sequence number (index)
            element (int): Element number (index)
            attribute_type (str): Type of the attribute, which is described by the text
        
        Returns:
            [UcSentence]: List of UcSentence's representing the text of attribute in a Use Case
        """
        
        if(text==None):
            text=''
        if (text ==''):
            print('!WARNING: No text found! ---' + 'Section ' + str(section) +': '  + '"' + attribute_type + '"' + ' in Sequence ' + str(sequence) + ' at Position: ' + str(element))
            sentences = self.__sent_detector.tokenize(text.strip())
        else:
            #remove html tags
            text = self._remove_html_tags(text)
            #sentence Tokenize
            sentences = self.__sent_detector.tokenize(text.strip())
            # prepare the sentences
            sentences = self._remove_non_ascii(sentences)
            sentences = self._filter_stopwords(sentences)
            sentences = self._to_lowercase(sentences)
            sentences = self._lemmatize_sentence(sentences)
            # remove punctuations which were self added for requirement category ids and information object ids 
            sentences = self._remove_punctuation(sentences, attribute_type)
        
        # build UcSentence objects, fill metadata
        uc_sentences = []
        for senten_number in range(0, len(sentences)):
            temp_md = UcMetaData(section, sequence, element, attribute_type, senten_number)
            temp_sentence = UcSentence(sentences[senten_number], temp_md)
            uc_sentences.append(temp_sentence)
        return uc_sentences
    
        
    def _prepare_section_1_1(self, root):    
        """Prepare the Use Case section 1.1
        
        Args:
            root (TYPE): root of a Use Case Xml Tree
        
        Returns:
            [NameOfUC_1_1]: List of section 1.1 objects
        """
        section_1_1= '1.1 Name of Use Case'
        if(root.find('id') is not None):
            uc_id = self._preparation(root.find('id').text, section_1_1, 0, 0 , 'ID')
        else:
            uc_id = self._preparation('', section_1_1, 0, 0 , 'ID')
        uc_domains = []
        indexx = 0
        if (root.findall('Domain')):
            for domain in root.findall('Domain'):
                uc_domains.append(self._preparation(domain.text, section_1_1, 0, indexx , 'Area Domain(s)/Zone(s)'))
                indexx = indexx+1
        else:
            uc_domains.append(self._preparation('', section_1_1, 0, indexx , 'Area Domain(s)/Zone(s)'))
        if (root.find('name') is not None):
            uc_name = self._preparation(root.find('name').text, section_1_1, 0, 0 , 'Name of use case')
        else:
            uc_name = self._preparation('', section_1_1, 0, 0 , 'Name of use case')
        name_of_uc_obj_1_1 = [NameOfUC_1_1(uc_id, uc_domains, uc_name)]
        return name_of_uc_obj_1_1
      
    def _prepare_section_1_2(self, root):    
        """Prepare the Use Case section 1.2
        
        Args:
            root (TYPE): root of a Use Case Xml Tree
        
        Returns:
            [VersionManagement_1_2]: List of section 1.2 objects
        """
        ## 1.2
        vm_objects_1_2 = []
        vm_indexx = 0
        # TODO: Ask Marion sequence or element index
        section_1_2 = '1.2 Version Management'
        if(root.findall('VersionInformation')):
            for vm in root.findall('VersionInformation'):
                if(vm.find('number') is not None):
                    v_number =  self._preparation(vm.find('number').text, section_1_2, 0, vm_indexx, 'Version no.')
                else:
                    v_number =  self._preparation('', section_1_2, 0, vm_indexx, 'Version no.')
                if(vm.find('date') is not None):
                    date = self._preparation(vm.find('date').text, section_1_2, 0, vm_indexx, 'Date')
                else:
                    date = self._preparation('', section_1_2, 0, vm_indexx, 'Date')
                if(vm.find('authors') is not None):
                    authors = self._preparation(vm.find('authors').text, section_1_2, 0, vm_indexx, 'Name of author(s)')
                else:
                    authors = self._preparation('', section_1_2, 0, vm_indexx, 'Name of author(s)')
                if(vm.find('changes') is not None):
                    changes = self._preparation(vm.find('changes').text, section_1_2, 0, vm_indexx, 'Changes')
                else:
                    changes = self._preparation('', section_1_2, 0, vm_indexx, 'Changes')
                if(vm.find('approvalStatus') is not None):
                    status = self._preparation(vm.find('approvalStatus').text, section_1_2, 0, vm_indexx, 'Approval status')
                else:
                    status = self._preparation('', section_1_2, 0, vm_indexx, 'Approval status')
                # add obj
                vm_objects_1_2.append(VersionManagement_1_2(v_number,date, authors, changes, status))
        else:
            vm_objects_1_2.append(VersionManagement_1_2(self._preparation('', section_1_2, 0, vm_indexx, 'Version no.'),
                                                        self._preparation('', section_1_2, 0, vm_indexx, 'Date')
                                                        , self._preparation('', section_1_2, 0, vm_indexx, 'Name of author(s)')
                                                        , self._preparation('', section_1_2, 0, vm_indexx, 'Changes')
                                                        , self._preparation('', section_1_2, 0, vm_indexx, 'Approval status')))
        return vm_objects_1_2
    
    def _prepare_section_1_3(self, root):    
        """Prepare the Use Case section 1.3
        
        Args:
            root (TYPE): root of a Use Case Xml Tree
        
        Returns:
            [Scope_1_3, Objective_1_3]: List of section 1.3 objects
        """
        ## 1.3 scope, objective
        objective_objects_1_3 = []
        indexx=0
        section_1_3 = '1.3 Scope and Objectives of Use Case'
        if (root.findall('RelatedObjective')):
            for child in root.findall('RelatedObjective'):
                if(child.find('name') is not None):
                    obj_name = self._preparation(child.find('name').text, section_1_3, 0, indexx, 'Objective_1_3-Name')
                else:
                    obj_name = self._preparation('', section_1_3, 0, indexx, 'Objective_1_3-Name')
                if(child.find('description') is not None):
                    obj_desc = self._preparation(child.find('description').text, section_1_3, 0, indexx, 'Objective_1_3-Description')
                else:
                    obj_desc = self._preparation('', section_1_3, 0, indexx, 'Objective_1_3-Description')      
                # add obj
                objective_objects_1_3.append(Objective_1_3(obj_name, obj_desc)) 
                indexx=indexx+1
        else:
            objective_objects_1_3.append(Objective_1_3(self._preparation('', section_1_3, 0, indexx, 'Objective_1_3-Name')
                                                       , self._preparation('', section_1_3, 0, indexx, 'Objective_1_3-Description')))
        
        if(root.find('scope') is not None):
            scope_text = self._preparation(root.find('scope').text, '1.3 Scope and Objectives of Use Case', 0, 0 , 'Scope')
        else:
            scope_text = self._preparation('', '1.3 Scope and Objectives of Use Case', 0, 0 , 'Scope')
        scope_obj_1_3 = [Scope_1_3(scope_text, objective_objects_1_3)]
        section_1_3_objects = [scope_obj_1_3, objective_objects_1_3]
        return section_1_3_objects

    
    def _prepare_section_1_4(self, root):    
        """Prepare the Use Case section 1.4
        
        Args:
            root (TYPE): root of a Use Case Xml Tree
        
        Returns:
            [Narrative_1_4]: List of section 1.4 objects
        """
        ## 1.4 narrative
        if(root.find('Narrative') is not None):
            narrative = root.find('Narrative')
            if(narrative.find('completeDescription') is not None):
                compl_desc = self._preparation(narrative.find('completeDescription').text, '1.4 Narrative of Use Case ', 0, 0 , 'Complete description')
            else:
                compl_desc = self._preparation('', '1.4 Narrative of Use Case ', 0, 0 , 'Complete description')
            if(narrative.find('shortDescription') is not None):
                short_desc = self._preparation(narrative.find('shortDescription').text, '1.4 Narrative of Use Case ', 0, 0 , 'Short description')
            else:
                short_desc = self._preparation('', '1.4 Narrative of Use Case ', 0, 0 , 'Short description')
            narrative_obj_1_4 = [Narrative_1_4(short_desc, compl_desc)]
        else:
            narrative_obj_1_4 = [Narrative_1_4(self._preparation('', '1.4 Narrative of Use Case ', 0, 0 , 'Short description')
                                               ,self._preparation('', '1.4 Narrative of Use Case ', 0, 0 , 'Complete description'))]
        return narrative_obj_1_4
    
    def _prepare_section_1_5(self, root):    
        """Prepare the Use Case section 1.5
        
        Args:
            root (TYPE): root of a Use Case Xml Tree
        
        Returns:
            [Kpi_1_5]: List of section 1.5 objects
        """
        ## 1.5 kpi
        kpi_objects_1_5 = []
        indexx=0
        section_1_5 = '1.5 KPI'
        if(root.findall('KeyPerformanceIndicator')):
            for child in root.findall('KeyPerformanceIndicator'):
                if(child.find('id') is not None):
                    kpi_id = self._preparation(child.find('id').text, section_1_5, 0, indexx, 'ID')
                else:
                    kpi_id = self._preparation('', section_1_5, 0, indexx, 'ID')
                if(child.find('name') is not None):
                    kpi_name = self._preparation(child.find('name').text, section_1_5, 0,  indexx, 'Name')
                else:
                    kpi_name = self._preparation('', section_1_5, 0,  indexx, 'Name')
                if(child.find('description') is not None):
                    kpi_desc = self._preparation(child.find('description').text, section_1_5, 0, indexx, 'Description')
                else:
                    kpi_desc = self._preparation('', section_1_5, 0, indexx, 'Description')
                if(child.find('referenceToMentionedUseCaseObjective') is not None):
                    kpi_reference = self._preparation(child.find('referenceToMentionedUseCaseObjective').text, section_1_5, 0, indexx, 'Reference to mentioned use case objectives')
                else:
                    kpi_reference = self._preparation('', section_1_5, 0, indexx, 'Reference to mentioned use case objectives')
                kpi_objects_1_5.append(Kpi_1_5(kpi_id, kpi_name, kpi_desc, kpi_reference))
                indexx = indexx+1
        else:
            kpi_idd = self._preparation('', section_1_5, 0, indexx, 'ID')
            kpi_namee = self._preparation('', section_1_5, 0,  indexx, 'Name')
            kpi_descc = self._preparation('', section_1_5, 0, indexx, 'Description')
            kpi_referencee = self._preparation('', section_1_5, 0, indexx, 'Reference to mentioned use case objectives')
            kpi_objects_1_5.append(Kpi_1_5(kpi_idd, kpi_namee, kpi_descc,kpi_referencee))
        return kpi_objects_1_5
        
    def _prepare_section_1_6(self, root):    
        """Prepare the Use Case section 1.6
        
        Args:
            root (TYPE): root of a Use Case Xml Tree
        
        Returns:
            [UseCaseConditions_1_6]: List of section 1.6 objects
        """
        ## 1.6
        condition_objects_1_6 = []
        condition_indexx = 0
        # TODO: Ask Marion sequence or element index
        section_1_6 = '1.6 Use Case Conditions'
        if(root.findall('Condition')):
            for condition in root.findall('Condition'):
                if(condition.find('assumption') is not None):
                    assumption =  self._preparation(condition.find('assumption').text, section_1_6, 0, condition_indexx, 'Assumptions')
                else:
                    assumption =  self._preparation('', section_1_6, 0, condition_indexx, 'Assumptions')
                if(condition.find('PreCondition') is not None):
                    prereq = self._preparation(condition.find('PreCondition').find('content').text, section_1_6, 0, condition_indexx, 'Prerequisites')
                else:
                    prereq = self._preparation('', section_1_6, 0, condition_indexx, 'Prerequisites')
                # add obj
                condition_objects_1_6.append(UseCaseConditions_1_6(assumption, prereq))
                condition_indexx = condition_indexx+1
        else:
            condition_objects_1_6.append(UseCaseConditions_1_6(self._preparation('', section_1_6, 0, condition_indexx, 'Assumptions')
                                                               , self._preparation('', section_1_6, 0, condition_indexx, 'Prerequisites')))
        return condition_objects_1_6
    
    def _prepare_section_1_7(self, root):    
        """Prepare the Use Case section 1.7
        
        Args:
            root (TYPE): root of a Use Case Xml Tree
        
        Returns:
            [FurtherInformation_1_7]: List of section 1.7 objects
        """
        ## 1.7 Further infos
        section1_7='1.7 Further Information to the Use Case for Classiﬁcation/Mapping'
        if(root.find('levelOfDepth') is not None):
            level_of_depth = self._preparation(root.find('levelOfDepth').text, section1_7, 0, 0,  'Level of depth')
        else:
            level_of_depth = self._preparation('', section1_7, 0, 0,  'Level of depth')
        if(root.find('prioritisation') is not None):
            prio = self._preparation(root.find('prioritisation').text, section1_7, 0, 0,  'Prioritisation')
        else:
            prio = self._preparation('', section1_7, 0, 0,  'Prioritisation')
        if(root.find('keywords') is not None):
            keywds = self._preparation(root.find('keywords').text, section1_7, 0, 0, 'Further keywords for classiﬁcation')
        else:
            keywds = self._preparation('', section1_7, 0, 0, 'Further keywords for classiﬁcation')
        ''' missing attributes'''
        nature = self._preparation('', section1_7, 0, 0, 'Nature of the use case')
        generic_regional_national_relation = self._preparation('', section1_7, 0, 0, 'Generic, regional or national relation')
        relation_to_other_uc = self._preparation('', section1_7, 0, 0, 'Relation to other use cases')
        '''missing attributes'''

        classification_info_obj_1_7 = [FurtherInformation_1_7(relation_to_other_uc, level_of_depth, prio, generic_regional_national_relation, nature, keywds)]
        
        return classification_info_obj_1_7
    
    def _prepare_section_1_8(self, root):    
        """Prepare the Use Case section 1.8
        
        Args:
            root (TYPE): root of a Use Case Xml Tree
        
        Returns:
            [GeneralRemark_1_8]: List of section 1.8 objects
        """
        ## 1.8 general remarks
        general_remark_objects_1_8 = []        
        indexx = 0
        if(root.findall('GeneralRemark')):
            for child in root.findall('GeneralRemark'):
                if(child.find('content') is not None):
                    gr_content = self._preparation(child.find('content').text, '1.8 General Remarks', 0, indexx, 'General remark')
                else:
                    gr_content = self._preparation('', '1.8 General Remarks', 0, indexx, 'General remark')
                general_remark_objects_1_8.append(GeneralRemark_1_8(gr_content))
                indexx = indexx+1
        else:
            general_remark_objects_1_8.append(GeneralRemark_1_8(self._preparation('', '1.8 General Remarks', 0, indexx, 'General remark')))
        return general_remark_objects_1_8
    
    def _prepare_section_3_1(self, root):    
        """Prepare the Use Case section 3.1
        
        Args:
            root (TYPE): root of a Use Case Xml Tree
        
        Returns:
            [ActorGrouping_3_1, Actor_3_1]: List of section 3.1 objects
        """
        ## 3.1
        actor_grouping_objects_3_1 = []
        actor_objects_3_1 =[]
        seq =0
        section_3_1 = '3.1 Actors'
        if(root.findall('ActorGrouping')):
            for child in root.findall('ActorGrouping'):
                if(child.find('name') is not None):
                    grouping_name = self._preparation(child.find('name').text, section_3_1, seq, 0, 'Grouping')
                else:
                    grouping_name = self._preparation('', section_3_1, seq, 0, 'Grouping')
                if(child.find('description') is not None):
                    group_desc = self._preparation(child.find('description').text, section_3_1, seq, 0, 'Group description')
                else:
                    group_desc = self._preparation('', section_3_1, seq, 0, 'Group description')
                temp_actors_objects = []
                if(child.findall('Actor')):
                    actors = child.findall('Actor')
                    indexx = 0
                    # actors
                    for actor in actors:
                        if(actor.find('name') is not None):
                            name = self._preparation(actor.find('name').text, section_3_1, seq, indexx, 'Actor name')
                        else:
                            name = self._preparation('', section_3_1, seq, indexx, 'Actor name')
                        if(actor.find('description') is not None):
                            desc = self._preparation(actor.find('description').text, section_3_1, seq, indexx, 'Actor description')
                        else:
                            desc = self._preparation('', section_3_1, seq, indexx, 'Actor description')
                        if(actor.find('furtherInformation') is not None):
                            further_actor_info = self._preparation(actor.find('furtherInformation').text, section_3_1, seq, indexx, 'Further informationspeciﬁc to this usecase')
                        else:
                            further_actor_info = self._preparation('', section_3_1, seq, indexx, 'Further informationspeciﬁc to this usecase')
                        '''missing attributes'''
                        typee = self._preparation('', section_3_1, seq, indexx, 'Actor type')
                        '''missing attributes'''
                
                        # add obj
                        actor_objects_3_1.append(Actor_3_1(name, typee, desc, further_actor_info))
                        temp_actors_objects.append(Actor_3_1(name, typee, desc, further_actor_info))
                        indexx = indexx+1
                else:
                    temp_actors_objects.append(Actor_3_1(self._preparation('', section_3_1, seq, 0, 'Actor name')
                                                         , self._preparation('', section_3_1, seq, 0, 'Actor type')
                                                         , self._preparation('', section_3_1, seq, 0, 'Actor description')
                                                         , self._preparation(actor.find('furtherInformation').text, section_3_1, seq, 0, 'Further informationspeciﬁc to this usecase')))
                temp_actor_grouping = ActorGrouping_3_1(grouping_name, group_desc, temp_actors_objects)
                actor_grouping_objects_3_1.append(temp_actor_grouping)
                seq = seq+1
            section_3_1_objects = [actor_grouping_objects_3_1, actor_objects_3_1]
        else:
            
            actor_objects_3_1.append(Actor_3_1(self._preparation('', section_3_1, seq, 0, 'Actor name')
                                               , self._preparation('', section_3_1, seq, 0, 'Actor type')
                                               , self._preparation('', section_3_1, seq, 0, 'Actor description')
                                               , self._preparation('', section_3_1, seq, 0, 'Further informationspeciﬁc to this usecase')))
            grp_name = self._preparation('', section_3_1, seq, 0, 'Grouping')
            grp_desc = self._preparation('', section_3_1, seq, 0, 'Group description')
            actor_grp = ActorGrouping_3_1(grp_name, grp_desc, actor_objects_3_1)
            actor_grouping_objects_3_1.append(actor_grp)
            section_3_1_objects = [actor_grouping_objects_3_1, actor_objects_3_1]
        return section_3_1_objects
        
    def _prepare_section_3_2(self, root):        
        """Prepare the Use Case section 3.2
        
        Args:
            root (TYPE): root of a Use Case Xml Tree
        
        Returns:
            [References_3_2]: List of section 3.2 objects
        """
        ## 3.2
        reference_objects_3_2 = []
        indexx = 0
        section_3_2 = '3.2 References'
        if(root.findall('Reference')):
            for child in root.findall('Reference'):
                if(child.find('name') is not None):
                    ref_name = self._preparation(child.find('name').text, section_3_2, 0, indexx, 'No.')
                else:
                    ref_name = self._preparation('', section_3_2, 0, indexx, 'No.')
                if(child.find('type') is not None):
                    ref_type = self._preparation(child.find('type').text, section_3_2, 0,indexx, 'Reference type')
                else:
                    ref_type = self._preparation('', section_3_2, 0,indexx, 'Reference type')
                if(child.find('description') is not None):
                    ref_desc = self._preparation(child.find('description').text, section_3_2, 0, indexx, 'Reference')
                else:
                    ref_desc = self._preparation('', section_3_2, 0, indexx, 'Reference')
                if(child.find('status') is not None):
                    ref_status = self._preparation(child.find('status').text, section_3_2, 0, indexx, 'Status')
                else:
                    ref_status = self._preparation('', section_3_2, 0, indexx, 'Status')
                if(child.find('impact') is not None):
                    ref_impact = self._preparation(child.find('impact').text, section_3_2, 0, indexx, 'Impact on use case')
                else:
                    ref_impact = self._preparation('', section_3_2, 0, indexx, 'Impact on use case')
                if(child.find('originatorOrganisation') is not None):
                    ref_org = self._preparation(child.find('originatorOrganisation').text, section_3_2, 0, indexx, 'Originator/organisation')
                else:
                    ref_org = self._preparation('', section_3_2, 0, indexx, 'Originator/organisation')
                if(child.find('URI') is not None):
                    ref_link = self._preparation(child.find('URI').text, section_3_2, 0, indexx, 'Link')
                else:
                    ref_link = self._preparation('', section_3_2, 0, indexx, 'Link')
            
            #add obj 
                reference_objects_3_2.append(References_3_2(ref_name, ref_type, ref_desc, ref_status, ref_impact, ref_org, ref_link))
                indexx=indexx+1
        else:
            reference_objects_3_2.append(References_3_2(self._preparation('', section_3_2, 0, indexx, 'No.')
                                                        , self._preparation('', section_3_2, 0,indexx, 'Reference type')
                                                        , self._preparation('', section_3_2, 0, indexx, 'Reference')
                                                        , self._preparation('', section_3_2, 0, indexx, 'Status')
                                                        , self._preparation('', section_3_2, 0, indexx, 'Impact on use case')
                                                        , self._preparation('', section_3_2, 0, indexx, 'Originator/organisation')
                                                        , self._preparation('', section_3_2, 0, indexx, 'Link')))   
        return reference_objects_3_2
    
    def _prepare_section_4_1(self, root):    
        """Prepare the Use Case section 4.1
        
        Args:
            root (TYPE): root of a Use Case Xml Tree
        
        Returns:
            [Scenario_4_1, Steps_4_2]: List of section 4.1 objects
        """
        ## 4.1 & 4.2
        scen_elem = 0
        scenario_objects_4_1 = []
        steps_objects_4_2 = []
        seq =0
        section_4_1 = '4.1 Overview of Scenarios' 
        section_4_2 = '4.2 Steps – Scenarios'
        '''scenarios'''
        if(root.findall('Scenario')):
            for child in root.findall('Scenario'):
                if(child.find('number') is not None):
                    scen_id = self._preparation(child.find('number').text, section_4_1, 0, scen_elem, 'No.')
                else:
                    scen_id = self._preparation('', section_4_1, 0, scen_elem, 'No.')
                if(child.find('name') is not None):
                    scen_name = self._preparation(child.find('name').text, section_4_1, 0, scen_elem, 'Scenario name')
                else:
                    scen_name = self._preparation('', section_4_1, 0, scen_elem, 'Scenario name')
                if(child.find('description') is not None):
                    scen_desc = self._preparation(child.find('description').text, section_4_1, 0, scen_elem , 'Scenario description')
                else:
                    scen_desc = self._preparation('', section_4_1, 0, scen_elem , 'Scenario description')
                if(child.find('PrimaryActor') is not None):
                    scen_prim_actor = self._preparation(child.find('PrimaryActor').find('name').text, section_4_1, 0, scen_elem, 'Primary actor')
                else:
                    scen_prim_actor = self._preparation('', section_4_1, 0, scen_elem, 'Primary actor')
                if(child.find('preCondition') is not None):
                    scen_precondition = self._preparation(child.find('preCondition').text, section_4_1, 0, scen_elem, 'Precondition')
                else:
                    scen_precondition = self._preparation('', section_4_1, 0, scen_elem, 'Precondition')
                if(child.find('postCondition') is not None):
                    scen_postcondition = self._preparation(child.find('postCondition').text, section_4_1, 0, scen_elem, 'Postcondition')
                else:
                    scen_postcondition = self._preparation('', section_4_1, 0, scen_elem, 'Postcondition')
                if(child.find('triggeringEvent') is not None):
                    scen_triggering_event = self._preparation(child.find('triggeringEvent').text, section_4_1, 0, scen_elem, 'Triggering event')
                else:
                    scen_triggering_event = self._preparation('', section_4_1, 0, scen_elem, 'Triggering event')
            
                scen_elem = scen_elem + 1
                '''Steps'''
                indexx = 0
                temp_steps_objects_4_2 = []
                ## 4.2
                if(child.findall('Step')):
                    for step in child.findall('Step'):
                        if(step.find('number') is not None):
                            step_no = self._preparation(step.find('number').text, section_4_2, seq, indexx, 'No.')
                        else:
                            step_no = self._preparation('', section_4_2, seq, indexx, 'No.')
                        if(step.find('event') is not None):
                            step_event = self._preparation(step.find('event').text, section_4_2, seq,  indexx, 'Event')
                        else:
                            step_event = self._preparation('', section_4_2, seq,  indexx, 'Event')
                        if(step.find('name') is not None):
                            step_process_name =  self._preparation(step.find('name').text, section_4_2, seq, indexx, 'Name of process/activity')
                        else:
                            step_process_name =  self._preparation('', section_4_2, seq, indexx, 'Name of process/activity')
                        if(step.find('description') is not None):
                            step_process_desc = self._preparation(step.find('description').text, section_4_2, seq, indexx, 'Description of process/activity')
                        else:
                            step_process_desc = self._preparation('', section_4_2, seq, indexx, 'Description of process/activity')
                        if(step.find('service') is not None):
                            step_service = self._preparation(step.find('service').text, section_4_2, seq, indexx, 'Service')
                        else:
                            step_service = self._preparation('', section_4_2, seq, indexx, 'Service')
                        if(step.find('InformationProducer') is not None):
                            step_io_producer = self._preparation(step.find('InformationProducer').find('name').text, section_4_2, seq, indexx, 'Information producer (actor)')
                        else:
                            step_io_producer = self._preparation('', section_4_2, seq, indexx, 'Information producer (actor)')
                        if(step.find('InformationReceiver') is not None):
                            step_io_receiver = self._preparation(step.find('InformationReceiver').find('name').text, section_4_2, seq, indexx, 'Information receiver (actor)')
                        else:
                            step_io_receiver = self._preparation('', section_4_2, seq, indexx, 'Information receiver (actor)')
                        step_ios_string = ''
                        #step_ios_sentences = []
                        # pop because the first id is step_id
                        all_ios_ids = step.findall('InformationObject')
                        if(all_ios_ids):
                            for io_id in all_ios_ids:
                                #add punctation for sentence tokenization
                                if(io_id.find('id') is not None):
                                    step_ios_string = step_ios_string + io_id.find('id').text + '. '
                                else:
                                    step_ios_string = step_ios_string + '' + '. '
                            step_io_ids = self._preparation(step_ios_string, section_4_2, seq, indexx, 'Inf. exchanged (IDs)')
                
                        step_reqs_string = ''
                        if (step.find('Requirements') is not None):
                            for step_req in step.find('Requirements').findall('Requirement'):
                                # hint: using category id, because the name is not included in the requirements export file!
                                if(step_req.find('requirementCategoryId') is not None):
                                    step_reqs_string = step_reqs_string + step_req.find('requirementCategoryId').text + '. '
                                else:
                                    step_reqs_string = step_reqs_string + '' + '. '
                            step_req_id = self._preparation(step_reqs_string, section_4_2, seq, indexx, 'Requirements (IDs)')
                            #if actual step has no requirements just give an empty string
                        else:
                            step_req_id = self._preparation('', section_4_2, seq, indexx, 'Requirements (IDs)')
                        
                        temp_step = Steps_4_2(step_no, step_event, step_process_name, step_process_desc, step_service, step_io_producer, step_io_receiver,step_io_ids, step_req_id)
                        temp_steps_objects_4_2.append(temp_step)
                        steps_objects_4_2.append(temp_step)
                        indexx = indexx + 1
                        
                    temp_scenario = Scenario_4_1(scen_id,scen_name, scen_desc,scen_prim_actor,scen_triggering_event,scen_precondition ,scen_postcondition,temp_steps_objects_4_2)
                    scenario_objects_4_1.append(temp_scenario)
                    seq = seq+1
                else:
                    temp_step = Steps_4_2(self._preparation('', section_4_2, seq, 0, 'No.')
                                          , self._preparation('', section_4_2, seq,  0, 'Event')
                                          , self._preparation('', section_4_2, seq, 0, 'Name of process/activity')
                                          , self._preparation('', section_4_2, seq, 0, 'Description of process/activity')
                                          , self._preparation('', section_4_2, seq, 0, 'Service')
                                          , self._preparation('', section_4_2, seq, 0, 'Information producer (actor)')
                                          , self._preparation('', section_4_2, seq, 0, 'Information receiver (actor)')
                                          , self._preparation('', section_4_2, seq, 0, 'Inf. exchanged (IDs)')
                                          , self._preparation('', section_4_2, seq, 0, 'Requirements (IDs)'))
                    steps_objects_4_2.append(temp_step)
                        #indexx = indexx + 1
                    temp_scenario = Scenario_4_1(scen_id,scen_name, scen_desc,scen_prim_actor,scen_triggering_event,scen_precondition ,scen_postcondition, [temp_step])
                    scenario_objects_4_1.append(temp_scenario)
                    seq = seq+1
                    
                section_4_1_objects = [scenario_objects_4_1, steps_objects_4_2]
        else:
            temp_step = Steps_4_2(self._preparation('', section_4_2, seq, 0, 'No.')
                                          , self._preparation('', section_4_2, seq,  0, 'Event')
                                          , self._preparation('', section_4_2, seq, 0, 'Name of process/activity')
                                          , self._preparation('', section_4_2, seq, 0, 'Description of process/activity')
                                          , self._preparation('', section_4_2, seq, 0, 'Service')
                                          , self._preparation('', section_4_2, seq, 0, 'Information producer (actor)')
                                          , self._preparation('', section_4_2, seq, 0, 'Information receiver (actor)')
                                          , self._preparation('', section_4_2, seq, 0, 'Inf. exchanged (IDs)')
                                          , self._preparation('', section_4_2, seq, 0, 'Requirements (IDs)'))
            steps_objects_4_2.append(temp_step)
            
            scn_id = self._preparation('', section_4_1, seq, 0, 'No.')
            scn_name = self._preparation('', section_4_1, seq, 0, 'Scenario name')
            scn_desc = self._preparation('', section_4_1, seq, 0 , 'Scenario description')
            scn_prim_actor = self._preparation('', section_4_1, seq, 0, 'Primary actor')
            scn_triggering_event = self._preparation('', section_4_1, seq, 0, 'Triggering event')
            scn_precondition = self._preparation('', section_4_1, seq, 0, 'Precondition')
            scn_postcondition = self._preparation('', section_4_1, seq, 0, 'Postcondition')
            temp_scenario = Scenario_4_1(scn_id
                                         ,scn_name
                                         ,scn_desc
                                         ,scn_prim_actor
                                         ,scn_triggering_event
                                         ,scn_precondition
                                         ,scn_postcondition
                                         ,steps_objects_4_2)
            scenario_objects_4_1.append(temp_scenario)
            
            section_4_1_objects = [scenario_objects_4_1, steps_objects_4_2]
        return section_4_1_objects
        
    def _prepare_section_5(self, root):    
        """Prepare the Use Case section 5
        
        Args:
            root (TYPE): root of a Use Case Xml Tree
        
        Returns:
            [InformationExchanged_5]: List of section 5 objects
        """
        #5
        io_objects_5 = []
        section_5 = '5 Information Exchanged'
        indexx=0
        if(root.find('InformationObjects') is not None):
            for io in root.find('InformationObjects').findall('InformationObject'):
                # hint: The 'id' is the database Id of the ucr!
                if(io.find('id') is not None):
                    ioe_id = self._preparation(io.find('id').text, section_5, 0, indexx, 'Inf. exchanged (IDs)')
                else:
                    ioe_id = self._preparation('', section_5, 0, indexx, 'Inf. exchanged (IDs)')
                if(io.find('name') is not None):
                    ioe_name= self._preparation(io.find('name').text, section_5, 0, indexx, 'Name of information exchanged')
                else:
                    ioe_name= self._preparation('', section_5, 0, indexx, 'Name of information exchanged')
                
                # hint: using category id, because the name is not included in the requirements export file!
                io_reqs_string = ''
                if (io.find('Requirements') is not None):
                    if(io.find('Requirements').findall('Requirement')):
                        for io_req in io.find('Requirements').findall('Requirement'):
                            # hint: using category id, because the name is not included in the requirements export file!
                            if(io_req.find('requirementCategoryId') is not None):
                                io_reqs_string = io_reqs_string + io_req.find('requirementCategoryId').text + '. '
                                io_req_id = self._preparation(io_reqs_string, section_5, 0, indexx, 'Req. ID')
                    else:
                        io_req_id = self._preparation('', section_5, 0, indexx, 'Req. ID')                            
                        #if actual io has no requirements just give an empty string
                else:
                    io_req_id = self._preparation('', section_5, 0, indexx, 'Req. ID')
            
                '''missing attributes'''
                ioe_desc = self._preparation('', section_5, 0, indexx, 'Description of information exchanged')
                '''missing attributes'''
            
                # add obj 
                io_objects_5.append(InformationExchanged_5(ioe_id,ioe_name, ioe_desc, io_req_id))
                indexx=indexx+1
        else:
            io_objects_5.append(InformationExchanged_5(self._preparation('', section_5, 0, indexx, 'Inf. exchanged (IDs)')
                                                       ,self._preparation('', section_5, 0, indexx, 'Name of information exchanged')
                                                       ,self._preparation('', section_5, 0, indexx, 'Description of information exchanged')
                                                       , self._preparation('', section_5, 0, indexx, 'Req. ID')))
        return io_objects_5
    
    def _prepare_section_6(self, root):    
        """Prepare the Use Case section 6
        
        Args:
            root (TYPE): root of a Use Case Xml Tree
        
        Returns:
            [RequirementsCategory_6, Requirement_6]: List of section 6 objects
        """
        section_6 = '6 Requirements (Optional)'
        req_categoy_number = 0
        req_categories_objects_6 = []
        #all requirements
        requirement_objects_6 = []
        requirement_cat_ids = []
        category_requirement_objects = []
        if(root.find('RequirementLibrary') is not None):
            for req in root.find('RequirementLibrary').findall('RequirementCategory'):
                #category specific requirements
                if (req.find('ParentCategory') == None):
                    req_categoy_number = len(req_categories_objects_6)
                    #hint: id is the database id, 'Category name for requirements' is missing
                    if(req.find('id') is not None):
                        category_id = self._preparation(req.find('id').text, section_6, req_categoy_number, 0, 'Categories ID')
                    else:
                        category_id = self._preparation('', section_6, req_categoy_number, 0, 'Categories ID')
                    if(req.find('id') is not None):
                        requirement_cat_ids.append(req.find('id').text)
                    else:
                        requirement_cat_ids.append('')
                    if(req.find('name') is not None):
                        category_name = self._preparation(req.find('name').text, section_6, req_categoy_number, 0, 'Category name for requirements')
                    else:
                        category_name = self._preparation('', section_6, req_categoy_number, 0, 'Category name for requirements')
                    if(req.find('description') is not None):
                        category_description = self._preparation(req.find('description').text, section_6, req_categoy_number, 0, 'Category description')
                    else:
                        category_description = self._preparation('', section_6, req_categoy_number, 0, 'Category description')
                    req_categories_objects_6.append(RequirementsCategory_6(category_id, category_name, category_description, category_requirement_objects))
                    category_requirement_objects = []
                else:
                    #for reqs_x in req_categories_elements:
                    req_indexx = 0
                        # this id is the database id, this req_name is normally the value in the list collumn Requirement_6 ID
                    if(req.find('id') is not None):
                        req_id = self._preparation(req.find('id').text, section_6, req_categoy_number, req_indexx, 'Requirement ID') 
                    else:
                        req_id = self._preparation('', section_6, req_categoy_number, req_indexx, 'Requirement ID')
                    if(req.find('name') is not None):
                        req_name = self._preparation(req.find('name').text, section_6, req_categoy_number, req_indexx, 'Requirement name')
                    else:
                        req_name = self._preparation('', section_6, req_categoy_number, req_indexx, 'Requirement name')
                    if(req.find('description') is not None):
                        req_desc = self._preparation(req.find('description').text, section_6, req_categoy_number, req_indexx, 'Requirement description')
                    else:
                        req_desc = self._preparation('', section_6, req_categoy_number, req_indexx, 'Requirement description')
                    # this Id exists only in the xml export (database) not in the template
                    if(req.find('ParentCategory').find('id') is not None):
                        req_category_id = self._preparation(req.find('ParentCategory').find('id').text, section_6, req_categoy_number, 0, 'Categories ID')
                    else:
                        req_category_id = self._preparation('', section_6, req_categoy_number, 0, 'Categories ID')

                    #add obj
                    requirement_objects_6.append(Requirement_6(req_id, req_name, req_desc, req_category_id))
                    category_requirement_objects.append(Requirement_6(req_id, req_name, req_desc, req_category_id))
                    req_indexx = req_indexx+1
                req_categories_objects_6[req_categoy_number].set_requirement_objects(category_requirement_objects)

        else:
            req_indexx = 0
            requirement_objects_6.append(Requirement_6(self._preparation('', section_6, req_categoy_number, req_indexx, 'Requirement ID')
                                                       , self._preparation('', section_6, req_categoy_number, req_indexx, 'Requirement name')
                                                       , self._preparation('', section_6, req_categoy_number, req_indexx, 'Requirement description')
                                                       , self._preparation('', section_6, req_categoy_number, 0, 'Categories ID')))
            cat_id = self._preparation('', section_6, req_categoy_number, 0, 'Categories ID')
            cat_name = self._preparation('', section_6, req_categoy_number, 0, 'Category name for requirements')
            cat_description = self._preparation('', section_6, req_categoy_number, 0, 'Category description')
            req_categories_objects_6.append(RequirementsCategory_6(cat_id
                                                                   , cat_name
                                                                   , cat_description
                                                                   , requirement_objects_6))
        
        if (not requirement_objects_6):
            req_indexx = 0
            requirement_objects_6.append(Requirement_6(self._preparation('', section_6, req_categoy_number, req_indexx, 'Requirement ID'),
                                                       self._preparation('', section_6, req_categoy_number, req_indexx, 'Requirement name')
                                                       , self._preparation('', section_6, req_categoy_number, req_indexx, 'Requirement description')
                                                       , self._preparation('', section_6, req_categoy_number, 0, 'Categories ID')))
            
        section_6_objects = [req_categories_objects_6, requirement_objects_6]
        return section_6_objects
    
    def _prepare_section_7(self, root):        
        """Prepare the Use Case section 7
        
        Args:
            root (TYPE): root of a Use Case Xml Tree
        
        Returns:
            [CommonTermsAndDefinitions_7]: List of section 7 objects
        """
        section_7 = '7 Common Terms and Deﬁnitions'
        term_indexx = 0
        common_term_objects_7 = []
        if(root.find('Glossary') is not None):
            for term in root.find('Glossary').findall('term'):     
                if(term.find('name') is not None):
                    term_name = self._preparation(term.find('name').text, section_7, 0, term_indexx, 'Term')
                else:
                    term_name = self._preparation('', section_7, 0, term_indexx, 'Term')
                if(term.find('description') is not None):
                    term_def = self._preparation(term.find('description').text, section_7, 0, term_indexx, 'Deﬁnition')
                else:
                    term_def = self._preparation('', section_7, 0, term_indexx, 'Deﬁnition')
                #add obj
                common_term_objects_7.append(CommonTermsAndDefinitions_7(term_name, term_def))
                term_indexx=term_indexx+1
        else:
            t_name= self._preparation('', section_7, 0, term_indexx, 'Term')
            t_def = self._preparation('', section_7, 0, term_indexx, 'Deﬁnition')
            common_term_objects_7.append(CommonTermsAndDefinitions_7(t_name, t_def))
        return common_term_objects_7
            
        # Section 8 is actually missing in the xml export, because of this the implementation is...
    def _prepare_section_8(self, root):
        return []
        '''these objects are missing in the export
        
        Args:
            root (TYPE): root of a Use Case Xml Tree
        '''
        
        '''
        section_8 = '8 Custom Information (Optional)'
        info_indexx = 0
        custom_info_objects_8 = []
        for ci in root.find('CustomInformation').findall('information'):     
            ci_name = self._preparation(ci.find('name').text, section_8, 0, term_indexx, 'Key')
            ci_desc = self._preparation(ci.find('description').text, section_8, 0, term_indexx, 'Value')
            ci_ref = self._preparation(ci.find('refersToSection').text, section_8, 0, term_indexx, 'Refers to section')
            # add obj
            custom_info_objects_8.append(CustomInformation_8(ci_name, ci_desc , ci_ref))
            info_indexx=info_indexx+1
        '''
    def create_usecase_62559 (self, filepath):        
        """Create a UseCase object
        
        Args:
            filepath (str): Filepath to a XML File representing the Usecase 
        
        Returns:
            UseCase: UseCase object, parsed and prepared content
        """
        root = self._import_file(filepath)  
        print('parsing the file...')
        use_case_obj = UseCase(self._prepare_section_1_1(root), self._prepare_section_1_2(root), self._prepare_section_1_3(root)[0], self._prepare_section_1_3(root)[1], self._prepare_section_1_4(root), self._prepare_section_1_5(root), self._prepare_section_1_6(root), self._prepare_section_1_7(root), self._prepare_section_1_8(root), self._prepare_section_3_1(root)[0], self._prepare_section_3_1(root)[1],self._prepare_section_3_2(root), self._prepare_section_4_1(root)[0], self._prepare_section_4_1(root)[1], self._prepare_section_5(root), self._prepare_section_6(root)[0], self._prepare_section_6(root)[1], self._prepare_section_7(root), self._prepare_section_8(root))
        print('Use Case created!' + '\n')
        return use_case_obj
                