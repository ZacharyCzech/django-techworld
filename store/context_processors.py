from .models import Category, Subcategory


def search_context(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', '')
    subcategory_id = request.GET.get('subcategory', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()

    category_groups = {
        "Laptopy i komputery": {
            "categories": ["Laptopy", "Komputery"],
            "icon": "assets/icons/laptops.svg"
        },
        "Podzespoły komputerowe": {
            "categories": ["Procesory", "Płyty główne", "Karty graficzne"],
            "icon": "assets/icons/parts.svg"
        },
        "Urządzenia peryferyjne": {
            "categories": ["Monitory", "Klawiatury", "Myszki", "Słuchawki"],
            "icon": "assets/icons/peripherals.svg"
        },
        "Smartfony i akcesoria": {
            "categories": ["Smartfony"],
            "icon": "assets/icons/smartphones.svg"
        }
    }

    categorized_groups = {}
    for group_name, group_data in category_groups.items():
        categorized_groups[group_name] = {
            "categories": [category for category in categories if category.name in group_data["categories"]],
            "icon": group_data["icon"]
        }

    return {
        'query': query,
        'category_id': category_id,
        'subcategory_id': subcategory_id,
        'min_price': min_price,
        'max_price': max_price,
        'categorized_groups': categorized_groups,
        'subcategories': subcategories
    }
