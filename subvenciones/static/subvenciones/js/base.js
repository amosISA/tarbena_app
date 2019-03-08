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

            // Breadcrumb for filtering
            var ul_inside_toolbar_datatables = $("<ul class='breadcrumb__filtering'><li class=''><span></span></li></ul>");
            $("div.toolbar").append(ul_inside_toolbar_datatables);

            var qd = {};
            if (location.search) location.search.substr(1).split("&").forEach(function(item) {
                var s = item.split("="),
                    k = s[0],
                    v = s[1] && decodeURIComponent(s[1].replace(/\+/g, ' ')); //  null-coalescing / short-circuit
                //(k in qd) ? qd[k].push(v) : qd[k] = [v]
                (qd[k] = qd[k] || []).push(v) // null-coalescing / short-circuit
            })
              
            for (var key in qd) {
                var obj = qd[key];

                if (key === 'ente') {
                    for (var prop in obj) {
                        if (obj[prop]) {
                            get_filter_ente_area_name('ente', obj[prop]);
                        }
                    }
                } else if (key === 'area') {
                    for (var prop in obj) {
                        if (obj[prop]) {
                            get_filter_ente_area_name('area', obj[prop]);
                        }
                    }
                } else {
                    for (var prop in obj) {
                        if (obj[prop]) {
                            $('.breadcrumb__filtering').append("<li class='filtered_choice'><span class='filtered_choice_remove'>x</span>" + obj[prop] + "</li>");
                        }
                    }
                }
            }
        }
    });
    $('#search-on-navigation').keyup(function(){
          oTable.search($(this).val()).draw();
    });

    function push_into_filter_array(element, array) {
        if (element) { array.push(element); }
    }
    function get_filter_ente_area_name(name, param) { // If area or ente, change the value number for the string inside select
        $('#id_' + name + ' > option').each(function() {
            if($(this).val() === param){
                return $('.breadcrumb__filtering').append("<li class='filtered_choice'><span class='filtered_choice_remove'>x</span>" + $(this).text() + "</li>");
            }
        });
    }

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
    $('#button-actual-subsidie-navigation, #button-actual-subsidie-dropdown').click(function() {
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
    $('#filtering-form-subs #id_fecha_publicacion').attr('placeholder', 'Inicio: 2018-03-26');
    $('#filtering-form-subs #id_fin').attr('placeholder', 'Fin: 2018-03-26');
    $('#filtering-form-subs #id_ente option:first-child').text('Ente');
    $('#filtering-form-subs #id_area option:first-child').text('Area');

    // Get parameters from url with jQuery
    function getUrlParameter(sParam) {
        var sPageURL = decodeURIComponent(window.location.search.substring(1)),
            sURLVariables = sPageURL.split('&'),
            sParameterName,
            i;

        for (i = 0; i < sURLVariables.length; i++) {
            sParameterName = sURLVariables[i].split('='); // ["estado", "Aprobada"]

            if (sParameterName[0] === sParam) {
                return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1].replace(/\+/g, ' '));
            }
        }
    };
});