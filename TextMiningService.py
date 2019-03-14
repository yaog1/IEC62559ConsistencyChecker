'''
Created on 12.12.2018

@author: yasino
'''
import nltk
from gensim.summarization import keywords
from py_stringmatching import OverlapCoefficient
import datetime
import re

class TmService(object):
    '''Implementation of the Text Mining step of the Text Mining Process. Includes Text Mining methods used for Use Case consistency checks.
    '''
    __output_filename = ''
    __output_object = ''    
    __actual_date = datetime.datetime.now()


    def __init__(self, filepath, filename_prefix = 'latest_usecase_' + __actual_date.strftime("%Y-%m-%d_%H:%M")):
        '''
        Constructor, params building the filepath and name for the output file. The filename will be: filename_prefix + _consistency_check.txt
        
        Args:
            filepath (str): Path where to save the consistency check output text file document. 
            filename (str, optional): Custom filename prefix for the consistency check output text file document. 
        '''
        self.__output_filename = filepath + filename_prefix + '_consistency_check.txt'
        self.__output_object = open(self.__output_filename, 'w', encoding ='utf-8')
        
    def _create_inconsistency_warning(self, td_sentence_content, td_meta_data_obj, inconsistency_msg, sd_sentence_content = "", sd_meta_data_obj = ""):
        """Creates the warning message used when a UcSentence is detected as a possible inconsistent object. The message includes meta data about the UcSentence
        
        Args:
            sentence_content (str): UcSentence content
            meta_data_obj (UcMetaData): Meta Data object of a UcSentence
            inconsistency_msg (str): base message, will be enhanced with metadata information
            sd_sentence_content (str, optional) : SourceData UcSentence content
            sd_meta_data_obj (UcMetaData, optional): SourceData Meta Data object of a UcSentence
        Returns:
            str: inconsistency warning
        """
        if(inconsistency_msg.count("similarity")>0):
            inconsistency_warning = 'HINT: Rule ' + inconsistency_msg + ':' + '\n' + "Testdata sentence: " + 'Attribute: ' + "'" + td_meta_data_obj.get_type() + "'" + '; section: ' + td_meta_data_obj.get_section() + '; sequence: ' + str(td_meta_data_obj.get_sequence()) + '; element: ' + str(td_meta_data_obj.get_element_number()) + '; sentence: ' + str(td_meta_data_obj.get_sentence_number()) + ";" + '\n' + "content: " + td_sentence_content + '\n' + "Highest similarity sentence: " + 'Attribute: ' + "'" + sd_meta_data_obj.get_type() + "'" + '; section: ' + sd_meta_data_obj.get_section() + '; sequence: ' + str(sd_meta_data_obj.get_sequence()) + '; element: ' + str(sd_meta_data_obj.get_element_number()) + '; sentence: ' + str(sd_meta_data_obj.get_sentence_number()) + ";" + '\n' + "content: " + sd_sentence_content + '\n'
        #if(inconsistency_msg.contains("keywords")):
        #    inconsistency_warning = 'Result: Rule ' + inconsistency_msg + '!!!:' + '\n' + 'Attribute: ' + "'" + td_meta_data_obj.get_type() + "'" + '; section: ' + td_meta_data_obj.get_section() + '; sequence: ' + str(td_meta_data_obj.get_sequence()) + '; element: ' + str(td_meta_data_obj.get_element_number()) + '; sentence: ' + str(td_meta_data_obj.get_sentence_number()) + ";" + '\n' + "content: " + td_sentence_content + '\n'
        else:
            inconsistency_warning = 'WARNING: Rule ' + inconsistency_msg + ' !!!:' + '\n' + 'Attribute: ' + "'" + td_meta_data_obj.get_type() + "'" + '; section: ' + td_meta_data_obj.get_section() + '; sequence: ' + str(td_meta_data_obj.get_sequence()) + '; element: ' + str(td_meta_data_obj.get_element_number()) + '; sentence: ' + str(td_meta_data_obj.get_sentence_number()) + ";" + '\n' + "content: " + td_sentence_content + '\n'
        return inconsistency_warning
  
    
    def write_output_file(self, text ):
        """Write a text into the output file
        
        Args:
            text (str): text
        """
        with open(self.__output_filename, 'a', encoding ='utf-8') as file:
            file.write(text + '\n')
    
    def get_list_uc_sentences(self, list_of_list_of_uc_sentences):
        """Helper function, converts set of list of UcSentence objects to a single flat list of UcSentence objects
        
        Args:
            list_of_list_of_uc_sentences (TYPE): A list containing a bunch of lists representing Use Case sentence attributes
        
        Returns:
            [UcSentence]: Flat list
        """
        list_of_ucs = []
        for list_of_uc_sentences in list_of_list_of_uc_sentences:
            for uc_sentence in list_of_uc_sentences:
                if type(uc_sentence) is list:
                    for uc_sent in uc_sentence:
                        list_of_ucs.append(uc_sent)
                else:
                    list_of_ucs.append(uc_sentence)
        return list_of_ucs
        
    def check_similarity(self, test_data, source_data, inconsistency_msg):
        """Check the similarity between two texts
        
        Args:
            test_data ([[UcSentence]]): test data
            source_data ([[UcSentence]]): source data
            inconsistency_msg (str): Base msg containing information about the violated rule
        """
        print("------ " + "FINDINGS " + "Rule: " + str(inconsistency_msg[: inconsistency_msg.find(":")]) + " ------" + '\n')
        self.write_output_file("------ " + "FINDINGS " + "Rule: " + str(inconsistency_msg[: inconsistency_msg.find(":")]) + " ------" + '\n')
        oc = OverlapCoefficient()
        list_td_sentences = self.get_list_uc_sentences(test_data)
        list_sd_sentences = self.get_list_uc_sentences(source_data) 
        for td_sentence in list_td_sentences:
            tmp_sim = 0.0
            highest_sim_value = 0.0
            highest_sim_sentence = ''
            if (td_sentence.get_content()):
                td_text = td_sentence.get_content()
                for sd_sentence in list_sd_sentences:
                    sd_text = sd_sentence.get_content()
                    #tmp_sim = textdistance.overlap.normalized_similarity(td_text, sd_text)
                    #tokenize texts and remove punctuations
                    td_words = [w for w in nltk.tokenize.word_tokenize(td_text) if (re.sub(r'[^\w\s]', '', w) != '')]
                    sd_words = [w for w in nltk.tokenize.word_tokenize(sd_text) if (re.sub(r'[^\w\s]', '', w) != '')]
                    tmp_sim = oc.get_sim_score(td_words, sd_words)
                    if (tmp_sim > highest_sim_value):
                        highest_sim_value = tmp_sim
                        highest_sim_sentence = sd_sentence
					# if no sentence with better similarity as 0.0 found, choose a sentence for output
                    if (tmp_sim == 0.0 and highest_sim_value== 0.0):
                        highest_sim_sentence = sd_sentence
                inconsistency_warning = self._create_inconsistency_warning(td_sentence.get_content(), td_sentence.get_meta_data(), inconsistency_msg, highest_sim_sentence.get_content(), highest_sim_sentence.get_meta_data()) + "similarity value: " + str(highest_sim_value*100) +'\n'
                print(inconsistency_warning)
                self.write_output_file(inconsistency_warning)
                td_sentence.get_meta_data().get_result_message().append(inconsistency_warning)

    def check_frequency(self, test_data, source_data, inconsistency_msg):
        """Check the frequency of the test_data in the source_data
        
        Args:
            test_data ([[UcSentence]]): test data
            source_data ([[UcSentence]]): source data
            inconsistency_msg (str): Base msg containing information about the violated rule
                        
        """
        if(not inconsistency_msg == "15: "+"Use Case 2 Information Exchanged "+"'Req. ID'" + " differs from " + "Use Case 1 Information Exchanged "+"'Req. ID'"):
            print("------ " + "FINDINGS " + "Rule: " + str(inconsistency_msg[: inconsistency_msg.find(":")]) + " ------" + '\n')
            self.write_output_file("------ " + "FINDINGS " + "Rule: " + str(inconsistency_msg[: inconsistency_msg.find(":")]) + " ------" + '\n')
        
        freq_matches = 0
        checking_rule9 = False
        checking_rule17 = False
        if(inconsistency_msg == "9: " + "'" + "Reference - No." + "'" + " not found in existing Use Case " + "'" + "Complete description" + "'"):
            checking_rule9 = True
        if(inconsistency_msg == "17: " + "'" + "Reference - No." + "'" + " not found in existing Use Case " + "'" + "Document" + "'"):
            checking_rule17 = True
        list_td_sentences = self.get_list_uc_sentences(test_data)
        list_sd_sentences = self.get_list_uc_sentences(source_data) 
        for td_sentence in list_td_sentences:
            freq_matched = False
            if (td_sentence.get_content()):
                td_text = td_sentence.get_content()
                for sd_sentence in list_sd_sentences:
                    sd_text = sd_sentence.get_content()
                    td_words = nltk.tokenize.word_tokenize(td_text)
                    if(len(td_words)==1):
                        sd_words = nltk.tokenize.word_tokenize(sd_text)
                        fd = nltk.FreqDist(sd_words)
                        frequency = fd[td_text]
                        if (frequency ==0):
                            frequency = fd[sd_text + "s"]
                    else:
                        frequency = sd_text.count(td_text)
                    if (frequency > 0):
                        freq_matched = True
                        freq_matches = freq_matches+1
                if not freq_matched:
                    if(inconsistency_msg == "15: "+"Use Case 1 Information Exchanged "+"'Req. ID'" + " differs from " + "Use Case 2 Information Exchanged "+"'Req. ID'"):
                        inconsistency_warning = self._create_inconsistency_warning(td_sentence.get_content(), td_sentence.get_meta_data(), inconsistency_msg)
                        inconsistency_warning = inconsistency_warning + "Use Case 1 Attribute " + "'" + sd_sentence.get_meta_data().get_type() + "'" + '; section: ' + sd_sentence.get_meta_data().get_section() + '; sequence: ' + str(sd_sentence.get_meta_data().get_sequence()) + '; element: ' + str(sd_sentence.get_meta_data().get_element_number()) + '\n'
                    else:
                        inconsistency_warning = self._create_inconsistency_warning(td_sentence.get_content(), td_sentence.get_meta_data(), inconsistency_msg) 
                    print(inconsistency_warning)
                    self.write_output_file(inconsistency_warning)
                    td_sentence.get_meta_data().set_validity(False)
                    td_sentence.get_meta_data().get_result_message().append(inconsistency_warning)

        if(checking_rule9 and freq_matches ==0):
            rule_9_not_ref = ("WARNING: Rule " + "9: None of the 'Reference - No.' found in existing Use Case 'Complete description'" + '!!!:' + '\n' + "The 'Complete description' is not referenced" + '\n')
            print(rule_9_not_ref)
            self.write_output_file(rule_9_not_ref)
        if(checking_rule17 and freq_matches ==0):
            rule_17_not_ref = "WARNING: Rule " + "17: None of the 'Reference - No.' found in existing Use Case 'Document'" + '!!!:' + '\n' + "The 'Document' is not referenced" + '\n'
            print(rule_17_not_ref)
            self.write_output_file(rule_17_not_ref)
                            
    def check_keywords(self, test_data, source_data, inconsistency_msg):
        """Extracts keyword suggestions by specific section texts (test_data). And checks the extracted keywords against keywords contained in the Use Case (source_data).
            ExtrChecks for matched words and gives suggestion for new keywords.
        
        Args:
            test_data ([[UcSentence]]): test data
            source_data ([[UcSentence]]): source data
            inconsistency_msg (str): Base msg containing information about the violated rule
        """
        
        print("------ " + "FINDINGS " + "Rule: " + str(inconsistency_msg[: inconsistency_msg.find(":")]) + " ------" + '\n')
        self.write_output_file("------ " + "FINDINGS " + "Rule: " + str(inconsistency_msg[: inconsistency_msg.find(":")]) + " ------" + '\n')
        
        
        td_text = ''
        sd_text = []    
        list_td_sentences = self.get_list_uc_sentences(test_data)
        list_sd_sentences = self.get_list_uc_sentences(source_data) 
        #fill list with td_sentence content
        for td_sentence in list_td_sentences:
            td_text = td_text + td_sentence.get_content() + ' '
        sd_sentence = list_sd_sentences[0]
        if(sd_sentence):
            sd_text = sd_sentence.get_content()
        source_keywords_tokens =  [w for w in nltk.word_tokenize(sd_text) if w.isalpha() ]

        extracted_kw = keywords(td_text, ratio=0.2, words=None, split=True, scores=False, pos_filter=('NN', 'JJ'), lemmatize=True, deacc=True)
        matched_keywords_count = 0
        matched_keywords = []
        for source_keyword in source_keywords_tokens:
            if source_keyword in extracted_kw:
                matched_keywords_count = matched_keywords_count+1 
                extracted_kw.remove(source_keyword)
                matched_keywords.append(source_keyword)
        #       print('matched keyword:' + source_keyword)
                
        extracted_kw_string = '; '.join(extracted_kw)
        matched_keywords_string = '; '.join(matched_keywords)
        #print('Matched keywords: ' + str(matched_keywords_count))
        
        ''' possible option to throw "Warning" if no keywords matched. ''' 
        '''
        if (matched_keywords_count == 0):
            print(inconsistency_msg + '\n')
            self.write_output_file( inconsistency_msg + '\n')
            sd_sentence.get_meta_data().set_validity(False)
            sd_sentence.get_meta_data().get_result_message().append(inconsistency_msg)
        else:
            print('Number of matched keywords: ' + str(matched_keywords_count) + '\n')
            self.write_output_file('Number of matched keywords: ' + str(matched_keywords_count) + '\n')
            sd_sentence.get_meta_data().get_result_message().append("Number of matched keywords: " + str(matched_keywords_count))
            print('Matched keywords from section 1.7: ' + matched_keywords_string + '\n')
            self.write_output_file('Matched keywords from section 1.7: ' + matched_keywords_string + '\n')
            sd_sentence.get_meta_data().get_result_message().append("Matched keywords from section 1.7: " + matched_keywords_string)
        '''
            
        print('Number of matched keywords: ' + str(matched_keywords_count) + '\n')
        self.write_output_file('Number of matched keywords: ' + str(matched_keywords_count) + '\n')
        sd_sentence.get_meta_data().get_result_message().append("Number of matched keywords: " + str(matched_keywords_count))
        print('Matched keywords from section 1.7: ' + matched_keywords_string + '\n')
        self.write_output_file('Matched keywords from section 1.7: ' + matched_keywords_string + '\n')
        sd_sentence.get_meta_data().get_result_message().append("Matched keywords from section 1.7: " + matched_keywords_string)    
        print('Some suggested keywords for section 1.7: ' + extracted_kw_string + '\n')
        self.write_output_file('Some suggested keywords for section 1.7: ' + extracted_kw_string + '\n')
        sd_sentence.get_meta_data().get_result_message().append('Some suggested keywords for section 1.7: ' + extracted_kw_string)
        
    
    