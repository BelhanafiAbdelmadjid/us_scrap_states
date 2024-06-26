from flask import Flask, render_template,redirect,url_for,request
from scrap import scrap_properties
from selenium.webdriver.common.by import By

app = Flask(__name__)

'''
    1 : stadard,
    2 : captcha + pagination,
    3 : pagination / no captcha
    4 : captcha no text /no pagination with button disabled until captcha done
    5 : special for HAWAI

'''

# scrap_properties(['Tyson',"Smith"],"VIRGINIA",'lastName','btn-recaptcha',"https://www.vamoneysearch.gov/app/claim-search",'https://www.vamoneysearch.gov/SWS/properties',[])
# scrap_properties(['Tyson'],"NORTH-CAROLINA",'lastName','btn-recaptcha','https://unclaimed.nccash.com/app/claim-search','https://unclaimed.nccash.com/SWS/properties',[])
app.config["STATES"] = []
app.config["STATES_CONFIG"] = {
    'TEXAS' : {
        'getUrl' : "https://www.claimittexas.gov/app/claim-search",
        'postUrl' : "https://www.claimittexas.gov/SWS/properties",
        'ButtonSubmitID' : 'btn-recaptcha',
        'lastName' : "lastName",
        "number_based" : {
            "attribute" : "propertyValue",
            "type" : "float"
        },
        'method' : 1,
    },
    'VIRGINIA' : {
        'getUrl' : "https://www.vamoneysearch.gov/app/claim-search",
        'postUrl' : "https://www.vamoneysearch.gov/SWS/properties",
        'ButtonSubmitID' : 'btn-recaptcha',
        'lastName' : "lastName",
        "number_based" : None,
        'method' : 1,
    },
    'NORTH_CAROLINA' : {
        'getUrl' : "https://unclaimed.nccash.com/app/claim-search",
        'postUrl' : "https://unclaimed.nccash.com/SWS/properties",
        'ButtonSubmitID' : 'btn-recaptcha',
        'lastName' : "lastName",
        "number_based" : None,
        'method' : 1,
    },
    'ALABAMA' : {
        'getUrl' : "https://alabama.findyourunclaimedproperty.com/app/claim-search",
        'postUrl' : "https://alabama.findyourunclaimedproperty.com/SWS/properties",
        'ButtonSubmitID' : 'btn-recaptcha',
        'lastName' : "lastName",
        "number_based" : None,
        'method' : 1,
    },
    'ALASKA' : {
        'getUrl' : "https://unclaimedproperty.alaska.gov/app/claim-search",
        'postUrl' : "https://unclaimedproperty.alaska.gov/SWS/properties",
        'ButtonSubmitID' : 'btn-recaptcha',
        'lastName' : "lastName",
        "number_based" : None,
        'method' : 1,
    },
    'CLAIMITAR' : {
        'getUrl' : "https://www.claimitar.gov/app/claim-search",
        'postUrl' : "https://www.claimitar.gov/SWS/properties",
        'ButtonSubmitID' : 'btn-recaptcha',
        'lastName' : "lastName",
        "number_based" : None,
        'method' : 1,
    },
    'CLAIMITAR' : {
        'getUrl' : "https://www.claimitar.gov/app/claim-search",
        'postUrl' : "https://www.claimitar.gov/SWS/properties",
        'ButtonSubmitID' : 'btn-recaptcha',
        'lastName' : "lastName",
        "number_based" : None,
        'method' : 1,
    },
    'COLORADO' : {
        'getUrl' : "https://colorado.findyourunclaimedproperty.com/app/claim-search",
        'postUrl' : "https://colorado.findyourunclaimedproperty.com/SWS/properties",
        'ButtonSubmitID' : 'btn-recaptcha',
        'lastName' : "lastName",
        "number_based" : {
            "attribute" : "propertyValueDescription",
            "type" : "$float"
        },
        'method' : 1,
    },
    'WASHINTON_DC' : {
        'getUrl' : "https://unclaimedproperty.dc.gov/app/claim-search",
        'postUrl' : "https://unclaimedproperty.dc.gov/SWS/properties",
        'ButtonSubmitID' : 'btn-recaptcha',
        'lastName' : "lastName",
        "number_based" : None,
        'method' : 1,
    },
    'IDAHO' : {
        'getUrl' : "https://yourmoney.idaho.gov/app/claim-search",
        'postUrl' : "https://yourmoney.idaho.gov/SWS/properties",
        'ButtonSubmitID' : 'btn-recaptcha',
        'lastName' : "lastName",
        "number_based" : {
            "attribute" : "propertyValueDescription",
            "type" : "$float"
        },
        'method' : 1,
    },
    'ILLINOIS' : {
        'getUrl' : "https://icash.illinoistreasurer.gov/app/claim-search",
        'postUrl' : "https://icash.illinoistreasurer.gov/SWS/properties",
        'ButtonSubmitID' : 'btn-recaptcha',
        'lastName' : "lastName",
        "number_based" : None,
        'method' : 1,
    },
    'KANSAS' : {
        'getUrl' : "https://unclaimedproperty.ks.gov/app/claim-search",
        'postUrl' : "https://unclaimedproperty.ks.gov/SWS/properties",
        'ButtonSubmitID' : 'btn-recaptcha',
        'lastName' : "lastName",
        "number_based" : None,
        'method' : 1,
    },
    'IOWA' : {
        'getUrl' : "https://www.greatiowatreasurehunt.gov/app/claim-search",
        'postUrl' : "https://www.greatiowatreasurehunt.gov/SWS/properties",
        'ButtonSubmitID' : 'btn-recaptcha',
        'lastName' : "lastName",
        "number_based" : {
            "attribute" : "propertyValue",
            "type" : "float"
        },
        'method' : 1,
    },
    'LOUISIANA' : {
        'getUrl' : "https://louisiana.findyourunclaimedproperty.com/app/claim-search",
        'postUrl' : "https://louisiana.findyourunclaimedproperty.com/SWS/properties",
        'ButtonSubmitID' : 'btn-recaptcha',
        'lastName' : "lastName",
        "number_based" : None,
        'method' : 1,
    },
    'MAINE' : {
        'getUrl' : "https://www.maineunclaimedproperty.gov/app/claim-search",
        'postUrl' : "https://www.maineunclaimedproperty.gov/SWS/properties",
        'ButtonSubmitID' : 'btn-recaptcha',
        'lastName' : "lastName",
        "number_based" : {
            "attribute" : "propertyValue",
            "type" : "float"
        },
        'method' : 1,
    },
    'MASSACHUSETTS' : {
        'getUrl' : "https://www.findmassmoney.gov/app/claim-search",
        'postUrl' : "https://www.findmassmoney.gov/SWS/properties",
        'ButtonSubmitID' : 'btn-recaptcha',
        'lastName' : "lastName",
        "number_based" : None,
        'method' : 1,
    },
    'MICHIGAN' : {
        'getUrl' : "https://unclaimedproperty.michigan.gov/app/claim-search",
        'postUrl' : "https://unclaimedproperty.michigan.gov/SWS/properties",
        'ButtonSubmitID' : 'btn-recaptcha',
        'lastName' : "lastName",
        "number_based" : {
            "attribute" : "propertyValue",
            "type" : "float"
        },
        'method' : 1,
    },
    'MINNESOTA' : {
        'getUrl' : "https://minnesota.findyourunclaimedproperty.com/app/claim-search",
        'postUrl' : "https://minnesota.findyourunclaimedproperty.com/SWS/properties",
        'ButtonSubmitID' : 'btn-recaptcha',
        'lastName' : "lastName",
        "number_based" : None,
        'method' : 1,
    },
    'MISSISSIPPI' : {
        'getUrl' : "https://ms.findyourunclaimedproperty.com/app/claim-search",
        'postUrl' : "https://ms.findyourunclaimedproperty.com/SWS/properties",
        'ButtonSubmitID' : 'btn-recaptcha',
        'lastName' : "lastName",
        "number_based" : None,
        'method' : 1,
    },
    'NEW_HAMPSHIRE' : {
        'getUrl' : "https://www.findnhmoney.gov/app/claim-search",
        'postUrl' : "https://www.findnhmoney.gov/SWS/properties",
        'ButtonSubmitID' : 'btn-recaptcha',
        'lastName' : "lastName",
        "number_based" : None,
        'method' : 1,
    },
    'NEW_JERSEY' : {
        'getUrl' : "https://unclaimedfunds.nj.gov/app/claim-search",
        'postUrl' : "https://unclaimedfunds.nj.gov/SWS/properties",
        'ButtonSubmitID' : 'btn-recaptcha',
        'lastName' : "lastName",
        "number_based" : None,
        'method' : 1,
    },
    'NORTH_DAKOTA' : {
        'getUrl' : "https://unclaimedproperty.nd.gov/app/claim-search",
        'postUrl' : "https://unclaimedproperty.nd.gov/SWS/properties",
        'ButtonSubmitID' : 'btn-recaptcha',
        'lastName' : "lastName",
        "number_based" : {
            "attribute" : "propertyValue",
            "type" : "float"
        },
        'method' : 1,
    },
    'OREGON' : {
        'getUrl' : "https://unclaimed.oregon.gov/app/claim-search",
        'postUrl' : "https://unclaimed.oregon.gov/SWS/properties",
        'ButtonSubmitID' : 'btn-recaptcha',
        'lastName' : "lastName",
        "number_based" : None,
        'method' : 1,
    },
    'RHOBE_ISLAND' : {
        'getUrl' : "https://findrimoney.com/app/claim-search",
        'postUrl' : "https://findrimoney.com/SWS/properties",
        'ButtonSubmitID' : 'btn-recaptcha',
        'lastName' : "lastName",
        "number_based" : {
            "attribute" : "propertyValue",
            "type" : "float"
        },
        'method' : 1,
    },
    'SOUTH_CAROLINA' : {
        'getUrl' : "https://southcarolina.findyourunclaimedproperty.com/app/claim-search",
        'postUrl' : "https://southcarolina.findyourunclaimedproperty.com/SWS/properties",
        'ButtonSubmitID' : 'btn-recaptcha',
        'lastName' : "lastName",
        "number_based" : None,
        'method' : 1,
    },
    'SOUTH_DAKOTA' : {
        'getUrl' : "https://southdakota.findyourunclaimedproperty.com/app/claim-search",
        'postUrl' : "https://southdakota.findyourunclaimedproperty.com/SWS/properties",
        'ButtonSubmitID' : 'btn-recaptcha',
        'lastName' : "lastName",
        "number_based" : {
            "attribute" : "propertyValueDescription",
            "type" : "$float"
        },
        'method' : 1,
    },
    'UTAH' : {
        'getUrl' : "https://mycash.utah.gov/app/claim-search",
        'postUrl' : "https://mycash.utah.gov/SWS/properties",
        'ButtonSubmitID' : 'btn-recaptcha',
        'lastName' : "lastName",
        "number_based" : {
            "attribute" : "propertyValue",
            "type" : "float"
        },
        'method' : 1,
    },
    'WASHIGTON' : {
        'getUrl' : "https://ucp.dor.wa.gov/app/claim-search",
        'postUrl' : "https://ucp.dor.wa.gov/SWS/properties",
        'ButtonSubmitID' : 'btn-recaptcha',
        'lastName' : "lastName",
        "number_based" : None,
        'method' : 1,
    },
    'WEST_VIRGINIA' : {
        'getUrl' : "https://www.wvunclaimedproperty.gov/app/claim-search",
        'postUrl' : "https://www.wvunclaimedproperty.gov/SWS/properties",
        'ButtonSubmitID' : 'btn-recaptcha',
        'lastName' : "lastName",
        "number_based" : None,
        'method' : 1,
    },
    'ARKANSAS' : {
        'getUrl' : "https://www.claimitar.gov/app/claim-search",
        'postUrl' : "https://www.claimitar.gov/SWS/properties",
        'ButtonSubmitID' : 'btn-recaptcha',
        'lastName' : "lastName",
        "number_based" : None,
        'method' : 1,
    },
    'DELAWARE' : {
        'getUrl' : "https://unclaimedproperty.delaware.gov/app/claim-search",
        'postUrl' : "https://unclaimedproperty.delaware.gov/SWS/properties",
        'ButtonSubmitID' : 'btn-recaptcha',
        'lastName' : "lastName",
        "number_based" : None,
        'method' : 1,
    },
    'DISTRICT_OF_COLUMBIA' : {
        'getUrl' : "https://unclaimedproperty.dc.gov/app/claim-search",
        'postUrl' : "https://unclaimedproperty.dc.gov/SWS/properties",
        'ButtonSubmitID' : 'btn-recaptcha',
        'lastName' : "lastName",
        "number_based" : None,
        'method' : 1,
    },
#########################################  METHOD2  #############################################
    'GEORGIA' : {
        'getUrl' : "https://gaclaims.unclaimedproperty.com/en/Property/SearchIndex",
        'postUrl' : None,
        'ButtonSubmitID' : {
            "BY" : By.NAME,
            "VALUE" : "submitStandard"
        },
        "more_to_check" : [
            {
                "BY" : By.ID,
                "VALUE" : "InterestedInSearch"
            }
        ],
        'lastName' : "SearchModel_LastName",
        "number_based" : None,
        'method' : 2,
        "filter_on_attribute" : "Amount:",
        'table' : {
            "BY" : By.ID,
            "VALUE" : "searchTable",
            "ROWS" : {
                "BY" : By.TAG_NAME,
                "VALUE" : "th"
            }
        },
        'pagination' : {
            'BY' : By.CSS_SELECTOR,
            "VALUE" : ".PagedList-skipToLast"
        },
    },
    'CALIFORNIA' : {
        'getUrl' : "https://ucpi.sco.ca.gov/en/Property/SearchIndex",
        'postUrl' : None,
        'ButtonSubmitID' : {
            "BY" : By.NAME,
            "VALUE" : "submitPersonAddress"
        },
        "more_to_check" : [],
        'lastName' : "AddressSearchModel_LastName",
        "number_based" : {
            "attribute" : "Amount:",
            "type" : "$float"
        },
        'method' : 2,
        'table' : {
            "BY" : By.ID,
            "VALUE" : "searchTable",
            "ROWS" : {
                "BY" : By.TAG_NAME,
                "VALUE" : "th"
            },
            "ROWS_CLASS_INT" : True,
            "ROWS_SPECIAL_CLASSES" : []
        },
        'pagination' : {
            'BY' : By.CSS_SELECTOR,
            "VALUE" : ".PagedList-skipToLast"
        },
        # "filter_on_attribute" : "Amount:"
    },
    'VERMONT' : {
        'getUrl' : "https://vermont.unclaimedproperty.com/en/Property/SearchIndex",
        'postUrl' : None,
        'ButtonSubmitID' : {
            "BY" : By.NAME,
            "VALUE" : "submitPerson"
        },
        "more_to_check" : [
            {
                "BY" : By.ID,
                "VALUE" : "rbSearchType"
            }
        ],
        'lastName' : "SearchModel_LastName",
        "number_based" : None,
        'method' : 2,
        'table' : {
            "BY" : By.ID,
            "VALUE" : "searchTable",
            "ROWS" : {
                "BY" : By.TAG_NAME,
                "VALUE" : "th"
            }
        },
        'pagination' : {
            'BY' : By.CSS_SELECTOR,
            "VALUE" : ".PagedList-skipToNext"
        },
        # "filter_on_attribute" : "Amount:"
    },
    'NEW_BRUNSWICK' : {
        'getUrl' : "https://www.fundsfinder-mesfondsnb.ca/en-US/",
  
        'postUrl' : None,
        'ButtonSubmitID' : {
            "BY" : By.ID,
            "VALUE" : "searchsubmit"
        },
        "more_to_check" : [],
        'lastName' : "searchfield",
        "number_based" : None,
        'method' : 4,
        'table' : {
            "BY" : By.CSS_SELECTOR,
            "VALUE" : ".table.table-striped.table-fluid",
            "ROWS" : {
                "BY" : By.TAG_NAME,
                "VALUE" : "tr"
            },
            "HEADERS" : {
                "BY" : By.TAG_NAME,
                "VALUE" : "th"
            },
        },
        "filter_on_attribute" : "Property Value"
    },
    'MISSOURI' : {
        'getUrl' : "https://treasurer.mo.gov/UnclaimedProperty/en/Property/SearchIndex",
        'postUrl' : None,
        'ButtonSubmitID' : {
            "BY" : By.NAME,
            "VALUE" : "submitPerson"
        },
        "more_to_check" : [
            {
                "BY" : By.ID,
                "VALUE" : "rbSearchType"
            }
        ],
        'lastName' : "SearchModel_LastName",
        "number_based" :  {
            "attribute" : "Amount:",
            "type" : "$float"
        },
        'method' : 2,
        'table' : {
            "BY" : By.ID,
            "VALUE" : "searchTable",
            "ROWS" : {
                "BY" : By.TAG_NAME,
                "VALUE" : "th"
            },
            "ROWS_CLASS_INT" : False,
            "ROWS_SPECIAL_CLASSES" : ["border_bottom"]
        },
        'pagination' : {
            'BY' : By.CSS_SELECTOR,
            "VALUE" : ".PagedList-skipToLast"
        },
        "filter_on_attribute" : "Amount:"
    },
    'NEVADA' : {
        'getUrl' : "https://claims.nevadaunclaimedproperty.gov/en/Property/SearchIndex",
        'postUrl' : None,
        'ButtonSubmitID' : {
            "BY" : By.NAME,
            "VALUE" : "submitPerson"
        },
        "more_to_check" : [
            {
                "BY" : By.ID,
                "VALUE" : "rbSearchType"
            }
        ],
        'lastName' : "SearchModel_LastName",
        "number_based" :  None,
        'method' : 2,
        'table' : {
            "BY" : By.ID,
            "VALUE" : "searchTable",
            "ROWS" : {
                "BY" : By.TAG_NAME,
                "VALUE" : "th"
            },
            "ROWS_CLASS_INT" : True,
            "ROWS_SPECIAL_CLASSES" : []
        },
        'pagination' : {
            'BY' : By.CSS_SELECTOR,
            "VALUE" : ".PagedList-skipToLast"
        },
        "filter_on_attribute" : "Amount:"
    },
    'PATREASURY' : {
        'getUrl' : "https://unclaimedproperty.patreasury.gov/en/Property/SearchIndex",
        'postUrl' : None,
        'ButtonSubmitID' : {
            "BY" : By.NAME,
            "VALUE" : "submitPersonAddress"
        },
        "more_to_check" : [],
        'lastName' : "AddressSearchModel_LastName",
        "number_based" :  None,
        'method' : 2,
        'table' : {
            "BY" : By.ID,
            "VALUE" : "searchTable",
            "ROWS" : {
                "BY" : By.TAG_NAME,
                "VALUE" : "th"
            },
            "ROWS_CLASS_INT" : True,
            "ROWS_SPECIAL_CLASSES" : []
        },
        'pagination' : {
            'BY' : By.CSS_SELECTOR,
            "VALUE" : ".PagedList-skipToLast"
        },
        "filter_on_attribute" : "Amount:"
    },






    #Text not disapearing like other when captcha solving, 
    #but has Recaptcha requires verification. appear on a div when submitting captcha and ok
    # 'HAWAI' : {
    #     'getUrl' : "https://unclaimedproperty.ehawaii.gov/lilo/property-list.html",
  
    #     'postUrl' : None,
    #     'ButtonSubmitID' : {
    #         "BY" : By.CSS_SELECTOR,
    #         "VALUE" : "button.btn.btn-primary.btn-lg.mt-3"
    #     },
    #     "more_to_check" : [],
    #     'lastName' : "lastName",
    #     "number_based" : None,
    #     'method' : 4,
    #     'table' : {
    #         "BY" : By.CSS_SELECTOR,
    #         "VALUE" : ".table.table-striped",
    #         "ROWS" : {
    #             "BY" : By.TAG_NAME,
    #             "VALUE" : "tr"
    #         }
    #     },
        
    #     # "filter_on_attribute" : "Amount:"
    # },

    #Problem is the links with pagination on url
    # 'FLORIDA' : {
    #     'getUrl' : "https://fltreasurehunt.gov/ControlServlet?ActionForm=GotoNewPublicSearch",
    #     'postUrl' : None,
    #     'ButtonSubmitID' : {
    #         "BY" : By.ID,
    #         "VALUE" : "searchBtn"
    #     },
    #     'lastName' : "lname",
    #     'table' : {
    #         "BY" : By.CSS_SELECTOR,
    #         "VALUE" : 'table[align="center"][style="width: 80%;"]'
    #     },
    #     "more_to_check" : [],
    #     "number_based" : {
    #         "attribute" : "Cash",
    #         "type" : "$float"
    #     },
    #     'method' : 3,
    #     'captcha' : False,
    #     'pagination' : {
    #         'BY' : By.ID,
    #         "VALUE" : ""
    #     },
    # },
}
for state in app.config["STATES_CONFIG"] :
    app.config["STATES"].append(state)

@app.route('/')
def index():
    return redirect(url_for('home'))


@app.route("/home", methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html',states=app.config["STATES"],results=[])
    else :
        state= request.form.get('state')
        filters = request.form.getlist('name_filters')
        
        names = request.form.getlist('specific_names')
        if len(names) == 0 :
            f = open("./common_name.txt",'r')
            names  = f.readlines()
        state_config = app.config["STATES_CONFIG"][state]
        res = scrap_properties(commonNames=names,
                               state=state,
                               lastNameInputID=state_config["lastName"],
                               ButtonSubmitID=state_config["ButtonSubmitID"],
                               fetch_link=state_config["getUrl"],
                               target_url=state_config["postUrl"],
                               looking_for_amount_str_array=filters,
                               number_based=state_config["number_based"],
                               method = state_config["method"],
                               filter_on_attribute=state_config.get("filter_on_attribute"),
                               state_conf = state_config
                               )
        return render_template('index.html',states=app.config["STATES"],result=res)


@app.route("/common-names", methods=['GET', 'POST'])
def commonNames():
    if request.method == 'POST':
        names:str = request.form.getlist('name')
        name = names[0].strip("")
        f = open("./common_name.txt","r")
        old_names = f.readlines()
        f.close()
        f = open("./common_name.txt","a")
        if name.strip("") + "\n" not in old_names :
            to_write = name.strip("") + "\n"
            f.write(to_write)
        f.close()
        return  redirect(url_for('commonNames'))
        # names = names[0].split("\n")
        # f = open("./common_name.txt","r")
        # old_names = f.readlines()
        # f.close()
        # f = open("./common_name.txt","a")
        # for name in names:
        #     if name.strip("") + "\n" not in old_names :
        #         to_write = name.strip("") + "\n"
        #         f.write(to_write)
        # f.close()
        # return  redirect(url_for('commonNames'))
    f = open("./common_name.txt","r")
    names = f.readlines()
    return render_template('common.html',names = names)

@app.post("/name")
def deletingName():
    if request.method == 'POST':
        name = request.form.getlist('name')
        name = name[0].strip("")

        f = open("./common_name.txt","r")
        old_names = f.readlines()
        f.close()

        i = 0
        while i < len(old_names):
            if name + "\n"  == old_names[i] :
                old_names.pop(i)
                break
            i = i +1

        f = open("./common_name.txt","w")
        f.writelines(old_names)
        f.close()
        return  redirect(url_for('commonNames'))

if __name__ == '__main__':

    app.run(debug=True)
