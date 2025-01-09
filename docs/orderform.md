# How to create order forms for post_orders(). 
The Schwab-api takes in a order schema that is a dictonary of key values pairs (and lists). Listed below are descriptions of variables and basic examples to help automate trades. Learning how to creates these by scratch is a pain, there are lots of variables and poor documentation on what keys are requried. This page will list as many example trades as possible, I recommend finding a similar trade to the one you are creating and tweaking the variables. 

Begin orderforms with the following: </br>
* ***orderType*** - This key defines what type of order form we are creating. Values can be:
  * **LIMIT**: Executes at a specified price or better.
  * **MARKET**: Executes immediately at the current market price.
  * **STOP**: Becomes a market order once a specified stop price is reached.
  * **STOP_LIMIT**: Becomes a limit order once a specified stop price is reached.
  * **TRAILING_STOP**: A stop order that moves with the market price.
  * **TRAILING_STOP_LIMIT**: A trailing stop order that becomes a limit order when triggered.

* ***session*** - Specifies the trading session during which the order will be active.
  * **NORMAL**: Regular trading hours.
  * **EXTENDED**: Extended trading hours.
  * **SEAMLESS**: Both regular and extended hours.

* ***duration*** - Indicates how long the order remains active.
  * **DAY**: Expires at the end of the trading day if not executed.
  * **GOOD_TILL_CANCEL**: Remains active until canceled.
  * **FILL_OR_KILL**: Must be executed immediately in its entirety or canceled.
  * **IMMEDIATE_OR_CANCEL**: Must be executed immediately; any portion not filled is canceled.
  * **GOOD_TILL_DATE**: Remains active until a specified date.

* ***price*** - Specifies the price at which to execute the order.
  * **Usage**: Must use keys: LIMIT or STOP_LIMIT to use.
  * **Values**: Any dollar amount e.g. 0.45, 1.55, 280.00.

* **orderLegCollection** - A list containing the details of each component of the order.
  * **instruction**: Action to take.
    * **BUY**: Purchase the security.
    * **SELL**: Sell the security.
    * **SELL_SHORT**: Sell the security short.
    * **BUY_TO_COVER**: Buy back a security previously sold short.
  * **instrument**: Details of the financial instrument Additonal Sub-dict{}.
    * **assetType**: Type of asset.
      * **EQUITY**: Stocks.
      * **OPTION**: Options contracts.
      * **MUTUAL_FUND**: Mutual funds.
      * **FIXED_INCOME**: Bonds and other fixed-income securities
      * **CASH_EQUIVALENT**: Cash or cash-like instruments.
    * **symbol**: Ticker symbol of the security (e.g., "AAPL" for Apple Inc.).
  * **quantity**: Number of shares or contracts to trade.
* **orderStrategyType**: Specifies the strategy type of the order.
  * **SINGLE**: A standalone order.
  * **OCO**: One-Cancels-Other order.
  * **TRIGGER**: An order that triggers another order upon execution.


---
### Buy Market: Stock ###
Buy 15 shares of Apple stock at the Market Price (ATM), good for the Day.
 
```yaml
{
  "orderType": "MARKET", 
  "session": "NORMAL", 
  "duration": "DAY", 
  "orderStrategyType": "SINGLE", 
  "orderLegCollection": [ 
   { 
    "instruction": "BUY", 
    "quantity": 15, 
    "instrument": { 
     "symbol": "AAPL", 
     "assetType": "EQUITY" 
    } 
   } 
  ] 
}
```

### Buy Market: Stock Limit Order. ###
Buy 1 share of Apple stock if the price reaches $160.00/share. Good until the end of the day.

``` yaml
{
 "orderType": "LIMIT",
 "session": "NORMAL",
 "price": "160",
 "duration": "DAY",
 "orderStrategyType": "SINGLE",
 "orderLegCollection": [
  {
   "instruction": "BUY",
   "quantity": 1,
   "instrument": {
     "symbol": "AAPL",
     "assetType": "EQUITY"
    }
   }
  ]
}
```


### Buy Limit: Single Option ###
Buy to open 10 contracts of the XYZ March 15, 2024 $50 CALL at a Limit of $6.45 good for the Day.
 
```yaml 
{ 
  "complexOrderStrategyType": "NONE", 
  "orderType": "LIMIT", 
  "session": "NORMAL", 
  "price": "6.45", 
  "duration": "DAY", 
  "orderStrategyType": "SINGLE", 
  "orderLegCollection": [ 
   { 
    "instruction": "BUY_TO_OPEN", 
    "quantity": 10, 
    "instrument": { 
     "symbol": "XYZ   240315C00500000", 
     "assetType": "OPTION" 
    } 
   } 
  ] 
}
```

### Buy Limit: Vertical Call Spread
Buy to open 2 contracts of the XYZ March 15, 2024 $45 Put and Sell to open 2 contract of the XYZ March 15, 2024 $43 Put at a LIMIT price of $0.10 good for the Day.
 
```yaml
{
  "orderType": "NET_DEBIT",
  "session": "NORMAL",
  "price": "0.10",
  "duration": "DAY",
  "orderStrategyType": "SINGLE",
  "orderLegCollection": [
   {
    "instruction": "BUY_TO_OPEN",
    "quantity": 2,
    "instrument": {
     "symbol": "XYZ   240315P00045000",
     "assetType": "OPTION"
    }
   },
   {
    "instruction": "SELL_TO_OPEN",
    "quantity": 2,
    "instrument": {
     "symbol": "XYZ   240315P00043000",
      "assetType": "OPTION"
    }
   }
  ]
}
```


### Conditional Order: One Triggers Another
Buy 10 shares of XYZ at a Limit price of $34.97 good for the Day. If filled, immediately submit an order to Sell 10 shares of XYZ with a Limit price of $42.03 good for the Day. Also known as 1st Trigger Sequence.
 
```yaml
{ 
  "orderType": "LIMIT", 
  "session": "NORMAL", 
  "price": "34.97", 
  "duration": "DAY", 
  "orderStrategyType": "TRIGGER", 
  "orderLegCollection": [ 
   { 
    "instruction": "BUY", 
    "quantity": 10, 
    "instrument": { 
     "symbol": "XYZ", 
     "assetType": "EQUITY" 
    } 
   } 
  ], 
  "childOrderStrategies": [ 
   { 
    "orderType": "LIMIT", 
    "session": "NORMAL", 
    "price": "42.03", 
    "duration": "DAY", 
    "orderStrategyType": "SINGLE", 
    "orderLegCollection": [ 
     { 
      "instruction": "SELL", 
      "quantity": 10, 
      "instrument": { 
       "symbol": "XYZ", 
       "assetType": "EQUITY" 
      } 
     } 
    ] 
   } 
  ] 
}
```

### Conditional Order: One Cancels Another
Sell 2 shares of XYZ at a Limit price of $45.97 and Sell 2 shares of XYZ with a Stop Limit order where the stop price is $37.03 and limit is $37.00. Both orders are sent at the same time. If one order fills, the other order is immediately cancelled. Both orders are good for the Day. Also known as an OCO order.
 
```yaml
{ 
  "orderStrategyType": "OCO", 
  "childOrderStrategies": [ 
   { 
    "orderType": "LIMIT", 
    "session": "NORMAL", 
    "price": "45.97", 
    "duration": "DAY", 
    "orderStrategyType": "SINGLE", 
    "orderLegCollection": [ 
     { 
      "instruction": "SELL", 
      "quantity": 2, 
      "instrument": { 
       "symbol": "XYZ", 
       "assetType": "EQUITY" 
      } 
     } 
    ] 
   }, 
   { 
    "orderType": "STOP_LIMIT", 
    "session": "NORMAL", 
    "price": "37.00", 
    "stopPrice": "37.03", 
    "duration": "DAY", 
    "orderStrategyType": "SINGLE", 
    "orderLegCollection": [ 
     { 
      "instruction": "SELL", 
      "quantity": 2, 
      "instrument": { 
       "symbol": "XYZ", 
       "assetType": "EQUITY" 
      } 
     } 
    ] 
   } 
  ] 
}
 ```

### Conditional Order: One Triggers A One Cancels Another
Buy 5 shares of XYZ at a Limit price of $14.97 good for the Day. Once filled, 2 sell orders are immediately sent: Sell 5 shares of XYZ at a Limit price of $15.27 and Sell 5 shares of XYZ with a Stop order where the stop price is $11.27. If one of the sell orders fill, the other order is immediately cancelled. Both Sell orders are Good till Cancel. Also known as a 1st Trigger OCO order.
 
```yaml
{ 
  "orderStrategyType": "TRIGGER", 
  "session": "NORMAL", 
  "duration": "DAY", 
  "orderType": "LIMIT", 
  "price": 14.97, 
  "orderLegCollection": [ 
   { 
    "instruction": "BUY", 
    "quantity": 5, 
    "instrument": { 
     "assetType": "EQUITY", 
     "symbol": "XYZ" 
    } 
   } 
  ], 
  "childOrderStrategies": [ 
   { 
    "orderStrategyType": "OCO", 
    "childOrderStrategies": [ 
     { 
      "orderStrategyType": "SINGLE", 
      "session": "NORMAL", 
      "duration": "GOOD_TILL_CANCEL", 
      "orderType": "LIMIT", 
      "price": 15.27, 
      "orderLegCollection": [ 
       { 
        "instruction": "SELL", 
        "quantity": 5, 
        "instrument": { 
         "assetType": "EQUITY", 
         "symbol": "XYZ" 
        } 
       } 
      ] 
     }, 
     { 
      "orderStrategyType": "SINGLE", 
      "session": "NORMAL", 
      "duration": "GOOD_TILL_CANCEL", 
      "orderType": "STOP", 
      "stopPrice": 11.27, 
      "orderLegCollection": [ 
       { 
        "instruction": "SELL", 
        "quantity": 5, 
        "instrument": { 
         "assetType": "EQUITY", 
         "symbol": "XYZ" 
        } 
       } 
      ] 
     } 
    ] 
   } 
  ] 
}
```

### Sell Trailing Stop: Stock
Sell 10 shares of XYZ with a Trailing Stop where the trail is a -$10 offset from the time the order is submitted. As the stock price goes up, the -$10 trailing offset will follow. If stock XYZ goes from $110 to $130, your trail will automatically be adjusted to $120. If XYZ falls to $120 or below, a Market order is submitted. This order is good for the Day.
 
```yaml
{ 
  "complexOrderStrategyType": "NONE", 
  "orderType": "TRAILING_STOP", 
  "session": "NORMAL", 
  "stopPriceLinkBasis": "BID", 
  "stopPriceLinkType": "VALUE", 
  "stopPriceOffset": 10, 
  "duration": "DAY", 
  "orderStrategyType": "SINGLE",
  "orderLegCollection": [ 
   { 
    "instruction": "SELL", 
    "quantity": 10, 
    "instrument": { 
     "symbol": "XYZ", 
     "assetType": "EQUITY" 
    } 
   } 
  ] 
}
```
 


