from django.shortcuts import render,redirect
from django.http import HttpResponse
from .algorithms import mySQLconn
from collections import defaultdict
from django.contrib.auth.models import User,auth
from django.core.files.storage import FileSystemStorage
from pprint import pprint


def index(request):
    temp = mySQLconn.sort_products_by_discount_first_six()
    categorii = mySQLconn.get_categories()
    return render(request, 'index.html', {"temp":temp, 'categories':categorii})

def account(request):
    if request.session['user_type'] == "client":
        infos = mySQLconn.get_user_infos(request.session['user_id'])
        return render(request, "account.html",{'infos':infos})
    else:
        return render(request, "404.html")

def change_password(request):
    if request.method == "POST":
        user_id = request.session['user_id']
        old_pass = request.POST['oldpass']
        new_pass = request.POST['newpass']
        cnew_pass = request.POST['cnewpass']
        print(old_pass != new_pass, new_pass == cnew_pass)
        if old_pass != new_pass and new_pass == cnew_pass:
            print("ma-ta")
            res = mySQLconn.change_password(user_id, old_pass, new_pass, cnew_pass)
            infos = mySQLconn.get_user_infos(request.session['user_id'])
            if res == 1:
                return render(request, "account.html",{"success": "1", "infos":infos})
            else:
                return render(request, "account.html",{"success": "0", "infos":infos})
        else:
            infos = mySQLconn.get_user_infos(request.session['user_id'])
            return render(request, "account.html",{"success": "0", "infos":infos})


def login(request):
    if request.method == 'POST':
        if request.POST['submit'] == "Signup":
            username = request.POST['username']
            password = request.POST['password']
            fname = request.POST['fname']
            lname = request.POST['lname']
            address = request.POST['address']
            phone = request.POST['phone']
            email = request.POST['email']

            result = mySQLconn.client_register(lname, fname, email, address, username, password, phone)
            try:
                result = int(result)
                request.session['user_id'] = result
                request.session['username'] = username
                return redirect('shop.html')
            except ValueError :
                request.session['resultRegister'] = result
            return render(request, 'login.html')
        elif request.POST['submit'] == 'Login':
            username = request.POST['username']
            password = request.POST['password']
            result = mySQLconn.login(username,password)
            if type(result) is tuple:
                res = int(result[0])
                request.session['user_id'] = res
                request.session['username'] = username
                request.session['user_type'] = result[1]
                if request.session['user_type'] == "supplier":
                    return redirect('supplier-orders.html')
                if request.session['user_type'] == "admin":
                    return redirect('admin.html')
                if request.session['user_type'] == "client":
                    return redirect('shop.html')
            elif type(result) is str:
                request.session['resultLogin'] = result
                return render(request, 'login.html')
    else:
        request.session['resultRegister'] = None
        request.session['resultLogin'] = None
        return render(request, 'login.html')

def displayCartProducts(request):
    temp = mySQLconn.show_shopping_cart(request.session['user_id'])
    return render(request,'cart.html',{"temp":temp})


def logout(request):
    request.session['user_id'] = None
    request.session['user_type'] = None
    request.session['products_visited'] = None
    return redirect('index.html')

def checkout(request):
    return render(request, 'checkout.html')



def shopShowAllProducts(request):
    categorii = mySQLconn.get_categories()
    if request.method == "POST":
        if "categories" in request.POST.keys():
            #print("sort: ",request.POST['sort'])
            temp = mySQLconn.show_products_by_category(request.POST['cat'])
            return render(request,'shop.html',{'filtered':temp,'categories':categorii})
        elif request.POST['sorting']:
            print("sort: ", request.POST['sort'])
            sortare = request.POST['sort']
            temp = {}
            pagina_curenta = {}
            pagina = ''
            prods_pages = {}
            pages , pg = {}, {}
            if sortare[6:len(sortare)].strip() == 'asc':
                temp = mySQLconn.sort_products_by_price(0)
            elif sortare[6:len(sortare)].strip() == 'desc':
                temp = mySQLconn.sort_products_by_price(-1)
            elif sortare.strip() == 'discount':
                temp = mySQLconn.sort_products_by_discount()
            elif sortare.strip() == 'stock':
                temp = mySQLconn.sort_products_by_stock()
            if 'page' in request.GET.keys():
                pagina = request.GET['page']
            else:
                pagina = '1'
            pages['nr_pages'] = round(len(temp['produse'])/6)
            pg['pages'] = [ i for i in range(1,pages['nr_pages']+1)]
            list_products = []
            for prod in temp['produse'].values():
                list_products.append(prod)
            lists = [list_products[x:x+6] for x in range(0,len(list_products),6)]
            key_dict = (list)(temp['produse'].keys())
            for l in range(len(lists)):
                prods_pages[l+1] = lists[l]
            #print("thos",prods_pages)

            pagina = int(pagina)
            pagina_curenta['pagina'] = pagina
            request.session['pagina_curenta'] = pagina
            return render(request,'shop.html',{'temp':temp,'categories':categorii,'pagina_curenta': pagina_curenta,'nr_pages':pages, 'pages':pg, 'produse_pagina':prods_pages[int(pagina)] })


    else:
        #print("sort: ",request.POST.keys())
        temp = mySQLconn.display_all_products()
        if 'page' in request.GET.keys():
            pagina = request.GET['page']
        else:
            pagina = '1'
        #print("pagina",pagina)
        prods_pages = {}
        pages , pg = {}, {}
        pages['nr_pages'] = round(len(temp['produse'])/6)
        pg['pages'] = [ i for i in range(1,pages['nr_pages']+1)]
        list_products = []
        for prod in temp['produse'].values():
            list_products.append(prod)
        lists = [list_products[x:x+6] for x in range(0,len(list_products),6)]
        key_dict = (list)(temp['produse'].keys())
        for l in range(len(lists)):
            prods_pages[l+1] = lists[l]
        #print("thos",prods_pages)

        pagina_curenta = {}
        pagina = int(pagina)
        pagina_curenta['pagina'] = pagina
        request.session['pagina_curenta'] = pagina
        return render(request,'shop.html',{'temp':temp,'categories':categorii,'pagina_curenta': pagina_curenta,'nr_pages':pages, 'pages':pg, 'produse_pagina':prods_pages[int(pagina)] })

def deleteProductFromCart(request):
    if request.method == "POST":
        mySQLconn.remove_product_from_shopping_cart(request.session['user_id'],request.POST['id_product'])
    return redirect('cart.html')

def addProductToCart(request):
    current_page = request.session["pagina_curenta"]
    if request.method == "POST":
        mySQLconn.add_product_shopping_cart(request.session['user_id'], request.POST['id_product'])
        if 'products_visited' in request.session.keys() and request.session['products_visited'] != None:
            request.session['products_visited'].append(int(request.POST['id_product']))
        else:
            request.session['products_visited'] = [int(request.POST['id_product']),]
        request.session['products_visited'] = list(set(request.session['products_visited']))
    string = "shop.html?page="+str(current_page)
    return redirect(string)

def addOneProduct(request):
    if request.method == "POST":
        mySQLconn.add_product_shopping_cart(request.session['user_id'], request.POST['id_product'])
    return redirect('cart.html')

def removeOneProduct(request):
    if request.method == "POST":
        mySQLconn.delete_one_product(request.session['user_id'], request.POST['id_product'])
    return redirect("cart.html")

def adminPage(request):
    if request.session['user_type'] == "admin":
        suppliers = mySQLconn.show_all_suppliers()
        messages = mySQLconn.show_all_messages()
        return render(request, "admin.html",{"suppliers":suppliers,"messages":messages})
    else:
        return render(request,"404.html")

def interested(request):
    temp = mySQLconn.show_interested(request.session['products_visited'])

def contact_us(request):
    if request.method == 'POST':
        mySQLconn.contact(request.POST['name'],request.POST['subject'],request.POST['email'],request.POST['message'])
    return redirect("index.html")

def delete_supp(request):
    if request.method == "POST":
        mySQLconn.delete_supplier(request.POST['username_delete'])
    return redirect("admin.html")

def create_supplier(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['accPassword']
        conf_pass = request.POST['confPassword']
        mySQLconn.supplier_register(name, email, username, password,conf_pass)
    return redirect("admin.html")

def update_infos(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['telephone']
        address = request.POST['address']
        mySQLconn.change_infos(request.session['user_id'], fname, lname, email, address, phone)
    return redirect("account.html")


def read_msg(request):
    if request.method == "POST":
        mySQLconn.read_message(request.POST['id_req'])
    # return redirect("admin.html")


def send_msg(request):
    if request.method == "POST":
        id_req = request.POST['id_request']
        email_req = request.POST['email_req']
        message = request.POST['response']
        mySQLconn.send_message(id_req, email_req, message)
    return redirect("admin.html")

def send_mail_to_client(request):
    if request.method == "POST":
        id_supp = request.session['user_id']
        msg = request.POST['response']
        subject = request.POST['mail_subject']
        send_to = request.POST['email_req']
        mySQLconn.send_mail(id_supp, send_to, subject, msg)
    return redirect("supplier-orders.html")

def delete_msg(request):
    if request.method == "POST":
        id_msg = request.POST['msg_id']
        mySQLconn.delete_message(id_msg)
    return redirect("admin.html")

def search_supp(request):
    # if request.method == "POST":
    #     name_supp = request.POST['search']
    #     supp = mySQLconn.search_supp(name_supp)
    # return
    pass

def supplierPage(request):
    if request.session['user_type'] == "supplier":
        comenzi = mySQLconn.display_all_orders(request.session['user_id'])
        return render(request, "supplier-orders.html", {"comenzi":comenzi} )
    else:
        return render(request,"404.html")

def modifyOrderState(request):
    if request.method == "POST":
        if request.POST.get("acceptOrderBtn"):
            mySQLconn.update_order_status("accepted",request.POST['id_req'])
            mySQLconn.send_mail(request.session["user_id"],request.POST['email_req'],"Status comanda ta cu id-ul ["+str(request.POST['id_req']+"]"),"Comanda ta a fost acceptata!")
        elif request.POST.get('refuseOrderBtn'):
            mySQLconn.update_order_status("denied",request.POST['id_req'])
            mySQLconn.send_mail(request.session["user_id"],request.POST['email_req'],"Status comanda ta cu id-ul ["+str(request.POST['id_req']+"]"),"Comanda ta a fost refuzata!")
    return redirect("supplier-orders.html")

def supplierPageProducts(request):
    if request.session['user_type'] == "supplier":
        produse = mySQLconn.display_supplier_products(request.session['user_id'])
        return render(request, "supplier-products.html", {"produse":produse} )
    else:
        return render(request,"404.html")

def update_discount(request):
    if request.session['user_type'] == "supplier":
        if request.method == "POST":
            id_prod = request.POST['prod_id']
            percent = request.POST['discount_prc']
            mySQLconn.update_discount(id_prod, percent)
    return redirect("supplier-products.html")

def place_order(request):
    if request.method == "POST":
        mySQLconn.place_order(request.session['user_id'])
    return redirect("cart.html")

def add_new_product(request):
    print("Dsaddas: ", request.FILES['myimage'])
    if request.method == "POST":
        id_supp = request.session['user_id']
        prod_name = request.POST['product_name']
        prod_mark = request.POST['product_mark']
        prod_category = request.POST['category']
        stock = request.POST['stock']
        price = request.POST['price']
        description = request.POST['description']
        discount_percent = request.POST['discount']
        my_image = request.FILES['myimage']
        fs = FileSystemStorage()
        filename = fs.save(my_image.name, my_image)
        upload_file_url = fs.url(filename)
        if int(discount_percent) > 0:
            discount = 1
        else:
            discount = 0
        image_bd = '/static/images1' + upload_file_url
        mySQLconn.product_register(prod_name, prod_mark, prod_category, id_supp, stock, description, price, discount, discount_percent, image_bd)
    return redirect("supplier-products.html")
