import mysql.connector
import hashlib
import math
import smtplib
from socket import gaierror
from smtplib import SMTPException

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  passwd="22051998",
  database = "icapitstop"
)
mycursor = mydb.cursor()

def login(username, password):
    sql = "select * from credentials where username = %s;"
    vals = (username,)
    mycursor.execute(sql, vals)
    values = mycursor.fetchone()
    if values:
        if str(values[2]) == str(hashlib.md5(password.encode()).hexdigest()):
            return values[0],values[3]
        else:
            return "Password incorrect"
    return "Username does not exist"



def display_all_products():
    sql = "select * from product;" #8 ,9
    mycursor.execute(sql)
    products = mycursor.fetchall()
    produse = {}
    prd = {}
    i = 0
    products1 = []
    for prod in products:
        if prod[8] == 1:
            p = [prod[0],prod[1],prod[2],prod[3],prod[4],prod[5],prod[6],prod[7],prod[8],prod[9], prod[10], prod[7] - (prod[7]*prod[9]/100)]
        else:
            p = [prod[0],prod[1],prod[2],prod[3],prod[4],prod[5],prod[6],prod[7],prod[8],prod[9], prod[10], prod[7]]
        prd[i] = p
        i += 1
    #pprint(prd)
    produse = {'produse':prd}
    return produse


def delete_supplier(name):
    sql = "select id_supp from suppliers where name = %s;"
    mycursor.execute(sql, (name,))
    id_supp = mycursor.fetchone()[0]
    sql = "delete from product where supplier_id = %s"
    sql = "delete from orders where id_supplier = %s"
    mycursor.execute(sql, (id_supp,))
    sql = "delete from suppliers where id_supp = %s;"
    mycursor.execute(sql, (id_supp,))
    sql = "delete from credentials where id_user = %s;"
    mycursor.execute(sql, (id_supp, ))
    mydb.commit()


def logout():
    return -1


def client_register(last_name, first_name, email, address, username, password, telephone):
    sql = "Select credentials.username, clients.email from credentials " \
          "Join clients on clients.id_cl = credentials.id_user where credentials.username = %s;"
    vals = (username, )
    mycursor.execute(sql, vals)
    exists = mycursor.fetchone()
    if not exists:
        if len(password) > 5:
            if len(telephone) < 10 or len(telephone) > 10:
                return "Telephone must have 10 digits"
            else:
                sql_cred = "Insert into credentials (username, password, user_type) values (%s, %s, %s);"
                password = hashlib.md5(password.encode())
                val_cred = (username, password.hexdigest(), "client")
                mycursor.execute(sql_cred, val_cred)
                sql_select = "select id_user from credentials where username = %s;"
                mycursor.execute(sql_select, (username,))
                id_user = mycursor.fetchone()
                sql_client = "Insert into clients (id_cl, last_name, first_name, email, address, telephone) values (%s, %s, %s, %s, %s, %s);"
                val_client = (int(id_user[0]), last_name, first_name, email, address, telephone)
                mycursor.execute(sql_client, val_client)
                mydb.commit()
                return id_user[0]
        else:
            return "Password must have min 6 chars"
    else:
        if username == exists[0]:
            return "Username exists"
        elif email == exists[1]:
            return "E-mail exists"
        else:
            return "Username and e-mail exists"


def supplier_register(name, email, username, password, cpassword):
    # print(username)
    sql = "Select credentials.username, suppliers.email from credentials Join suppliers on suppliers.id_supp = credentials.id_user where credentials.username = %s;"
    vals = (username, )
    mycursor.execute(sql, vals)
    exists = mycursor.fetchone()
    if not exists:
        if password == cpassword:
            if len(password) > 5:
                sql_cred = "Insert into credentials (username, password, user_type) values (%s, %s, %s);"
                password = hashlib.md5(password.encode()).hexdigest()
                val_cred = (username, password, "supplier")
                mycursor.execute(sql_cred, val_cred)
                sql_select = "select id_user from credentials where username = %s;"
                mycursor.execute(sql_select, (username,))
                id_user = mycursor.fetchone()
                sql_supplier = "Insert into suppliers (id_supp, name, email) values (%s, %s, %s);"
                val_supplier = (int(id_user[0]), name, email)
                mycursor.execute(sql_supplier, val_supplier)
                mydb.commit()
                return mycursor.rowcount, "record inserted"
            else:
                return "Password must have min 6 chars"
        else:
            return "Password and Confirmation Password doesn't match"
    else:
        if username == exists[0]:
            return "Username exists"
        elif email == exists[1]:
            return "E-mail exists"
        else:
            return "Username and e-mail exists"

def update_stock(product_id, stock):
    sql = "Update table product " \
          "set stock=%s where product_id = %s;"
    vals = (stock, product_id)
    mycursor.execute(sql, vals)
    mydb.commit()

def remove_discount(product_id):
    sql = "Update table product " \
          "set discount = %s, discount_percent = %s " \
          "where product_id = %s;"
    vals = (0, 0, product_id)
    mycursor.execute(sql, vals)
    mydb.commit()

def update_discount(product_id, discount_percent):
    if discount_percent == 0:
        sql = "Update product " \
            "set discount = %s, discount_percent = %s " \
            "where product_id = %s;"
        vals = (0, discount_percent, product_id)
        mycursor.execute(sql, vals)
        mydb.commit()
    else:
        sql = "Update product " \
            "set discount = %s, discount_percent = %s " \
            "where product_id = %s;"
        vals = (1, discount_percent, product_id)
        mycursor.execute(sql, vals)
        mydb.commit()

def display_new_orders(id_supplier):
    sql = "select * from order where id_supplier = %s and status = 'processing';"
    mycursor.execute(sql, (id_supplier,))
    new_orders = mycursor.fetchall()
    for new_order in new_orders:
        print(new_order)

def get_user_infos(user_id):
    sql = "select * from clients as c join credentials as cr on cr.id_user=c.id_cl where c.id_cl = %s;"
    mycursor.execute(sql, (user_id,))
    info = mycursor.fetchone()
    infos = {'username':info[7], 'last_name':info[1], 'first_name':info[2], 'email':info[3], 'address':info[4], 'telephone':info[5]}
    return infos

def change_infos(user_id, fname, lname, email, address, telephone):
    sql = "update clients set email=%s, address=%s, telephone=%s, first_name=%s, last_name=%s where id_cl = %s"
    vals = (email, address, telephone, fname, lname, user_id)
    mycursor.execute(sql, vals)
    mydb.commit()

def change_password(user_id, old_password, new_password, conf_new_pass):
    sql = "select password from credentials where id_user = %s;"
    mycursor.execute(sql, (user_id, ))
    parola = mycursor.fetchone()[0]
    parola_veche_criptata = str(hashlib.md5(old_password.encode()).hexdigest())
    if str(parola) == parola_veche_criptata:
        if new_password == conf_new_pass:
            parola_noua = hashlib.md5(new_password.encode()).hexdigest()
            sql = "update credentials set password = %s where id_user = %s;"
            vals = (parola_noua, user_id)
            mycursor.execute(sql, vals)
            mydb.commit()
        return 1
    else:
        return 0


def product_register(name, mark, category, supplier_id, stock, description, price, discount, discount_percent, images):
    sql_product = "Insert into product (supplier_id, name,mark, category, stock, description, price, discount, discount_percent, images) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    val_product = (supplier_id, name, mark, category, stock, description, price, discount, discount_percent, images)
    mycursor.execute(sql_product, val_product)
    mydb.commit()

def add_product_shopping_cart(id_user, product_id):
    sql = "select price, discount, discount_percent from product where product_id = %s;"
    vals = (product_id, )
    mycursor.execute(sql, vals)
    details = mycursor.fetchone()
    price = details[0]
    discount = details[1]
    discount_percent = details[2]
    sql = "select * from shopping_cart where id_client = %s"
    vals = (id_user, )
    mycursor.execute(sql, vals)
    result = mycursor.fetchone()
    produse = ''
    if result :
        sql = "select products from shopping_cart where id_client = %s"
        vals = (id_user,)
        mycursor.execute(sql, vals)
        products = mycursor.fetchone()[0]
        products = products.split(", ")
        prods = []
        prood = []
        if len(products) == 1:
            pr = products[0].replace("(","").replace(")","").split(",")
            if int(pr[0]) == int(product_id):
                produse = "("+str(pr[0])+","+str(int(pr[1])+1)+")"
            else:
                produse =  "("+str(pr[0])+","+str(pr[1])+"), " + "("+str(product_id)+","+str(1)+")"
        elif len(products) == 0:
            produse = "("+str(product_id)+","+str(1)+")"
        else:
            for p in range(len(products)):
                pr = products[p].replace("(","").replace(")","").split(",")
                if p == 0:
                    if int(pr[0]) == int(product_id):
                        produse += "("+str(pr[0])+","+str(int(pr[1])+1)+")"
                    else:
                        produse += "("+str(pr[0])+","+str(pr[1])+")"
                else:
                    if int(pr[0]) == int(product_id):
                        produse += ", ("+str(pr[0])+","+str(int(pr[1])+1)+")"
                    else:
                        produse += ", ("+str(pr[0])+","+str(pr[1])+")"
                prods.append(int(pr[0]))
            if int(product_id) not in prods:
                produse += ", ("+str(product_id)+","+str(1)+")"

        sql = "update shopping_cart set products = %s where id_client = %s"
        vals = (produse ,id_user)
        mycursor.execute(sql, vals)
        mydb.commit()
    else:
        products = "(" +str(product_id)+","+str(1)+")"
        sql = "insert into shopping_cart (id_client, products) values (%s, %s);"
        vals = (id_user,products)
        mycursor.execute(sql, vals)
        mydb.commit()

def delete_one_product(id_user, product_id):
    sql = "select price, discount, discount_percent from product where product_id = %s;"
    vals = (product_id, )
    mycursor.execute(sql, vals)
    details = mycursor.fetchone()
    price = details[0]
    discount = details[1]
    discount_percent = details[2]
    sql = "select * from shopping_cart where id_client = %s"
    vals = (id_user, )
    mycursor.execute(sql, vals)
    result = mycursor.fetchone()
    produse = ''
    sql = "select products from shopping_cart where id_client = %s"
    vals = (id_user,)
    mycursor.execute(sql, vals)
    products = mycursor.fetchone()[0]
    products = products.split(", ")
    prods = []
    prood = []
    if len(products) == 1:
        pr = products[0].replace("(","").replace(")","").split(",")
        if int(pr[0]) == int(product_id):
            if int(pr[1]) > 1:
                produse = "("+str(pr[0])+","+str(int(pr[1])-1)+")"
        else:
            produse =  "("+str(pr[0])+","+str(pr[1])+")"
    else:
        for p in range(len(products)):
            pr = products[p].replace("(","").replace(")","").split(",")
            if p == 0:
                if int(pr[0]) == int(product_id):
                    if int(pr[1]) > 1:
                        produse += "("+str(pr[0])+","+str(int(pr[1])-1)+")"
                else:
                    produse += "("+str(pr[0])+","+str(pr[1])+")"
            else:
                if int(pr[0]) == int(product_id):
                    if int(pr[1]) > 1:
                        produse += ", ("+str(pr[0])+","+str(int(pr[1])-1)+")"
                else:
                    if produse == '':
                        produse += "("+str(pr[0])+","+str(pr[1])+")"
                    else:
                        produse += ", ("+str(pr[0])+","+str(pr[1])+")"
            prods.append(int(pr[0]))

    if produse:
        sql = "update shopping_cart set products = %s where id_client = %s"
        vals = (produse ,id_user)
        mycursor.execute(sql, vals)
        mydb.commit()
    else:
        sql = "delete from shopping_cart where id_client = %s"
        vals = (id_user,)
        mycursor.execute(sql, vals)
        mydb.commit()

def remove_product_from_shopping_cart(id_user, id_product):
    sql = "select products from shopping_cart where id_client = %s;"
    mycursor.execute(sql, (id_user, ))
    products = mycursor.fetchone()[0]
    produse = []
    prods = ''
    if len(products) > 14:
        products = products.split(", ")
        for p in range(len(products)):
            prod = products[p].replace("(","").replace(")","").split(",")
            if int(prod[0]) != int(id_product):
                produse.append((int(prod[0]),int(prod[1])))
        for p in range(len(produse)-1):
            prods += "("+str(produse[p][0])+','+str(produse[p][1])+")"+", "
        prods += "("+str(produse[len(produse)-1][0])+','+str(produse[len(produse)-1][1])+")"
    elif len(products) > 6:
        products = products.split(", ")
        for p in products:
            prod = p.replace("(","").replace(")","").split(",")
            produse.append((int(prod[0]),int(prod[1])))
            if int(prod[0]) != int(id_product):
                prods += "("+str(prod[0])+','+str(prod[1])+")"
    else:
        products = products.replace("(","").replace(")","").split(",")
        if int(products[0]) != int(id_product):
                prods += "("+str(products[0])+','+str(products[1])+")"
    if prods != '' :
        sql = "update shopping_cart set products = %s where id_client = %s;"
        vals = (prods, id_user)
        mycursor.execute(sql, vals)
        mydb.commit()
    else:
        sql = "delete from shopping_cart where id_client = %s;"
        vals = (id_user, )
        mycursor.execute(sql, vals)
        mydb.commit()


def delete_product(product_id):
    sql = "select * from shopping_cart;"
    mycursor.execute(sql)
    shopping_carts = mycursor.fetchall()
    for cart in shopping_carts:
        products = cart[2]
        total = cart[3]
        prods = ''
        for product in products:
            if int(product) == int(product_id):
                sql = "select price from product where product_id = %s;"
                mycursor.execute(sql, (product_id, ))
                price = mycursor.fetchone()[0]
                total -= float(price)
            else:
                prods = str(product)
        sql = "update table shopping_cart set products = %s, total = %s where id = %s;"
        vals = (prods, total, cart[0])
        mycursor.execute(sql, vals)
        mydb.commit()
    sql = "select * from orders where products=;"
    mycursor.execute(sql)
    orders = mycursor.fetchall()
    for order in orders:
        products = order[3].split(",")
        total = float(order[4])
        prods = ''
        for product in products:
            if int(product) == int(product_id):
                sql = "select price from product where product_id = %s;"
                mycursor.execute(sql, (product_id, ))
                price = mycursor.fetchone()[0]
                total -= float(price)
            else:
                prods = str(product)
        sql = "update table orders set products = %s, total = %s where id = %s;"
        vals = (prods, total, order[0])
        mycursor.execute(sql, vals)
        mydb.commit()
    sql = "delete from product where product_id = %s;"
    mycursor.execute(sql, (product_id,))
    mydb.commit()


def place_order(id_user):
    sql = "select * from shopping_cart where id_client = %s;"
    mycursor.execute(sql, (id_user,))
    vals = mycursor.fetchone()
    id_shop = vals[0]
    products = vals[2]
    supl_prods = {}
    if len(products) > 7:
        products = products.split(", ")
        for p in products:
            pr = p.replace(")","").replace("(","").split(",")
            sql = "select supplier_id, stock from product where product_id = %s;"
            mycursor.execute(sql, (pr[0],))
            supp_id, stock = mycursor.fetchone()
            if int(stock) >= int(pr[1]):
                if supp_id not in supl_prods.keys():
                    supl_prods[supp_id] = [(pr[0],pr[1]),]
                else:
                    supl_prods[supp_id].append((pr[0],pr[1]))
        for k,e in supl_prods.items():
            prods = ''
            if len(e) > 1:
                prods = "(" + str(e[0][0]) + "," + str(e[0][1]) + ")"
                for p in range(1, len(e)):
                    prods += ", (" + str(e[p][0]) + "," + str(e[p][1]) + ")"
            else:
                prods = "(" + str(e[0][0]) + "," + str(e[0][1]) + ")"
            sql = "Insert into orders (id_supplier, client_id, products) values (%s, %s, %s);"
            valori = (k, id_user, prods)
            mycursor.execute(sql, valori)
            mydb.commit()
    else:
        products = products.replace("(","").replace(")","").split(",")
        sql = "select supplier_id, stock from product where product_id = %s;"
        mycursor.execute(sql, (products[0],))
        supp_id, stock = mycursor.fetchone()
        if int(stock) >= int(products[1]):
            supl_prods[supp_id] = (products[0], products[1])
            prods = "("+str(supl_prods[supp_id][0])+","+str(supl_prods[supp_id][1])+")"
            sql = "Insert into orders (id_supplier, client_id, products) values (%s, %s, %s);"
            valori = (supp_id, id_user, prods)
            mycursor.execute(sql, valori)
            mydb.commit()
    sql = "delete from shopping_cart where id = %s"
    mycursor.execute(sql, (id_shop,))
    mydb.commit()


def update_order_status(status, order_id):
    sql = "update orders set status = %s where order_id = %s;"
    vals = (status, order_id)
    mycursor.execute(sql, vals)
    mydb.commit()

def return_suppliers():
    supp = []
    sql = "select * from suppliers as s join credentials as c on c.id_user = s.id;"
    mycursor.execute(sql)
    for i in mycursor:
        supp.append(i)
    return supp


def show_all_suppliers():
    sql = "select * from suppliers;"
    mycursor.execute(sql)
    supps = mycursor.fetchall()
    suppliers = []
    for s in supps:
        suppliers.append(s)
    return {"suppliers": suppliers}

def show_all_messages():
    sql = "select * from contact;"
    mycursor.execute(sql)
    msgs = mycursor.fetchall()
    messages = []
    for m in msgs:
        messages.append(m)
    return {"messages": messages}

def show_shopping_cart(id_user):
    sql = "select products from shopping_cart where id_client = %s;"
    vals = (id_user, )
    mycursor.execute(sql,vals)
    shopping = mycursor.fetchone()
    if(shopping):
        products = shopping[0]
        prods_return = {}
        produse = []
        total1 = 0
        #for pr in products:
        if len(products) > 6:
            products = products.split(", ")
            for p in products:
                prod = p.replace("(","").replace(")","").split(",")
                print("ma-ta: ",prod)
                produse.append((int(prod[0]),int(prod[1])))
            print("prd : ",produse)
            for product in produse:
                sql = "select name, price, discount_percent, images from product where product_id = %s;"
                mycursor.execute(sql, (product[0],))
                details = mycursor.fetchone()
                if details[2] > 0:
                    tot_str  = str(float(product[1])* (details[1] - ((details[1]*details[2])/100)))
                    tot_str = tot_str.split('.')
                    if len(tot_str[1]) < 2:
                        tot_str[1] = tot_str[1] + "00"
                    prods_return[product[0]] = {'name': details[0], 'price_after': details[1] - (details[1]*details[2])/100, "total_price": tot_str[0]+'.'+tot_str[1][0:2], "price_before":details[1],'quantity':product[1], "images":details[3]}
                    total1 += float(product[1]) * prods_return[product[0]]['price_after']
                else:
                    tot_str  = str(float(product[1]) * details[1])
                    tot_str = tot_str.split('.')
                    if len(tot_str[1]) < 2:
                        tot_str[1] = tot_str[1] + "00"
                    prods_return[product[0]] = {'name': details[0], 'price_after': details[1], 'total_price': tot_str[0]+'.'+tot_str[1][0:2] , 'price_before':details[1], 'quantity':product[1], "images":details[3]}
                    total1 += float(product[1]) * details[1]
                total_str = str(total1)
                total_str = total_str.split('.')
                if len(total_str[1]) < 2:
                    total_str[1] = total_str[1] + "00"
                prods_return['total'] = float(total_str[0] + "." + total_str[1][0:2])
                if float(prods_return['total']) < 250:
                    total_price = str(float(prods_return['total']) +16 )
                    total_price = total_price.split(".")
                    if len(total_price[1]) < 2:
                        total_price[1] = total_price[1] + "00"
                    prods_return["total_price"] = total_price[0] + "." + total_price[1][0:2]
                else:
                    total_price = str(prods_return['total'])
                    total_price = total_price.split(".")
                    if len(total_price[1]) < 2:
                        total_price[1] = total_price[1] + "00"
                    prods_return["total_price"] = total_price[0] + "." + total_price[1][0:2]
        else:
            products = products.replace("(","").replace(")","").split(",")
            if(len(products) > 0):
                produse = (int(products[0]), int(products[1]))
                sql = "select name, price, discount_percent, images from product where product_id = %s;"
                mycursor.execute(sql, (produse[0],))
                details = mycursor.fetchone()
                if details[2] > 0:
                    tot_str  = str(produse[1] * (details[1] - ((details[1]*details[2])/100)))
                    tot_str = tot_str.split('.')
                    if len(tot_str[1]) < 2:
                        tot_str[1] = tot_str[1] + "00"
                    prods_return[produse[0]] = {'name': details[0], 'price_after': (details[1] - ((details[1]*details[2])/100)), "total_price": tot_str[0] + "." + tot_str[1][0:1], "price_before":details[1],'quantity':produse[1], "images":details[3]}
                    total1 += produse[1] * prods_return[produse[0]]['price_after']
                else:
                    tot_str  = str(produse[1] * details[1])
                    tot_str = tot_str.split('.')
                    if len(tot_str[1]) < 2:
                        tot_str[1] = tot_str[1] + "00"
                    prods_return[produse[0]] = {'name': details[0], 'price_after': details[1], 'total_price': tot_str[0] + "." + tot_str[1][0:1] , 'price_before':details[1], 'quantity':produse[1], "images":details[3]}
                    total1 += produse[1] * details[1]
                total_str = str(total1)
                total_str = total_str.split('.')
                if len(total_str[1]) < 2:
                    total_str[1] = total_str[1] + "00"
                prods_return['total'] = float(total_str[0] + "." + total_str[1][0:2])
                if float(prods_return['total']) < 250:
                    total_price = str(float(prods_return['total']) + 16 )
                    total_price = total_price.split(".")
                    if len(total_price[1]) < 2:
                        total_price[1] = total_price[1] + "00"
                    prods_return["total_price"] = total_price[0] + "." + total_price[1][0:1]
                else:
                    total_price = str(prods_return['total'])
                    total_price = total_price.split(".")
                    if len(total_price[1]) < 2:
                        total_price[1] = total_price[1] + "00"
                    prods_return["total_price"] = total_price[0] + "." + total_price[1][0:1]
            else:
                prods_return = {'produse':"nimic"}
    else:
        prods_return = {'produse':"nimic"}
    return prods_return

def show_products_by_category(category):
    sql = "select * from product where category = %s;"
    vals = (category, )
    mycursor.execute(sql, vals)
    products = mycursor.fetchall()
    produse = []
    for prod in products:
        if prod[8] == 1:
            p = (prod[0],prod[1],prod[2],prod[3],prod[4],prod[5],prod[6],prod[7],prod[8],prod[9], prod[10], prod[7] - (prod[7]*prod[9]/100))
        else:
            p = (prod[0],prod[1],prod[2],prod[3],prod[4],prod[5],prod[6],prod[7],prod[8],prod[9], prod[10], prod[7])
        produse.append(p)
    return {'produse':produse}

def show_products_by_supplier(supplier_name):
    sql = "Select id_supp from suppliers where name = %s"
    mycursor.execute(sql, (supplier_name, ))
    id_supp = mycursor.fetchone()[0]
    sql = "select * from product where supplier_id = %s;"
    mycursor.execute(sql, (id_supp, ))
    products = mycursor.fetchall()
    produse = []
    for prod in products:
        if prod[8] == 1:
            p = (prod[0],prod[1],prod[2],prod[3],prod[4],prod[5],prod[6],prod[7],prod[8],prod[9], prod[10], prod[7] - (prod[7]*prod[9]/100))
        else:
            p = (prod[0],prod[1],prod[2],prod[3],prod[4],prod[5],prod[6],prod[7],prod[8],prod[9], prod[10], prod[7])
        produse.append(p)
    return {'produse':produse}


def display_supplier_products(id_supp):
    sql = "select * from product where supplier_id = %s;"
    mycursor.execute(sql, (id_supp, ))
    products = mycursor.fetchall()
    produse = {}
    prd = {}
    i = 0
    products1 = []
    for prod in products:
        if prod[8] == 1:
            p = {'id_produs':prod[0],'id_supplier':prod[1],'nume_produs':prod[2],'mark':prod[3],'category':prod[4],'stock':prod[5],'description':prod[6],'price':prod[7],'discount':prod[8],'discount_percent':prod[9], 'images':prod[10], 'final_price':prod[7] - (prod[7]*prod[9]/100)}
        else:
            p = {'id_produs':prod[0],'id_supplier':prod[1],'nume_produs':prod[2],'mark':prod[3],'category':prod[4],'stock':prod[5],'description':prod[6],'price':prod[7],'discount':prod[8],'discount_percent':prod[9], 'images':prod[10], 'final_price':prod[7]}
        prd[i] = p
        i += 1
    #pprint(prd)
    produse = {'produse':prd}
    return produse


def show_products_by_name(product_name):
    sql = "select * from products where name = %s;"
    mycursor.execute(sql, (product_name, ))
    products = mycursor.fetchall()
    produse = []
    for prod in products:
        if prod[8] == 1:
            p = (prod[0],prod[1],prod[2],prod[3],prod[4],prod[5],prod[6],prod[7],prod[8],prod[9], prod[10], prod[7] - (prod[7]*prod[9]/100))
        else:
            p = (prod[0],prod[1],prod[2],prod[3],prod[4],prod[5],prod[6],prod[7],prod[8],prod[9], prod[10], prod[7])
        produse.append(p)
    return {'produse':produse}


def sort_products_by_price(type_sort_price):
    if type_sort_price == -1:
        sorting = "desc"
    else:
        sorting = "asc"
    sql = "select * from product order by price " + sorting +";"
    mycursor.execute(sql)
    products = mycursor.fetchall()
    produse = {}
    prd = {}
    i = 0
    products1 = []
    for prod in products:
        print(prod)
        if prod[8] == 1:
            p = [prod[0],prod[1],prod[2],prod[3],prod[4],prod[5],prod[6],prod[7],prod[8],prod[9], prod[10], prod[7] - (prod[7]*prod[9]/100)]
        else:
            p = [prod[0],prod[1],prod[2],prod[3],prod[4],prod[5],prod[6],prod[7],prod[8],prod[9], prod[10], prod[7]]
        prd[i] = p
        i += 1
    #pprint(prd)
    produse = {'produse':prd}
    return produse

def sort_products_by_stock():
    sql = "select * from product order by stock desc;"
    mycursor.execute(sql)
    products = mycursor.fetchall()
    produse = {}
    prd = {}
    i = 0
    products1 = []
    for prod in products:
        if prod[8] == 1:
            p = [prod[0],prod[1],prod[2],prod[3],prod[4],prod[5],prod[6],prod[7],prod[8],prod[9], prod[10], prod[7] - (prod[7]*prod[9]/100)]
        else:
            p = [prod[0],prod[1],prod[2],prod[3],prod[4],prod[5],prod[6],prod[7],prod[8],prod[9], prod[10], prod[7]]
        prd[i] = p
        i += 1
    #pprint(prd)
    produse = {'produse':prd}
    return produse

def sort_products_by_discount():
    sql = "select * from product order by discount_percent desc;"
    mycursor.execute(sql)
    products = mycursor.fetchall()
    produse = {}
    prd = {}
    i = 0
    products1 = []
    for prod in products:
        print(prod)
        if prod[8] == 1:
            p = [prod[0],prod[1],prod[2],prod[3],prod[4],prod[5],prod[6],prod[7],prod[8],prod[9], prod[10], prod[7] - (prod[7]*prod[9]/100)]
        else:
            p = [prod[0],prod[1],prod[2],prod[3],prod[4],prod[5],prod[6],prod[7],prod[8],prod[9], prod[10], prod[7]]
        prd[i] = p
        i += 1
    #pprint(prd)
    produse = {'produse':prd}
    return produse

def sort_products_by_discount_first_six():
    sql = "select * from product where discount_percent > 0 order by discount_percent desc LIMIT 6;"
    mycursor.execute(sql)
    products = mycursor.fetchall()
    produse = []
    for prod in products:
        if prod[8] == 1:
            p = (prod[0],prod[1],prod[2],prod[3],prod[4],prod[5],prod[6],prod[7],prod[8],prod[9], prod[10], prod[7] - (prod[7]*prod[9]/100))
        produse.append(p)
    return {'produse':produse}

def show_interested(prods):
    produse = []
    if len(prods) > 0:
        for p in prods:
            sql = "select * from product where product_id = %s;"
            mycursor.execute(sql, (p, ))
            details = mycursor.fetchone()[0]
            if p[8] == 1:
                pr = (p[0],p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9], p[10], p[7] - (p[7]*p[9]/100))
            else:
                pr = (p[0],p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9], p[10], p[7])
            produse.append(p)
    return {'produse':produse}

def contact(name, subject, email, content):
    sql = "insert into contact (client_name, email, subject, content) values (%s, %s, %s, %s);"
    vals = (name, email, subject, content)
    mycursor.execute(sql,vals)
    mydb.commit()

def read_message(id_message):
    sql = "update contact set wasRead = 1 where request_id = %s"
    mycursor.execute(sql, (id_message,))
    mydb.commit()

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
from email.mime.base import MIMEBase
from pprint import pprint


def send_message(req_id, recv, message):
    email = smtplib.SMTP("smtp.gmail.com",587)
    email.starttls()
    email.login("icapitstop@gmail.com","Ica123456")
    email.sendmail("ICAPitstopAutoshop@domain.com", recv, message)
    email.quit()


def send_mail(supplier, recv, subject, message):
    sql = "select email from suppliers where id_supp = %s;"
    mycursor.execute(sql, (supplier,))
    supp_email = mycursor.fetchone()[0]
    mail = "From: {}\nTo: {}\nSubject: {}\n{}".format(supplier, recv, subject, message)
    email = smtplib.SMTP("smtp.gmail.com",587)
    email.starttls()
    email.login("icapitstop@gmail.com","Ica123456")
    email.sendmail("ICAPitstopAutoshop@domain.com", recv, mail)
    email.quit()


def delete_message(msg_id):
    sql = "delete from contact where request_id = %s;"
    mycursor.execute(sql,(msg_id, ))
    mydb.commit()

def search_supp(name):
    sql = "select * from suppliers where name = %s;"
    mycursor.execute(sql, (name, ))
    supp = mycursor.fetchone()[0]
    return {"supp": supp}


def display_all_orders(id_supplier):
    sql = "select * from orders where id_supplier = %s;" # order_id, id_supplier, client_id,products, status
    mycursor.execute(sql, (id_supplier,))
    orders = mycursor.fetchall()
    comenzi = {}
    for i in range(len(orders)):
        products = orders[i][3].split(", ")
        total = 0.0
        produs = {}
        for p in products:
            prod = p.replace(")","").replace("(","").split(",")
            sql = "select * from product where product_id = %s;"
            mycursor.execute(sql, (prod[0],))
            det = mycursor.fetchone()
            if int(det[5]) >= int(prod[1]):
                if int(det[8]):
                    total += (det[7] - (det[7]*det[9]/100)) * float(prod[1])
                else:
                    total += det[7] * float(prod[1])
                produs[prod[0]] = [det[2], det[3], det[4], det[6], prod[1]] #name, mark,category, price
        sql = "select * from clients where id_cl = %s;"
        mycursor.execute(sql, (orders[i][2],))
        client = mycursor.fetchone()
        comenzi[orders[i][0]] = {"client_name":client[1]+" "+client[2], 'email':client[3], "address":client[4], "telephone":client[5],"total": total, "products": produs, "state": orders[i][4], "client_id" : orders[i][2]}
    return comenzi

def get_categories():
    sql = "select distinct category from product;"
    mycursor.execute(sql)
    categorii = mycursor.fetchall()
    categ = set()
    for i in categorii:
        categ.add(i[0])

    return {'categories' : list(categ)}
