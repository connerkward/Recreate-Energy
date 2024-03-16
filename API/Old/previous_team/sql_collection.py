# Sql_collection contains all the SQL queries

class Sql_collection:
    def select_all():
        return '''SELECT * FROM chamber_data'''

    def select_temp(chamber, time):
        return '''SELECT temperature FROM chamber_data where chmb_id = ''' + chamber + ''' AND time = ''' + time

    #try making the other api calls like this one Michael, I want to order them by date
    def select_recent(chamber):
        return "SELECT * FROM chamber_data WHERE chmb_id = {id} ORDER BY sub_date DESC LIMIT 100".format(id = chamber)
    
    def select_temp_in_dates(chamber, startTime, endTime):
        return "SELECT temp, sub_date FROM chamber_data WHERE chmb_id = {id} AND sub_date >= \'{start}\' and sub_date < \'{end}\'".format(id = chamber, start = startTime, end = endTime)
    
    def select_chamber_details(chamber):
        return "SELECT * FROM chamber_data WHERE chmb_id = {id} limit 100".format(id = chamber)
    
    def select_ph_in_dates(chamber, startTime, endTime):
        return "SELECT ph, sub_date FROM chamber_data WHERE chmb_id = {id} AND sub_date >= \'{start}\' and sub_date < \'{end}\'".format(id = chamber, start = startTime, end = endTime)
    
    def select_ADCRAW_ADCVOLT_in_dates(chamber, startTime, endTime):
        return "SELECT ADCRaw, ADCVolt, sub_date FROM chamber_data WHERE chmb_id = {id} AND sub_date >= \'{start}\' and sub_date < \'{end}\'".format(id = chamber, start = startTime, end = endTime)
    
    def select_DOX_in_dates(chamber, startTime, endTime):
        return "SELECT DOX, sub_date FROM chamber_data WHERE chmb_id = {id} AND sub_date >= \'{start}\' and sub_date < \'{end}\'".format(id = chamber, start = startTime, end = endTime)
    

    def add_user_n_psw(email, psw, org_id):
        return "INSERT INTO users(email, password, org_id, authenticated) VALUES(\'{e}\', \'{p}\', \'{org}\', {auth})".format(e = email, p = psw, org = org_id, auth = False)

    def get_psw(email):
        return "SELECT password FROM users WHERE email = \'{e}\'".format(e = email)

    def get_user_info(email):
        return "SELECT email, org_id, authenticated FROM users WHERE email = \'{e}\'".format(e = email)
    
    # def count_email(email):
    #     return "SELECT COUNT(email) FROM users WHERE email = \'{e}\'".format(e = email)
        