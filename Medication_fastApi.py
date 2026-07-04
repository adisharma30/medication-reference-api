from fastapi import FastAPI, HTTPException
from typing import Optional,List
from pydantic import BaseModel
from Medications_data import MEDICATIONS

app= FastAPI(title='Medication Reference API')

class Med_fix(BaseModel):
	pzn:str
	name:str
	active_ingredient:str
	dosage_from: str
	strength:str
	prescription_only: Optional[bool]

@app.get("/")
def Med_home():
	message="Welcome to Medication Reference API"
	return message			

@app.get("/medications",response_model=List[Med_fix])
def Med_list():
	return MEDICATIONS 

@app.get("/medications/query",response_model=List[Med_fix])
def Med_list_addtional_query(dosage_from: Optional[str]=None,prescription_only: Optional[bool]=None):
	if dosage_from is not None:
		meds= [x for x in MEDICATIONS if x['dosage_from']==dosage_from.lower()]

	if prescription_only is not None:
		meds=[x for x in MEDICATIONS if x['prescription_only']==prescription_only]

	if dosage_from is None and prescription_only is None:
		meds=MEDICATIONS
	return meds

@app.get("/medications/search",response_model=List[Med_fix])
def  Med_Search(q:str):
	q=q.lower()
	return [x for x in MEDICATIONS 
	if q in x["name"].lower() or q in x["active_ingredient"].lower()]
 
@app.get("/medications/{pzn}",response_model=Med_fix)
def Med_extract_pzn(pzn:str):
	 for x in MEDICATIONS:
	 	if x["pzn"]==pzn:
	 		return x
	 raise HTTPException(status_code=404,detail="Medication Not Found")


 
@app.get("/medications_dosage_from")
def Dosage_Stats():
	stats={}
	for med in MEDICATIONS:
		form=med['dosage_from']
		stats[form]=stats.get(form,0)+1
	return stats

	
	