import os
import random
import string

from PIL import Image, ImageChops
from django.shortcuts import redirect

# Delete default image of object
from project.settings import BASE_DIR

def previous_page_redirect(request, default='/'):
    if request.META.get('HTTP_REFERER'):
        request.session['previous_page'] = request.META.get('HTTP_REFERER')
    return redirect(default)
# def delete_main_photo(model, pk):
#     item = model.objects.filter(id=pk)
#     if item.exists():
#         try:
#             default_image_url = model.objects.get(id=pk).image.url
#             os.remove(str(BASE_DIR) + default_image_url)
#         except:  # noqa: E722
#             pass
#
#
# # Delete all images of object
# def delete_all_photos(model, object_pk):
#     images_of_cpu = model.objects.filter(product_id=object_pk)
#     if images_of_cpu.exists():
#         for item in images_of_cpu:
#             try:
#                 os.remove(str(BASE_DIR) + item.image.url)
#             except:  # noqa E722
#                 pass
#             item.delete()


# Sort default image dirs of products by name
def upload_image_product_url(instance, filename):
    return f'product/{instance.title}-/default-image/{filename}'


# Sort other images dirs of products
def upload_other_images_product_url(instance, filename):
    return f'product/{instance.name}/{filename}'


# Check difference between two images
# def has_difference_images(img1, img2):
#     image_1 = Image.open(img1)
#     image_2 = Image.open(img2)
#     if image_1.size == image_2.size:
#         result = ImageChops.difference(image_1, image_2)
#         if result.getbbox() is None:
#             # difference not found
#             return False
#     # difference found
#     return True

def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid

def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))