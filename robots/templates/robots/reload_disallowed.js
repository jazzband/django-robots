<script>
(function ($) {
    function append_spinner(containerDiv, existingSelector, spinner){
	containerDiv.css('position','relative');
        existingSelector.css('opacity', '.3');
        var posx = (existingSelector.position().left + existingSelector.width()) / 2 - 16;
        var posy = (existingSelector.position().top + existingSelector.height()) / 2 - 16;
        spinner.css('left', posx);
        spinner.css('top', posy);
        spinner.css('position','absolute');
        containerDiv.append(spinner);
    }

    $('#id_sites').change(function() {
        var val = $(this).val();
        var selector = "#id_sites option[value='" + val + "']";
        var site = $(selector)[0];
        var spinnerUrl = '{{ STATIC_URL }}admin/img/ajax-loader.gif';

        $.ajax({url:'{{ site_patterns_url }}',
            data:{site_id:site.value},
            beforeSend:function (xhr, settings) {
                var containerDiv = $("div.field-disallowed div.selector div.selector-available");
                var existingSelector = $("div.field-disallowed div.selector div.selector-available select");
		append_spinner(containerDiv, existingSelector, $('<img />').attr('src', spinnerUrl));

                containerDiv = $("div.field-disallowed div.selector div.selector-chosen");
                existingSelector = $("div.field-disallowed div.selector div.selector-chosen select");
		append_spinner(containerDiv, existingSelector, $('<img />').attr('src', spinnerUrl));
            },
            success:function (data) {
                if (data != ""){
                    $("div.field-disallowed div.selector").remove()
                    $(data).insertAfter("div.field-disallowed div label")
                    window.SelectFilter.init("id_disallowed", "Disallows", 0, "/s/admin/");
                }
            },
        });});
    SelectBox.init('id_sites');
    $('#id_sites_input').keyup(function() {
	SelectBox.filter('id_sites', this.value);
    });
})(django.jQuery);
</script>