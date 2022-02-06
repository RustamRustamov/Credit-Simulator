import pandas as pd
import uuid
import time
from datetime import date, timedelta
import random
import _datetime


n = 0
result_customer = pd.DataFrame()
customer_id = []
date = []


# generates unique customer ID
def customerid():
    customerid = uuid.uuid4()
    customer_id.append(customerid)

# generates random date for the n days before
def activationdate():
    rand = random.randint(2, 2000)
    Acdate = _datetime.date.today() - timedelta(rand)
    date.append(Acdate)

# executes loop for the unique customers and activation date
while n < 100:
    n += 1
    customerid()
    activationdate()
    time.sleep(2)

#create dataframe
result_customer["Customer_id"]=customer_id
result_customer["Activationdate"]=date
result_customer['Daysonnetwork']=_datetime.date.today()- result_customer['Activationdate']
print(result_customer)
###################################################################################################################
#create recharges table
m = 0
RECHARGES = pd.DataFrame()
topup_date = []
topup_amount = []
recharged_customer = []

def RECHARGEDATETIME():
    now = _datetime.datetime.now()
    topup_date.append(now)

def RECHARGEAMOUNT():
    rand = random.randint(1, 10)
    topup_amount.append(rand)

def rechargedcustomer():
    topup_cus = random.choice(customer_id)
    recharged_customer.append(topup_cus)

while m < 150:
    m += 1
    RECHARGEDATETIME()
    RECHARGEAMOUNT()
    rechargedcustomer()
    time.sleep(2)

RECHARGES["Customer_id"] = recharged_customer
RECHARGES["RECHARGEDATETIME"]=topup_date
RECHARGES["RECHARGEAMOUNT"]=topup_amount
RECHARGES["Status"]='N'

#add column cumulative topup to the updated customers table result_customer_upd
dz=RECHARGES.groupby(['Customer_id']).sum().reset_index().rename(columns={'RECHARGEAMOUNT':'cumulative_topup'})
f=0
while f<2:
    f+=1
    result_customer_upd= pd.merge(result_customer,dz, on=['Customer_id'], how='left')
    time.sleep(5)

#create charge for customer
k = 0
result_charge = pd.DataFrame()
Charge_amount = []
charge_date = []
charged_customer = []

def CHARGEAMOUNT():
    rand = random.uniform(0.1, 1.5)
    Charge_amount.append(rand)

def chargedcustomer():
    topup_cus = random.choice(customer_id)
    charged_customer.append(topup_cus)

def CHARGEDATETIME():
    now = _datetime.datetime.now()
    charge_date.append(now)

while k < 180:
    k += 1
    CHARGEAMOUNT()
    chargedcustomer()
    CHARGEDATETIME()
    time.sleep(1.5)

result_charge["Customer_id"] = charged_customer
result_charge["CHARGEDATETIME"] = charge_date
result_charge["CHARGEAMOUNT"]=Charge_amount
cum_charge=result_charge.groupby(['Customer_id']).sum().reset_index().rename(columns={'CHARGEAMOUNT':'cumulative_charge'})

#Balance of customers total topups minus total charges
result_customer_upd['balance'] = result_customer_upd['cumulative_topup'].sub(result_customer_upd['Customer_id'].map(cum_charge.set_index('Customer_id')['cumulative_charge']), fill_value=0)

#generation of requests

initial_value = 1

REQUESTSERVICE=result_customer_upd.sample(n=74)
REQUESTSERVICE = REQUESTSERVICE[['Customer_id','Daysonnetwork','cumulative_topup']]
REQUESTSERVICE['MESSAGEID'] = range(initial_value, len(REQUESTSERVICE) +initial_value)
REQUESTSERVICE['REQUESTDATETIME'] = _datetime.datetime.now()

#######################################################################################################
# scores the customers generated requests and provides credit
credit_amount=[0.5,1,0.2,2,3]
Scorring_SERVICE_pr = REQUESTSERVICE.loc[(result_customer_upd['cumulative_topup']> 10) &
              (result_customer_upd['Daysonnetwork'] >  pd.Timedelta(5, unit='d'))]
SCORRINGSERVICE=Scorring_SERVICE_pr.copy()
SCORRINGSERVICE.rename(columns={'REQUESTDATETIME':'Scorring_date'})
SCORRINGSERVICE['loan_amount']=random.choice(credit_amount)