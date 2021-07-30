import numpy as np
from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd
import  math

app=Flask(__name__)
model_b0=pickle.load(open('base_m0.pkl','rb'))
model_b1=pickle.load(open('base_m1.pkl','rb'))
model_b2=pickle.load(open('base_m2.pkl','rb'))
model_b3=pickle.load(open('base_m3.pkl','rb'))
model_b4=pickle.load(open('base_m4.pkl','rb'))
model_b5=pickle.load(open('base_m5.pkl','rb'))
model_b6=pickle.load(open('base_m6.pkl','rb'))
model_meta=pickle.load(open('meta_model.pkl','rb'))
model_num=pickle.load(open('minmax_scale.pkl','rb'))

@app.route('/')
@cross_origin()

def home():
    return render_template('home.html')

@app.route('/predict',methods=['GET','POST'])

@cross_origin()
def predict():
    if request.method=='POST':

        #opened at
        opened_at = request.form["opened"]
        opened_day = int(pd.to_datetime(opened_at, format="%Y-%m-%dT%H:%M").day)
        opened_month = int(pd.to_datetime(opened_at, format ="%Y-%m-%dT%H:%M").month)
        opened_week = str(pd.to_datetime(opened_at, format="%Y-%m-%dT%H:%M").day_name())

        # Total Stops
        sys_mod_count = int(request.form["sys_mod_count"])

        # weekday
        if (opened_week == 'Monday'):
            Monday = 1
            Tuesday = 0
            Wednesday = 0
            Thursday = 0
            Friday = 0
            Saturday = 0
            Sunday = 0

        elif (opened_week == 'Tuesday'):
            Monday = 0
            Tuesday = 1
            Wednesday = 0
            Thursday = 0
            Friday = 0
            Saturday = 0
            Sunday = 0

        elif (opened_week == 'Wednesday'):
            Monday = 0
            Tuesday = 0
            Wednesday = 1
            Thursday = 0
            Friday = 0
            Saturday = 0
            Sunday = 0

        elif (opened_week == 'Thursday'):
            Monday = 0
            Tuesday = 0
            Wednesday = 0
            Thursday = 1
            Friday = 0
            Saturday = 0
            Sunday = 0

        elif (opened_week == 'Friday'):
            Monday = 0
            Tuesday = 0
            Wednesday = 0
            Thursday = 0
            Friday = 1
            Saturday = 0
            Sunday = 0

        elif (opened_week == 'Saturday'):
            Monday = 0
            Tuesday = 0
            Wednesday = 0
            Thursday = 0
            Friday = 0
            Saturday = 1
            Sunday = 0

        elif (opened_week == 'Sunday'):
            Monday = 0
            Tuesday = 0
            Wednesday = 0
            Thursday = 0
            Friday = 0
            Saturday = 0
            Sunday = 1
        else:
            Monday = 0
            Tuesday = 0
            Wednesday = 0
            Thursday = 0
            Friday = 0
            Saturday = 0
            Sunday = 0

        #vendor
        vendor = request.form['Vendor']
        if (vendor == 'Others'):
            Vendor_Unknown = 1
            code_8s = 0
            Vendor_1 = 0
            Vendor_2 = 0
            Vendor_3 = 0

        elif(vendor == 'code_8s'):
            Vendor_Unknown = 0
            code_8s = 1
            Vendor_1 = 0
            Vendor_2 = 0
            Vendor_3 = 0

        elif(vendor == 'Vendor_1'):
            Vendor_Unknown = 0
            code_8s = 0
            Vendor_1 = 1
            Vendor_2 = 0
            Vendor_3 = 0

        elif(vendor == 'Vendor_2'):
            Vendor_Unknown = 0
            code_8s = 0
            Vendor_1 = 0
            Vendor_2 = 1
            Vendor_3 = 0

        elif(vendor == 'Vendor_3'):
            Vendor_Unknown = 0
            code_8s = 0
            Vendor_1 = 0
            Vendor_2 = 0
            Vendor_3 = 1
        else:
            Vendor_Unknown = 0
            code_8s = 0
            Vendor_1 = 0
            Vendor_2 = 0
            Vendor_3 = 0

        #Incident State
        Incident_State = request.form['Incident_State']
        if (Incident_State == 'Active'):
            Active = 1
            Closed = 0
            New = 0
            Resolved = 0
            Awaiting_User_Info = 0
            Awaiting_Vendor=0
            Awaiting_Problem=0
            Awaiting_Evidence=0

        elif(Incident_State == 'Closed'):
            Active = 0
            Closed = 1
            New = 0
            Resolved = 0
            Awaiting_User_Info = 0
            Awaiting_Vendor=0
            Awaiting_Problem=0
            Awaiting_Evidence=0

        elif(Incident_State == 'New'):
            Active = 0
            Closed = 0
            New = 1
            Resolved = 0
            Awaiting_User_Info = 0
            Awaiting_Vendor=0
            Awaiting_Problem=0
            Awaiting_Evidence=0

        elif(Incident_State == 'Resolved'):
            Active = 0
            Closed = 0
            New = 0
            Resolved = 1
            Awaiting_User_Info = 0
            Awaiting_Vendor=0
            Awaiting_Problem=0
            Awaiting_Evidence=0

        elif(Incident_State == 'Awaiting_User_Info'):
            Active = 0
            Closed = 0
            New = 0
            Resolved = 0
            Awaiting_User_Info = 1
            Awaiting_Vendor=0
            Awaiting_Problem=0
            Awaiting_Evidence=0

        elif(Incident_State == 'Awaiting_Vendor'):
            Active = 0
            Closed = 0
            New = 0
            Resolved = 0
            Awaiting_User_Info = 0
            Awaiting_Vendor=1
            Awaiting_Problem=0
            Awaiting_Evidence=0

        elif(Incident_State == 'Awaiting_Problem'):
            Active = 0
            Closed = 0
            New = 0
            Resolved = 0
            Awaiting_User_Info = 0
            Awaiting_Vendor=0
            Awaiting_Problem=1
            Awaiting_Evidence=0

        elif(Incident_State == 'Awaiting_Evidence'):
            Active = 0
            Closed = 0
            New = 0
            Resolved = 0
            Awaiting_User_Info = 0
            Awaiting_Vendor=0
            Awaiting_Problem=0
            Awaiting_Evidence=1

        else:
            Active = 0
            Closed = 0
            New = 0
            Resolved = 0
            Awaiting_User_Info = 0
            Awaiting_Vendor=0
            Awaiting_Problem=0
            Awaiting_Evidence=0


        #Active_Status
        Active_Status = request.form['Active_Status']
        if (Active_Status == 'True'):
            active = 1

        else  :
            active = 0

        #Made SLA
        Made_SLA = request.form['Made_SLA']
        if (Made_SLA == 'True'):
            made_sla=1

        else:
            made_sla = 0

        #Contact type
        Contact_Type = request.form['Contact_Type']
        if (Contact_Type == 'Phone'):
            Phone = 1
            Email = 0
            IVR = 0
            Direct_opening = 0
            Self_service = 0

        elif(Contact_Type == 'Email'):
            Phone = 0
            Email = 1
            IVR = 0
            Direct_opening = 0
            Self_service = 0

        elif (Contact_Type == 'IVR'):
            Phone = 0
            Email = 0
            IVR = 1
            Direct_opening = 0
            Self_service = 0

        elif (Contact_Type == 'Direct_opening'):
            Phone = 0
            Email = 0
            IVR = 0
            Direct_opening = 1
            Self_service = 0

        elif (Contact_Type == 'Self_service'):
            Phone = 0
            Email = 0
            IVR = 0
            Direct_opening = 0
            Self_service = 1

        else:
            Phone = 0
            Email = 0
            IVR = 0
            Direct_opening = 0
            Self_service = 0

        #Imapct
        Impact = request.form['Impact']
        if (Impact == 'Medium'):
            impact2__Medium = 1
            impact3__Low = 0
            impact1__High = 0

        elif(Impact == 'Low'):
            impact2__Medium = 0
            impact3__Low = 1
            impact1__High = 0

        elif(Impact == 'High'):
            impact2__Medium = 0
            impact3__Low = 0
            impact1__High = 1

        else:
            impact2__Medium = 0
            impact3__Low = 0
            impact1__High = 0

        #Urgency
        Urgency = request.form['Urgency']
        if (Urgency == 'Medium'):
            urgency2__Medium = 1
            urgency3__Low = 0
            urgency1__High = 0

        elif(Urgency == 'Low'):
            urgency2__Medium = 0
            urgency3__Low = 1
            urgency1__High = 0

        elif(Urgency == 'High'):
            urgency2__Medium = 0
            urgency3__Low = 0
            urgency1__High = 1

        else:
            urgency2__Medium = 0
            urgency3__Low = 0
            urgency1__High = 0

        #Priority
        Priority = request.form['Priority']
        if (Priority == 'Modetare'):
            priority3__Moderate = 1
            priority4__Low = 0
            priority2__High = 0
            priority1__Critical=0

        elif(Priority == 'Low'):
            priority3__Moderate = 0
            priority4__Low = 1
            priority2__High = 0
            priority1__Critical=0

        elif(Priority == 'High'):
            priority3__Moderate = 0
            priority4__Low = 0
            priority2__High = 1
            priority1__Critical=0

        elif(Priority == 'Critical'):
            priority3__Moderate = 0
            priority4__Low = 0
            priority2__High = 0
            priority1__Critical=1

        else:
            priority3__Moderate = 0
            priority4__Low = 0
            priority2__High = 0
            priority1__Critical=0

        #Knowledge
        Knowledge = request.form['Knowledge']
        if (Knowledge == 'True'):
            knowledge=1

        else:
            knowledge=0

        #Notify
        Notify = request.form['Notify']
        if (Notify == 'True'):
            Send_Email= 1
            Do_Not_Notify = 0

        else :
            Send_Email = 0
            Do_Not_Notify = 1


        #Priority_Confirmation
        Priority_Confirmation = request.form['Priority_Confirmation']
        if (Priority_Confirmation == 'True'):
            u_priority_confirmation=1

        else:
            u_priority_confirmation=0


        #PLocation
        Location = request.form['Location']
        if (Location == 'Location 204'):
            Location_A=1
            Location_B = 0
            Location_C = 0
            Location_D = 0
            Location_E = 0
            Location_F = 0
            Location_Unknown = 0

        elif(Location == 'Location 161'):
            Location_A=0
            Location_B = 1
            Location_C = 0
            Location_D = 0
            Location_E = 0
            Location_F = 0
            Location_Unknown = 0

        elif (Location == 'Location 143'):
            Location_A = 0
            Location_B = 0
            Location_C = 1
            Location_D = 0
            Location_E = 0
            Location_F = 0
            Location_Unknown = 0

        elif (Location == 'Location 108'):
            Location_A = 0
            Location_B = 0
            Location_C = 0
            Location_D = 1
            Location_E = 0
            Location_F = 0
            Location_Unknown = 0

        elif (Location == 'Location 93'):
            Location_A = 0
            Location_B = 0
            Location_C = 0
            Location_D = 0
            Location_E = 1
            Location_F = 0
            Location_Unknown = 0

        elif (Location == 'Location 51'):
            Location_A = 0
            Location_B = 0
            Location_C = 0
            Location_D = 0
            Location_E = 0
            Location_F = 1
            Location_Unknown = 0

        elif (Location == 'Location others'):
            Location_A = 0
            Location_B = 0
            Location_C = 0
            Location_D = 0
            Location_E = 0
            Location_F = 0
            Location_Unknown = 1

        else:
            Location_A = 0
            Location_B = 0
            Location_C = 0
            Location_D = 0
            Location_E = 0
            Location_F = 0
            Location_Unknown = 0


        num_lis = model_num.transform([[sys_mod_count,opened_day,opened_month]])
        sys_mod_count = num_lis[0][0]
        opened_day = num_lis[0][1]
        opened_month = num_lis[0][2]

        predict_0 = model_b0.predict([[Active, Awaiting_Evidence, Awaiting_Problem, Awaiting_User_Info, Awaiting_Vendor,
                                       Closed, New, Resolved, Direct_opening, Email, IVR, Phone, Self_service,
                                       Location_A, Location_B,
                                       Location_C, Location_D, Location_E, Location_F, Location_Unknown, Do_Not_Notify,
                                       Send_Email, Vendor_1,
                                       Vendor_2, Vendor_3, Vendor_Unknown, code_8s, Friday, Monday, Saturday, Sunday,
                                       Thursday, Tuesday, Wednesday,
                                       sys_mod_count, opened_day, opened_month, active, made_sla, knowledge,
                                       u_priority_confirmation, impact1__High,
                                       impact2__Medium, impact3__Low, priority1__Critical, priority2__High,
                                       priority3__Moderate, priority4__Low,
                                       urgency1__High, urgency2__Medium, urgency3__Low]])

        predict_1 = model_b1.predict([[Active, Awaiting_Evidence, Awaiting_Problem, Awaiting_User_Info, Awaiting_Vendor,
                                       Closed, New, Resolved, Direct_opening, Email, IVR, Phone, Self_service,
                                       Location_A, Location_B,
                                       Location_C, Location_D, Location_E, Location_F, Location_Unknown, Do_Not_Notify,
                                       Send_Email, Vendor_1,
                                       Vendor_2, Vendor_3, Vendor_Unknown, code_8s, Friday, Monday, Saturday, Sunday,
                                       Thursday, Tuesday, Wednesday,
                                       sys_mod_count, opened_day, opened_month, active, made_sla, knowledge,
                                       u_priority_confirmation, impact1__High,
                                       impact2__Medium, impact3__Low, priority1__Critical, priority2__High,
                                       priority3__Moderate, priority4__Low,
                                       urgency1__High, urgency2__Medium, urgency3__Low]])

        predict_2 = model_b2.predict([[Active, Awaiting_Evidence, Awaiting_Problem, Awaiting_User_Info, Awaiting_Vendor,
                                       Closed, New, Resolved, Direct_opening, Email, IVR, Phone, Self_service,
                                       Location_A, Location_B,
                                       Location_C, Location_D, Location_E, Location_F, Location_Unknown, Do_Not_Notify,
                                       Send_Email, Vendor_1,
                                       Vendor_2, Vendor_3, Vendor_Unknown, code_8s, Friday, Monday, Saturday, Sunday,
                                       Thursday, Tuesday, Wednesday,
                                       sys_mod_count, opened_day, opened_month, active, made_sla, knowledge,
                                       u_priority_confirmation, impact1__High,
                                       impact2__Medium, impact3__Low, priority1__Critical, priority2__High,
                                       priority3__Moderate, priority4__Low,
                                       urgency1__High, urgency2__Medium, urgency3__Low]])

        predict_3 = model_b3.predict([[Active, Awaiting_Evidence, Awaiting_Problem, Awaiting_User_Info, Awaiting_Vendor,
                                       Closed, New, Resolved, Direct_opening, Email, IVR, Phone, Self_service,
                                       Location_A, Location_B,
                                       Location_C, Location_D, Location_E, Location_F, Location_Unknown, Do_Not_Notify,
                                       Send_Email, Vendor_1,
                                       Vendor_2, Vendor_3, Vendor_Unknown, code_8s, Friday, Monday, Saturday, Sunday,
                                       Thursday, Tuesday, Wednesday,
                                       sys_mod_count, opened_day, opened_month, active, made_sla, knowledge,
                                       u_priority_confirmation, impact1__High,
                                       impact2__Medium, impact3__Low, priority1__Critical, priority2__High,
                                       priority3__Moderate, priority4__Low,
                                       urgency1__High, urgency2__Medium, urgency3__Low]])

        predict_4 = model_b4.predict([[Active, Awaiting_Evidence, Awaiting_Problem, Awaiting_User_Info, Awaiting_Vendor,
                                       Closed, New, Resolved, Direct_opening, Email, IVR, Phone, Self_service,
                                       Location_A, Location_B,
                                       Location_C, Location_D, Location_E, Location_F, Location_Unknown, Do_Not_Notify,
                                       Send_Email, Vendor_1,
                                       Vendor_2, Vendor_3, Vendor_Unknown, code_8s, Friday, Monday, Saturday, Sunday,
                                       Thursday, Tuesday, Wednesday,
                                       sys_mod_count, opened_day, opened_month, active, made_sla, knowledge,
                                       u_priority_confirmation, impact1__High,
                                       impact2__Medium, impact3__Low, priority1__Critical, priority2__High,
                                       priority3__Moderate, priority4__Low,
                                       urgency1__High, urgency2__Medium, urgency3__Low]])

        predict_5 = model_b5.predict([[Active, Awaiting_Evidence, Awaiting_Problem, Awaiting_User_Info, Awaiting_Vendor,
                                       Closed, New, Resolved, Direct_opening, Email, IVR, Phone, Self_service,
                                       Location_A, Location_B,
                                       Location_C, Location_D, Location_E, Location_F, Location_Unknown, Do_Not_Notify,
                                       Send_Email, Vendor_1,
                                       Vendor_2, Vendor_3, Vendor_Unknown, code_8s, Friday, Monday, Saturday, Sunday,
                                       Thursday, Tuesday, Wednesday,
                                       sys_mod_count, opened_day, opened_month, active, made_sla, knowledge,
                                       u_priority_confirmation, impact1__High,
                                       impact2__Medium, impact3__Low, priority1__Critical, priority2__High,
                                       priority3__Moderate, priority4__Low,
                                       urgency1__High, urgency2__Medium, urgency3__Low]])

        predict_6 = model_b6.predict([[Active, Awaiting_Evidence, Awaiting_Problem, Awaiting_User_Info, Awaiting_Vendor,
                                       Closed, New, Resolved, Direct_opening, Email, IVR, Phone, Self_service,
                                       Location_A, Location_B,
                                       Location_C, Location_D, Location_E, Location_F, Location_Unknown, Do_Not_Notify,
                                       Send_Email, Vendor_1,
                                       Vendor_2, Vendor_3, Vendor_Unknown, code_8s, Friday, Monday, Saturday, Sunday,
                                       Thursday, Tuesday, Wednesday,
                                       sys_mod_count, opened_day, opened_month, active, made_sla, knowledge,
                                       u_priority_confirmation, impact1__High,
                                       impact2__Medium, impact3__Low, priority1__Critical, priority2__High,
                                       priority3__Moderate, priority4__Low,
                                       urgency1__High, urgency2__Medium, urgency3__Low]])
        total_pred=np.array([predict_0,predict_1,predict_2,predict_3,predict_4,predict_5,predict_6]).T
        predict_final = model_meta.predict(total_pred)
        # output=predict_final
        output = math.floor(abs(predict_final))

        return render_template('home.html', Prediction="Approximate days to close the incident is {} days".format(output))

    return render_template("home.html")

if __name__ == "__main__":
    app.run()