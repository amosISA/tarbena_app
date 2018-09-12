$(document).mouseup(function(e){
    if($(e.target).attr("class") != "boards-drawer") {
        $('.boards-drawer').hide();
        e.stopPropagation();
    }
});

$(document).ready(function() {
    $('[data-toggle="popover"]').popover();
    //$.fn.dataTable.moment('D/M/YYYY');
    oTable= $('#subv_table_ordering').DataTable({
        "ordering": false,
        //"searching": false,
        "language": {
            url: "/static/home/location/es_ES.json"
        },
        //"aaSorting": [[ 2, "asc" ]], // sort by fin
        "lengthMenu": [[10000, -1], [10000, "Todas"]],
        //if I want to show the lengthMenu also do this: Blfrtip
        dom: '<"toolbar">Bfrtip',
        columns: [
            { "orderable": false },
            { "orderable": false },
            { "orderable": false },
            { "orderable": false }
        ],
        buttons: [
            'print'
        ],

        initComplete: function() {
            // Hide actions buttons and delegate his functionality into the hamburger into the navbar
            // Only for print functionality
            var $buttons = $('.dt-buttons').hide();

            $('#subvenciones-nav-dropdown-toggle').click(function(e) {
                if ($(e.target).is('.buttons-print')) {
                    var btnClass = '.buttons-' + $(e.target)[0].id;
                    $buttons.find(btnClass).click();
                } else if ($(e.target).is('.subv_inside__anchor--drop')) {
                    var btnClass = '.buttons-' + $(e.target)[0].parentElement.id;
                    $buttons.find(btnClass).click();
                } else if ($(e.target).is('.fas.fa-print')) {
                    var btnClass = '.buttons-' + $(e.target)[0].parentElement.parentElement.parentElement.id;
                    $buttons.find(btnClass).click();
                }
            });
        }
    });
    $('#search-on-navigation').keyup(function(){
          oTable.search($(this).val()).draw();
    });

    $("div.toolbar").html('<b>Custom tool bar! Text/images etc.</b>');

    // Scroll to subsidie that have the actual day and blink the subsidies that have as end date the actual day
    var CurrentDate = new Date();
    var dataFormated = ('0' + CurrentDate.getDate()).slice(-2)+"/"+('0'+(CurrentDate.getMonth()+1)).slice(-2)+"/"+CurrentDate.getFullYear();
    // console.log(dataFormated.   split("/"));

    // Compare dates with format DD/MM/YYYY
    function process(date){
        var parts = date.split("/");
        return new Date(parts[2], parts[1] - 1, parts[0]);
    }

    // Navigation click on button that is left to the search box for scrolling to actual subsidie
    $('#button-actual-subsidie-navigation').click(function() {
        $('.date-end').each(function(i, v) {
            // if date equals to today or if date is greater than today then get that one
            if ($.trim($(this).text()) == dataFormated || process($.trim($(this).text())) > process(dataFormated)) {
                $('html, body').animate({
                    scrollTop: $(this).parent().offset().top=($(this).parent().offset().top)-($(this).parent().outerHeight())
                }, 250);
                $(this).parent().parent().fadeIn(200).fadeOut(200).fadeIn(200).fadeOut(200).fadeIn(200);
                return i === 0; // just return the first result 
            }
        });
    });

    // Back to top functionality
    if ($('#back-to-top').length) {
        var scrollTrigger = 100, // px
            backToTop = function () {
                var scrollTop = $(window).scrollTop();
                if (scrollTop > scrollTrigger) {
                    $('#back-to-top').addClass('show');
                } else {
                    $('#back-to-top').removeClass('show');
                }
            };
        backToTop();
        $(window).on('scroll', function () {
            backToTop();
        });
        $('#back-to-top').on('click', function (e) {
            e.preventDefault();
            $('html,body').animate({
                scrollTop: 0
            }, 700);
        });
    }

    /* Info ESTADOS */
    $('.estados-info').click(function() {
        $('.boards-drawer').toggle();
    });
    $('ul.sidebar-boards-list li').click(function() {
        $('.boards-drawer').show();
    });

    /* Estados hover */
    $('.compact-board-tile-link').each(function() {
        $(this).mouseover(function() {
            $('span:first', this).css({'opacity': 1});
        }).mouseleave(function() {
            $('span:first', this).css({'opacity': .7});
        });
    });



    // Toggle filtering dropdown with checkboxes
    $("#custom-select, #custom-select2").on("click",function(){
        $("#custom-select-option-box, #custom-select-option-box2").toggle();
    });

    // Keep them open (dropdown filtering) when you click on the checkbox inside of them
    function toggleFillColor(obj) {
        $("#custom-select-option-box").show();
    }
    $(".custom-select-option").on("click", function() {
        var checkboxObj = $(this).children("input");
        toggleFillColor(checkboxObj);
    });

    function toggleFillColor2(obj) {
        $("#custom-select-option-box2").show();
    }
    $(".custom-select-option2").on("click", function() {
        var checkboxObj = $(this).children("input");
        toggleFillColor2(checkboxObj);
    });

    $("body").on("click",function(e){ // Close dropdown filtering when click outside of them
        if(e.target.id != "custom-select" && $(e.target).attr("class") != "custom-select-option") {
            $("#custom-select-option-box").hide();
        }
        if (e.target.id != "custom-select2" && $(e.target).attr("class") != "custom-select-option2") {
            $("#custom-select-option-box2").hide();
        }
    });

    // Change filter placeholders
    $('#filtering-form-subs #id_fecha_publicacion').attr('placeholder', 'Año inicio');
    $('#filtering-form-subs #id_fin').attr('placeholder', 'Año fin');
    $('#filtering-form-subs #id_ente option:selected').text('Ente');
    $('#filtering-form-subs #id_area option:selected').text('Area');
});