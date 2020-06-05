from django.db import models
from django.urls import reverse


class ProductCategory(models.Model):
    # use this decimal number to indicator category level, 0 --> level 1, 1 --> level2, etc.
    level = models.IntegerField()
    # name of this category
    name = models.CharField(max_length=64)
    # parent category level of current category
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children')
    product_count = models.IntegerField
    product_unit = models.CharField(max_length=64)

    icon = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'product_category'
        verbose_name_plural = 'product_categories'

    def __str__(self):
        return 'Product Category: %s, level: %s' % (self.name, self.level + 1)

    def get_absolute_url(self):
        return reverse('product_category_detail', args=[str(self.id)])


class ProductBrand(models.Model):
    name = models.CharField(max_length=64)
    first_letter = models.CharField(max_length=8)
    product_count = models.IntegerField()
    logo = models.CharField(max_length=255)
    brand_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'product_brand'
        verbose_name_plural = 'product_brands'

    def __str__(self):
        return 'Product Brand: %s' % self.name

    def get_absolute_url(self):
        return reverse('product_brand_detail', args=[str(self.id)])


# use this to create attribute category and not related to our product category
class ProductAttributeCategory(models.Model):
    name = models.CharField(max_length=64)
    attribute_count = models.IntegerField()
    parameter_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'product_attribute_category'
        verbose_name_plural = 'product_attribute_categories'

    def __str__(self):
        return 'Product Attribute Category : %s' % self.name

    def get_absolute_url(self):
        return reverse('product_attribute_category_detail', args=[str(self.id)])


class ProductAttribute(models.Model):
    category = models.ForeignKey(ProductAttributeCategory, on_delete=models.CASCADE, related_name='attributes')
    name = models.CharField(max_length=64)
    # only or single selection or multi selection (0, 1, 2)
    selection_type = models.IntegerField()
    # user input or enum selection (0, 1)
    input_type = models.IntegerField()
    # input enum list, separate with comma
    input_enum_list = models.CharField(max_length=255)
    # 0 for user selectable specs, 1 for general specs
    type = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'product_attribute'
        verbose_name_plural = 'product_attributes'

    def __str__(self):
        if self.type == 0:
            return 'Product User Selectable Specs: %s' % self.name
        else:
            return 'Product General Specs: %s' % self.name

    def get_absolute_url(self):
        return reverse('product_attribute_detail', args=[str(self.id)])


class ProductCategoryAttributeRelation(models.Model):
    product_category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        related_name='product_category_attributes'
    )
    product_attribute = models.ForeignKey(
        ProductAttributeCategory,
        on_delete=models.CASCADE,
        related_name='product_categories'
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Product(models.Model):
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    attribute_category = models.ForeignKey(ProductAttributeCategory, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=64)
    subtitle = models.CharField(max_length=64)
    description = models.TextField()
    thumbnail = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=64)
    brand_name = models.CharField(max_length=64)
    category_name = models.CharField(max_length=64)
    is_deleted = models.BooleanField()
    is_published = models.BooleanField()
    is_new = models.BooleanField()
    is_recommended = models.BooleanField()
    is_verified = models.BooleanField()
    sale_volume = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    unit = models.CharField(max_length=16)

    detail_pic_album = models.CharField(max_length=255)
    detail_title = models.CharField(max_length=255)
    detail_description = models.TextField()
    detail_html = models.TextField()
    detail_mobile_html = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    product_attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE, related_name='products')
    value = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'product_attribute_value'
        verbose_name_plural = 'product_attribute_values'

    def __str__(self):
        return 'Product Attribute Value: %s' % self.value

    def get_absolute_url(self):
        return reverse('product_attribute_value_detail', args=[str(self.id)])


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    sku_code = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    low_stock_threshold = models.IntegerField()
    # specs list, separate with comma.
    customizable_specs = models.CharField(max_length=255)
    sale_volume = models.IntegerField()
    detail_pic = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class ProductVerifyingRecord(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='verifying_records')
    # todo: should add verifier
    # 0 for pending, 1 for accept, 2 for reject
    status = models.IntegerField()
    detail = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class ProductPriceOperationLog(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='price_operation_logs')
    old = models.DecimalField(max_digits=10, decimal_places=2)
    new = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


class ProductStockOperationLog(models.Model):
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='stock_operation_logs')
    old = models.IntegerField()
    new = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

