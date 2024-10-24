# Checker bundle: xoscBundle

* Build version:  v1.0.0-rc.1
* Description:    OpenScenario checker bundle

## Parameters

* InputFile
* resultFile

## Checkers

### check_asam_xosc_xml_valid_xml_document

* Description: The given file to check must be a valid XML document.
* Addressed rules:
  * asam.net:xosc:1.0.0:xml.valid_xml_document

### check_asam_xosc_xml_root_tag_is_openscenario

* Description: The root element of a valid XML document must be OpenSCENARIO.
* Addressed rules:
  * asam.net:xosc:1.0.0:xml.root_tag_is_openscenario

### check_asam_xosc_xml_fileheader_is_present

* Description: Below the root element a tag with FileHeader must be defined.
* Addressed rules:
  * asam.net:xosc:1.0.0:xml.fileheader_is_present

### check_asam_xosc_xml_version_is_defined

* Description: The FileHeader tag must have the attributes revMajor and revMinor and of type unsignedShort.
* Addressed rules:
  * asam.net:xosc:1.0.0:xml.version_is_defined

### check_asam_xosc_xml_valid_schema

* Description: Input xml file must be valid according to the schema.
* Addressed rules:
  * asam.net:xosc:1.0.0:xml.valid_schema

### check_asam_xosc_reference_control_uniquely_resolvable_entity_references

* Description: Reference names must be unique
* Addressed rules:
  * asam.net:xosc:1.2.0:reference_control.uniquely_resolvable_entity_references

### check_asam_xosc_reference_control_resolvable_signal_id_in_traffic_signal_state_action

* Description: TrafficSignalStateAction:name -> Signal ID must exist within the given road network.
* Addressed rules:
  * asam.net:xosc:1.2.0:reference_control.resolvable_signal_id_in_traffic_signal_state_action

### check_asam_xosc_reference_control_resolvable_traffic_signal_controller_by_traffic_signal_controller_ref

* Description: The trafficSignalController according to the trafficSignalControllerRef property must exist within the scenarios RoadNetwork definition.
* Addressed rules:
  * asam.net:xosc:1.2.0:reference_control.resolvable_traffic_signal_controller_by_traffic_signal_controller_ref

### check_asam_xosc_reference_control_valid_actor_reference_in_private_actions

* Description: In a ManeuverGroup, if the defined action is a private action an actor must be defined.
* Addressed rules:
  * asam.net:xosc:1.2.0:reference_control.valid_actor_reference_in_private_actions

### check_asam_xosc_reference_control_resolvable_entity_references

* Description: A named reference in the EntityRef must be resolvable.
* Addressed rules:
  * asam.net:xosc:1.2.0:reference_control.resolvable_entity_references

### check_asam_xosc_reference_control_resolvable_variable_reference

* Description: The VariableDeclaration according to the variableRef property must exist within the ScenarioDefinition.
* Addressed rules:
  * asam.net:xosc:1.2.0:reference_control.resolvable_variable_reference

### check_asam_xosc_reference_control_resolvable_storyboard_element_reference

* Description: The attribute storyboardElementRef shall point to an existing element of the corresponding type and shall be uniquely resolvable.
* Addressed rules:
  * asam.net:xosc:1.2.0:reference_control.resolvable_storyboard_element_reference

### check_asam_xosc_reference_control_unique_element_names_on_same_level

* Description: Element names at each level shall be unique at that level.
* Addressed rules:
  * asam.net:xosc:1.2.0:reference_control.unique_element_names_on_same_level

### check_asam_xosc_parameters_valid_parameter_declaration_in_catalogs

* Description: All parameters used within a catalog shall be declared within their ParameterDeclaration in the same catalog, which sets a default value for each parameter.
* Addressed rules:
  * asam.net:xosc:1.2.0:parameters.valid_parameter_declaration_in_catalogs

### check_asam_xosc_data_type_allowed_operators

* Description: Expressions in OpenSCENARIO must only use the allowed operands.
* Addressed rules:
  * asam.net:xosc:1.2.0:data_type.allowed_operators

### check_asam_xosc_data_type_non_negative_transition_time_in_light_state_action

* Description: Expressions in OpenSCENARIO must only use the allowed operands.
* Addressed rules:
  * asam.net:xosc:1.2.0:data_type.non_negative_transition_time_in_light_state_action

### check_asam_xosc_positive_duration_in_phase

* Description: Expressions in OpenSCENARIO must only use the allowed operands.
* Addressed rules:
  * asam.net:xosc:1.2.0:data_type.positive_duration_in_phase
