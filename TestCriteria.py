'''
Created on 18.12.2018

@author: yasino
'''
    
'''TODO: similiarity'''
''' TODO: scenario name vergleich mit complete desc -> erst freq check, dann simi'''
class TestCriteria(object):

    """Implementation of the consistency rules for the Use Case IEC 62559 Methodology.
    """
    
    __tms = None
    
    def __init__(self, tms):
        """Constructor
        
        Args:
            tms (TmService): Text Mining Service object needed to run text mining methods
        """
        self.__tms = tms
    
    def _check_not_possible_msg(self, rule_number, attributes_section, attribute_name):
        """Print a message, when a rule check is impossible
        
        Args:
            rule_number (str): number of the tested rule
            attributes_section (str): section of the missing attribute which makes the check impossible
            attribute_name (str): name of the missing attribute which makes the check impossible
        """
        
        print("------ " + "FINDINGS " + "Rule: " + rule_number + " ------" + '\n')
        self.__tms.write_output_file("------ " + "FINDINGS " + "Rule: " + rule_number + " ------" + '\n')
        print("Rule " + rule_number + ": " + "Check not possible!!!: " + '\n' + "Use Case has no section " + attributes_section + " '" + attribute_name + "'" + " informations." + '\n')
        self.__tms.write_output_file("Rule " + rule_number + ": " + "Check not possible!!!: " + '\n' + "Use Case has no " + "'" + attribute_name + "'" + " informations." + '\n')
        
    def check_rule_1(self, usecase):
        """Rule 1 Implementation
        
        Args:
            usecase (TYPE): Description
            
        Returns:
            [UseCase]: Checked UseCase
        """
        check_1 = "1: " + "'" + "Reference to mentioned use case objectives" + "'" + " not found in existing Use Case " + "'" + "Objective Names" + "'"
        '''create test objects'''
        kpi_mentioned_objectives_1_5 = []
        for child in usecase.get_kpi_1_5():
            kpi_mentioned_objectives_1_5.append(child.get_mentioned_objective())
            
        objective_names_1_3 = []
        for child in usecase.get_scope_1_3():
            for objective in child.get_objectives():
                objective_names_1_3.append(objective.get_name())
                
        td_not_empty = False
        for s in kpi_mentioned_objectives_1_5:
            if (s):
                td_not_empty = True
                
        sd_not_empty = False
        for st in objective_names_1_3:
            if (st):
                sd_not_empty = True
                
        '''check'''
        if(td_not_empty and sd_not_empty):
            self.__tms.check_frequency(kpi_mentioned_objectives_1_5, objective_names_1_3, check_1)
        if (not td_not_empty):
            self._check_not_possible_msg("1","1.5" , "Reference to mentioned use case objectives")
        if (not sd_not_empty):
            self._check_not_possible_msg("1", "1.3" , "Objective Names")
        
        return usecase
    
    def check_rule_2(self, usecase):
        """Rule 2 Implementation
        
        Args:
            usecase (UseCase): Use Case that has to be checked
        """
        # 2. Template Abschnitt 1.5 - Key Performance Indicators (KPI)
        check_2 = "2: " + "'" + "1.5 - Description" + "'" + " has highest similarity to following " + "'" + "Objective Description" + "'"
        '''create test objects'''
        
        kpi_desc_1_5 = []
        for child in usecase.get_kpi_1_5():
            kpi_desc_1_5.append(child.get_description())
            
        objective_desc_1_3 = []
        for child in usecase.get_scope_1_3():
            for objective in child.get_objectives():
                objective_desc_1_3.append(objective.get_description())
            
        td_not_empty = False
        for s in kpi_desc_1_5:
            if (s):
                td_not_empty = True
                
        sd_not_empty = False
        for st in objective_desc_1_3:
            if (st):
                sd_not_empty = True
        
        
        if (not td_not_empty):
            self._check_not_possible_msg("2", "1.5", "Description")
        if (not sd_not_empty):
            self._check_not_possible_msg("2", "1.3", "Objective - Description")
        
        if(td_not_empty and sd_not_empty):
            counter_sim = 0
            for kpi in usecase.get_kpi_1_5():
                kpi_description_sentence_list = kpi.get_description()
                kpi_mentioned_obj_sentence_list = kpi.get_mentioned_objective()
                #compare mentioned objective with objective names
                ## get mentioned objective:
                if type(kpi_mentioned_obj_sentence_list) is list:
                    for kpi_mentioned_obj_sentence in kpi_mentioned_obj_sentence_list:
                        if(kpi_mentioned_obj_sentence.get_content()):
                            kpi_mentioned_obj_txt = kpi_mentioned_obj_sentence.get_content()
                            ### get objective names
                            for child in usecase.get_scope_1_3():
                                for objective in child.get_objectives():
                                    objective_description_sentence_list = objective.get_description()
                                    objective_name_sentence_list = objective.get_name()
                                    if type(objective_name_sentence_list) is list:
                                        for objective_name_sentence in objective_name_sentence_list:
                                            if(objective_name_sentence.get_content()):
                                                objective_name_txt = objective_name_sentence.get_content()
                                                if(kpi_mentioned_obj_txt == objective_name_txt):
                                                    self.__tms.check_similarity([kpi_description_sentence_list], [objective_description_sentence_list], check_2)
                                                    counter_sim = counter_sim+1
            if(counter_sim==0):
                self._check_not_possible_msg("2","1.5 - 1.3" , "'Reference to mentioned use case objectives' in relation to a 'Objective - Description'")
        return usecase
    
    def check_rule_3(self, usecase):
        """Rule 3 Implementation
        
        Args:
            usecase (UseCase): Use Case that has to be checked
            
        Returns:
            [UseCase]: Checked UseCase
        """
    # 3. Template Abschnitt 4.1 - Overview of scenarios:
        check_3 =  "3: " + "'" + "Scenario name" + "'" + " not found in existing Use Case " + "'" + "Complete description" + "'"
        '''create test objects'''
        scenario_names_4_1 = []
        for scenario in usecase.get_scenarios_4_1():
            scenario_names_4_1.append(scenario.get_name())
            
        complete_descriptions_1_4 =[]
        for child in usecase.get_narrative_1_4():
            complete_descriptions_1_4.append(child.get_complete_description())
            
        td_not_empty = False
        for s in scenario_names_4_1:
            if (s):
                td_not_empty = True
                
        sd_not_empty = False
        for st in complete_descriptions_1_4:
            if (st):
                sd_not_empty = True
        '''check'''
        if(td_not_empty and sd_not_empty):
            self.__tms.check_frequency(scenario_names_4_1, complete_descriptions_1_4, check_3)
        if (not td_not_empty):
            self._check_not_possible_msg("3", "4.1", "Scenario name")
        if (not sd_not_empty):
            self._check_not_possible_msg("3", "1.4" , "Complete description")
                    
        return usecase

            
    def check_rule_4(self, usecase):
        """Rule 4 Implementation
        
        Args:
            usecase (UseCase): Use Case that has to be checked
            
        Returns:
            [UseCase]: Checked UseCase
        """
        check_4 =  "4: " + "'" + "Scenario description" + "'" + " sentence " + " has highest similarity to following " + "'" + "Complete description" + "'" + " sentence "
        '4: scenario_description check_similarity complete_description'
        '''create test objects'''
        scenario_descriptions_4_1 = []
        for scenario in usecase.get_scenarios_4_1():
            scenario_descriptions_4_1.append(scenario.get_description())
        
        complete_descriptions_1_4 =[]
        for child in usecase.get_narrative_1_4():
            complete_descriptions_1_4.append(child.get_complete_description())
        '''check'''
        td_not_empty = False
        for s in scenario_descriptions_4_1:
            if (s):
                td_not_empty = True
        
        sd_not_empty = False
        for st in complete_descriptions_1_4:
            if (st):
                sd_not_empty = True
            
        if(td_not_empty and sd_not_empty):
            self.__tms.check_similarity(scenario_descriptions_4_1, complete_descriptions_1_4, check_4)
        if (not sd_not_empty):
            self._check_not_possible_msg("4", "4.1", "Scenario description")
        if (not td_not_empty):
            self._check_not_possible_msg("4", "1.4", "Complete description")

        return usecase
          
    # 5. Template Abschnitt 4.2 - Steps - Scenarios:
    def check_rule_5(self, usecase):
        """Rule 5 Implementation
        
        Args:
            usecase (UseCase): Use Case that has to be checked
            
        Returns:
            [UseCase]: Checked UseCase
        """
        check_5 = "5: " + "'" + "Inf. exchanged (IDs)" + "'" + " not found in existing Use Case " + "'" + "Inf. ID" + "'"

        '''create test objects'''
        step_informations_exchanged_4_2 = []
        for step in usecase.get_steps_4_2():        
            step_informations_exchanged_4_2.append(step.get_inf_exchanged_id())
            
        information_exchanged_ids_5 = []
        for child in usecase.get_information_exchanged_5():
            information_exchanged_ids_5.append(child.get_id())
        '''check'''
        td_not_empty = False
        for s in step_informations_exchanged_4_2:
            if (s):
                td_not_empty = True
        
        sd_not_empty = False
        for st in information_exchanged_ids_5:
            if (st):
                sd_not_empty = True
        
        if(td_not_empty and sd_not_empty):
            self.__tms.check_frequency(step_informations_exchanged_4_2, information_exchanged_ids_5, check_5)
        if (not td_not_empty):
            self._check_not_possible_msg("5", "4.2", "Inf. exchanged (IDs)")
        if (not sd_not_empty):
            self._check_not_possible_msg("5", "5", "Inf. ID")
        
        return usecase

    
    def check_rule_6(self, usecase):
        """Rule 6 Implementation
        
        Args:
            usecase (UseCase): Use Case that has to be checked
            
        Returns:
            [UseCase]: Checked UseCase
        """
        check_6 = "6: " + "'" + "Requirements (IDs)" + "'" + " not found in existing Use Case " + "'" + "Requirement ID" + "'"
        '''create test objects'''
        step_requirement_ids_4_2 = []
        for step in usecase.get_steps_4_2():        
            step_requirement_ids_4_2.append(step.get_requirements_ids())
            
        requirement_ids_6= []
        for child in usecase.get_requirements_6():
            requirement_ids_6.append(child.get_id())
            
        requirement_cat_ids_6= []
        for child in usecase.get_requirements_category_6():
            requirement_cat_ids_6.append(child.get_id())
        
        req_objects_6 = requirement_ids_6 + requirement_cat_ids_6
        '''check'''
        '''
        td_not_empty = False
        for s in step_requirement_ids_4_2:
            if (s):
                td_not_empty = True
        
        sd_not_empty = False
        for st in information_exchanged_ids_5:
            if (st):
                sd_not_empty = True
        '''
        
        
        if(requirement_ids_6[0] or requirement_cat_ids_6[0]):
            self.__tms.check_frequency(step_requirement_ids_4_2, req_objects_6, check_6)
        #if (not step_requirement_ids_4_2[0]):
        #    self._check_not_possible_msg("6", "Requirements (IDs)")
        if (not requirement_ids_6[0] and not requirement_cat_ids_6[0]):
            self._check_not_possible_msg("6", "6", "Requirement and Requirement Category")
            
        return usecase
    
    def check_rule_7(self, usecase ):
        """Rule 7 Implementation
        
        Args:
            usecase (UseCase): Use Case that has to be checked
            
        Returns:
            [UseCase]: Checked UseCase
        """
    # 7. Template Abschnitt 5 - Information Exchanged:
        check_7 = "7: " + "'" + "Req. ID" + "'" + " not found in existing Use Case " + "'" + "Requirement ID" + "'"
        '''create test objects'''
        information_exchanged_reqs_5 = []
        for child in usecase.get_information_exchanged_5():
            information_exchanged_reqs_5.append(child.get_requirement_id())
            
        requirement_ids_6= []
        for child in usecase.get_requirements_6():
            requirement_ids_6.append(child.get_id())
            
        requirement_cat_ids_6= []
        for child in usecase.get_requirements_category_6():
            requirement_cat_ids_6.append(child.get_id())
            
        req_objects_6 = requirement_ids_6 + requirement_cat_ids_6
        
        td_not_empty = False
        for s in information_exchanged_reqs_5:
            if (s):
                td_not_empty = True
                
        sd_not_empty = False
        for st in req_objects_6:
            if (st):
                sd_not_empty = True
        '''check'''
        if(td_not_empty and sd_not_empty):
            self.__tms.check_frequency(information_exchanged_reqs_5, req_objects_6, check_7)
        if (not td_not_empty):
            self._check_not_possible_msg("7", "5", "Req. ID")
        if (not sd_not_empty):
            self._check_not_possible_msg("7", "6", "Requirement and Requirement Category")    
        
        return usecase
    
    # 8. Template Abschnitt 1.4 - Narrativ of Use Case:
    def check_rule_8(self, usecase):
        """Rule 8 Implementation
        
        Args:
            usecase (UseCase): Use Case that has to be checked
            
        Returns:
            [UseCase]: Checked UseCase
        """
        check_8 = "8: " + "'" + "Actor name" + "'" + " not found in existing Use Case " + "'" + "Complete description" + "'"
        '''create test objects'''
        actor_names_3_1 = []
        for child in usecase.get_actor_grouping_3_1():
            for actor in child.get_actors_objects():
                actor_names_3_1.append(actor.get_name())
            
        complete_descriptions_1_4 =[]
        for child in usecase.get_narrative_1_4():
            complete_descriptions_1_4.append(child.get_complete_description())
            
        td_not_empty = False
        for s in actor_names_3_1:
            if (s):
                td_not_empty = True
        
        sd_not_empty = False
        for st in complete_descriptions_1_4:
            if (st):
                sd_not_empty = True
        '''check'''
        if(td_not_empty and sd_not_empty):
            self.__tms.check_frequency(actor_names_3_1, complete_descriptions_1_4, check_8)
        if (not td_not_empty):
            self._check_not_possible_msg("8", "3.1", "Actor name")
        if (not sd_not_empty):
            self._check_not_possible_msg("8", "1.4", "Complete description")   
        
        return usecase
    
    def check_rule_9(self, usecase):
        """Rule 9 Implementation
        
        Args:
            usecase (UseCase): Use Case that has to be checked
            
        Returns:
            [UseCase]: Checked UseCase
        """
        check_9 = "9: " + "'" + "Reference - No." + "'" + " not found in existing Use Case " + "'" + "Complete description" + "'"
        '''create test objects'''
        reference_names_3_2 = []
        for child in usecase.get_references_3_2():
            reference_names_3_2.append(child.get_name())
            
        complete_descriptions_1_4 =[]
        for child in usecase.get_narrative_1_4():
            complete_descriptions_1_4.append(child.get_complete_description())
            
        
        td_not_empty = False
        for s in reference_names_3_2:
            if (s):
                td_not_empty = True
        
        sd_not_empty = False
        for st in complete_descriptions_1_4:
            if (st):
                sd_not_empty = True
        '''check'''
        if(td_not_empty and sd_not_empty):
            self.__tms.check_frequency(reference_names_3_2, complete_descriptions_1_4, check_9)
        if (not td_not_empty):
            self._check_not_possible_msg("9", "3.2", "Reference - No.")
        if (not sd_not_empty):
            self._check_not_possible_msg("9", "1.4", "Complete description") 
        
        return usecase
    
    def check_rule_10(self, usecase):
        """Rule 10 Implementation
        
        Args:
            usecase (UseCase): Use Case that has to be checked
            
        Returns:
            [UseCase]: Checked UseCase
        """
    # 10. Template Abschnitt 1.7 - Further Information to the Use Case for Classification\Mapping:
        check_10 = '10: check_keywords extracted by complete_description + scenario_description + process_description'
        '''create test objects'''
        
        complete_descriptions_1_4 =[]
        for child in usecase.get_narrative_1_4():
            complete_descriptions_1_4.append(child.get_complete_description())
        
        scenario_descriptions_4_1 = []
        for scenario in usecase.get_scenarios_4_1():
            scenario_descriptions_4_1.append(scenario.get_description())
        
        step_process_descriptions_4_2 = []
        for step in usecase.get_steps_4_2():
            step_process_descriptions_4_2.append(step.get_process_description())
        
        keywords_testdata = complete_descriptions_1_4 + scenario_descriptions_4_1 + step_process_descriptions_4_2
        
        td_not_empty = False
        for s in keywords_testdata:
            if (s):
                td_not_empty = True
            
        keywords_1_7 = []
        for child in usecase.get_further_infos_1_7():
            keywords_1_7.append(child.get_further_keywords())
            
        sd_not_empty = False
        for st in keywords_1_7:
            if (st):
                sd_not_empty = True
        '''check'''
        if(td_not_empty and sd_not_empty):
            self.__tms.check_keywords(keywords_testdata, keywords_1_7, check_10)
        else:
            self._check_not_possible_msg("10", "0", "Complete description, Scenario description, Description of process/activity")
        if (not sd_not_empty):
            self._check_not_possible_msg("10", "1.7", "Further keywords for classiﬁcation")

        return usecase
    
    def check_rule_11(self, usecase):
        """Rule 11 Implementation
        
        Args:
            usecase (UseCase): Use Case that has to be checked
            
        Returns:
            [UseCase]: Checked UseCase
        """
    # 11. Template Abschnitt 4.1 - Overview of scenarios
        check_11 = "11: " + "'" + "Primary actor" + "'" + " not found in existing Use Case " + "'" + "Actor name" + "'"
        '''create test objects'''
        scenario_primary_actors_4_1 = []
        for scenario in usecase.get_scenarios_4_1():
            scenario_primary_actors_4_1.append(scenario.get_primary_actor())
        
        actor_names_3_1 = []
        for child in usecase.get_actor_grouping_3_1():
            for actor in child.get_actors_objects():
                actor_names_3_1.append(actor.get_name())
                
        td_not_empty = False
        for s in scenario_primary_actors_4_1:
            if (s):
                td_not_empty = True
        
        sd_not_empty = False
        for st in actor_names_3_1:
            if (st):
                sd_not_empty = True
        '''check'''
                
        if(td_not_empty and sd_not_empty):
            self.__tms.check_frequency(scenario_primary_actors_4_1, actor_names_3_1, check_11)
        if (not td_not_empty):
            self._check_not_possible_msg("11", "4.1", "Primary actor")
        if (not sd_not_empty):
            self._check_not_possible_msg("11", "3.1", "Actor name") 
        
        return usecase
    
    def check_rule_12(self, usecase):
        """Rule 12 Implementation
        
        Args:
            usecase (UseCase): Use Case that has to be checked
            
        Returns:
            [UseCase]: Checked UseCase
        """
        #check_12 = '12: scenario has steps'
        #for scenario in usecase.get_scenarios_4_1():
        print("------ FINDINGS Rule: 12 ------" + '\n')
        self.__tms.write_output_file("------ FINDINGS Rule: 12 ------" + '\n')
        
        '''check scenarios exists'''
        scenario_names = []
        for scenario in usecase.get_scenarios_4_1():
            scenario_names.append(scenario.get_name())
            
        td_not_empty = False
        for s in scenario_names:
            if (s):
                td_not_empty = True
        
        if (not td_not_empty):
            self._check_not_possible_msg("12", "4.1", "Scenario name") 

        else:
            for scenario in usecase.get_scenarios_4_1():
                steps = scenario.get_steps()
                if (not (steps[0].get_event() and steps[0].get_number() and steps[0].get_process_name())):
                    scenario.get_name()[0].get_meta_data().set_validity(False)
                    scenario.get_name()[0].get_meta_data().get_result_message().append("WARNING: Rule 12: 'Scenario' has no 'Step' !!!:" + '\n' + "Scenario name: " + scenario.get_name()[0].get_content() + "; section: 4.1 Steps – Scenarios; sequence: 0" + "; element: " + str(scenario.get_name()[0].get_meta_data().get_element_number()) +"; sentence: 0")
                    print("WARNING: Rule 12: 'Scenario' has no 'Step' !!!:" + '\n' + "Scenario name: " + scenario.get_name()[0].get_content() + "; section: 4.1 Steps – Scenarios; sequence: 0" + "; element: " + str(scenario.get_name()[0].get_meta_data().get_element_number()) +"; sentence: 0" + '\n')
                    self.__tms.write_output_file("WARNING: Rule 12: 'Scenario' has no 'Step' !!!:" + '\n' + "Scenario name: " + scenario.get_name()[0].get_content() + "; section: 4.1 Overview of Scenarios; sequence: 0" + "; element: " + str(scenario.get_name()[0].get_meta_data().get_element_number()) +"; sentence: 0" + '\n')

        
        return usecase
                
    # 13. Template Abschnitt 4.2 - Steps - Scenario
    def check_rule_13(self, usecase):
        """Rule 13 Implementation
        
        Args:
            usecase (UseCase): Use Case that has to be checked
            
        Returns:
            [UseCase]: Checked UseCase
        """
        check_13 = "13: " + "'" + "Information producer (actor)" + "'" + " not found in existing Use Case " + "'" + "Actor name" + "'"
        '''create test objects'''
        step_information_producers_4_2 = []
        for step in usecase.get_steps_4_2():  
            step_information_producers_4_2.append(step.get_information_producer())
        
        actor_names_3_1 = []
        for child in usecase.get_actor_grouping_3_1():
            for actor in child.get_actors_objects():
                actor_names_3_1.append(actor.get_name())
                
        td_not_empty = False
        for s in step_information_producers_4_2:
            if (s):
                td_not_empty = True
        
        sd_not_empty = False
        for st in actor_names_3_1:
            if (st):
                sd_not_empty = True
                
        '''check'''
        if(td_not_empty and sd_not_empty):
            self.__tms.check_frequency(step_information_producers_4_2, actor_names_3_1, check_13)
        if (not td_not_empty):
            self._check_not_possible_msg("13", "4.2", "Information producer (actor)")
        if (not sd_not_empty):
            self._check_not_possible_msg("13", "3.1", "Actor name") 
        
        return usecase
    
    def check_rule_14(self, usecase):
        """Rule 14 Implementation
        
        Args:
            usecase (UseCase): Use Case that has to be checked
            
        Returns:
            [UseCase]: Checked UseCase
        """
        check_14 = "14: " + "'" + "Information receiver (actor)" + "'" + " not found in existing Use Case " + "'" + "Actor name" + "'"
        '''create test objects'''
        step_information_receivers_4_2 = []
        for step in usecase.get_steps_4_2():
            step_information_receivers_4_2.append(step.get_information_receiver())
        
        actor_names_3_1 = []
        for child in usecase.get_actor_grouping_3_1():
            for actor in child.get_actors_objects():
                actor_names_3_1.append(actor.get_name())
                
        td_not_empty = False
        for s in step_information_receivers_4_2:
            if (s):
                td_not_empty = True
        
        sd_not_empty = False
        for st in actor_names_3_1:
            if (st):
                sd_not_empty = True
        
        '''check'''
        if(td_not_empty and sd_not_empty):
            self.__tms.check_frequency(step_information_receivers_4_2, actor_names_3_1, check_14)
        if (not td_not_empty):
            self._check_not_possible_msg("14", "4.2" , "Information receiver (actor)")
        if (not sd_not_empty):
            self._check_not_possible_msg("14", "3.1" ,"Actor name") 
        
        return usecase
    
    # 15. Template Abschnitt 5 - Information Exchanged
    # not implemented yet!
    def check_rule_15(self, usecase1, usecase2):
        """Rule 15 Implementation
        
        Args:
            usecase1 (UseCase): Use Case that has to be checked
            usecase2 (UseCase): Use Case that has to be checked
            
        Returns:
            [UseCase]: Checked UseCase
        """
        check_15 = "15: "+"Use Case 2 Information Exchanged "+"'Req. ID'" + " differs from " + "Use Case 1 Information Exchanged "+"'Req. ID'"
                
        uc1_information_exchanged_reqs_5 = []
        for child in usecase1.get_information_exchanged_5():
            uc1_information_exchanged_reqs_5.append(child.get_requirement_id())
            
        uc2_information_exchanged_reqs_5 = []
        for child in usecase2.get_information_exchanged_5():
            uc2_information_exchanged_reqs_5.append(child.get_requirement_id())
            
        td_not_empty = False
        for s in uc1_information_exchanged_reqs_5:
            if (s):
                td_not_empty = True
                
        sd_not_empty = False
        for st in uc2_information_exchanged_reqs_5:
            if (st):
                sd_not_empty = True
        
        if (not sd_not_empty):
            self._check_not_possible_msg("15", "Use Case 2 - 5", "Req. ID")
        if (not td_not_empty):
            self._check_not_possible_msg("15", "Use Case 1 - 5", "Req. ID")
        
        
        if(td_not_empty and sd_not_empty):   
            uc2_requirements_6= []
            for child in usecase2.get_requirements_6():
                uc2_requirements_6.append(child.get_id())
        
            for child in usecase2.get_requirements_category_6():
                uc2_requirements_6.append(child.get_id())
            uc2_requirements_6_sentence_list = self.__tms.get_list_uc_sentences(uc2_requirements_6)
        
            counter = 0
            for uc1_io in usecase1.get_information_exchanged_5():
                uc1_io_name_sentence_list = uc1_io.get_name()
                uc1_io_req_sentence_list = uc1_io.get_requirement_id()
                #check that uc1 io_req exists in the requirements of uc2
                if type(uc1_io_req_sentence_list) is list:
                    for uc1_io_req_sentence in uc1_io_req_sentence_list:
                        if(uc1_io_req_sentence.get_content()):
                            #uc1 io req
                            uc1_io_req_txt = uc1_io_req_sentence.get_content()
                            #check if this req exists in uc2
                            if type(uc2_requirements_6_sentence_list) is list:
                                for uc2_requirements_sentence in uc2_requirements_6_sentence_list:
                                    if(uc2_requirements_sentence.get_content()):
                                        uc2_requirements_sentence_txt = uc2_requirements_sentence.get_content()
                                        if(uc1_io_req_txt == uc2_requirements_sentence_txt):
                                            #compare uc1 io's with uc2 io's
                                            ## get uc1 io's:
                                            if type(uc1_io_name_sentence_list) is list:
                                                for uc1_io_name_sentence in uc1_io_name_sentence_list:
                                                    if(uc1_io_name_sentence.get_content()):
                                                        uc1_io_name_txt = uc1_io_name_sentence.get_content()
                                                        ### get uc2 io's:
                                                        for uc2_io in usecase2.get_information_exchanged_5():
                                                            uc2_io_name_sentence_list = uc2_io.get_name()
                                                            uc2_io_req_sentence_list = uc2_io.get_requirement_id()
                                                            if type(uc2_io_name_sentence_list) is list:
                                                                for uc2_io_name_sentence in uc2_io_name_sentence_list:
                                                                    if(uc2_io_name_sentence.get_content()):
                                                                        uc2_io_name_txt = uc2_io_name_sentence.get_content()
                                                                        if(uc1_io_name_txt == uc2_io_name_txt):
                                                                            #compare mentioned requirements
                                                                            '''check'''
                                                                            counter = counter + 1
                                                                            if(counter == 1):
                                                                                print("------ " + "FINDINGS " + "Rule: " + str(15) + " ------" + '\n')
                                                                                self.__tms.write_output_file("------ " + "FINDINGS " + "Rule: " + str(15) + " ------" + '\n') 
                                                                            self.__tms.check_frequency([uc2_io_req_sentence_list], [uc1_io_req_sentence_list], check_15)
            if (counter ==0):
                self._check_not_possible_msg("15", "5 & 6", "Matching Io's and or Requirements")
        return usecase1
    
    # 16. Template Abschnitt 3.1 - Actors
    def check_rule_16(self, usecase):
        """Rule 16 Implementation
        
        Args:
            usecase (UseCase): Use Case that has to be checked
            
        Returns:
            [UseCase]: Checked UseCase
        """
        check_16 = "16: " + "'" + "Actor name" + "'" + " not found in existing Use Case " + "'" + "Section 4.1 and 4.2" + "'"
        '''create test objects'''
        actor_names_3_1 = []
        for child in usecase.get_actor_grouping_3_1():
            for actor in child.get_actors_objects():
                actor_names_3_1.append(actor.get_name())
        
        source_data_16 = []
        scenarios = usecase.get_scenarios_4_1()
        steps = usecase.get_steps_4_2()
        scenario_and_steps = scenarios + steps
        for section in scenario_and_steps:
            if(section):
                source_data_16.append(section.get_all_attributes())
        
        scenario_names = []
        for scenario in usecase.get_scenarios_4_1():
            scenario_names.append(scenario.get_name())
            
        step_numbers = []
        for step in usecase.get_steps_4_2():
            step_numbers.append(step.get_number())
        
        
        td_not_empty = False
        for s in actor_names_3_1:
            if (s):
                td_not_empty = True
        
        sd_not_empty = False
        for st in (scenario_names+step_numbers):
            if (st):
                sd_not_empty = True        
        
        '''check'''
        if(td_not_empty and sd_not_empty):
            self.__tms.check_frequency(actor_names_3_1, source_data_16, check_16)
        if(not td_not_empty):
            self._check_not_possible_msg("16", "3.1" ,"Actor name") 
        if(not sd_not_empty):
            self._check_not_possible_msg("16", "4.1 & 4.2" ,"Scenarios and Steps") 
        return usecase
    
    # 17. Template Abschnitt 3.2 - References
    def check_rule_17(self, usecase):
        """Rule 17 Implementation
        
        Args:
            usecase (UseCase): Use Case that has to be checked
            
        Returns:
            [UseCase]: Checked UseCase
        """
        check_17 = "17: " + "'" + "Reference - No." + "'" + " not found in existing Use Case " + "'" + "Document" + "'"
        '''create test objects'''
        reference_names_3_2 = []
        for child in usecase.get_references_3_2():
            reference_names_3_2.append(child.get_name())
        
        source_data_17 = []
        doc_without_references = [item for item in usecase.get_all_attributes() if item not in usecase.get_references_3_2()]
        for section in doc_without_references:
            if(section):
                source_data_17.append(section.get_all_attributes())
                
        td_not_empty = False
        for s in reference_names_3_2:
            if (s):
                td_not_empty = True
                
        '''check'''
        if(td_not_empty):
            self.__tms.check_frequency(reference_names_3_2, source_data_17, check_17)
        if(not td_not_empty):
            self._check_not_possible_msg("17", "1.7" ,"Reference - No.") 
        
        return usecase
    
    # 18. Template Abschnitt 5 - Information Exchanged
    def check_rule_18(self, usecase):
        """Rule 18 Implementation
        
        Args:
            usecase (UseCase): Use Case that has to be checked
            
        Returns:
            [UseCase]: Checked UseCase
        """
        check_18 = "18: " + "'" + "Inf. exchanged (IDs)" + "'" + " not found in existing Use Case " + "'" + "Inf. ID" + "'"
        '''create test objects'''
        step_informations_exchanged_4_2 = []
        for step in usecase.get_steps_4_2():        
            step_informations_exchanged_4_2.append(step.get_inf_exchanged_id())
            
        information_exchanged_ids_5 = []
        for child in usecase.get_information_exchanged_5():
            information_exchanged_ids_5.append(child.get_id())
        '''check'''
            
        
        td_not_empty = False
        for s in step_informations_exchanged_4_2:
            if (s):
                td_not_empty = True
        
        sd_not_empty = False
        for st in information_exchanged_ids_5:
            if (st):
                sd_not_empty = True        
        
        '''check'''
        if(td_not_empty and sd_not_empty):
            self.__tms.check_frequency(information_exchanged_ids_5, step_informations_exchanged_4_2, check_18)
        if(not td_not_empty):
            self._check_not_possible_msg("18", "4.2" ,"Inf. exchanged (IDs)") 
        if(not sd_not_empty):
            self._check_not_possible_msg("18", "5" ,"Inf. ID") 
        
    
        return usecase

    # 19. Template Abschnitt 6 - Requirements
    def check_rule_19(self, usecase):
        """Rule 19 Implementation
        
        Args:
            usecase (UseCase): Use Case that has to be checked
            
        Returns:
            [UseCase]: Checked UseCase
        """
        check_19 = "19: " + "'" + "Requirement ID" + "'" + " not found in existing Use Case " + "'" + "Req. ID" + "'"
        '''create test objects'''    
        requirement_ids_6= []
        for child in usecase.get_requirements_6():
            requirement_ids_6.append(child.get_id())
        
        requirement_cat_ids_6= []
        for child in usecase.get_requirements_category_6():
            requirement_cat_ids_6.append(child.get_id())
                    
        step_requirement_ids_4_2 = []
        for step in usecase.get_steps_4_2():        
            step_requirement_ids_4_2.append(step.get_requirements_ids())
        
        information_exchanged_reqs_5 = []
        for child in usecase.get_information_exchanged_5():
            information_exchanged_reqs_5.append(child.get_requirement_id())
        
        sourcedata_19 = step_requirement_ids_4_2 + information_exchanged_reqs_5
        
        if (requirement_ids_6[0]):
            self.__tms.check_frequency(requirement_ids_6, sourcedata_19, check_19)
        
        if (not requirement_ids_6[0] and requirement_cat_ids_6[0]):
            self.__tms.check_frequency(requirement_cat_ids_6, sourcedata_19, check_19)
            
        if (not requirement_ids_6[0] and not requirement_cat_ids_6[0]):
            self._check_not_possible_msg("19", "6", "Requirement and Requirement Category")
            
        return usecase

    # 20. Template Abschnitt 7 - Common terms and definitions:
    def check_rule_20(self, usecase):
        """Rule 20 Implementation
        
        Args:
            usecase (UseCase): Use Case that has to be checked
            
        Returns:
            [UseCase]: Checked UseCase
        """
        check_20 = "20: " + "'" + "Term" + "'" + " not found in existing Use Case " + "'" + "Document" + "'"
        '''create test objects'''
        terms_7 = []
        for child in usecase.get_glossary_7():
            terms_7.append(child.get_term())
        
        source_data_20 = []
        doc_without_terms = [item for item in usecase.get_all_attributes() if item not in usecase.get_glossary_7()]
        for section in doc_without_terms:
            if(section):
                source_data_20.append(section.get_all_attributes())
                
        td_not_empty = False
        for s in terms_7:
            if (s):
                td_not_empty = True
        '''check'''
        if(td_not_empty):
            self.__tms.check_frequency(terms_7, source_data_20, check_20)
        else:
            self._check_not_possible_msg("20", "7" ,"Term") 
            
        return usecase