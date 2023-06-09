import interface
import flet as ft
from time import sleep
from helpers import thread


pairs = {
    "BTC": "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599",
    "ETH": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
}


class Table(ft.UserControl):
    tokens = {
        token['address']: token for token in interface.get_token()
    }

    _columns = ['PAIR', 'BUY', 'SELL', 'PROFIT USDT', 'PROFIT %', 'ADDRESS', '']

    def __init__(self, page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page
        self._popup = None
        self._table = None
        self.sync()
        self.render()

    def build(self):
        return ft.Column([
            self.popup,
            self.table
        ], 
        horizontal_alignment="center")

    @property
    def table(self):
        if self._table == None:
            self._table = ft.DataTable(
                columns=self.columns
            )

        return self._table

    @classmethod
    @property
    def columns(cls):
        return [
            ft.DataColumn(ft.Text(col)) for col in cls._columns
        ]

    def render(self):
        self.page.add(self.build())

    @property
    def trades(self):
        trades = []
        prices = interface.get_best_prices()

        for trade in interface.get_trades():
            token = self.tokens[trade['address']]
            pair = token['symbol'] + token['pair']
            if token['pair'] in ['BTC', 'ETH']:
                addr = pairs[token['pair']]
                usdt = prices[addr]['uniswap']['sell']
            else:
                continue

            trades.append({
                'pair': pair,
                'buy': trade['buy'],
                'sell': trade['sell'],
                'usdt': usdt * trade['profit_percentage'] / 100,
                'profit': trade['profit_percentage'],
                'address': trade['address'],
            })

        trades.sort(key=lambda x: x['profit'], reverse=True)
        return trades
    
    
    def update_table(self):
        rows = []
        for trade in self.trades:
            if not trade['profit'] > 0:
                continue

            pair = ft.Text(trade['pair'])
            buy = ft.Text(trade['buy'])
            sell = ft.Text(trade['sell'])


            color, sign = ("#FFAC1C", "⬆️") if trade['profit'] > 3 else ("#50C878", "⬆️") if trade['profit'] > 0 else ("#EE4B2B", "⬇️")
            usdt = ft.Text(f"{sign}{abs(trade['usdt']):0.2f}$", color=color)
            profit = ft.Text(f"{sign}{abs(trade['profit']):0.2f}%", color=color)
            
            
            on_click = lambda e, x=trade['address']: (self.page.set_clipboard(x), self.snack("Copied to clipboard!"))
            address = ft.TextButton(trade['address'][:3]+'...'+trade['address'][-3:], 
                                    on_click=on_click)
            

            icon = ft.IconButton(icon=ft.icons.DELETE,
                                 icon_color=ft.colors.RED,
                                 tooltip="Delete Token",
                                 on_click=lambda x,address=trade['address'] : (self.delete(x, address), 
                                                                               self.snack('Pair closed')))
            
            cells = [
                ft.DataCell(pair),
                ft.DataCell(buy),
                ft.DataCell(sell),
                ft.DataCell(usdt),
                ft.DataCell(profit),
                ft.DataCell(address),
                ft.DataCell(icon),
            ]
            rows.append(ft.DataRow(cells=cells))
        
        
        self.table.rows = rows
        self.page.update()

    @thread
    def sync(self):
        while True:
            self.update_table()
            sleep(1)

    def snack(self, msg):
        self.page.snack_bar = ft.SnackBar(ft.Text(msg), action="Ok")
        self.page.snack_bar.open = True
        self.page.update()

    def delete(self, e, address):
        interface.close_pair(address)

        if self._popup is not None:
            self._popup.items = self.closed_tokens
            self.page.update()

    @property
    def closed_tokens(self):
        tokens = []
        for token in interface.get_token():
            if token['track']:
                continue
            if token['pair'] is None:
                continue

            on_click = lambda e, x=token['address']: (self.open_pair(x), self.snack("Pair opened"))
            item = ft.PopupMenuItem(text=token['symbol']+token['pair'],
                                    on_click=on_click) 
                
            tokens.append(item)
        return tokens

    @property
    def popup(self):
        if self._popup == None:
            self._popup = ft.PopupMenuButton(
            items=self.closed_tokens
        )
        return self._popup

    def open_pair(self, address):
        interface.open_pair(address)

        if self._popup is not None:
            self._popup.items = self.closed_tokens
            self.page.update()