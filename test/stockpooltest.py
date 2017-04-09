import stockpool as sp


if __name__ == '__main__':

    mystockpool = sp.StockBase()

    print("Check stock date format:")
    # check stock date format
    for stock in mystockpool.stock_id_iter():
        try:
            for sday in mystockpool.stock_date_iter(stock): break
        except Exception as e:
            print("Error at stock %s: %s" %(stock, e))
            break

    print("Check stock id not in the pool exception:")
    # test stock id not in the pool exception
    try:
        for sday in  mystockpool.stock_date_iter("23"): break
    except Exception as e:
        print(e)

