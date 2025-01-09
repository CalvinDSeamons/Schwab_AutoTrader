# Schwab AutoTrader

Welcome to the **Schwab AutoTrader** repository!  This Python application connects to the Schwab API to enable automated trading and real-time market monitoring. Designed for traders and developers, it offers a flexible and efficient way to interact with financial data while supporting advanced strategies and seamless integration into your workflow.

---

## Features

- **Market Data Queries**: Retrieve real-time stock price and market-infromation by ticker or other variables using the Schwab API.
- **Real Time Market Analysis**: Retrieved market information can immediately be passed into custom built trade functions for analysis.
- **Authentication**: Securely handles API authentication, including `client_secrets`, `auth_tokens`, and `access_tokens` with encryption and passwords.
- **Customizable Trading Logic**: Supports the development of custom trading strategies using python or the language of your choice.
- **Email Alerting**: Sends automatic emails with infromation on, trade status, trigger-conditions, general market data etc. 
- **Trading!!!**: Lastly and most obviously, this application allows users to interface with their own Schwab brokerage account to trade stocks. 

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



### 2. Clone the Repository

```bash
git clone <private_repo_url>
cd schwab-trader-app



