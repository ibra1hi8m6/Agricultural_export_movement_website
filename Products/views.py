from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .models import ProductsName
from django.contrib.auth.decorators import login_required
from django.db.models import Count, F
from django.contrib import messages



# Create your views here.

def ShopDetailsPage(request , product_id):
    # Retrieve the product details using the product ID
    product = get_object_or_404(Product, id=product_id)
    
    return render(request, 'Products_html/shop_detail.html', {'products': product})


def insertion_sort(products):
    products_list = list(products)
    for i in range(1, len(products_list)):
        key = products_list[i]
        j = i - 1
        while j >= 0 and key.price > products_list[j].price:
            products_list[j + 1] = products_list[j]
            j -= 1
        products_list[j + 1] = key
    return products_list

def selection_sort(products):
    products_list = list(products)
    for i in range(len(products_list)):
        min_index = i
        for j in range(i + 1, len(products_list)):
            if products_list[j].price < products_list[min_index].price:
                min_index = j
        products_list[i], products_list[min_index] = products_list[min_index], products_list[i]
    return products_list







def substringMatching(string, substring):
    for i in range(len(string) - len(substring) + 1):
        found = True
        for j in range(len(substring)):
            if not string[i + j] == substring[j]:
                found = False
                break
        if found:
            return True
    return False

def search_products(query):
    # Function to perform substring search on products
    if not query:
        # If there is no search query, return all products
        return Product.objects.all()
    # Function to perform substring search on products
    matching_products = []
    for product in Product.objects.all():
        if substringMatching(product.productName.lower(), query.lower()):
            matching_products.append(product)
    return matching_products






def ShopPage(request):
    query = request.GET.get('q')
    sort_option = request.GET.get('sort', '2')

    # Retrieve all categories with their respective product counts
    categories = Category.objects.annotate(product_count=Count('product_set'))
    
    # Retrieve all products with their respective categories
    products = Product.objects.select_related('category')

    # Fetch all products for search or sorting
    products = Product.objects.all()
    
    if query:
        products = search_products(query)

        # Count the number of products with the same name for the given query
        desired_name = query
        product_count = Product.objects.filter(productName=desired_name).count()
        print(f"The number of products with the name '{desired_name}' is: {product_count}")

    if sort_option == '2':  # High Price → Low Price (Insertion Sort)
        products = insertion_sort(products)
    elif sort_option == '3':  # Low Price → High Price (Selection Sort)
        products = selection_sort(products)

    results_count = len(products)  # Update results count based on sorted or searched products

    # # Aggregate product counts by name for each category
    # product_counts_by_category = {}
    # for category in categories:
    #     products_in_category = Product.objects.filter(category=category)
    #     product_counts_by_category[category.id] = {'categoryName': category.categoryName,'product_counts': Product.objects.filter(category=category).values('productName').annotate(count=Count('id'))}
    # Aggregate product counts by category
    product_counts_by_category = Category.objects.annotate(product_count=Count('product_set'))
    return render(request, 'Products_html/shop.html', {
        'products': products,
        'query': query,
        'sort_option': sort_option,
        'results_count': results_count,
        'categories': categories,
        'product_counts_by_category': product_counts_by_category,
    })






def IndexPage(request):
    Categories=Category.objects.all()
    return render(request, 'index.html',{'Categories': Categories})








@login_required
def AddProductPage(request):
    categories = Category.objects.all()
    ProductsNames = ProductsName.objects.all()

    if request.method == 'POST':
        user = request.user
        product_name = request.POST.get('product')
        description = request.POST.get('Description')
        price = request.POST.get('price')
        category_name = request.POST.get('category')
        quantity = request.POST.get('quantity')
        image_product = request.FILES.get('image')

        # Get or create the category
        category, created = Category.objects.get_or_create(categoryName=category_name)

        # Create a new product
        product = Product(
            user=user,
            productName=product_name,
            description=description,
            mainImage=image_product,
            price=price,
            quantity=quantity,
            category=category,
        )

        # Save the product
        product.save()

        # Render the same form page with a success message
        return render(request, 'Products_html/addproduct.html', {'categories': categories, 'Products_Names': ProductsNames, 'success_message': 'Product added successfully'})

    else:
        # Handle GET request (initial form rendering)
        return render(request, 'Products_html/addproduct.html', {'categories': categories, 'Products_Names': ProductsNames})







def category_exists(category_name):
    return Category.objects.filter(categoryName=category_name).exists()

def product_names_exist(product_names_list):
    return ProductsName.objects.filter(nameOfProducts__in=product_names_list).values_list('nameOfProducts', flat=True)

def AddCategoryPage(request):
    categories = Category.objects.all()

    if request.user.is_superuser:
        if request.method == 'POST':
            category_name = request.POST.get('categoryName')
            category_image = request.FILES.get('categoryImage')
            product_names_input = request.POST.get('typesNames')
            product_names_list = [name.strip() for name in product_names_input.split(',')]

            selected_category_id = request.POST.get('category')
            if selected_category_id:
                # Scenario 1: Add new product names to an existing category
                selected_category = Category.objects.get(pk=selected_category_id)

                # Check if the product names already exist for the selected category
                existing_product_names = ProductsName.objects.filter(category=selected_category, nameOfProducts__in=product_names_list)
                if existing_product_names:
                    existing_names = ', '.join(existing_product_names.values_list('nameOfProducts', flat=True))
                    messages.error(request, f"The following product names already exist for the selected category '{selected_category.categoryName}': {existing_names}")
                    return render(request, 'Products_html/addcategory.html', {'categories': categories})

                # Create new product names associated with the selected category
                for product_name in product_names_list:
                    new_product = ProductsName(nameOfProducts=product_name, category=selected_category)
                    new_product.save()

                messages.success(request, f"Product names have been added to the category '{selected_category.categoryName}' successfully.")
                return render(request, 'Products_html/addcategory.html', {'categories': categories})

            # Scenario 2: Add a new category with its associated product names
            if category_exists(category_name) or product_names_exist(product_names_list):
                if category_exists(category_name):
                    messages.error(request, f"The category '{category_name}' already exists.")
                if product_names_exist(product_names_list):
                    existing_product_names = ', '.join(product_names_exist(product_names_list))
                    messages.error(request, f"The following product names already exist: {existing_product_names}")
                return render(request, 'Products_html/addcategory.html', {'categories': categories})

            new_category = Category.objects.create(
                categoryName=category_name,
                mainImage=category_image
            )

            for product_name in product_names_list:
                new_product = ProductsName(nameOfProducts=product_name, category=new_category)
                new_product.save()

            messages.success(request, f"New category '{category_name}' and product names have been added successfully.")
            return render(request, 'Products_html/addcategory.html', {'categories': categories})

        return render(request, 'Products_html/addcategory.html', {'categories': categories})

  # Redirect non-superusers to the home page
