'''
SIMPLE WEB SERVER
Implements invoice.py functions with a web front end.
'''
from flask import Flask, request, url_for, redirect
import jinja2

from invoice import loadStock, createInvoiceData, saveStockData, display_invoice_list
from invoice import getItemName, saveOrderToFile, loadOrders

STOCK_FILENAME = "stock.txt"

app = Flask(__name__)

env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))


@app.route('/')
def index():
    '''
    Reroute index page to getOrders
    '''
    return redirect(url_for('get_orders'))


@app.route('/item_list')
def item_list():
    '''
    Show list of stock items
    '''
    tmp = env.get_template("stock.html.j2")
    stock_data = loadStock(STOCK_FILENAME)
    # items = itemList(stockData)
    page = tmp.render(data=stock_data)
    return page


@app.route('/enter_invoice')
def enter_invoice():
    '''
    Enter details for a new invoice
    '''
    tmp = env.get_template("enterInvoice.html.j2")
    stock_data = loadStock(STOCK_FILENAME)
    page = tmp.render(title="Create Invoice", data=stock_data, ccys=['EUR', 'GBP', 'USD'])
    return page


@app.route('/create_invoice', methods=['GET', 'POST'])
def create_invoice():
    '''
    Called when enter invoice form is submitted.
    Calculates the values of the invoice from request form data.
    Generates invoice for submitted details.
    '''
    sel_item = int(request.form['item']) - 1
    sel_quantity = int(request.form['quantity'])
    sel_ccy = request.form['selccy']
    print(f"createInvoice: {sel_item}, {sel_quantity}")
    stock_data = loadStock(STOCK_FILENAME)
    generated_invoice_values = createInvoiceData(stock_data, sel_item, sel_quantity, sel_ccy)
    item_name = getItemName(stock_data, sel_item)
    order_id = saveOrderToFile("orders.txt", [item_name, sel_quantity, sel_ccy] + generated_invoice_values)
    saveStockData(STOCK_FILENAME, stock_data)

    page = redirect(f'/showInvoice?orderId={order_id + 1}')
    return page


@app.route("/get_orders")
def get_orders():
    '''
    Returns list of orders
    '''
    orders = loadOrders("orders.txt")
    # print(orders)
    tmp = env.get_template("orders.html.j2")
    page = tmp.render(orders=orders)
    return page


@app.route("/showInvoice")
def show_invoice():
    '''
    Shows an invoice with order id passed as an argument
    '''
    order_id = int(request.args.get('orderId')) - 1
    print(order_id)
    orders = loadOrders("orders.txt")
    order = orders[order_id]
    tmp = env.get_template("showInvoice.html.j2")
    invoice_info = display_invoice_list(*order)
    page = tmp.render(invoice=invoice_info)
    return page


app.run(host="127.0.0.1", port=3000)
