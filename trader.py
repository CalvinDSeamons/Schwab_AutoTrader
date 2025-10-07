# Trader.py is where the simplified trade class is. 
# Imports
import os
import requests
import urllib.parse
import json
import datetime as dt
from tokens import Tokens
from localutils.log_obj import Log
from zoneinfo import ZoneInfo

class Trader:

    def __init__(self, args):
        self.tokens = Tokens(args)
        self.log = Log()
        self.timeout = 5

    def _params_parser(self, params: dict):
        for key in list(params.keys()):
            if params[key] is None: del params[key]
        return params
    
    def time_parser(self, time_value: str, time_format: str):
            """
            Time parser checks the time value and format and return the correct time var.
            :param time_value: A str containing a date
            :type time_value: str
            :param time_format: A string specifying a datetime format.
            :type time_format: ISO-8601 or just yyyy-MM-dd.
            :return: datetime object with correct format.
            :rtype dt.datetime.date
            """
            if time_format == "yyyy-MM-dd":
            # Parse and return as a datetime.date
                try:
                    parsed_date = dt.datetime.strptime(time_value, "%Y-%m-%d").date()
                    return parsed_date
                except ValueError:
                    raise ValueError("Invalid date format. Expected yyyy-MM-dd.")
            elif time_format == "ISO-8601":
                # Ensure time_value has the full ISO-8601 structure
                try:
                    if len(time_value) < 10:
                        raise ValueError("ISO-8601 format requires at least year-month-day.")
                    
                    # Pad with zeros if necessary to form a complete ISO-8601
                    if len(time_value) == 10:  # yyyy-MM-dd
                        time_value += "T00:00:00.000Z"
                    elif len(time_value) == 19:  # yyyy-MM-ddThh:mm:ss
                        time_value += ".000Z"
                    
                    if time_value.endswith("Z"):
                        # Parse directly as UTC if the input ends with 'Z'
                        parsed_time = dt.datetime.strptime(time_value, "%Y-%m-%dT%H:%M:%S.%fZ")
                        return parsed_time.isoformat()  # Return in ISO-8601 format
                    else:
                        # Parse and adjust for local timezone if no 'Z' is present
                        naive_dt = dt.datetime.strptime(time_value, "%Y-%m-%dT%H:%M:%S.%f")
                        local_tz = dt.datetime.now().astimezone().tzinfo
                        local_dt = naive_dt.replace(tzinfo=dt.timezone.utc).astimezone(local_tz)
                        return local_dt.isoformat()
                
                except ValueError:
                    self.log.error("Invalid ISO-8601 format. Must be [yyyy-MM-ddTHH:mm:ss.SSS]")
            
            else:
                self.log.error("Unsupported time format. Try 'yyyy-MM-dd' or 'ISO-8601'.")

                        

# ---------- Account Methods ---------- #
# Account Methods retrieve information about user account information, accountnum, funds, holdings, etc.

    def get_account(self, fields: str | None = None):
        response = requests.get(f'{self.tokens.base_url}/trader/v1/accounts/',
                            headers={'Authorization': f'Bearer {self.tokens.access_token}'},
                            params={'fields': fields},
                            timeout=self.timeout)
        
        if response.status_code == 200:
            data = response.json()
            return data
        
        else:
            self.log.error(response)

    def get_account_number(self):
        response = requests.get(f'{self.tokens.base_url}/trader/v1/accounts/accountNumbers',
                            headers={'Authorization': f'Bearer {self.tokens.access_token}'},
                            timeout=self.timeout)
        
        if response.status_code == 200:
            data = response.json()
            return data
        
        else:
            self.log.error(response)

    def get_account_accountNumber(self, fields: str | None = None):
        # Lol fix the account hash store. 
        response = requests.get(f'{self.tokens.base_url}/trader/v1/accounts/{(self.tokens.account_hash[0]['hashValue'])}',
                            headers={'Authorization': f'Bearer {self.tokens.access_token}'},
                            params={'fields': fields},
                            timeout=self.timeout)
        
        if response.status_code == 200:
            data = response.json()
            return data
        
        else:
            self.log.error(response)

# ---------- Info Methods ----------- #
# This section contains methods used for querying infromation about stocks. 

    def get_single_quote(self, ticker):
        """
        Get single quote, can take a single string as a symbol just use that.) 
        """
        response = requests.get(f'{self.tokens.base_url}/marketdata/v1/{ticker}/quotes',
                           headers = {'Authorization': f'Bearer {self.tokens.access_token}'},
                           params=())
        
        if response.status_code == 200:
            data = response.json()
            return data
        
        else:
            #self.log.error(response.json())
            return None
        
    
    
    def get_quotes(self, tickers: str | list[str], fields=None, indicative: bool = False) -> dict:
        """
        Get quotes for a list of tickers. 
        :param tickers: list of symbol string e.g. ("AAPL"), ["AAPL", "$SPX", "NVDA", "ADUR"]
        :type tickers: list[str] | str
        param fields: string specifying the amount of return data e.g. ("all", "quote", "fundamental") 
        :type fields: str | None
        :param indicative: whether to get indicative quotes (True/False)
        :type indicative: boolean | None
        :return: dictonary of quotes
        :rtype: dict[]
        """
        response = requests.get(f'{self.tokens.base_url}/marketdata/v1/quotes',
                           headers = {'Authorization': f'Bearer {self.tokens.access_token}'},
                           params=({'symbols':tickers, 'fields': fields, 'indicative': indicative}),
                           timeout=self.timeout)
        

        if response.status_code == 200:
            data = response.json()
            return data
        
        else:
            data = response.json()
            print(data)
            self.log.error(response)
        
    def get_movers(self, exchange: str, sort: str = None, frequency: any = None) -> dict:
        """
        Get movers list of largest stock changes of a given exchange.
        param exchange: symbol ("$DJI"|"$COMPX"|"$SPX"|"NYSE"|"NASDAQ"|"OTCBB"|
                              "INDEX_ALL"|"EQUITY_ALL"|"OPTION_ALL"|
                              "OPTION_PUT"|"OPTION_CALL")
        :type symbol: str
        :param sort: sort ("VOLUME"|"TRADES"|"PERCENT_CHANGE_UP"|"PERCENT_CHANGE_DOWN")
        :type sort: str
        :param frequency: frequency (0|1|5|10|30|60)
        :type frequency: int
        :return: movers
        :rtype: dict[]
        """

        response = requests.get(f'{self.tokens.base_url}/marketdata/v1/movers/{exchange}',
                            headers = {'Authorization': f'Bearer {self.tokens.access_token}'},
                            params=({'sort': sort, 'frequency': frequency}), timeout=self.timeout)
        
        if response.status_code == 200:
            data = response.json()
            return data
        
        else:
            self.log.error(response)

    def get_instruments(self, symbol: str, projection: str) -> dict:
        """
        Get Instruments details by using different projections. No idea what this is.
        :param symbol: symbol
        :type symbol: str
        :param projection: projection ("symbol-search"|"symbol-regex"|"desc-search"|"desc-regex"|"search"|"fundamental")
        :type projection: str
        :return: instruments
        :rtype: dict[]
        """
        response = requests.get(f'{self.tokens.base_url}/marketdata/v1/instruments',
                            headers={'Authorization': f'Bearer {self.tokens.access_token}'},
                            params={'symbol': symbol, 'projection': projection},
                            timeout=self.timeout)
    
        if response.status_code == 200:
            data = response.json()
            return data
        
        else:
            self.log.error(response)
    
    def get_instrument_cusip(self, cusip_id: str | int) -> dict:
        """
        Get instrument for a symbol using cusip id.
        :param cusip_id: cusip id
        :type cusip_id: str|int
        :return: instrument
        :rtype: dict[]
        """
        response = requests.get(f'{self.tokens.base_url}/marketdata/v1/instruments/{cusip_id}',
                            headers={'Authorization': f'Bearer {self.tokens.access_token}'},
                            timeout=self.timeout)

        if response.status_code == 200:
            data = response.json()
            return data
        
        else:
            self.log.error(response)

    def get_market_hours(self, symbols: list[str], date: dt.datetime | str = None) -> dict:
        """
        Get Market Hours for dates in the future across different markets.
        :param symbols: list of market symbols ("equity", "option", "bond", "future", "forex")
        :type symbols: list
        :param date: date
        :type date: datetime | str
        :return: market hours
        :rtype: dict[]
        """
        
        response = requests.get(f'{self.tokens.base_url}/marketdata/v1/markets',
                            headers={'Authorization': f'Bearer {self.tokens.access_token}'},
                            params={'markets': symbols,
                                    'date': (date)},
                            timeout=self.timeout)

        if response.status_code == 200:
            data = response.json()
            return data
        
        else:
            self.log.error(response.json())
            pass

    def get_market_hours_by_id(self, market_id: str, date: dt.datetime):
        """
        :param marketId: Available values : equity, option, bond, future, forex
        :type marketId: str
        :param date: Valid date range is from currentdate to 1 year from today. 
                     It will default to current day if not entered. Date format:YYYY-MM-DD
        :type date: datetime YYYY_MM-DD
        """
        response = requests.get(f'{self.tokens.base_url}/marketdata/v1/markets/{market_id}',
                            headers={'Authorization': f'Bearer {self.tokens.access_token}'},
                            params={'date': (date)},timeout=self.timeout)

        if response.status_code == 200:
            data = response.json()
            return data
        
        else:
            self.log.error(response.json())
            pass
    


    def get_option_chains(self, symbols: list[str], contractType: str | None=None, strikeCount: int | None=None, 
                          includeUnderlyingQuote: bool | None=None, strategy: str | None=None, interval: int | None=None, 
                          strike: int | None=None, range: str | None=None, toDate: dt.datetime | None=None,
                          fromDate: dt.datetime | None=None, volatility: int | None=None, underlyingPrice: int | None=None, 
                          interestRate: int | None=None, daysToExpiration: int | None=None, 
                          expirationMonth: str | None=None, optionType: str | None=None, entitlement: str | None=None) -> dict:
        """
        Cancer Cancer Cancer Cancer!
        Get Option Chain data from a specific stock. Holy God so many args.
        :param symbols: list of stocks/etf/etc ("$SPX", "AAPL", etc).
        :type symbols: list
        :param contractType: 'CALL', 'PUT', or 'ALL'
        :type contractType: str
        :param strikeCount: The Number of strikes to return above or below the at-the-money price.
        :type strikeCount: int 
        :param includeUnderlyingQuote Includes underlying quote information
        :type includeUnderlyingQuote: boolean
        :param strategy: OptionChain strategy. Default is SINGLE. ANALYTICAL allows the use of volatility, 
                         underlyingPrice, interestRate, and daysToExpiration params to calculate theoretical values.
                         Other options are: [SINGLE, ANALYTICAL, COVERED, VERTICAL, CALENDAR, STRANGLE, STRADDLE, 
                                            BUTTERFLY, CONDOR, DIAGONAL, COLLAR, ROLL].
        :type strategy: str
        :param interval: Strike interval for spread strategy chains (see strategy param).
        :type interval: int (should be double though).
        :param strike: Strike price of the option.
        :type strike: int
        :param range: Range(ITM/NTM/OTM etc.)
        :type range: str
        :param toDAte: Range to this date.
        :type toDate: datetime
        :param fromDate: Range from this date.
        :type fromDate: datetime
        :param volatility: Volatility to use in calculations. Applies only to ANALYTICAL strategy chains (see strategy param)
        :type volatility: int
        :param underlyingPrice: Underlying price to use in calculations. Applies only to ANALYTICAL strategy chains (see strategy param)
        :type underlyingPrice: int
        :param interestRate: Interest rate to use in calculations. Applies only to ANALYTICAL strategy chains (see strategy param)
        :type interestRate: int
        :param daysToExpiration: Days to expiration to use in calculations. Applies only to ANALYTICAL strategy chains (see strategy param)
        :type daysToExpiration: int
        :param expirationMonth: Expiration month e.g. [JAN, FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC, ALL].
        :type expirationMonth: str
        :param optionType: Option Type.
        :type optionType: str
        :param entitlement: Entitlement Only ifretail token, entitlement of client PP-PayingPro, NP-NonPro and PN-NonPayingPro [PN,NN,PP]
        :type entitlement: str
        :return: Option Chain Data.
        :rtype: dict[]
        """

        response = requests.get(f'{self.tokens.base_url}/marketdata/v1/chains',
                            headers={'Authorization': f'Bearer {self.tokens.access_token}'},
                            params={'symbol': symbols, 'contractType': contractType, 'StrikeCount': strikeCount,
                                    'inculdeUnderlyingQuotes': includeUnderlyingQuote, 'strategy': strategy, 'interval': interval,
                                    'strike': strike, 'range': range, 'toDate': toDate, 'fromDate': fromDate, 'volatility': volatility,
                                    'underlyingPrice': underlyingPrice, 'interestRate': interestRate, 'datsToExpiration': daysToExpiration, 
                                    'expirationMonth': expirationMonth,'optionType': optionType, 'entitlement': entitlement},
                            timeout=self.timeout)
        
        if response.status_code == 200:
            data = response.json()
            return data
        
        else:
            self.log.error(response.json())
            pass


    def get_expiration_option_chain(self,symbol):
        """
        Get Option Expiration (Series) information for an optionable symbol. 
        Does not include individual options contracts for the underlying.
        :param symbol: Stock symbol to search.
        :type symbol: str
        :return: Option Chain Data.
        :rtype: dict[]
        """
        response = requests.get(f'{self.tokens.base_url}/marketdata/v1/expirationchain',
                            headers={'Authorization': f'Bearer {self.tokens.access_token}'},
                            params={'symbol': symbol},
                            timeout=self.timeout)
        
        if response.status_code == 200:
            data = response.json()
            return data
        
        else:
            self.log.error(response.json())
            pass

    def get_price_history(self, symbol = str, periodType: str | None=None, period: int | None=None, frequencyType: str | None=None,
                          frequency: int | None=None, startDate: int | None=None, endDate: int | None=None, 
                          needExtendedHoursData: bool | None=None, needPreviousClose: bool | None = None):
        """
        Get Price History returns the price hsitroy of a given stock based of a date range. 
        :param symbol: The Equity symbol used to look up price history
        :type symbol: str
        :param periodType: The chart period being requested. Available values : day, month, year, ytd.
        :type periodType: str
        :param period: The number of chart period types. days(1,2,3,4,5,10), month(1,2,3,6), year(1,2,3,5,10,15,20), ytd(1).
        :type period: int
        :param frequencyType: The time frequencyType: If the periodType is day(minute), month(daily, weekly), year(daily, weekly, monthly) 
                                                                           ytd(daily, weekly)
        :type frequencyType: str
        :param frequency: The time frequency duration. Minute vales are (1,5,10,15,20) all others value is 1. 
        :type frequency: int
        :param startDate: The start date, Time in milliseconds since the UNIX epoch eg 1451624400000, If not specified startDate 
                          will be (endDate - period) excluding weekends and holidays.
        :type startDate: int
        :param endDate: The end date, Time in milliseconds since the UNIX epoch eg 1451624400000
                        If not specified, the endDate will default to the market close of previous business day.
        :type endDate: int
        :param needExtendedHoursData: Get Extended hours dat.
        :type needExtendedHoursData: bool
        :param needPreviousClose: Get price information from prior close.
        :type needPreviousClose: bool
        :return: Price History Data.
        :rtype: dict[]
        """
        
        response = requests.get(f'{self.tokens.base_url}/marketdata/v1/pricehistory',
                            headers={'Authorization': f'Bearer {self.tokens.access_token}'},
                            params=({'symbol': symbol, 'periodType': periodType, 'period': period, 'frequencyType':frequencyType,
                                     'frequency':frequency, 'startDate': startDate, 'endDate':endDate, 'needExtendedHoursData':
                                     needExtendedHoursData, 'needPreviousClose': needPreviousClose}))
        
        if response.status_code == 200:
            data = response.json()
            return data
        
        else:
            self.log.error(response.json())
            pass

  # ---------- Trade Methods ---------- #
  # [WARNING] -- This section contains functions that execute stock trades, use caution when calling. 


    def get_orders(self, accountHash: str, fromEnteredTime: dt.datetime, toEnteredTime: dt.datetime, maxResults: int | None=None,
                    status: str | None=None) -> dict:
        """
        Get set or all orders from a specific account.
        :param accountNumner: hashed account number. 
        :type accountNumber: str
        :param maxResults: The max number of orders to retrieve. Default is 3000.
        :type maxResults: int
        :param fromEnteredTime: Specifies that no orders entered before this time should be returned.
        :type fromEnteredTime: datetime yyyy-MM-dd'T'HH:mm:ss.SSSZ
        :param toEnteredTime: Specifies that no orders entered after this time should be returned.
        :type toEnteredTime: datetime yyyy-MM-dd'T'HH:mm:ss.SSSZ
        :param status: Specifies that only orders of this status should be returned. List of values are:  
                       AWAITING_PARENT_ORDER, AWAITING_CONDITION, AWAITING_STOP_CONDITION, AWAITING_MANUAL_REVIEW, 
                       ACCEPTED, AWAITING_UR_OUT, PENDING_ACTIVATION, QUEUED, WORKING, REJECTED, PENDING_CANCEL, 
                       CANCELED, PENDING_REPLACE, REPLACED, FILLED, EXPIRED, NEW, AWAITING_RELEASE_TIME, 
                       PENDING_ACKNOWLEDGEMENT, PENDING_RECALL, UNKNOWN.
        :type status: str
        :return: Account Order Data.
        :rtype: dict[]
        """
       
        response = requests.get(f'{self.tokens.base_url}/accounts{accountHash}/orders',
                            headers={'Authorization': f'Bearer {self.tokens.access_token}'},
                            params=({'accountHash': accountHash, 'maxResults': maxResults, 'fromEnteredTime': fromEnteredTime,
                                     'toEnteredTime': toEnteredTime, 'status': status}))
        return response
        
    def post_orders(self, accountHash: str, orderForm: dict):
        """
        Post Order sends and orderForm to execute a specified trade. 
        :param accountHash: hashed account number. Trade will be executed on this Accounts!
        :type accountHash: str
        :param orderForm: dictonary schema that contains the trade information. 
        :type orderForm: dict
        :return: Emtpy response code if successful. 
        :rtype: Request.response
        """
        data =  requests.post(f'{self.tokens.base_url}/trader/v1/accounts/{accountHash}/orders',
                             headers={"Accept": "application/json", 'Authorization': f'Bearer {self.tokens.access_token}',
                                      "Content-Type": "application/json"},
                             json=orderForm,
                             timeout=self.timeout)
         
    def get_order_by_id(self, accountHash: str, orderId: int):
        """
        Get a specific order by its ID, for a specific account.
        :param accountHash: hashed account number. Trade will be executed on this Accounts!
        :type accountHash: str
        :param orderId: The ID of the order being retrieved.
        :type orderId: int
        :return: Dictonary of the submitted Order.
        :rtype: dict
        """
        
        response = requests.post(f'{self.tokens.base_url}/trader/v1/accounts/{accountHash}/orders/{orderId}',
                             headers={"Accept": "application/json", 'Authorization': f'Bearer {self.tokens.access_token}',
                                      "Content-Type": "application/json"},
                             timeout=self.timeout)
        
        if response.status_code == 200:
            data = response.json()
            return data
        
        else:
            self.log.error(response.json())
            pass
        
    def delete_order(self, accountHash: str, orderId: int):
        """
        Cancel a specific order for a specific account
        :param accountHash: hashed account number. Trade will be executed on this Accounts!
        :type accountHash: str
        :param orderId: The ID of the order being retrieved.
        :type orderId: int
        :return: Dictonary of the submitted Order.
        :rtype: dict
        """
        response = requests.post(f'{self.tokens.base_url}/trader/v1/accounts/{accountHash}/orders/{orderId}',
                             headers={"Accept": "application/json", 'Authorization': f'Bearer {self.tokens.access_token}',
                                      "Content-Type": "application/json"},
                             timeout=self.timeout)
        
        if response.status_code == 200:
            data = response.json()
            return data
        
        else:
            self.log.error(response.json())
            pass

    def change_order(self, accountHash: str, orderId: str, orderForm: dict):
        """
        Replace an existing order for an account. The existing order will be replaced by the new order. 
        Once replaced, the old order will be canceled and a new order will be created.
        :param accountHash: hashed account number. Trade will be executed on this Accounts!
        :type accountHash: str
        :param orderId: order id
        :type orderId: int
        :param order: dictonary schema that contains the trade information. 
        :type order: dict
        :return: response of order change. 
        :rtype: dict
        """
        response = requests.put(f'{self.tokens.base_url}/trader/v1/accounts/{accountHash}/orders/{orderId}',
                            headers={"Accept": "application/json", 'Authorization': f'Bearer {self.tokens.access_token}',
                                     "Content-Type": "application/json"},
                            json=orderForm,
                            timeout=self.timeout)
    
        if response.status_code == 200:
            data = response.json()
            return data
        
        else:
            self.log.error(response.json())
            pass

    def get_all_orders(self, fromEnteredTime: str, toEnteredTime: str, maxResults: int | None=None, status: str | None=None):
        """
        Get all orders for all accounts
        :param fromEnteredTime: Specifies that no orders entered before this time should be returned. 
                                Valid ISO-8601 formats are- yyyy-MM-dd'T'HH:mm:ss.SSSZ
                                Date must be within 60 days from today's date. 'toEnteredTime' must also be set.
        :type fromEnteredTime: datetime [yyyy-MM-dd'T'HH:mm:ss.SSSZ]
        :param toEnteredTime: same as fromEnteredTime...
        :type toEnteredTime: datetime [yyyy-MM-dd'T'HH:mm:ss.SSSZ]
        :param status: Specifies that only orders of this status should be returned.
                       Available values : AWAITING_PARENT_ORDER, AWAITING_CONDITION, AWAITING_STOP_CONDITION, 
                       AWAITING_MANUAL_REVIEW, ACCEPTED, AWAITING_UR_OUT, PENDING_ACTIVATION, QUEUED, WORKING, 
                       REJECTED, PENDING_CANCEL, CANCELED, PENDING_REPLACE, REPLACED, FILLED, EXPIRED, NEW, 
                       AWAITING_RELEASE_TIME, PENDING_ACKNOWLEDGEMENT, PENDING_RECALL, UNKNOWN
        :type status: str
        :return: List of dictionaries containing all orders in the time range.
        :rtype: list[dict] 
        """

        response = requests.get(f'{self.tokens.base_url}/trader/v1/orders',
                            headers={'Authorization': f'Bearer {self.tokens.access_token}'},
                            params=({'maxResults':maxResults, 'fromEnteredTime':fromEnteredTime, 'toEnteredTime':toEnteredTime,
                                     'status':status}))
        
        if response.status_code == 200:
            data = response.json()
            return data
        
        else:
            self.log.error(response.json())
            pass
        

    def preview_orders(self):
        """
        API_Request still under development by Schwab.
        """
        pass

# -------------Transactions and Util Methods---------- #
# Following contains util and transaction history methods.

    def get_all_transactions(self, accountHash:str, startDate: str, endDate: str, symbol: str | None=None):
        """
        All transactions for a specific account. Maximum number of transactions in response is 3000. Maximum date range is 1 year.
        :param accountNumber: The encrypted ID of the account.
        :type accountNumber: str
        :param startDate: Specifies that no transactions entered before this time should be returned.
        :type startDate: datetime [yyyy-MM-dd'T'HH:mm:ss.SSSZ]
        :param endDate: Specifies that no transactions entered after this time should be returned.
        :type endDate: datetime [yyyy-MM-dd'T'HH:mm:ss.SSSZ]
        :param symbol: It filters all the transaction activities based on the symbol specified. 
                       If there is any special character in the symbol, please send th encoded value.
        :type symbol: Available values : TRADE, RECEIVE_AND_DELIVER, DIVIDEND_OR_INTEREST, ACH_RECEIPT, ACH_DISBURSEMENT, 
                                         CASH_RECEIPT, CASH_DISBURSEMENT, ELECTRONIC_FUND, WIRE_OUT, WIRE_IN, JOURNAL, MEMORANDUM,
                                         MARGIN_CALL, MONEY_MARKET, SMA_ADJUSTMENT
        :return: List of dictionaries containg transaction histroy for a specific account.
        :rtype: list[dict]
        """
        response = requests.get(f'{self.tokens.base_url}/trader/v1/accounts/{self.tokens.account_hash}/transactions',
                            headers={'Authorization': f'Bearer {self.tokens.access_token}'},
                            params=({'accountHash':accountHash, 'startDate':startDate, 'endDate':endDate,
                                     'symbol':symbol}))
        if response.status_code == 200:
            data = response.json()
            return data
        
        else:
            self.log.error(response.json())
            pass

    def get_transaction_by_id(self, accountHash: str, transactionId: int):
        """
        Get specific transaction information for a specific account
        :param accountNumber: The encrypted ID of the account.
        :type accountNumber: str
        :param transactionId: The ID of the transaction being retrieved.
        :type accountNumber: int
        :return: Dictionary containg the transaction for a specific Id.
        :rtype: list[dict]
        """
        response = requests.get(f'{self.tokens.base_url}/trader/v1/accounts/{self.tokens.account_hash}/transactions/{transactionId}',
                            headers={'Authorization': f'Bearer {self.tokens.access_token}'},
                            params=({'accountHash':accountHash, 'transactionId':transactionId}))
        if response.status_code == 200:
            data = response.json()
            return data
        
        else:
            self.log.error(response.json())
            pass

    def get_user_preferences(self):
        """
        Get user preference information for the logged in user.
        :return: User Preferences and Streaming Info
        :rtype: request.Response
        """
        return requests.get(f'{self.tokens.base_url}/trader/v1/userPreference',
                            headers={'Authorization': f'Bearer {self.tokens.access_token}'},
                            timeout=self.timeout)


# ----------- Trade Orders ---------- #
# Trade orders contains simple order methods to make basic stock trades.
# These serve as helper methods if the user doesn't want ot build out an entire order.
# I dont know how useful this will be seeing that so many parameters are needed, this are super simple orders

    def buy_stock(self, symbol: str, price: int, quantity: int):
        """
        Buy a stock, ETF, or fund at a specificed price, 
        Order is good until the end of day. 
        """
        return {
            "orderType" : "LIMIT",
            "session" : "NORMAL",
            "price": price,
            "duration" : "DAY",
            "orderStrategyType" : "SINGLE",
            "orderLegCollection" : [{
                "instruction" : "BUY",
                "quantity" : int(quantity),
                "instrument" :{
                    "symbol" : symbol,
                    "assetType" : "EQUITY"
                }
            }

            ]
        }