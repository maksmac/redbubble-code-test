import json
import time

cart_json_path = input('What is the file name of the cart? ')
base_price_json_path = input('What is the file name of the base prices? ')
print('\n')

#list will contain lists of items in cart
#product-type, color, size, artistmarkup, quantity
itemincart = []

def openCart(cartname):
    global itemincart
    with open(cartname, 'r') as cart:
        data = json.load(cart)
        cart.close()
        #print(data)
        items = []
        #itterate through each item in the cart and collect nessicary info
        for item in range(len(data)):
            itemname = data[item]['product-type']
            items.append(itemname)
            #if theres no color for item append none
            try:
                itemcolor = data[item]['options']['colour']
            except:
                itemcolor = None
            items.append(itemcolor)
            #if theres no color for item append none
            try:
                itemsize = data[item]['options']['size']
            except:
                itemsize = None
            items.append(itemsize)
            artistmarkup = data[item]['artist-markup']
            items.append(artistmarkup)
            quantity = data[item]['quantity']
            items.append(quantity)
            itemincart.append(items)
            #reset items array for next item in cart
            items = []
    return

#read in the base prices
def openBasePrices(baseprice):
    with open(baseprice, 'r') as price:
        data = json.load(price)
        return data

def calculate():
    cart = itemincart
    cartTotal = 0
    for items in range(len(cart)):
        itemname = cart[items][0]
        itemcolor = cart[items][1]
        itemsize = cart[items][2]

        artistmarkup = cart[items][3]
        quantity = cart[items][4]
        baseprice = openBasePrices(base_price_json_path)
        itemprice = 0
        for x in range(len(baseprice)):
            if baseprice[x]['product-type'] == itemname:
                #check if product has a color option if it does excecute try block
                try:
                    #itterate over each colour option till the matching colour is found
                    for y in range(len(baseprice[x]['options']['colour'])):
                        if baseprice[x]['options']['colour'][y] == itemcolor:
                            #itterate over each size option till the matching size is found
                            for z in range(len(baseprice[x]['options']['size'])):
                                if baseprice[x]['options']['size'][z] == itemsize:
                                    #print(baseprice[x])
                                    itemprice = baseprice[x]['base-price']
                                    #print('Base Price: '+ str(itemprice))
                #if product does not have color execute except block
                except:
                    #try, product for size if size is there excecute try block
                    try:
                        #itterate over each size option till the matching size is found
                        for z in range(len(baseprice[x]['options']['size'])):
                            if baseprice[x]['options']['size'][z] == itemsize:
                                #print(baseprice[x])
                                itemprice = baseprice[x]['base-price']
                                #print('Base Price: '+ str(itemprice))
                    #if product does not have a size, use except block
                    except:
                        itemprice = baseprice[x]['base-price']
                        #print('Base Price: '+ str(itemprice) + '\n')

        Itemtotal = itemprice + round(itemprice * (artistmarkup/100)) * quantity
        cartTotal += Itemtotal

    print('This Carts Total Is: ', str(cartTotal), 'Cents' ,"\n")



if __name__ == '__main__':
    #start = time.time()
    openCart(cart_json_path)
    calculate()
    #print('Time taken to run ' + str(time.time() - start))
