# Checker bundle: xoscBundle

* Build version:  0.1.0
* Description:    ASAM OpenScenario XML checker bundle

## Parameters

* InputFile: The path of the input file.

## Checkers

### basic_xosc

* Description: Check if basic properties of input file are properly set
* Addressed rules:
  * asam.net:xosc:1.0.0:xml.valid_xml_document

### schema_xosc

* Description: Check if xml properties of input file are properly set
* Addressed rules:
  * asam.net:xosc:1.0.0:xml.valid_schema

### reference_xosc

* Description: Check if xml properties of input file are properly set
* Addressed rules:
  * asam.net:xosc:1.2.0:reference_control.uniquely_resolvable_entity_references
  * asam.net:xosc:1.2.0:reference_control.resolvable_signal_id_in_traffic_signal_state_action
  * asam.net:xosc:1.2.0:reference_control.resolvable_traffic_signal_controller_by_traffic_signal_controller_ref
  * asam.net:xosc:1.2.0:reference_control.valid_actor_reference_in_private_actions
  * asam.net:xosc:1.2.0:reference_control.resolvable_entity_references
  * asam.net:xosc:1.2.0:reference_control.resolvable_variable_reference
  * asam.net:xosc:1.2.0:reference_control.resolvable_storyboard_element_reference
  * asam.net:xosc:1.2.0:reference_control.unique_element_names_on_same_level

### parameters_xosc

* Description: Check if parameters properties of input file are properly set
* Addressed rules:
  * asam.net:xosc:1.2.0:parameters.valid_parameter_declaration_in_catalogs

### data_type_xosc

* Description: Check if data_type properties of input file are properly set
* Addressed rules:
  * asam.net:xosc:1.2.0:data_type.allowed_operators
  * asam.net:xosc:1.2.0:data_type.non_negative_transition_time_in_light_state_action
  * asam.net:xosc:1.2.0:data_type.positive_duration_in_phase
