from pymongo import MongoClient
from owlready2 import *

onto = get_ontology("http://www.w3.org/ns/prov-o#")
set_log_level(0) # to debug (0 - 9)

MONGODB_URL = "mongodb://localhost/"
client = MongoClient(MONGODB_URL)
db = client['elivestock']

listVacas = db["animal"]
listOnfarm = db["onfarm"]
listBalanca = db["balanca"]
listHumidity = db["humidity"]
listProdLeite = db["prodLeite"]
listTemperature  = db["temperature"]

exclusion_criteria = { "_id": 0, "__v": 0}

def factoryFind(brinco, listMongo):
    brinco_trace = str(brinco)+"-1"
    result = list(listMongo.find({"$or":[ {"brinco": brinco_trace}, {"brinco": str(brinco)}]}, exclusion_criteria))
    if result:
        return result[len(result) - 1]
    else:
        return None

def getAnimalOnFarm(brinco):
    return factoryFind(brinco, listOnfarm)
    
def getAnimalBalanca(brinco):
    return factoryFind(brinco, listBalanca)

def getAnimalProdLeite(brinco):
    return factoryFind(brinco, listProdLeite)

def getLotesWithMastitis():
    lotes = []
    list_lotes_with_mastitis = []

    for cow in listVacas.find({}, exclusion_criteria):
        lote_name = f"prov-o.{cow['lote'].replace(' ', '_')}"
        if lote_name in lotes:
            index = lotes.index(lote_name)
            list_lotes_with_mastitis[index]['count'] = list_lotes_with_mastitis[index]['count'] + 1 # add +1 cow
        else:
            lotes.append(lote_name)
            list_lotes_with_mastitis.append({'name': lote_name, 'count': 1, 'mastitis': 0})

    return list_lotes_with_mastitis    

def getAnimalsLotes(onto):
    list_cow = []
    list_lotes = getLotesWithMastitis()

    for cow in onto.individuals():
        class_name = str(cow.__class__).lower()
        if class_name == "new_provcow.cow":
            if cow.is_mastitis == 1:
                list_cow.append(cow)
        else:
            try:
                class_name = class_name.index('cow')
                if cow.is_mastitis == 1:
                    list_cow.append(cow)
            except Exception as e:
                pass
                

    for lote in list_lotes:
        for cow in list_cow:
            if lote['name'] == str(cow.batch):
                lote['mastitis'] = lote['mastitis'] + 1

    for lote in list_lotes:
        pct = round(lote['mastitis'] / lote['count'] * 100, 2)
        mastiti_warning = getMastiteWarning(pct)
        lote['name'] = lote['name'].replace("prov-o.", "").replace("_", " ")
        lote['pct'] = pct
        lote['warning'] = mastiti_warning
        
    return list_lotes

def getTempAndHumidity(onto):
    list_measure = []

    for measure in onto.individuals():
        class_name = str(measure.__class__).lower()
        if class_name == "new_provcow_ambiente.measure":
            if str(measure.measure_source).lower() == 'new_provcow_ambiente.sensor_t':
                list_measure.append({'measure_date':measure.measure_date, 'internal_measure_value': measure.internal_measure_value, 'external_measure_value': measure.external_measure_value, 'type': 'temperature'})
            elif str(measure.measure_source).lower() == 'new_provcow_ambiente.sensor_u':
                list_measure.append({'measure_date':measure.measure_date, 'internal_measure_value': measure.internal_measure_value, 'external_measure_value': measure.external_measure_value, 'type': 'humidity'})

    return list_measure

def getAnimalsPeso(onto):
    listWeight = []
    for cow in onto.individuals():
        class_name = str(cow.__class__).lower()
        if class_name.__contains__("supercow"):
            listWeight.append(cow.weight)
    return listWeight

def getMastiteWarning(pct):
    if pct == 0:
        return f"CLEAN BATCH - REPORT - no contaminated animals!"

    if pct >= 80:
        return f"EPIDEMIC - URGENT - {pct}% contaminated animals!"
    if pct >= 60:
        return f"CHANCE OF EPIDEMIC - SEVERE - {pct}% contaminated animals!"
    if pct >= 40:
        return f"WARNING DO INTERVENTION - SEVERE - {pct}% contaminated animals!"
    if pct >= 20:
        return f"WARNING - MEDIUM - {pct}% contaminated animals!"
    if pct >= 10:
        return f"WARNING - REPORT - {pct}% contaminated animals!"
    if pct < 10:
        return f"CONTROLLED - REPORT - only {pct}% contaminated animals!"

def createRules():
    humidity_rule = Imp()
    humidity_rule.set_as_rule("Measure(?m), internal_measure_value(?m, ?v), greaterThan(?v, 95) -> is_alert(?m, 1)")
    temperature_rule = Imp()
    temperature_rule.set_as_rule("Measure(?m), internal_measure_value(?m, ?v), greaterThan(?v, 23.5), lessThan(?v, 45) -> is_alert(?m, 1)")
    
    sickcow_rule = Imp()
    sickcow_rule.set_as_rule("Cow(?x), is_mastitis(?x, ?m), equal(?m, 1) -> SickCow(?x)")
    supercow_rule = Imp()
    supercow_rule.set_as_rule("Cow(?c), DairyMilk(?d), cow_milked(?d, ?cm), dairy_value(?d, ?v), greaterThan(?v, 30), is_mastitis(?c, ?m), equal(?m, 0), SameAs(?c, ?cm) -> SuperCow(?c)")

    temp_rule_1 = Imp()
    temp_rule_2 = Imp()
    temp_rule_3 = Imp()
    temp_rule_4 = Imp()
    temp_rule_5 = Imp()
    temp_rule_6 = Imp()
    temp_rule_7 = Imp()
    temp_rule_8 = Imp()
    temp_rule_9 = Imp()
    
    temp_rule_1.set_as_rule("Measure(?m), external_measure_value(?m, ?v), lessThan(?v, 16.0), subtract(?r, ?v, 1.98) -> internal_measure_value(?m, ?r)")
    temp_rule_2.set_as_rule("Measure(?m), external_measure_value(?m, ?v), greaterThan(?v, 17.0), lessThan(?v, 18.0), subtract(?r, ?v, 2.35) -> internal_measure_value(?m, ?r)")
    temp_rule_3.set_as_rule("Measure(?m), external_measure_value(?m, ?v), greaterThan(?v, 18.0), lessThan(?v, 19.0), subtract(?r, ?v, 1.72) -> internal_measure_value(?m, ?r)")
    temp_rule_4.set_as_rule("Measure(?m), external_measure_value(?m, ?v), greaterThan(?v, 19.0), lessThan(?v, 20.0), subtract(?r, ?v, 2.32) -> internal_measure_value(?m, ?r)")
    temp_rule_5.set_as_rule("Measure(?m), external_measure_value(?m, ?v), greaterThan(?v, 20.0), lessThan(?v, 21.0), subtract(?r, ?v, 2.13) -> internal_measure_value(?m, ?r)")
    temp_rule_6.set_as_rule("Measure(?m), external_measure_value(?m, ?v), greaterThan(?v, 21.0), lessThan(?v, 22.0), subtract(?r, ?v, 2.08) -> internal_measure_value(?m, ?r)")
    temp_rule_7.set_as_rule("Measure(?m), external_measure_value(?m, ?v), greaterThan(?v, 22.0), lessThan(?v, 23.0), subtract(?r, ?v, 2.00) -> internal_measure_value(?m, ?r)")
    temp_rule_8.set_as_rule("Measure(?m), external_measure_value(?m, ?v), greaterThan(?v, 23.0), lessThan(?v, 24.0), subtract(?r, ?v, 1.14) -> internal_measure_value(?m, ?r)")
    temp_rule_9.set_as_rule("Measure(?m), external_measure_value(?m, ?v), greaterThan(?v, 24.0), lessThan(?v, 45.0), subtract(?r, ?v, 2.18) -> internal_measure_value(?m, ?r)")
			
    hum_rule_1 = Imp()
    hum_rule_2 = Imp()
    hum_rule_3 = Imp()
    hum_rule_4 = Imp()
    hum_rule_5 = Imp()
    hum_rule_6 = Imp()
    hum_rule_7 = Imp()
    hum_rule_8 = Imp()
    hum_rule_9 = Imp()
    hum_rule_10 = Imp()
    hum_rule_11 = Imp()
    hum_rule_12 = Imp()
    hum_rule_13 = Imp()
    hum_rule_14 = Imp()
    hum_rule_15 = Imp()
    hum_rule_16 = Imp()
    hum_rule_17 = Imp()
    hum_rule_18 = Imp()
    hum_rule_19 = Imp()

    hum_rule_1.set_as_rule("Measure(?m), external_measure_value(?m, ?v), greaterThan(?v, 45), lessThan(?v, 68.0), add(?r, ?v, 27.27)  -> internal_measure_value(?m, ?r)")
    hum_rule_2.set_as_rule("Measure(?m), external_measure_value(?m, ?v), greaterThan(?v, 68), lessThan(?v, 69.0), add(?r, ?v, 21.84)  -> internal_measure_value(?m, ?r)")
    hum_rule_3.set_as_rule("Measure(?m), external_measure_value(?m, ?v), greaterThan(?v, 69), lessThan(?v, 72.0), add(?r, ?v, 21.63)  -> internal_measure_value(?m, ?r)")
    hum_rule_4.set_as_rule("Measure(?m), external_measure_value(?m, ?v), greaterThan(?v, 72), lessThan(?v, 73.0), add(?r, ?v, 26.21)  -> internal_measure_value(?m, ?r)")
    hum_rule_5.set_as_rule("Measure(?m), external_measure_value(?m, ?v), greaterThan(?v, 73), lessThan(?v, 74.0), add(?r, ?v, 21.37)  -> internal_measure_value(?m, ?r)")
    hum_rule_6.set_as_rule("Measure(?m), external_measure_value(?m, ?v), greaterThan(?v, 74), lessThan(?v, 75.0), add(?r, ?v, 19.62)  -> internal_measure_value(?m, ?r)")
    hum_rule_7.set_as_rule("Measure(?m), external_measure_value(?m, ?v), greaterThan(?v, 75), lessThan(?v, 76.0), add(?r, ?v, 17.32)  -> internal_measure_value(?m, ?r)")
    hum_rule_8.set_as_rule("Measure(?m), external_measure_value(?m, ?v), greaterThan(?v, 76), lessThan(?v, 77.0), add(?r, ?v, 15.67)  -> internal_measure_value(?m, ?r)")
    hum_rule_9.set_as_rule("Measure(?m), external_measure_value(?m, ?v), greaterThan(?v, 77), lessThan(?v, 78.0), add(?r, ?v, 13.12)  -> internal_measure_value(?m, ?r)")
    hum_rule_10.set_as_rule("Measure(?m), external_measure_value(?m, ?v), greaterThan(?v, 78), lessThan(?v, 79.0), add(?r, ?v, 12.95) -> internal_measure_value(?m, ?r)")
    hum_rule_11.set_as_rule("Measure(?m), external_measure_value(?m, ?v), greaterThan(?v, 79), lessThan(?v, 80.0), add(?r, ?v, 13.11) -> internal_measure_value(?m, ?r)")
    hum_rule_12.set_as_rule("Measure(?m), external_measure_value(?m, ?v), greaterThan(?v, 80), lessThan(?v, 81.0), add(?r, ?v, 15.90) -> internal_measure_value(?m, ?r)")
    hum_rule_13.set_as_rule("Measure(?m), external_measure_value(?m, ?v), greaterThan(?v, 81), lessThan(?v, 82.0), add(?r, ?v, 14.73) -> internal_measure_value(?m, ?r)")
    hum_rule_14.set_as_rule("Measure(?m), external_measure_value(?m, ?v), greaterThan(?v, 82), lessThan(?v, 83.0), add(?r, ?v, 13.61) -> internal_measure_value(?m, ?r)")
    hum_rule_15.set_as_rule("Measure(?m), external_measure_value(?m, ?v), greaterThan(?v, 83), lessThan(?v, 84.0), add(?r, ?v, 14.12) -> internal_measure_value(?m, ?r)")
    hum_rule_16.set_as_rule("Measure(?m), external_measure_value(?m, ?v), greaterThan(?v, 84), lessThan(?v, 87.0), add(?r, ?v, 13.23) -> internal_measure_value(?m, ?r)")
    hum_rule_17.set_as_rule("Measure(?m), external_measure_value(?m, ?v), greaterThan(?v, 87), lessThan(?v, 88.0), add(?r, ?v,  8.46) -> internal_measure_value(?m, ?r)")
    hum_rule_18.set_as_rule("Measure(?m), external_measure_value(?m, ?v), greaterThan(?v, 88), lessThan(?v, 89.0), add(?r, ?v,  8.64) -> internal_measure_value(?m, ?r)")
    hum_rule_19.set_as_rule("Measure(?m), external_measure_value(?m, ?v), greaterThan(?v, 89), lessThan(?v, 100.0), add(?r, ?v, 8.92) -> internal_measure_value(?m, ?r)")
			
            
		

def generateOntology(run_reasoner = False, save = True, run_sensor = False):

    with onto:
        class Activity(Thing): pass
        class Agent(Thing): pass
        class Entity(Thing): pass

        class DairyMilk(Activity): pass
        class Insemination(Activity): pass
        class Discard(Activity): pass
        class ProcessMilk(Activity): pass
        class Calving(Activity): pass
        class Measure(Activity): pass

        class Farmer(Agent): pass
        class Researcher(Agent): pass

        class Cow(Entity): pass
        class Batch(Entity): pass
        class Feed(Entity): pass
        class Bacteria(Entity): pass
        class Mastitis(Entity): pass
        class Sensor(Entity): pass

        class wasGeneratedBy(Entity >> Activity, FunctionalProperty): pass
        class used(Activity >> Entity, FunctionalProperty): pass
        class wasAttributedTo(Entity >> Agent, FunctionalProperty): pass
        class wasAssociatedWith(Activity >> Agent, FunctionalProperty): pass
        class wasDerivedFrom(Entity >> Entity, FunctionalProperty):  pass
        class wasInformedBy(Activity >> Activity, FunctionalProperty):  pass
        class actedBehalfOf(Agent >> Agent, FunctionalProperty):  pass

        class proccess_milk_date(ProcessMilk >> str, FunctionalProperty): pass
        class dairy_milk_date(DairyMilk >> str, FunctionalProperty): pass
        class dairy_value(DairyMilk >> float, FunctionalProperty): pass

        class cow_milked(DairyMilk >> Cow, FunctionalProperty): pass
        class was_discarted_by(DairyMilk >> Discard, FunctionalProperty): pass
        class was_processed(DairyMilk >> ProcessMilk, FunctionalProperty): pass

        #object-properties
        class was_milked(Cow >> DairyMilk, FunctionalProperty): pass
        class had_calving(Cow >> Calving, FunctionalProperty): pass
        class had_mastitis(Cow >> Mastitis, FunctionalProperty): pass    
        class had_bacteria_type(Cow >> Bacteria, FunctionalProperty): pass

        #data-properties
        class brinco(Cow >> str, FunctionalProperty): pass
        class dea(Cow >> float, FunctionalProperty): pass
        class days_lactation(Cow >> float, FunctionalProperty): pass
        class mastitis_grau(Cow >> str, FunctionalProperty): pass
        class is_mastitis(Cow >> int, FunctionalProperty): pass
        class weight(Cow >> float, FunctionalProperty): pass
        class level_production(Cow >> float, FunctionalProperty): pass

        class total_animals(Batch >> int, FunctionalProperty): pass    

        class leite(Cow >> float, FunctionalProperty): pass    
        class gram_type(Bacteria >> int, FunctionalProperty): pass

        class internal_measure_value(Measure >> float, FunctionalProperty): pass
        class external_measure_value(Measure >> float, FunctionalProperty): pass
        class measure_source(Measure >> Sensor, FunctionalProperty): pass
        class measure_date(Measure >> str, FunctionalProperty): pass 
        class measure_time(Measure >> str, FunctionalProperty): pass 
        class is_alert(Measure >> int, FunctionalProperty): pass 

        class is_clinical(Mastitis >> int, FunctionalProperty): pass
        class mastitis_date(Mastitis >> str, FunctionalProperty): pass
        class mastitis_origin(Mastitis >> Bacteria, FunctionalProperty): pass

        class sensor_unit(Sensor >> str, FunctionalProperty): pass

        class MeasureInmet(Measure):
            equivalent_to = [Sensor & sensor_unit.some(ConstrainedDatatype (str, length = 1))]

        class MeasureSensor(Measure):
            equivalent_to = [Sensor & sensor_unit.some(ConstrainedDatatype (str, length = 1))]

        class Humidity(Sensor):
            equivalent_to = [Sensor & sensor_unit.some(ConstrainedDatatype (str, length = 1))]
        class Temperature(Sensor):
            equivalent_to = [Sensor & sensor_unit.some(ConstrainedDatatype (str, length = 4))]
        
        class Clinical(Mastitis):
            equivalent_to = [Mastitis & (is_clinical >= 1) ]
        class SubClinical(Mastitis): 
            equivalent_to = [Mastitis & (is_clinical <= 0) ]
        class Contagious(Bacteria):
            equivalent_to = [Bacteria & (gram_type <= 0) ]
        class Environmental(Bacteria):
            equivalent_to = [Bacteria & (gram_type >= 1) ]

        class SuperCow(Cow): pass

        class SickCow(Cow): pass
        
        # createRules()
        
        def createBacteria(onFarm):
            if onFarm["strepUberis"] == "1":            
                # return Environmental("Streptococcus_uberis")
                return "Streptococcus_uberis"
            elif onFarm["klebsiellaEnterobacter"] == "1":            
                # return Environmental("Klebsiella_ssp")
                return "Klebsiella_ssp"
            elif onFarm["staphAureus"] == "1":
            #    return Contagious("Staphylococcus_aureus")
                return "Staphylococcus_aureus"
            elif onFarm["strepAgalactiaeDysgalactiae"] == "1":
            #    return Contagious("Streptococcus_Agalactiae_Dysgalactiae")
                return "Streptococcus_Agalactiae_Dysgalactiae"
            elif onFarm["gramPositiva"] == "1" or onFarm["outrosGramPositiva"] == "1":            
                # return Environmental("Ambiental")                        
                return "Ambiental"                     
            elif onFarm["gramNegativa"] == "1" or onFarm["outrosGramNegativa"] == "1":
            #    return Contagious("Contagiante")    
                return "Contagiante" 
            else:
                # return Bacteria('bacteria')
                return 'bacteria'

        def getTypeOfBacteria(onFarm):
            if onFarm["strepUberis"] == "1" or onFarm["klebsiellaEnterobacter"] == "1" or  onFarm["gramPositiva"] == "1" or onFarm["outrosGramPositiva"] == "1":
                return 1            
            elif onFarm["staphAureus"] == "1" or onFarm["strepAgalactiaeDysgalactiae"] == "1" or onFarm["gramNegativa"] == "1" or onFarm["outrosGramNegativa"] == "1":
                return 0
            else:
                return 1            
        
        def createClassCow(data):
            name = data['animal'].replace(" ", "_")
            lote = data['lote'].replace(" ", "_")

            onFarm = getAnimalOnFarm(data["brinco"])
            balanca = getAnimalBalanca(data["brinco"])
            ordenha = getAnimalProdLeite(data["brinco"])

            instance = Cow(name,
                    brinco = data['brinco'],
                    dea = data['DEA'],
                    days_lactation = data['DEL'],
                    batch = Batch(lote)
                )

            if onFarm:
                bacteria_index = getTypeOfBacteria(onFarm)
                bacteria = Bacteria(createBacteria(onFarm), gram_type = bacteria_index)
                Mastitis(f"Mastiti_{bacteria_index}", is_clinical = bacteria_index, mastitis_date = onFarm["data"], mastitis_origin = bacteria)

                instance.is_mastitis = 1
                instance.mastitis_grau = onFarm["grau"]
                # instance.had_bacteria_type = bacteria
            else:
                instance.is_mastitis = 0

            if balanca:
                instance.weight = balanca["peso"]
            else:
                instance.weight = 0

            if ordenha:
                milk_value = ordenha["ordenha1"] + ordenha["ordenha2"] + ordenha["ordenha3"]
                date = ordenha['date']
                ProcessMilk(f"{date}", proccess_milk_date = date)                        
                instance.leite = milk_value
                instance.was_milked = DairyMilk(dairy_milk_date = date, cow_milked = instance, dairy_value = milk_value)

        def createClassAmbiente(data, type = 1, sensor = Sensor()):
            if type == 1:
                name = "Measure_Temp_"+data["date"]+"_"+data["horario"]
                Measure(name,
                    # internal_measure_value = 0,
                    external_measure_value = data["tempExterna"],
                    measure_source = sensor,
                    measure_date = data["date"],
                    measure_time = data["horario"]
                )
            else:
                name = "Measure_Humidity_"+data["date"]+"_"+data["horario"]
                Measure(name,
                    # internal_measure_value = 0,
                    external_measure_value = data["humidityExterna"],
                    measure_source = sensor,
                    measure_date = data["date"],
                    measure_time = data["horario"]
                )

        for vaca in listVacas.find({}, exclusion_criteria):
            createClassCow(vaca)

        sensor_temperatura = Sensor("Sensor_T", sensor_unit="grau")
        typeAmbiente = 1
        for temperatura in listTemperature.find({ "source" : "inmet"}, exclusion_criteria):
            createClassAmbiente(temperatura, typeAmbiente, sensor_temperatura)

        typeAmbiente = 2
        sensor_umidade = Sensor("Sensor_U", sensor_unit="%")
        for umidade in listHumidity.find({ "source" : "inmet" }, exclusion_criteria):
            createClassAmbiente(umidade, typeAmbiente, sensor_umidade)
    
        # sync_reasoner([onto]) #example Hermit
        # sync_reasoner(infer_property_values =True, infer_data_property_values =True) #example Hermit
        # HermiT does not allow inferring the values of data properties
        
        # using below:
        if run_reasoner:
            sync_reasoner_pellet(infer_property_values = True, infer_data_property_values = True) # Pellet
        
        # for c in onto.classes(): print('class', c.name) 
        # for i in onto.individuals(): print('individual', i)
        if save:
            onto.save("new_provcow.owl", format = "rdfxml")            
            
        return onto