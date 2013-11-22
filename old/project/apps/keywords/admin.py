from django.contrib import admin
from keywords.models import *

from xauto_lib.admin import SLBaseModelAdmin
from flexselect import FlexSelectWidget

# ----------------------------------------------------------------------------
# keyword = models.CharField(max_length=200)
# category = models.CharField(max_length=100)
# parent_category = models.CharField(max_length=100)
# description = models.TextField(blank=True, help_text="Meta description")
# is_active = models.BooleanField("active?", default=True)
# event_count = models.PositiveIntegerField(default=0)
# ----------------------------------------------------------------------------



class MainKeywordServiceAdmin(SLBaseModelAdmin):
    list_display = ('name',  'description', 'is_active', 'is_system', 'icon',  )
    list_filter = ('is_active', 'is_system')
    search_fields = ('name',)
    fields = ('name', 'description', 'is_active', 'is_system', 'icon',  )
    ordering = ('name',)


class SubCategoryAdmin(admin.ModelAdmin):
    """
    name = models.CharField(max_length=100, default='', db_index=True)
    parent = models.ForeignKey(MainKeywordService, blank=True, null=True, related_name='main_subcateg_keyword')
    description = models.TextField(blank=True, help_text="Meta description")
    is_active = models.BooleanField("active?", default=True)
    is_system = models.BooleanField("system?", default=False)
    event_count = models.PositiveIntegerField(default=0)                           # -- active Event for this keyword
    provider_count = models.PositiveIntegerField(default=0)                      # -- active providers for this keyword
    """
    list_display = ('name',  'parent', 'description', 'is_active', 'is_system', 'is_hidden', )
    list_filter = ('is_active', 'is_system' , 'is_hidden', 'parent')
    search_fields = ('name',)
    fields = ('name', 'description', 'is_active', 'is_system','is_hidden', 'parent', )
    ordering = ('name',)



class KeywordServiceAdmin(admin.ModelAdmin):
    """
    parent = models.ForeignKey(MainKeywordService, blank=True, null=True, related_name='main_keyword')
    keyword = models.CharField(max_length=100, default='')
    category = models.ForeignKey(Category, blank=True, null=True, related_name='main_category')           #
    sub_category = models.ForeignKey(SubCategKeywords, blank=True, null=True, related_name='sub_category')        #
    link_keyword = models.CharField(max_length=100, default='', db_index=True, null=True, blank=True)     #
    link_keyword2 = models.CharField(max_length=100, default='', db_index=True, null=True, blank=True)    #
    link_keyword3 = models.CharField(max_length=100, default='', db_index=True, null=True, blank=True)    #
    description = models.TextField(blank=True, help_text="Meta description")
    is_active = models.BooleanField("active?", default=True)                     # --- activate pr deactivate a keyword
    is_system = models.BooleanField("system?", default=False)                    # --- System admin only  /backend admin
    is_event = models.BooleanField("Event Page?", default=False)             # --- Find Work > Category Page
    can_add = models.BooleanField("Can add?", default=True)                      # --- account Page and Post Event Page
    event_count = models.PositiveIntegerField(default=0)                           # -- active Event for this keyword
    owner = models.ForeignKey(User, null=True, blank=True)
    date_add = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    migrated = models.BooleanField("Migrated ?", default=False)                  # --- account Page and Post Event Page
    position = models.PositiveSmallIntegerField("Position")
    """

    list_display = ('id', 'parent', 'sub_category', 'keyword',  'description', 'is_active', 'is_system', 'can_add',  )
    list_filter = ('is_active', 'is_system', 'parent', 'sub_category', 'can_add',)
    search_fields = ('keyword', 'category__name')
    ordering = ('parent', 'keyword', 'sub_category', )
    readonly_fields = ("date_add",)

    change_list_filter_template = "admin/filter_listing.html"
    sortable_field_name = "position"
    save_on_top = True

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Alters the widget displayed for the base field.
        """
        if db_field.name == "sub_category":
            kwargs['widget'] =  SubCategPerParentWidget(
                base_field=db_field,
                modeladmin=self,
                request=request,
            )
            kwargs['label'] = 'Sub Category'
        return super(KeywordServiceAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class SubCategPerParentWidget(FlexSelectWidget):
    """
    The widget must extend FlexSelectWidget and implement trigger_fields,
    details(), queryset() and empty_choices_text().
    """

    trigger_fields = ['parent']
    """Fields which on change will update the base field."""

    def details(self, base_field_instance, instance):
        """
        HTML appended to the base_field.
        """
        return ""

    def queryset(self, instance):
        """
        Returns the QuerySet populating the base field. If either of the
        trigger_fields is None, this function will not be called.

        - instance: A partial instance of the parent model loaded from the
                    request.
        """
        parent = instance.parent
        return SubCategKeywords.objects.filter(parent=parent)

    def empty_choices_text(self, instance):
        """
        If either of the trigger_fields is None this function will be called
        to get the text for the empty choice in the select box of the base
        field.

        - instance: A partial instance of the parent model loaded from the
                    request.
        """
        return "Please update the Sub Categ field"



admin.site.register(KeywordService, KeywordServiceAdmin)
admin.site.register(MainKeywordService, MainKeywordServiceAdmin)
admin.site.register(SubCategKeywords, SubCategoryAdmin)

