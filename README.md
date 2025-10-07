# Schwab AutoTrader

Welcome to the **Schwab AutoTrader** repository!  This Python application connects to the Schwab API to enable automated trading and real-time market monitoring. Designed for traders and developers, it offers a flexible and efficient way to interact with financial data while supporting advanced strategies and seamless integration into your workflow. (This summary was definitely not written by chatGPT).

---

## Features

- **Market Data Queries**: Retrieve real-time stock price and market-infromation by ticker or other variables using the Schwab API.
- **Real Time Market Analysis**: Retrieved market information can immediately be passed into custom built trade functions for analysis.
- **Authentication**: Securely handles API authentication, including `client_secrets`, `auth_tokens`, and `access_tokens` with encryption and passwords.
- **Customizable Trading Logic**: Supports the development of custom trading strategies using python or the language of your choice.
- **Email Alerting**: Sends automatic emails with infromation on, trade status, trigger-conditions, general market data etc. 
- **Trading!!!**: Lastly and most obviously, this application allows users to interface with their own Schwab brokerage account to trade stocks. [Examples Trades](docs/orderform.md).

## Setup Instructions

### 1. Set up your Schwab Credentials 
 1) Create a Schwab account at [Schwab.com](https://www.schwab.com/client-home). You then need to be approved for an account: (Brokerage, IRA, 401k, etc)
 2) Create a Schwab developer account at: [developer.Schwab.com](https://developer.schwab.com). This is different from your Schwab Brokerage Account.
 3) Get approved to be an individual developer:
    * Select the **Profile** tab and fill out user information. 
    * Scroll down and select **Add Individual Developer Role** and fill out all infromation and justifications. 
    * (It may take a few days to a weeks to get approval) Just be patient. 
    * One you see **Developer Portal Roles** = Individual Developer, with **Member Since** = $Date under the **Profile** tab you are set to move on to app creation.  
 4) On the **Home** menu click on the **Dashboard** tab in the upper right and select **Create App** on the right side of the screen.
 5) Set up your trading app options:
    * Select an API Product: Select Both 'Accounts and Trading Production' AND 'Market Data Production'. 
    * Enter App Name: Add 'autotrader'
    * Enter App Description: Write whatever you want.
    * Enter Callback URL(s): Add 'https://127.0.0.1'
 6) The App will be in a pending state. You can select 'Modify' and in the **Order Limit** option add '120'. 
 7) This Software WILL NOT WORK until the app Status says 'Ready For Use'. This can take a few weeks. 



### 2. Clone the Repository & Installation
   1) Start by cloning this repository on github: [SchwabAutoTrader](https://github.com/CalvinDSeamons/Schwab_AutoTrader.git).

      ```bash
         cd /$wherever_you_want_to_install/
         git clone git@github.com:CalvinDSeamons/Schwab_AutoTrader.git
         cd Schwab_AutoTrader/
      ```
   2) To set up the environment simply run ```python3 setup.py```.
      If you would like to setup the environment manually execute the following commands:
      ```bash
         python3 -m venv venv # This sets up a python virtual environment
         source vnev/bin/activate
         # To leave the venv run 'deactivate'
      ```
      Install the following packages:
      ```bash
         pip install requests pyyaml cryptography 
      ```

### 3 Set up the Schwab Configuration Files
   The first thing the program will ask you for is an Encryption Password. If you forget this password it is not the end of the world. The point of the password is to secure your App Key, App Secret and Scwhab Authentication creds.
   When this application has been activated it can bybass schwab authentication for 6-7 days, so keeping these protected in an encyrpted file is Importanto! You can disable this if you want. 
   1) Enter a encryption password you'll use to refresh the Access-Token and Refresh-Token.
      ```bash
      % "Enter encryption password to secure schwab-credentials and schwab-tokens."
      % "If you have already entered this, please submit the password you set:" $Your_password
      ```
   2) Add the App-Key and App-Secret to the configuration file. If this is your first time running the application you'll be prompted in the commandline to add them.
      ```bash
      % "We've detected an Empty Schwab Credential file! This will be saved in an encryped file at ~/.schwab_auto_trader/schwab-credentials.yaml"
      % "Please provide your APP_KEY [found on developer.schwab.com]:" $your_app_key
      % "Please provide your APP_SECRET [found on developer.schwab.com]:" $your_app_secret
      ```

### 4 Retrieve Schwab Authetication Tokens. 
   1) This application will prompt you to connect to schwab.com, follow the instructions there and paste the return URL in the command line output where you see: 
      ```bash
      % [INFO] Paste Returned URL:
      ```
      If this step is confusing, here is a detailed breakdown of how to get the return URL. [Retrieve Schwab Authentication Token](docs/schwab-authentication.md).

   2) One you past the URL (if valid) you will see the following message: 
      ```bash
         Paste Returned URL: https://127.0.0.1/?code=$your_own_unique_code&session=$your_own_unique_session
         [SUCCESS] Authentication with Schwab successful.
      ```
   3) If everything worked as expected, you are now able to connect to the schwab-api for market prodction and trading commands, have fun!
      You can run custom commands in the command line, build custom trades/market visualizations etc, or use the flask web interface to conduct trades. 
