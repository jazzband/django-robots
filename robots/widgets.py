from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import Select


class CustomDisallowsSelector(FilteredSelectMultiple):

    def __init__(self, verbose_name, is_stacked):
        super(CustomDisallowsSelector, self).\
            __init__(verbose_name=verbose_name, is_stacked=is_stacked)

    # def render(self, name, value, attrs=None, choices=()):
    #     import ipdb; ipdb.set_trace()
    #     output = super(CustomDisallowsSelector, self).render(name, value, attrs=attrs, choices=choices)
    #     return output


class CustomSitesSelector(Select):

    def value_from_datadict(self, data, files, name):
        return (super(CustomSitesSelector, self).value_from_datadict(data, files, name), )

    def render(self, name, value, attrs=None, choices=()):
        from django.core.urlresolvers import reverse
        value = value[0] if value else value
        output = super(CustomSitesSelector, self).render(name, value, attrs=attrs, choices=choices)
        return output + on_change % reverse('site_patterns')


on_change = """
<script>
var $ = django.jQuery
$('#id_sites').change(function() {
    var val = $(this).val();
    var selector = "#id_sites option[value='" + val + "']";
    var site = $(selector)[0];
/*
    var spinnerUrl = (spinner_url)s;
    var spinner = $('<img />').attr('src', spinnerUrl);
*/
    $.ajax({url:'%s',
         data:{site_id:site.value},
/*
         beforeSend:function (xhr, settings) {
              $("div.field_disallowed div.selector_available").css('position','relative');
              var existingSelector = $("div.field_disallowed div.selector_available select");
              existingSelector.css('opacity', '.3');
              var posx = (existingSelector.position().left + existingSelector.width()) / 2 + 32;
              var posy = (existingSelector.position().top + existingSelector.height()) / 2 - 16;
              spinner.css('left', posx);
              spinner.css('top', posy);
              spinner.css('position','absolute');
              $("div.field_disallowed div.selector_available").append(spinner);
         },
         complete:function (xhr) {
             $("div.field_disallowed div.selector_available").remove(spinner);
             $("div.field_disallowed div.selector_available selector").css('opacity', '');
         },*/
         success:function (data) {
              if (data != ""){
                   $("div.field-disallowed div.selector").remove()
                   $(data).insertAfter("div.field-disallowed div label")
                   window.SelectFilter.init("id_disallowed", "Disallows", 0, "/s/admin/");
              }
         },
    });

});
</script>
"""
