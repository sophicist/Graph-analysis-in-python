# imports
from colorama import init
from termcolor import colored
import gspread as gs
from oauth2client.service_account import ServiceAccountCredentials
from termcolor import colored, cprint
import pandas as pd

# variables
ethiopia = '1cUREwZjTEqeC2WiaxgLZPLgiwUo-rDA_UPdtfp-8iL0'

def Reader(link,sheet):
    gc = gs.service_account(filename='../../credentials.json')
    wks = gc.open_by_key(link)
    sheetname = wks.worksheet(sheet)
    record = pd.DataFrame(sheetname.get_all_records())
    return record

# EThiopian analysis
# aspirations
aspire = Reader(ethiopia,"Aspirations and Strategy")
pattern ="Firm ID|SFD-AST-010"

class survey:
    def __init__(self,aspire):
        self.ethiopia_aspire = aspire

    def yes_no_question(self,pattern,id_var,message):
        next_year = self.ethiopia_aspire.copy()
        next_year = aspire[aspire.columns[aspire.columns.str.contains(pattern)]].melt(id_vars =id_var)
        next_year['survey'] = 'aspirations'
        next_year['Question']  = [i.split('_')[0] for i in next_year['variable']]
        next_year['answer']  = [i.split('_')[1] for i in next_year['variable']]
        next_year = next_year[next_year['value']=='Yes']
        print(f'{message}  ---> completed')
        next_year.columns = ['firm_id','variable','value','survey','question','answer']
        return next_year.drop('variable',axis =1)
    def other_question(self,pattern,id_var,message):
        next_year = self.ethiopia_aspire.copy()
        next_year = aspire[aspire.columns[aspire.columns.str.contains(pattern)]].melt(id_vars =id_var)
        next_year['survey'] = 'aspirations'
        next_year['Question']  = [i.split('_')[0] for i in next_year['variable']]
        next_year['answer']  = [i.split('_')[1] for i in next_year['variable']]
        next_year = next_year[~next_year['value'].isin(['-1',-1])]
        print(f'{message}  ---> completed')
        next_year.columns = ['firm_id','variable','value','survey','question','answer']
        return next_year.drop('variable',axis =1)
# define a function for one question only
# aspirations
asp = survey(aspire)
yr_one      = asp.yes_no_question("Firm ID|SFD-AST-010",['Firm ID'],"Aspirations 1 year")
yr_five     = asp.yes_no_question("Firm ID|SFD-AST-020",['Firm ID'],"Aspirations 5 year")
measure     = asp.yes_no_question("Firm ID|SFD-AST-030",['Firm ID'],"Measure business")
often       = asp.other_question("Firm ID|SFD-AST-050",['Firm ID'],"often")
prices      = asp.yes_no_question("Firm ID|SFD-AST-070",['Firm ID'],"set_prices")
challenges  = asp.yes_no_question("Firm ID|SFD-AST-080",['Firm ID'],"challenges")

aspires = [yr_one,yr_five,measure,often,prices,challenges]
final = pd.concat(aspires)
print(final.shape)
final.to_excel('Outputs/aspirations_ethiopia.xlsx')
print('final------> saved to disk')
print(often.head())

