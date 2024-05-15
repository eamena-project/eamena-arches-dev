from eamena.bulk_uploader import BulkUploadSheet
import json, uuid, re, urllib.request, sys

class HeritagePlaceBulkUploadSheet(BulkUploadSheet):

	def __prune(self, data):

		if isinstance(data, (list)):
			ret = []
			for item in data:
				newitem = self.__prune(item)
				if isinstance(newitem, (bool)):
					ret[key] = value
				else:
					if len(newitem) > 0:
						if newitem != 'x':
							ret.append(newitem)
			return ret
		if isinstance(data, (dict)):
			ret = {}
			for keyob in data.keys():
				key = str(keyob)
				value = self.__prune(data[key])
				if isinstance(value, (bool)):
					ret[key] = value
				else:
					if len(value) > 0:
						if value != 'x':
							ret[key] = value
			return ret
		return data

	def __parse_archaeological_assessment(self, index, uniqueid=''):

		if len(self._BulkUploadSheet__data[index]) == 1: # Support the old 'one item per line' style
			exceptions = ['SITE_FEATURE_FORM_TYPE', 'SITE_FEATURE_FORM_TYPE_CERTAINTY', 'SITE_FEATURE_SHAPE_TYPE', 'SITE_FEATURE_ARRANGEMENT_TYPE', 'SITE_FEATURE_NUMBER_TYPE', 'SITE_FEATURE_INTERPRETATION_TYPE', 'SITE_FEATURE_INTERPRETATION_NUMBER', 'SITE_FEATURE_INTERPRETATION_CERTAINTY', 'BUILT_COMPONENT_RELATED_RESOURCE', 'HP_RELATED_RESOURCE']
		else:
			c = len(self._BulkUploadSheet__data[index])
			for ii in range(0, c):
				i = (c - (ii + 1))
				item = self._BulkUploadSheet__data[index][i]
				if 'CULTURAL_PERIOD_TYPE' in item:
					if len(item['CULTURAL_PERIOD_TYPE'].strip()) > 0:
						continue
				if 'CULTURAL_SUBPERIOD_TYPE' in item:
					if len(item['CULTURAL_SUBPERIOD_TYPE'].strip()) > 0:
						if not('CULTURAL_SUBPERIOD_TYPE' in self._BulkUploadSheet__data[index][(i - 1)]):
							self._BulkUploadSheet__data[index][(i - 1)]['CULTURAL_SUBPERIOD_TYPE'] = ''
						if not('CULTURAL_SUBPERIOD_CERTAINTY' in self._BulkUploadSheet__data[index][(i - 1)]):
							self._BulkUploadSheet__data[index][(i - 1)]['CULTURAL_SUBPERIOD_CERTAINTY'] = ''
						newvalue = (self._BulkUploadSheet__data[index][(i - 1)]['CULTURAL_SUBPERIOD_TYPE'].split('|')) + (self._BulkUploadSheet__data[index][i]['CULTURAL_SUBPERIOD_TYPE'].split('|'))
						fixedvalue = []
						for value in newvalue:
							if value.strip() == '':
								continue
							fixedvalue.append(value)
						self._BulkUploadSheet__data[index][(i - 1)]['CULTURAL_SUBPERIOD_TYPE'] = ('|'.join(fixedvalue))
						self._BulkUploadSheet__data[index][i]['CULTURAL_SUBPERIOD_TYPE'] = ''
						newvalue = (self._BulkUploadSheet__data[index][(i - 1)]['CULTURAL_SUBPERIOD_CERTAINTY'].split('|')) + (self._BulkUploadSheet__data[index][i]['CULTURAL_SUBPERIOD_CERTAINTY'].split('|'))
						fixedvalue = []
						for value in newvalue:
							if value.strip() == '':
								continue
							fixedvalue.append(value)
						self._BulkUploadSheet__data[index][(i - 1)]['CULTURAL_SUBPERIOD_CERTAINTY'] = ('|'.join(fixedvalue))
						self._BulkUploadSheet__data[index][i]['CULTURAL_SUBPERIOD_CERTAINTY'] = ''
			exceptions = ['CULTURAL_SUBPERIOD_TYPE', 'CULTURAL_SUBPERIOD_CERTAINTY', 'SITE_FEATURE_FORM_TYPE', 'SITE_FEATURE_FORM_TYPE_CERTAINTY', 'SITE_FEATURE_SHAPE_TYPE', 'SITE_FEATURE_ARRANGEMENT_TYPE', 'SITE_FEATURE_NUMBER_TYPE', 'SITE_FEATURE_INTERPRETATION_TYPE', 'SITE_FEATURE_INTERPRETATION_NUMBER', 'SITE_FEATURE_INTERPRETATION_CERTAINTY', 'BUILT_COMPONENT_RELATED_RESOURCE', 'HP_RELATED_RESOURCE']
		unparsed = self.pre_parse(index, ['OVERALL_ARCHAEOLOGICAL_CERTAINTY_VALUE', 'OVERALL_SITE_MORPHOLOGY_TYPE', 'CULTURAL_PERIOD_TYPE', 'CULTURAL_PERIOD_CERTAINTY', 'CULTURAL_SUBPERIOD_TYPE', 'CULTURAL_SUBPERIOD_CERTAINTY', 'DATE_INFERENCE_MAKING_ACTOR', 'ARCHAEOLOGICAL_DATE_FROM__CAL_', 'ARCHAEOLOGICAL_DATE_TO__CAL_', 'BP_DATE_FROM', 'BP_DATE_TO', 'AH_DATE_FROM', 'AH_DATE_TO', 'SH_DATE_FROM', 'SH_DATE_TO', 'SITE_FEATURE_FORM_TYPE', 'SITE_FEATURE_FORM_TYPE_CERTAINTY', 'SITE_FEATURE_SHAPE_TYPE', 'SITE_FEATURE_ARRANGEMENT_TYPE', 'SITE_FEATURE_NUMBER_TYPE', 'SITE_FEATURE_INTERPRETATION_TYPE', 'SITE_FEATURE_INTERPRETATION_NUMBER', 'SITE_FEATURE_INTERPRETATION_CERTAINTY', 'BUILT_COMPONENT_RELATED_RESOURCE', 'HP_RELATED_RESOURCE', 'MATERIAL_CLASS', 'MATERIAL_TYPE', 'CONSTRUCTION_TECHNIQUE', 'MEASUREMENT_NUMBER', 'MEASUREMENT_UNIT', 'DIMENSION_TYPE', 'MEASUREMENT_SOURCE_TYPE', 'RELATED_GEOARCH_PALAEO'], exceptions)

		oacv = []
		osmt = []
		rel_geoarch = []
		periods = []
		cron = []
		site_features = []
		materials = []
		measurements = []

		for item in unparsed:

			oacv_item = item["OVERALL_ARCHAEOLOGICAL_CERTAINTY_VALUE"].strip()
			osmt_item = item["OVERALL_SITE_MORPHOLOGY_TYPE"].strip()
			geoarch_item = ''
			if "RELATED_GEOARCH_PALAEO" in item:
				geoarch_item = item["RELATED_GEOARCH_PALAEO"].strip()
			if len(oacv_item) > 0:
				oacv.append({"OVERALL_ARCHAEOLOGICAL_CERTAINTY_VALUE": oacv_item})
			if len(osmt_item) > 0:
				osmt.append({"OVERALL_SITE_MORPHOLOGY_TYPE": osmt_item})
			if len(geoarch_item) > 0:
				rel_geoarch.append(geoarch_item)

			# PERIODIZATION

			cp_actor = ''
			if 'DATE_INFERENCE_MAKING_ACTOR' in item:
				cp_actor = item["DATE_INFERENCE_MAKING_ACTOR"].strip()

			cp_type = item["CULTURAL_PERIOD_TYPE"].strip()
			cp_cert = item["CULTURAL_PERIOD_CERTAINTY"].strip()
			csp_type = item["CULTURAL_SUBPERIOD_TYPE"].split('|')
			csp_cert = item["CULTURAL_SUBPERIOD_CERTAINTY"].split('|')

			cp = {}
			if ((len(cp_cert) > 0) & (len(csp_cert) == len(csp_type))):
				if len(cp_type) > 0:
					cp['CULTURAL_PERIOD_TYPE'] = cp_type
				cp['CULTURAL_PERIOD_CERTAINTY'] = cp_cert
				subperiods = []
				for i in range(0, len(csp_type)):
					csp = {"CULTURAL_SUBPERIOD_TYPE": csp_type[i], "CULTURAL_SUBPERIOD_CERTAINTY": csp_cert[i]}
					subperiods.append(csp)
				if len(subperiods) > 0:
					cp['CULTURAL_SUBPERIOD'] = subperiods
				if len(cp_actor) > 0:
					cp['DATE_INFERENCE_MAKING_ACTOR_NAME'] = cp_actor
			if len(cp) > 0:
				periods.append(cp)

			# ABSOLUTE CHRONOLOGY

			a_date_from = ''
			a_date_to = ''
			bp_date_from = ''
			bp_date_to = ''
			ah_date_from = ''
			ah_date_to = ''
			sh_date_from = ''
			sh_date_to = ''
			if 'ARCHAEOLOGICAL_DATE_FROM__CAL_' in item:
				a_date_from = item["ARCHAEOLOGICAL_DATE_FROM__CAL_"].strip()
			if 'ARCHAEOLOGICAL_DATE_TO__CAL_' in item:
				a_date_to = item["ARCHAEOLOGICAL_DATE_TO__CAL_"].strip()
			if 'BP_DATE_FROM' in item:
				bp_date_from = item["BP_DATE_FROM"].strip()
			if 'BP_DATE_TO' in item:
				bp_date_to = item["BP_DATE_TO"].strip()
			if 'AH_DATE_FROM' in item:
				ah_date_from = item["AH_DATE_FROM"].strip()
			if 'AH_DATE_TO' in item:
				ah_date_to = item["AH_DATE_TO"].strip()
			if 'SH_DATE_FROM' in item:
				sh_date_from = item["SH_DATE_FROM"].strip()
			if 'SH_DATE_TO' in item:
				sh_date_to = item["SH_DATE_TO"].strip()
			a_cron = {}
			if len(a_date_from) > 0:
				a_cron["ARCHAEOLOGICAL_DATE_FROM__CAL_"] = a_date_from
			if len(a_date_to) > 0:
				a_cron["ARCHAEOLOGICAL_DATE_TO__CAL_"] = a_date_to
			if len(bp_date_from) > 0:
				a_cron["BP_DATE_FROM"] = bp_date_from
			if len(bp_date_to) > 0:
				a_cron["BP_DATE_TO"] = bp_date_to
			if len(ah_date_from) > 0:
				a_cron["AH_DATE_FROM"] = ah_date_from
			if len(ah_date_to) > 0:
				a_cron["AH_DATE_TO"] = ah_date_to
			if len(sh_date_from) > 0:
				a_cron["SH_DATE_FROM"] = sh_date_from
			if len(sh_date_to) > 0:
				a_cron["SH_DATE_TO"] = sh_date_to
			if len(a_cron) > 0:
				cron.append(a_cron)

			# SITE FEATURES

			sf = {"SITE_FEATURE_FORM": [], "SITE_FEATURE_INTERPRETATION": [], "BUILT_COMPONENT_RELATED_RESOURCE": [], "HP_RELATED_RESOURCE": []}

			if 'BUILT_COMPONENT_RELATED_RESOURCE' in item:
				for bcr in item["BUILT_COMPONENT_RELATED_RESOURCE"].strip().split('|'):
					if len(bcr) == 0:
						continue
					sf["BUILT_COMPONENT_RELATED_RESOURCE"].append(bcr)
			if 'HP_RELATED_RESOURCE' in item:
				for hpr in item["HP_RELATED_RESOURCE"].strip().split('|'):
					if len(hpr) == 0:
						continue
					sf['HP_RELATED_RESOURCE'].append(hpr)

			sf_int_type = item["SITE_FEATURE_INTERPRETATION_TYPE"].split('|')
			sf_int_num = []
			if item["SITE_FEATURE_INTERPRETATION_NUMBER"].strip() != '':
				sf_int_num = item["SITE_FEATURE_INTERPRETATION_NUMBER"].split('|')
			if item["SITE_FEATURE_INTERPRETATION_TYPE"].strip() != '':
				sf_int_type = item["SITE_FEATURE_INTERPRETATION_TYPE"].split('|')
			sf_int_cert = item["SITE_FEATURE_INTERPRETATION_CERTAINTY"].split('|')
			if ((len(sf_int_type) == len(sf_int_num)) & (len(sf_int_num) == len(sf_int_cert)) & (len(sf_int_num) > 0)):
				for i in range(0, len(sf_int_num)):
					sf["SITE_FEATURE_INTERPRETATION"].append({"SITE_FEATURE_INTERPRETATION_TYPE": sf_int_type[i], "SITE_FEATURE_INTERPRETATION_NUMBER": sf_int_num[i], "SITE_FEATURE_INTERPRETATION_CERTAINTY": sf_int_cert[i]})

			sff_type = item["SITE_FEATURE_FORM_TYPE"].split('|')
			sff_cert = item["SITE_FEATURE_FORM_TYPE_CERTAINTY"].split('|')
			sff_shape = item["SITE_FEATURE_SHAPE_TYPE"].split('|')
			sff_arr = item["SITE_FEATURE_ARRANGEMENT_TYPE"].split('|')
			sff_num = item["SITE_FEATURE_NUMBER_TYPE"].split('|')
			if ((len(sff_type) == len(sff_cert)) & (len(sff_cert) == len(sff_shape)) & (len(sff_shape) == len(sff_arr)) & (len(sff_arr) == len(sff_num)) & (len(sff_num) > 0)):
				for i in range(0, len(sff_num)):
					sf["SITE_FEATURE_FORM"].append({"SITE_FEATURE_FORM_TYPE": sff_type[i], "SITE_FEATURE_FORM_TYPE_CERTAINTY": sff_cert[i], "SITE_FEATURE_SHAPE_TYPE": [{"SITE_FEATURE_SHAPE_TYPE": sff_shape[i]}], "SITE_FEATURE_ARRANGEMENT_TYPE": [{"SITE_FEATURE_ARRANGEMENT_TYPE": sff_arr[i]}], "SITE_FEATURE_NUMBER_TYPE": [{"SITE_FEATURE_NUMBER_TYPE": sff_num[i]}]})

			if not((len(sf["BUILT_COMPONENT_RELATED_RESOURCE"]) == 0) & (len(sf["SITE_FEATURE_FORM"]) == 0) & (len(sf["HP_RELATED_RESOURCE"]) == 0) & (len(sf["SITE_FEATURE_INTERPRETATION"]) == 0)):
				site_features.append(sf)

			# MATERIALS

			m_class = ''
			m_type = ''
			m_tech = ''
			if "MATERIAL_CLASS" in item:
				m_class = item["MATERIAL_CLASS"].strip()
			if "MATERIAL_TYPE" in item:
				m_type = item["MATERIAL_TYPE"].strip()
			if "CONSTRUCTION_TECHNIQUE" in item:
				m_tech = item["CONSTRUCTION_TECHNIQUE"].strip()
			material = {}
			if len(m_class) > 0:
				material["MATERIAL_CLASS"] = m_class
			if len(m_type) > 0:
				material["MATERIAL_TYPE"] = m_type
			if len(m_tech) > 0:
				material["CONSTRUCTION_TECHNIQUE"] = m_tech
			if len(material) > 0:
				materials.append(material)

			# MEASUREMENTS

			m_num = ''
			m_unit = ''
			m_dum = ''
			if 'MEASUREMENT_NUMBER' in item:
				m_num = item["MEASUREMENT_NUMBER"].strip()
			if 'MEASUREMENT_UNIT' in item:
				m_unit = item["MEASUREMENT_UNIT"].strip()
			if 'DIMENSION_TYPE' in item:
				m_dim = item["DIMENSION_TYPE"].strip()
			if 'MEASUREMENT_SOURCE_TYPE' in item:
				m_source = item["MEASUREMENT_SOURCE_TYPE"].strip()
			measurement = {}
			if (len(m_num) > 0):
				try:
					m_num_float = float(m_num)
				except:
					self.error(uniqueid, "Error in Measurements", "'" + str(m_num) + "' is not a valid measurement, a measurement must be a single number with no additional information.")
				measurement["MEASUREMENT_NUMBER"] = m_num
			if ((len(m_unit) > 0) & (len(m_dim) > 0) & (len(m_source) > 0)):
				measurement["MEASUREMENT_UNIT"] = m_unit
				measurement["DIMENSION_TYPE"] = m_dim
				measurement["MEASUREMENT_SOURCE_TYPE"] = m_source
			else:
				if not(((len(m_unit) == 0) & (len(m_dim) == 0) & (len(m_source) == 0))):
					self.error(uniqueid, "Error in Measurements.", "A valid measurement contains a Measurement Source Type, a Measurement Unit and a Dimension Type.")
			if len(measurement) > 0:
				measurements.append(measurement)

		return {"ARCHAEOLOGICAL_CERTAINTY_OBSERVATION": oacv, "OVERALL_SITE_MORPHOLOGY_TYPE": osmt, "PERIODIZATION": periods, "ABSOLUTE_CHRONOLOGY": cron, "SITE_FEATURES": site_features, "MATERIAL": materials, "MEASUREMENTS": measurements, "RELATED_GEOARCH_PALAEO": rel_geoarch}

	def __parse_condition_assessment(self, index, uniqueid=''):

		exceptions = ['EFFECT_TYPE', 'EFFECT_CERTAINTY']
		if len(self._BulkUploadSheet__data[index]) == 1: # Support the old 'one item per line' style
			exceptions = []

		unparsed = self.pre_parse(index, ['OVERALL_CONDITION_STATE', 'DAMAGE_EXTENT_TYPE', 'DISTURBANCE_CAUSE_CATEGORY_TYPE', 'DISTURBANCE_CAUSE_TYPE', 'DISTURBANCE_CAUSE_CERTAINTY', 'DISTURBANCE_DATE_FROM', 'DISTURBANCE_DATE_TO', 'DISTURBANCE_DATE_OCCURRED_BEFORE', 'DISTURBANCE_DATE_OCCURRED_ON', 'DISTURBANCE_CAUSE_ASSIGNMENT_ASSESSOR_NAME', 'EFFECT_TYPE', 'EFFECT_CERTAINTY', 'THREAT_CATEGORY', 'THREAT_TYPE', 'THREAT_PROBABILITY', 'THREAT_INFERENCE_MAKING_ASSESSOR_NAME', 'INTERVENTION_ACTIVITY_TYPE', 'RECOMMENDATION_TYPE', 'PRIORITY_TYPE', 'RELATED_DETAILED_CONDITION_RESOURCE'], exceptions)
		states = []
		types = []
		disturbances = []
		threats = []
		plans = []
		dcr = []

		for item in unparsed:

			rel_cr = ''
			overall_condition_state = item["OVERALL_CONDITION_STATE"].strip()
			damage_extent_type = item["DAMAGE_EXTENT_TYPE"].strip()
			if 'RELATED_DETAILED_CONDITION_RESOURCE' in item:
				rel_cr = item["RELATED_DETAILED_CONDITION_RESOURCE"].strip()

			if len(overall_condition_state) > 0:
				states.append(overall_condition_state)
			if len(damage_extent_type) > 0:
				types.append({"DAMAGE_EXTENT_TYPE": damage_extent_type})
			if len(rel_cr) > 0:
				dcr.append(rel_cr)

			dc_cat_type = item["DISTURBANCE_CAUSE_CATEGORY_TYPE"].strip()
			dc_type = item["DISTURBANCE_CAUSE_TYPE"].strip()
			dc_certainty = item["DISTURBANCE_CAUSE_CERTAINTY"].strip()
			d_date_from = item["DISTURBANCE_DATE_FROM"].strip()
			d_date_to = item["DISTURBANCE_DATE_TO"].strip()
			d_date_before = item["DISTURBANCE_DATE_OCCURRED_BEFORE"].strip()
			d_date_on = item["DISTURBANCE_DATE_OCCURRED_ON"].strip()
			dd_name = item["DISTURBANCE_CAUSE_ASSIGNMENT_ASSESSOR_NAME"].strip()
			eff_type = item["EFFECT_TYPE"]
			eff_certainty = item["EFFECT_CERTAINTY"]
			t_cat = item["THREAT_CATEGORY"].strip()
			t_type = item["THREAT_TYPE"].strip()
			t_prob = item["THREAT_PROBABILITY"].strip()
			t_name = ''
			int_act_type = ''
			rec_type = ''
			priority = ''
			if 'THREAT_INFERENCE_MAKING_ASSESSOR_NAME' in item:
				t_name = item["THREAT_INFERENCE_MAKING_ASSESSOR_NAME"].strip()
			if 'INTERVENTION_ACTIVITY_TYPE' in item:
				int_act_type = item["INTERVENTION_ACTIVITY_TYPE"].strip()
			if 'RECOMMENDATION_TYPE' in item:
				rec_type = item["RECOMMENDATION_TYPE"].strip()
			if 'PRIORITY_TYPE' in item:
				priority = item["PRIORITY_TYPE"].strip()

			if ((len(eff_type) > 0) & (len(eff_certainty) > 0) & (len(dc_type) > 0) & (len(dc_certainty) > 0)):
				eff_types = eff_type.split('|')
				eff_certs = eff_certainty.split('|')
				if (len(eff_certs) != len(eff_types)):

					self.error(uniqueid, "Cannot map effect types to certainties.", "There should be the same number of each. Please check the Effect Type and Effect Certainty columns for stray pipe (|) characters and leading/trailing spaces.")

				else:

					if ((len(dc_type) > 0) & (len(dc_certainty) == 0)):
						self.error(uniqueid, "Invalid Disturbance Data", "Item contains a Disturbance Cause Type but no Disturbance Cause Type Certainty.")
					if ((len(dc_type) == 0) & (len(dc_certainty) > 0)):
						self.error(uniqueid, "Invalid Disturbance Data", "Item contains a Disturbance Cause Type Certainty but no Disturbance Cause Type.")

					dist = {"EFFECTS": []}

					dist["DISTURBANCE_CAUSE_ASSIGNMENT"] = {}
					dist["DISTURBANCE_CAUSE_ASSIGNMENT"]["DAMAGE_OBSERVATION"] = []
					if len(dc_cat_type) > 0:
						dist["DISTURBANCE_CAUSE_CATEGORY_TYPE"] = dc_cat_type
					if len(dc_type) > 0:
						dist["DISTURBANCE_CAUSE_ASSIGNMENT"]["DISTURBANCE_CAUSE_TYPE"] = dc_type
					if len(dc_certainty) > 0:
						dist["DISTURBANCE_CAUSE_ASSIGNMENT"]["DISTURBANCE_CAUSE_CERTAINTY"] = dc_certainty
					if len(d_date_from) > 0:
						dist["DISTURBANCE_CAUSE_ASSIGNMENT"]["DISTURBANCE_DATE_FROM"] = d_date_from
					if len(d_date_to) > 0:
						dist["DISTURBANCE_CAUSE_ASSIGNMENT"]["DISTURBANCE_DATE_TO"] = d_date_to
					if len(d_date_before) > 0:
						dist["DISTURBANCE_CAUSE_ASSIGNMENT"]["DISTURBANCE_DATE_OCCURRED_BEFORE"] = d_date_before
					if len(d_date_on) > 0:
						dist["DISTURBANCE_CAUSE_ASSIGNMENT"]["DISTURBANCE_DATE_OCCURRED_ON"] = d_date_on
					if len(dd_name) > 0:
						dist["DISTURBANCE_CAUSE_ASSIGNMENT"]["DISTURBANCE_CAUSE_ASSIGNMENT_ASSESSOR_NAME"] = dd_name

					for i in range(0, len(eff_types)):
						effect = {"EFFECT_TYPE": eff_types[i], "EFFECT_CERTAINTY": eff_certs[i]}
						dist["DISTURBANCE_CAUSE_ASSIGNMENT"]["DAMAGE_OBSERVATION"].append(effect)

					disturbances.append(dist)

			if ((len(t_type) > 0) & (len(t_prob) == 0)):
				self.error(uniqueid, "Invalid Threat Data", "Item contains a Threat Type '" + t_type + "' but no Threat Type Probability.")
			if ((len(t_type) == 0) & (len(t_prob) > 0)):
				self.error(uniqueid, "Invalid Threat Data", "Item contains a Threat Type Probability '" + t_prob + "' but no Threat Type.")
			if ((len(t_type) > 0) & (len(t_prob) > 0)):
				threat = {"THREAT_TYPE": t_type, "THREAT_PROBABILITY": t_prob}
				if len(t_cat) > 0:
					threat["THREAT_CATEGORY"] = t_cat
				if len(t_name) > 0:
					threat["THREAT_INFERENCE_MAKING_ASSESSOR_NAME"] = t_name
				threats.append(threat)

			rec = {}
			if len(int_act_type) > 0:
				rec["INTERVENTION_ACTIVITY_TYPE"] = int_act_type
			if len(rec_type) > 0:
				rec["RECOMMENDATION_TYPE"] = rec_type
			if len(priority) > 0:
				rec["PRIORITY_TYPE"] = priority
			if len(rec) > 0:
				plans.append(rec)

		return {"OVERALL_CONDITION_STATE": states, "ESTIMATED_DAMAGE_EXTENT": types, "DAMAGE_STATE": {"DISTURBANCE_EVENT": disturbances}, "THREATS": threats, "RECOMMENDATION_PLAN": plans, "RELATED_DETAILED_CONDITION_RESOURCE": dcr}

	def __parse_environment_assessment(self, index, uniqueid=''):

		topography_type = []
		land_cover = []
		bedrock_geology = []
		surficial_geology = []
		marine_environment = []
		depth_elevation = []

		unparsed = self.pre_parse(index, ['TOPOGRAPHY_TYPE', 'LAND_COVER_TYPE', 'LAND_COVER_ASSESSMENT_DATE', 'SURFICIAL_GEOLOGY_TYPE', 'DEPOSITIONAL_PROCESS', 'BEDROCK_GEOLOGY', 'FETCH_TYPE', 'WAVE_CLIMATE', 'TIDAL_ENERGY', 'MINIMUM_DEPTH_MAX_ELEVATION_M_', 'MAXIMUM_DEPTH_MIN_ELEVATION_M_', 'DATUM_TYPE', 'DATUM_DESCRIPTION_EPSG_CODE'])

		for item in unparsed:

			top_type = item["TOPOGRAPHY_TYPE"].strip()
			bedrock_geo = item["BEDROCK_GEOLOGY"].strip()

			if len(top_type) > 0:
				topography_type.append(top_type)
			if len(bedrock_geo) > 0:
				bedrock_geology.append({"BEDROCK_GEOLOGY_TYPE": bedrock_geo})

			lc_type = item["LAND_COVER_TYPE"].strip()
			lc_ass_date = item["LAND_COVER_ASSESSMENT_DATE"].strip()
			lc = {}
			if (len(lc_type) > 0):
				lc['LAND_COVER_TYPE'] = lc_type
			if (len(lc_ass_date) > 0):
				lc['LAND_COVER_ASSESSMENT_DATE'] = lc_ass_date
			if len(lc) > 0:
				land_cover.append(lc)

			s_geo_type = item["SURFICIAL_GEOLOGY_TYPE"].strip()
			dep_proc = item["DEPOSITIONAL_PROCESS"].strip()
			s_geo = {}
			if (len(s_geo_type) > 0):
				s_geo['SURFICIAL_GEOLOGY_TYPE'] = s_geo_type
			if (len(dep_proc) > 0):
				s_geo['DEPOSITIONAL_PROCESS'] = dep_proc
			if len(s_geo) > 0:
				surficial_geology.append(s_geo)

			fetch_type = item["FETCH_TYPE"].strip()
			wave_climate = item["WAVE_CLIMATE"].strip()
			tidal_energy = item["TIDAL_ENERGY"].strip()
			marine_env = {}
			if (len(fetch_type) > 0):
				marine_env['FETCH_TYPE'] = fetch_type
			if (len(wave_climate) > 0):
				marine_env['WAVE_CLIMATE'] = wave_climate
			if (len(tidal_energy) > 0):
				marine_env['TIDAL_ENERGY'] = tidal_energy
			if (len(marine_env) > 0):
				marine_environment.append(marine_env)

			min_depth = item["MINIMUM_DEPTH_MAX_ELEVATION_M_"].strip()
			max_depth = item["MAXIMUM_DEPTH_MIN_ELEVATION_M_"].strip()
			datum_type = item["DATUM_TYPE"].strip()
			epsg_code = item["DATUM_DESCRIPTION_EPSG_CODE"].strip()
			depth_elev = {}
			if len(min_depth) > 0:
				depth_elev["MINIMUM_DEPTH_MAX_ELEVATION_M_"] = min_depth
			if len(max_depth) > 0:
				depth_elev["MAXIMUM_DEPTH_MIN_ELEVATION_M_"] = max_depth
			if len(datum_type) > 0:
				depth_elev["DATUM_TYPE"] = datum_type
			if len(epsg_code) > 0:
				depth_elev["DATUM_DESCRIPTION_EPSG_CODE"] = epsg_code
			if len(depth_elev):
				depth_elevation.append(depth_elev)

			topography = []
			for t in topography_type:
				topography.append({"TOPOGRAPHY_TYPE": t})

		return {"TOPOGRAPHY": topography, "LAND_COVER": land_cover, "GEOLOGY": {"BEDROCK_GEOLOGY": bedrock_geology, "SURFICIAL_GEOLOGY": surficial_geology}, "MARINE_ENVIRONMENT": marine_environment, "DEPTH_ELEVATION": depth_elevation}

	def __parse_geography(self, index, uniqueid=''):

		unparsed = self.pre_parse(index, ['SITE_OVERALL_SHAPE_TYPE', 'GRID_ID', 'COUNTRY_TYPE', 'CADASTRAL_REFERENCE', 'RESOURCE_ORIENTATION', 'ADDRESS', 'ADDRESS_TYPE', 'ADMINISTRATIVE_SUBDIVISION', 'ADMINISTRATIVE_SUBDIVISION_TYPE'])
		ret = {}

		address = []
		subdiv = []

		for item in unparsed:

			geog_sost = item["SITE_OVERALL_SHAPE_TYPE"].strip()
			geog_gid = item["GRID_ID"].strip()
			geog_ct = item["COUNTRY_TYPE"].strip()
			geog_cr = item["CADASTRAL_REFERENCE"].strip()
			geog_ro = item["RESOURCE_ORIENTATION"].strip()

			addr = {"ADDRESS": item['ADDRESS'].strip(), "ADDRESS_TYPE": item['ADDRESS_TYPE'].strip()}
			if len(addr['ADDRESS']) > 0:
				address.append(addr)

			sd = {"ADMINISTRATIVE_SUBDIVISION": item['ADMINISTRATIVE_SUBDIVISION'].strip(), "ADMINISTRATIVE_SUBDIVISION_TYPE": item['ADMINISTRATIVE_SUBDIVISION_TYPE'].strip()}
			if len(sd['ADMINISTRATIVE_SUBDIVISION']) > 0:
				subdiv.append(sd)

			if geog_sost != '':
				ret['SITE_OVERALL_SHAPE_TYPE'] = geog_sost
			if geog_gid != '':
				ret['GRID_ID'] = geog_gid
			if geog_ct != '':
				ret['COUNTRY_TYPE'] = geog_ct
			if geog_cr != '':
				ret['CADASTRAL_REFERENCE'] = geog_cr
			if geog_ro != '':
				ret['RESOURCE_ORIENTATION'] = geog_ro

		ret['ADDRESS'] = address
		ret['ADMINISTRATIVE_SUBDIVISION'] = subdiv

		return ret


	def __parse_geometries(self, index, uniqueid=''):

		unparsed = self.pre_parse(index, ['GEOMETRIC_PLACE_EXPRESSION', 'GEOMETRY_QUALIFIER', 'LOCATION_CERTAINTY', 'SITE_LOCATION_CERTAINTY', 'GEOMETRY_EXTENT_CERTAINTY'])
		ret = []

		for item in unparsed:

			if not('SITE_LOCATION_CERTAINTY' in item):
				item['SITE_LOCATION_CERTAINTY'] = ''
			if item["SITE_LOCATION_CERTAINTY"].strip() == '':
				item["SITE_LOCATION_CERTAINTY"] = item["LOCATION_CERTAINTY"]

			if item["GEOMETRIC_PLACE_EXPRESSION"].strip() == '':
				continue
			if item["SITE_LOCATION_CERTAINTY"].strip() == '':
				self.error(uniqueid, "Missing Location Certainty", "Record cannot have a geometry without a location certainty.")
				continue
			if item["GEOMETRY_EXTENT_CERTAINTY"].strip() == '':
				self.error(uniqueid, "Missing Extent Certainty", "Record cannot have a geometry without an extent certainty.")
				continue

			geom = {}
			geom["GEOMETRIC_PLACE_EXPRESSION"] = item["GEOMETRIC_PLACE_EXPRESSION"].strip()
			geom["SITE_LOCATION_CERTAINTY"] = item["SITE_LOCATION_CERTAINTY"].strip()
			geom["GEOMETRY_EXTENT_CERTAINTY"] = item["GEOMETRY_EXTENT_CERTAINTY"].strip()
			if item["GEOMETRY_QUALIFIER"].strip() != '':
				geom["GEOMETRY_QUALIFIER"] = item["GEOMETRY_QUALIFIER"].strip()
			ret.append(geom)

		return ret


	def __parse_resource_summary(self, index, uniqueid=''):

		unparsed = self.pre_parse(index, ['RESOURCE_NAME', 'NAME_TYPE', 'HERITAGE_PLACE_TYPE', 'GENERAL_DESCRIPTION_TYPE', 'GENERAL_DESCRIPTION', 'HERITAGE_PLACE_FUNCTION', 'HERITAGE_PLACE_FUNCTION_CERTAINTY', 'DESIGNATION', 'DESIGNATION_FROM_DATE', 'DESIGNATION_TO_DATE'])

		rs_type = []
		rs_resource_name = []
		rs_resource_desc = []
		rs_resource_class = []
		rs_resource_designation = []

		for item in unparsed:

			type = item["HERITAGE_PLACE_TYPE"].strip()
			name = item["RESOURCE_NAME"].strip()
			desc = item["GENERAL_DESCRIPTION"].strip()
			func = item["HERITAGE_PLACE_FUNCTION"].strip()
			desg = item["DESIGNATION"].strip()

			if len(type) > 0:
				rs_type.append(type)
			if len(name) > 0:
				value = {}
				value["RESOURCE_NAME"] = name
				if len(item["NAME_TYPE"].strip()) > 0:
					value["NAME_TYPE"] = item["NAME_TYPE"]
				rs_resource_name.append(value)
			if len(desc) > 0:
				value = {}
				value["GENERAL_DESCRIPTION"] = desc
				if len(item["GENERAL_DESCRIPTION_TYPE"].strip()) > 0:
					value["GENERAL_DESCRIPTION_TYPE"] = item["GENERAL_DESCRIPTION_TYPE"]
				rs_resource_desc.append(value)
			if len(func) > 0:
				value = {}
				value["HERITAGE_PLACE_FUNCTION"] = func
				if len(item["HERITAGE_PLACE_FUNCTION_CERTAINTY"].strip()) > 0:
					value["HERITAGE_PLACE_FUNCTION_CERTAINTY"] = item["HERITAGE_PLACE_FUNCTION_CERTAINTY"]
				else:
					self.error(uniqueid, "Heritage Place Function Certainty missing", "The entry contains a Heritage Place Function, but not a Heritage Place Function Certainty.")
				rs_resource_class.append(value)
			else:
				if len(item["HERITAGE_PLACE_FUNCTION_CERTAINTY"].strip()) > 0:
					self.error(uniqueid, "Heritage Place Function missing", "The entry contains a Heritage Place Function Certainty, but not a Heritage Place Function.")
			if len(desg) > 0:
				value = {}
				value["DESIGNATION"] = desg
				if len(item["DESIGNATION_FROM_DATE"].strip()) > 0:
					value["DESIGNATION_FROM_DATE"] = item["DESIGNATION_FROM_DATE"]
				if len(item["DESIGNATION_TO_DATE"].strip()) > 0:
					value["DESIGNATION_TO_DATE"] = item["DESIGNATION_TO_DATE"]
				rs_resource_designation.append(value)

		return{"RESOURCE_NAME": rs_resource_name,"HERITAGE_PLACE_TYPE": rs_type,"DESCRIPTION_ASSIGNMENT": rs_resource_desc,"HERITAGE_PLACE_ASSIGNMENT": rs_resource_class,"DESIGNATION": rs_resource_designation}

	def __parse_assessment_summary(self, index, uniqueid=''):

		unparsed = self.pre_parse(index, ['ASSESSMENT_INVESTIGATOR___ACTOR','INVESTIGATOR_ROLE_TYPE','ASSESSMENT_ACTIVITY_TYPE','ASSESSMENT_ACTIVITY_DATE','GE_ASSESSMENT_YES_NO_','GE_IMAGERY_ACQUISITION_DATE','INFORMATION_RESOURCE','INFORMATION_RESOURCE_USED','INFORMATION_RESOURCE_ACQUISITION_DATE'])
		activity_data = []
		activity = {}
		actor = ''
		role = ''
		for item in unparsed:

			if 'ASSESSMENT_INVESTIGATOR___ACTOR' in item:
				if len(item['ASSESSMENT_INVESTIGATOR___ACTOR']) > 0:
					actor = item['ASSESSMENT_INVESTIGATOR___ACTOR']
			if 'INVESTIGATOR_ROLE_TYPE' in item:
				if len(item['INVESTIGATOR_ROLE_TYPE']) > 0:
					role = item['INVESTIGATOR_ROLE_TYPE']

			act_type = item['ASSESSMENT_ACTIVITY_TYPE'].strip()
			act_date = item['ASSESSMENT_ACTIVITY_DATE'].strip()
			act_ge = 'No'
			if 'GE_ASSESSMENT_YES_NO_' in item:
				act_ge = item['GE_ASSESSMENT_YES_NO_'].strip()
			if 'GE_ASSESSMENT_YES_NO' in item:
				act_ge = item['GE_ASSESSMENT_YES_NO'].strip()
			if act_type != '':
				if len(activity) > 0:
					activity_data.append(activity)
				activity = {"GE_IMAGERY_ACQUISITION_DATE": [], "INFORMATION_RESOURCE_USED": []}
			if act_type != '':
				activity["ASSESSMENT_ACTIVITY_TYPE"] = act_type
			if act_date != '':
				activity["ASSESSMENT_ACTIVITY_DATE"] = act_date
			if act_ge != '':
				activity["GE_ASSESSMENT_YES_NO_"] = self.__boolean_cast(act_ge)

			act_ge_date = ''
			if 'GE_IMAGERY_ACQUISITION_DATE' in item:
				act_ge_date = item['GE_IMAGERY_ACQUISITION_DATE'].strip()
			act_infores = ''
			if 'INFORMATION_RESOURCE' in item:
				if item['INFORMATION_RESOURCE'] != '':
					act_infores = item['INFORMATION_RESOURCE'].strip()
			if 'INFORMATION_RESOURCE_USED' in item:
				if item['INFORMATION_RESOURCE_USED'] != '':
					act_infores = item['INFORMATION_RESOURCE_USED'].strip()
			act_infores_date = ''
			if 'INFORMATION_RESOURCE_ACQUISITION_DATE' in item:
				act_infores_date = item['INFORMATION_RESOURCE_ACQUISITION_DATE'].strip()

			if len(act_ge_date) > 0:
				if not('GE_IMAGERY_ACQUISITION_DATE' in activity):
					activity['GE_IMAGERY_ACQUISITION_DATE'] = []
				activity['GE_IMAGERY_ACQUISITION_DATE'].append(act_ge_date)
			if len(act_infores) > 0:
				infores = {"INFORMATION_RESOURCE_USED": act_infores}
				if len(act_infores_date) > 0:
					infores['INFORMATION_RESOURCE_ACQUISITION_DATE'] = act_infores_date
				if not('INFORMATION_RESOURCE_USED' in activity):
					activity['INFORMATION_RESOURCE_USED'] = []
				activity['INFORMATION_RESOURCE_USED'].append(infores)
			if len(actor) > 0:
				activity['ASSESSMENT_INVESTIGATOR___ACTOR'] = actor
			if len(role) > 0:
				activity['INVESTIGATOR_ROLE_TYPE'] = role

		if len(activity) > 0:
			activity_data.append(activity)

		return activity_data

	def __parse_access(self, index, uniqueid=''):

		unparsed = self.pre_parse(index, ['RESTRICTED_ACCESS_RECORD_DESIGNATION'])
		return {"RESTRICTED_ACCESS_RECORD_DESIGNATION": self.__boolean_cast(unparsed[0]["RESTRICTED_ACCESS_RECORD_DESIGNATION"])}

	def __parse_uid(self, index):

		unparsed = self.pre_parse(index, ['UNIQUEID'])
		if len(unparsed) == 0:
			return ''
		if not('UNIQUEID' in unparsed[0]):
			return ''
		return unparsed[0]["UNIQUEID"]

	def data(self, index):

		uid = self.__parse_uid(index)

		assessment_summary = self.__parse_assessment_summary(index, uid)
		resource_summary = self.__parse_resource_summary(index, uid)
		geometries = self.__parse_geometries(index, uid)
		geography = self.__parse_geography(index, uid)
		arc_assessment = self.__parse_archaeological_assessment(index, uid)
		cond_assessment = self.__parse_condition_assessment(index, uid)
		env_assessment = self.__parse_environment_assessment(index, uid)
		access = self.__parse_access(index, uid)

		ret = {}
		ret["_"] = uid
		ret["ASSESSMENT_SUMMARY"] = assessment_summary
		ret["RESOURCE_SUMMARY"] = resource_summary
		ret["GEOMETRIES"] = geometries
		ret["GEOGRAPHY"] = geography
		ret["ARCHAEOLOGICAL_ASSESSMENT"] = arc_assessment
		ret["CONDITION_ASSESSMENT"] = cond_assessment
		ret["ENVIRONMENT_ASSESSMENT"] = env_assessment
		#ret["ACCESS"] = access

		return self.__prune(ret)

	def __boolean_cast(self, text):
		t = str(text).lower()
		if t == 'yes':
			return True
		if t == '1':
			return True
		if t == 'true':
			return True
		if t == 'y':
			return True
		return False

	def __init__(self, filename, uidkey='UNIQUEID'):

		super().__init__(filename, uidkey)
		self.__required_fields = ["UNIQUEID", "ASSESSMENT_ACTIVITY_DATE","ASSESSMENT_ACTIVITY_TYPE","ASSESSMENT_INVESTIGATOR___ACTOR","COUNTRY_TYPE","CULTURAL_PERIOD_CERTAINTY","CULTURAL_SUBPERIOD_CERTAINTY","DAMAGE_EXTENT_TYPE","DIMENSION_TYPE","DISTURBANCE_CAUSE_CERTAINTY","DISTURBANCE_CAUSE_TYPE","EFFECT_CERTAINTY","EFFECT_TYPE","GEOMETRIC_PLACE_EXPRESSION","GEOMETRY_EXTENT_CERTAINTY","HERITAGE_PLACE_FUNCTION","HERITAGE_PLACE_FUNCTION_CERTAINTY","HERITAGE_PLACE_TYPE","INVESTIGATOR_ROLE_TYPE","MEASUREMENT_SOURCE_TYPE","MEASUREMENT_UNIT","OVERALL_ARCHAEOLOGICAL_CERTAINTY_VALUE","OVERALL_CONDITION_STATE","OVERALL_SITE_MORPHOLOGY_TYPE","SITE_FEATURE_ARRANGEMENT_TYPE","SITE_FEATURE_FORM_TYPE","SITE_FEATURE_FORM_TYPE_CERTAINTY","SITE_FEATURE_INTERPRETATION_CERTAINTY","SITE_FEATURE_INTERPRETATION_NUMBER","SITE_FEATURE_INTERPRETATION_TYPE","SITE_FEATURE_NUMBER_TYPE","SITE_FEATURE_SHAPE_TYPE","SITE_LOCATION_CERTAINTY","THREAT_PROBABILITY","THREAT_TYPE","TOPOGRAPHY_TYPE"]
		self.__errors = []
		for i in range(0, len(self._BulkUploadSheet__data)):
			for row in range(0, len(self._BulkUploadSheet__data[i])):
				for field in self.__required_fields:
					if field in self._BulkUploadSheet__data[i][row]:
						continue
					self._BulkUploadSheet__data[i][row][field] = ''
