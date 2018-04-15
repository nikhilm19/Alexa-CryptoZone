my_url = "https://www.cryptonator.com/api/ticker/"
d = {'bitcoin': 'BTC', 'ethereum': 'ETH', 'ripple': 'XRP', 'bitcoincash': 'BCH', 'litecoin': 'LTC', 'eos': 'EOS',
     'stellar': 'XLM', 'cardano': 'ADA', 'neo': 'NEO', 'iota': 'MIOTA', 'monero': 'XMR', 'dash': 'DASH',
     'tether': 'USDT', 'tron': 'TRX', 'nem': 'XEM', 'binancecoin': 'BNB', 'ethereumclassic': 'ETC', 'vechain': 'VEN',
     'qtum': 'QTUM', 'omisego': 'OMG', 'lisk': 'LSK', 'verge': 'XVG', 'icon': 'ICX', 'nano': 'NANO',
     'bitcoingold': 'BTG', 'zcash': 'ZEC', 'steem': 'STEEM', 'ontology': 'ONT', 'bytom': 'BTM', 'populous': 'PPT',
     'digixdao': 'DGD', 'bytecoinbcn': 'BCN', 'bitshares': 'BTS', 'waves': 'WAVES', 'stratis': 'STRAT', 'siacoin': 'SC',
     'status': 'SNT', 'aeternity': 'AE', 'rchain': 'RHOC', 'bitcoindiamond': 'BCD', 'dogecoin': 'DOGE', 'maker': 'MKR',
     'decred': 'DCR', 'zilliqa': 'ZIL', 'augur': 'REP', 'komodo': 'KMD', '0x': 'ZRX', 'ardor': 'ARDR',
     'waltonchain': 'WTC', 'hshare': 'HSR', 'aion': 'AION', 'veritaseum': 'VERI', 'ark': 'ARK', 'loopring': 'LRC',
     'pivx': 'PIVX', 'cryptonex': 'CNX', 'kucoinshares': 'KCS', 'qash': 'QASH', 'iostoken': 'IOST',
     'basicattentiontoken': 'BAT', 'monacoin': 'MONA', 'digibyte': 'DGB', 'factom': 'FCT', 'nebulastoken': 'NAS',
     'golemnetworktokens': 'GNT', 'gas': 'GAS', 'gxchain': 'GXS', 'ethos': 'ETHOS', 'revain': 'R', 'syscoin': 'SYS',
     'dragonchain': 'DRGN', 'funfair': 'FUN', 'kybernetwork': 'KNC', 'aelf': 'ELF', 'zcoin': 'XZC',
     'electroneum': 'ETN', 'storm': 'STORM', 'kin': 'KIN', 'substratum': 'SUB', 'powerledger': 'POWR', 'nxt': 'NXT',
     'reddcoin': 'RDD', 'maidsafecoin': 'MAID', 'salt': 'SALT', 'mithril': 'MITH', 'byteball': 'GBYTE', 'dent': 'DENT',
     'enigmaproject': 'ENG', 'storj': 'STORJ', 'nucleusvision': 'NCASH', 'requestnetwork': 'REQ', 'neblio': 'NEBL',
     'skycoin': 'SKY', 'tenx': 'PAY', 'bancor': 'BNT', 'chainlink': 'LINK', 'emercoin': 'EMC', 'genaronetwork': 'GNX',
     'dentacoin': 'DCN', 'dropil': 'DROP'}
import json
import requests

## 2. Skill Code =======================================================================================================
def speechResponse(say, endSession, sessionAttributes):
    print('say = ' + say)
    return {
        'version': '1.0',
        'sessionAttributes': sessionAttributes,
        'response': {
            'outputSpeech': {
                'type': 'SSML',
                'ssml': "<speak>" + say + "</speak>"

            },
            'shouldEndSession': endSession
        }
    }


def lambda_handler(event, context):

    if event['request']['type'] == "LaunchRequest":

        say = "Welcome to Crypto Teller. You can ask me something like What is the price of Bitcoin? or How is Bitcoin doing as compared to ethereum"

        return speechResponse(say, False, {})

    elif event['request']['type'] == "IntentRequest":


        intentName = event['request']['intent']['name']
        if intentName=="CryptoRateIntent":
            global d
            currency_received = event['request']['intent']['slots']['Currency']['value']
            if currency_received not in d:
                say="sorry i dont know that"
            else:
                price,change,cents,speak_point,speak_zero = httpsGet(d[currency_received])  ## see the helper function defined below
                say=whatToSay(price,currency_received,speak_zero,speak_point,change,cents)
                if say=="":
                    say="Sorry I don't know that"
            print(say)

        elif intentName=="CryptoCompareIntent":
            ##call compare function
            say=""
            currency_received_1 = event['request']['intent']['slots']['FirstCurrency']['value']
            currency_received_2 = event['request']['intent']['slots']['SecondCurrency']['value']
            if currency_received_1 not in d or currency_received_2 not in d:
                say="Sorry I don't know that"
            else:
                if currency_received_1==currency_received_2 :
                    say="Can't Compare same currencies"
                else:
                    
                    vars= list(httpsGet(d[currency_received_1],d[currency_received_2],True))  ## vars is list of values of currency_1 and currency_2, see return values
                    if vars[0]!=0 and vars[5]!=0:
                        if vars[0]>vars[5] :
                            say="1 " + currency_received_1 +" is equivalent to "+ str(abs(int(vars[0]/vars[5]))) + " "+currency_received_2
                        else:
                            say = "1 " + currency_received_2 + " is equivalent to " + str(abs(int(vars[5] / vars[0]))) + " "+currency_received_1
                    say+="<break time='100ms'/> and "
                    if vars[1]>vars[6]:
                        say+=currency_received_1 + " is making profit of " + str(abs(int(vars[1])-int(vars[6]))) + " dollars as compared to "+ currency_received_2
                        
                    else:
                        say+=currency_received_2 + " is making profit of " + str(abs(int(vars[1])-int(vars[6]))) + " dollars as compared to "+ currency_received_1
                        
                    
            ##say+=" While the price "
        return speechResponse(say, False, {})

    elif event['request']['type'] == "SessionEndedRequest":
        say = 'goodbye'
        return speechResponse(say, True, {})


## 3. Helper Function  =================================================================================================
def httpsGet(my_Currency_1,my_Currency_2=None,compare=False):
    """
    :param my_Currency_1: takes input of User-asked-currency
    :return price_1 and change_1 percentage in past 24 hrs:

    """
    global my_url
    my_local_url_1 = my_url + my_Currency_1 + "-usd"
    r_1= requests.get(my_local_url_1)
    #print(my_local_url_1,r_1)
    my_js_1 =(r_1.json())
    print(my_js_1)
    price_1, change_1, cents_1, speak_point_1, speak_zero_1 = findPrice(my_js_1)
    if compare == True:
        # find price_1 of currency1 and currency 2
        my_local_url_2 = my_url + my_Currency_2 + "-usd"
        r_2 = requests.get(my_local_url_2)
        my_js_2 = (r_2.json())
        price_2,change_2,cents_2,speak_point_2,speak_zero_2=findPrice(my_js_2)
        print(price_2,change_2)
        return price_1, change_1, cents_1, speak_point_1, speak_zero_1,price_2,change_2,cents_2,speak_point_2,speak_zero_2

    return price_1, change_1, cents_1, speak_point_1, speak_zero_1

def findPrice(js):
    """
    returns the final price in dollars or cents as per the current price
    """
    if "price" in js["ticker"]:
        price = float(js["ticker"]['price'])
        change = int(float(js["ticker"]['change']))
        cents, speak_point, speak_zero = findSpeakPoint(price)
        if price < 1:
            cents, speak_point, speak_zero = findSpeakPoint(price)
            print(price, change, cents, speak_point, speak_zero)
            return 0, change, cents, speak_point, speak_zero
        else:
            # if not less than 1 directly return dollars
            return int(price), change, 0, False, False
    else:
        print('Error, web service return data not in expected format')
        return 0
def findSpeakPoint(price):
    """
    returns the speak_point,speak_zero and cents if price less than 1 dollar.
    """
    cents = price * 100  # type:float
    if cents < 1.00:
        speak_point = True
        speak_zero = False
        if cents < 0.1:
            speak_zero = True
        cents *= 10000
    else:
        speak_point = speak_zero = False
    return int(cents),speak_point,speak_zero

def whatToSay(price,currency_received,speak_zero,speak_point,change,cents):
    """
    returns the speech response string as "say"
    """
    say=""
    if price == 0:
        say += "The price of " + currency_received + " is "
        if speak_zero == True:
            say += "0 point " + "0 " + str((int)(cents/100)) + " " +str(((int)(cents/10))%10) +" "+str(cents%10) +" cents"
        elif speak_point == True:
            say += "0 point " + str(cents) +" cents"
        else:
            say+=str(cents) + " cents"
    else:
        say = "The price of  " + currency_received + " is " + str(price) + " US  Dollars <break time='100ms'/>"
        if int(change)==0:
            say+="varying very minimal in the last hour"
        else:
            if change>0:
                if int(change)==1:
                    say+="up by 1 dollar in the last hour"
                else:
                    
                    say+="up by "+(str(abs(int(change))))+ " dollars in the last hour"
            else:
                if int(change)==-1:
                    say+="down by 1 dollar in the last hour "
                else:
                    say+=" down by "+ (str(abs(int(change))))+" dollars in the last hour"
    return  say
