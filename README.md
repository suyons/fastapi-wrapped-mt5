# FastAPI wrapped MT5

This repository provides a FastAPI wrapper around the MetaTrader 5 (MT5) trading platform, enabling users to interact with MT5 through RESTful API endpoints. This allows for easier integration with other applications and services.

## Functions for integrating MetaTrader 5 and Python

Source: [MetaTrader 5 Python API Reference](https://www.mql5.com/en/docs/python_metatrader5)

The following table lists the available functions in the FastAPI wrapper for MetaTrader 5, along with their descriptions:

| Function             | Action                                                                                                     |
| -------------------- | ---------------------------------------------------------------------------------------------------------- |
| initialize           | Establish a connection with the MetaTrader 5 terminal                                                      |
| login                | Connect to a trading account using specified parameters                                                    |
| shutdown             | Close the previously established connection to the MetaTrader 5 terminal                                   |
| version              | Return the MetaTrader 5 terminal version                                                                   |
| last_error           | Return data on the last error                                                                              |
| account_info         | Get info on the current trading account                                                                    |
| terminal_Info        | Get status and parameters of the connected MetaTrader 5 terminal                                           |
| symbols_total        | Get the number of all financial instruments in the MetaTrader 5 terminal                                   |
| symbols_get          | Get all financial instruments from the MetaTrader 5 terminal                                               |
| symbol_info          | Get data on the specified financial instrument                                                             |
| symbol_info_tick     | Get the last tick for the specified financial instrument                                                   |
| symbol_select        | Select a symbol in the MarketWatch window or remove a symbol from the window                               |
| market_book_add      | Subscribes the MetaTrader 5 terminal to the Market Depth change events for a specified symbol              |
| market_book_get      | Returns a tuple from BookInfo featuring Market Depth entries for the specified symbol                      |
| market_book_release  | Cancels subscription of the MetaTrader 5 terminal to the Market Depth change events for a specified symbol |
| copy_rates_from      | Get bars from the MetaTrader 5 terminal starting from the specified date                                   |
| copy_rates_from_pos  | Get bars from the MetaTrader 5 terminal starting from the specified index                                  |
| copyrates_range      | Get bars in the specified date range from the MetaTrader 5 terminal                                        |
| copy_ticks_from      | Get ticks from the MetaTrader 5 terminal starting from the specified date                                  |
| copy_ticks_range     | Get ticks for the specified date range from the MetaTrader 5 terminal                                      |
| orders_total         | Get the number of active orders                                                                            |
| orders_get           | Get active orders with the ability to filter by symbol or ticket                                           |
| order_calc_margin    | Return margin in the account currency to perform a specified trading operation                             |
| order_calc_profit    | Return profit in the account currency for a specified trading operation                                    |
| order_check          | Check funds sufficiency for performing a required trading operation                                        |
| order_send           | Send a request to perform a trading operation                                                              |
| positions_total      | Get the number of open positions                                                                           |
| positions_get        | Get open positions with the ability to filter by symbol or ticket                                          |
| history_orders_total | Get the number of orders in trading history within the specified interval                                  |
| history_orders_get   | Get orders from trading history with the ability to filter by ticket or position                           |
| history_deals_total  | Get the number of deals in trading history within the specified interval                                   |
| history_deals_get    | Get deals from trading history with the ability to filter by ticket or position                            |
