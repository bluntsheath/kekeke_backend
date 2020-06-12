from django.db import models
from django.contrib.postgres.fields import ArrayField
from product.models import Product

class MoXing(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='moxing')
    url = models.CharField(max_length=255)


class MoXingVariant(models.Model):
    title = models.CharField(max_length=64)
    moxing = models.ForeignKey(MoXing, on_delete=models.CASCADE, related_name='variants')


class MoXingVariantValue(models.Model):
    key = models.CharField(max_length=64)
    base_color = models.CharField(max_length=255, null=True)
    base_color_map = models.CharField(max_length=255, null=True)
    metallic = models.CharField(max_length=255, null=True)
    metallic_map = models.CharField(max_length=255, null=True)
    roughness = models.CharField(max_length=255, null=True)
    roughness_map = models.CharField(max_length=255, null=True)
    normal_map = models.CharField(max_length=255, null=True)
    # 0 for opaque, 1 for alpha blend, 2 for alpha clip
    blend_mode = models.IntegerField()
    alpha = models.FloatField()
    alpha_map = models.CharField(max_length=255, null=True)
    moxing_variant = models.ForeignKey(MoXingVariant, on_delete=models.CASCADE, related_name='values')

class Component(models.Model):
    key = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    description = models.TextField()
    moxing = models.ForeignKey(MoXing, on_delete=models.CASCADE, related_name='components')


class Pattern(models.Model):
    tex_coord_index = models.IntegerField()
    title = models.CharField(max_length=64)
    component = models.ForeignKey(Component, on_delete=models.CASCADE, related_name='patterns')


class Region(models.Model):
    # use array to store the center info, 0 for x, 1 for y
    center = ArrayField(models.CharField(max_length=255, blank=True), size=2)
    # use array to store the size info, 0 for width, 1 for height
    size = ArrayField(models.CharField(max_length=255, blank=True), size=2)
    rotation = models.FloatField()
    # save the mask curve as svg file, upload to our oss server.
    mask = models.CharField(max_length=255)
    pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE, related_name='regions')


class Design(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    # todo: creator info
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='designs')


class ComponentDesign(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    component_key = models.CharField(max_length=64)
    design = models.ForeignKey(Design, on_delete=models.CASCADE, related_name='component_designs')


class PatternDesign(models.Model):
    tex_coord_index = models.IntegerField()
    component_design = models.ForeignKey(ComponentDesign, on_delete=models.CASCADE, related_name='pattern_designs')


class RegionDesign(models.Model):
    # use array to store the center info, 0 for x, 1 for y
    center = ArrayField(models.CharField(max_length=255, blank=True), size=2)
    # use array to store the size info, 0 for width, 1 for height
    size = ArrayField(models.CharField(max_length=255, blank=True), size=2)
    rotation = models.FloatField()
    pattern_design = models.ForeignKey(PatternDesign, on_delete=models.CASCADE, related_name='region_designs')


class StickerLayout(models.Model):
    # the location of the sticker
    url = models.CharField(max_length=255, null=True)
    # todo: link the sticker model
    center = ArrayField(models.CharField(max_length=255, blank=True), size=2)
    # use array to store the size info, 0 for width, 1 for height
    scale = ArrayField(models.CharField(max_length=255, blank=True), size=2)
    rotation = models.FloatField()
    region_design = models.ForeignKey(RegionDesign, on_delete=models.CASCADE, related_name='sticker_layouts')


class BaseColorBackgroundLayout(models.Model):
    color = models.CharField(max_length=64)
    region_design = models.OneToOneField(RegionDesign, on_delete=models.CASCADE, related_name='base_color_background')


class StickerBackgroundLayout(models.Model):
    url = models.CharField(max_length=255, null=True)
    # todo: link the sticker background model
    center = ArrayField(models.CharField(max_length=255, blank=True), size=2)
    scale = ArrayField(models.CharField(max_length=255, blank=True), size=2)
    region_design = models.OneToOneField(RegionDesign, on_delete=models.CASCADE, related_name='sticker_background')
