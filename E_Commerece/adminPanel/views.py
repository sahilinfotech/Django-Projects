from django.shortcuts import render, redirect
from adminPanel.models import *
from django.contrib import messages
from django.core.files.storage import FileSystemStorage  #for File storage
from django.http import HttpResponse, JsonResponse
from datetime import datetime






# Create your views here.

def dashboardAdmin(request):
    return render(request, 'dashboard.html')

def productregisterFun(request):
    if request.method == "POST":
        Product_name_ = request.POST['productName'] # productName from HTML PAGE (addproduct.html)
        Product_price_ = request.POST['productPrice']
        Product_image_ = request.FILES.get('productImage', False) 
        Product_is_active_ = request.POST.get('disabled') 

        if len(Product_name_) <= 0:
            messages.error(request, "Please Enter Product Name!!")
            return redirect(productregisterFun)
        
        if len(Product_price_) <= 0:
            messages.error(request, "Please Enter Product Price!!")
            return redirect(productregisterFun)

        if Product_is_active_ == None:
            messages.error(request, "Please Product Activation Select!!")
            return redirect(productregisterFun)


        if not Product_image_:
            messages.error(request, "Please Select Product Image ")
            return redirect(productregisterFun)

        if not (Product_image_.name.endswith(".png") or Product_image_.name.endswith(".jpeg") or Product_image_.name.endswith(".jpg")):
            messages.error(request, "Please Select .PNG, .JPEG, or .JPG Format Only!!")
            return redirect(productregisterFun)


        fs = FileSystemStorage()   # For save image in particular folder

        fs.save("Product/" + Product_image_.name, Product_image_)


        Productdataadd = ProductModel(
            Product_name = Product_name_,    # Product_name from Model.py or database AND Product_name_ from above function
            Product_price = Product_price_,
            Product_is_active = Product_is_active_,
            Product_image = "media/Product/" + Product_image_.name,
        )

        Productdataadd.save()

        if Productdataadd.id:
            messages.success(request, "Product Add succesfully!!")
        else:
            messages.error(request, "Something is wrong!!")
            return redirect(productregisterFun)
            
    return render(request, 'addproduct.html')


def productviewFun(request):

    view_Product = ProductModel.objects.using("default").all()

    return render(request, 'viewproduct.html',{"id": id,"view_Product" : view_Product}) 


def productfetchFun(request):
    
    productid = request.POST['productdata'] # productdata from viewproduct.html script

    productfetch = ProductModel.objects.filter(pk = productid).values()
    print(productfetch , "KKKKKKKKKKK")
    
    productlist = list(productfetch)
    response_product = {"productlist": productlist}
    return JsonResponse(response_product)


def producteditFun(request):

    productid = request.POST['productdata']
    Product_name_ = request.POST['productName']
    Product_price_ = request.POST['productPrice']
    Product_old_image_ = request.POST['oldproductimage'] 
    Product_is_active_ = request.POST.get('productactivate')

    
    if len(Product_name_) <= 0:
        response = "Please Enter Product Name!!"
        return HttpResponse(response)

        
    if len(Product_price_) <= 0:
        response = "Please Enter Product Price!!"
        return HttpResponse(response)


    if Product_is_active_ == None:
        response = "Please Product Activation Select!!"
        return HttpResponse(response)

    Product_image_ = request.FILES.get('productImage', False) 


    productdataupdate = ProductModel.objects.get(pk = productid)
    productdataupdate.Product_name = Product_name_
    productdataupdate.Product_price = Product_price_
    productdataupdate.Product_is_active = int(Product_is_active_)

    fs = FileSystemStorage()

    if Product_image_ != False:

        fs.save("Product/" + Product_image_.name, Product_image_)
        productimagesave = "media/Product/" + Product_image_.name

    else:

        productimagesave = Product_old_image_

    productdataupdate.Product_image = productimagesave




    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    input_datetime = datetime.strptime(dt_string, "%d/%m/%Y %H:%M:%S")

    # Format the datetime object into the desired output format
    output_string = input_datetime.strftime("%b. %d, %Y, %I:%M %p")

    productdataupdate.Product_created_at_update = output_string
    productdataupdate.save()


    if productdataupdate.id:
        response =  "1"
        return HttpResponse(response)
    else:
        response =  "Something goes wrong in updation"
        return HttpResponse(response)

    return HttpResponse('1')


def productdeleteFun(request):

    productid = request.POST['productdata']
    productdatadelete = ProductModel.objects.filter(pk = productid)
    productdatadelete.delete()

    return HttpResponse('1')

def productdetailregisterFun(request):    
    if request.method == "POST":
        Product_ = request.POST['productNameselect']
        Productdetail_description_ = request.POST['productdetailDescription'] 
        Productdetail_type_ = request.POST['productdetailType'] 
        Productdetail_colour_ = request.POST['productdetailColour'] 
        Productdetail_is_active_ = request.POST.get('productdetailActive')

        if len(Productdetail_description_) <= 0:
            messages.error(request, "Product Detail Description is Enter!!")
            return redirect(productdetailregisterFun)
        
        if len(Productdetail_type_) <= 0:
            messages.error(request, "Product Detail Type is Enter!!")
            return redirect(productdetailregisterFun)
        
        if len(Productdetail_colour_) <= 0:
            messages.error(request, "Product Detail Colour is Enter!!")
            return redirect(productdetailregisterFun)

        if Productdetail_is_active_ == None:
            messages.error(request, "Product Detail activation is not selected!!")
            return redirect(productdetailregisterFun)
        
        product_instance = ProductModel.objects.get(Product_name=Product_)

        productdetailadddata = ProductdetailModel(
            Product = product_instance,
            Productdetail_description = Productdetail_description_,
            Productdetail_type = Productdetail_type_,
            Productdetail_colour = Productdetail_colour_,
            Productdetail_is_active = Productdetail_is_active_,
            )
        productdetailadddata.save()

        if productdetailadddata.id:
            messages.success(request, "Product Detail is add sucessfully!!")
        else:
            messages.error(request, "Somthing is wrong!!")
            return redirect(productdetailregisterFun)
    
    else:
        productdataview = ProductModel.objects.all()
        return render(request,'addproductdetail.html', {"productdataview": productdataview})

def productdetailviewFun(request):
    view_Productdetail = ProductdetailModel.objects.all()
    productdataview = ProductModel.objects.all()
    
    return render(request,'viewproductdetail.html',{"view_Productdetail": view_Productdetail, "productdataview": productdataview} )
 
def productdetailfetchFun(request):

    productdetail_id = request.POST['productdetail_id']
    print(productdetail_id)
    
    productdetails = ProductdetailModel.objects.filter(pk = productdetail_id).values()    
    productdatafetch = ProductModel.objects.get(pk = productdetails[0]['Product_id'])
    print(productdatafetch.Product_name , "HHHHHHHHHHHHHHHHHHHHHHHHH")
   
    productdetaillist = list(productdetails)
    productdetaillist.append({"Product_name_": productdatafetch.Product_name})
    productdetaillist.append({"productdetail_id": productdetail_id})

    res = {"productdetaillist": productdetaillist}
    return JsonResponse(res)


def productdetaileditFun(request):

    Product_ = request.POST['productNameselect']
    Productdetail_description_ = request.POST['productdetailDescription'] 
    Productdetail_type_ = request.POST['productdetailType'] 
    Productdetail_colour_ = request.POST['productdetailColour'] 
    Productdetail_is_active_ = request.POST.get('productdetailActive')
    productdetail_id = request.POST['productdetail_id']
    
    # filepath = request.FILES.get('subcategoryimage', False)
    if len(Productdetail_description_) <= 0:
        response = "Product Detail Description is Enter!!"
        return HttpResponse(response)

    if len(Productdetail_type_) <= 0:
        response = "Product Detail Type is Enter!!"
        return HttpResponse(response)

    if len(Productdetail_colour_) <= 0:
        response = "Product Detail Colour is Enter!!"
        return HttpResponse(response)

    if Productdetail_is_active_ == None:
        response = "Product Detail activation is not selected!!"
        return HttpResponse(response)
        
    productdata = ProductModel.objects.get(Product_name = Product_)
    productdetaildataupdate = ProductdetailModel.objects.get(pk = productdetail_id)

    productdetaildataupdate.Productdetail_description = Productdetail_description_
    productdetaildataupdate.Productdetail_type = Productdetail_type_
    productdetaildataupdate.Productdetail_colour = Productdetail_colour_
    productdetaildataupdate.Product = productdata
    productdetaildataupdate.Productdetail_is_active = int(Productdetail_is_active_)

    productdetaildataupdate.save()

    if productdetaildataupdate.id:
        response =  "1"
        return HttpResponse(response)
    else:
        response =  "Something goes wrong in updation"
        return HttpResponse(response)


def productdetaildeleteFun(request):

    productdetail_id = request.POST['productdetail_id']
    productdetail_id = ProductdetailModel.objects.filter(pk = productdetail_id)
    productdetail_id.delete()

    return HttpResponse('1')







