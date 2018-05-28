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
        dom: 'Bfrtip',
        columns: [
            { "orderable": false },
            { "orderable": false },
            { "orderable": false },
            { "orderable": false }
        ],
        buttons: [
            {
                extend: 'collection',
                text: 'Acciones',
                buttons: [
                    {extend: 'copy', orientation: 'landscape', pageSize: 'LEGAL'},
                    {extend: 'excel', orientation: 'landscape', pageSize: 'LEGAL',
                        customize: function( xlsx ) {
                            var sheet = xlsx.xl.worksheets['sheet1.xml'];
                            $('row c[r^="C"]', sheet).attr( 's', '2' );
                        }
                    },
                    {extend: 'csv', orientation: 'landscape', pageSize: 'LEGAL'},
                    {extend: 'pdf', orientation: 'landscape', pageSize: 'LEGAL'},
                    {extend: 'print', orientation: 'landscape', pageSize: 'LEGAL'}
                ]
            }
        ],
    });
    $('#search-on-navigation').keyup(function(){
          oTable.search($(this).val()).draw();
    });

    // Scroll to subsidie that have the actual day and blink the subsidies that have as end date the actual day
    var CurrentDate = new Date();
    var dataFormated = ('0' + CurrentDate.getDate()).slice(-2)+"/"+('0'+(CurrentDate.getMonth()+1)).slice(-2)+"/"+CurrentDate.getFullYear();

    // Navigation click on button that is left to the search box for scrolling to actual subsidie
    $('#button-actual-subsidie-navigation').click(function() {
        $('.date-end').each(function() {
            if ($.trim($(this).text()) == dataFormated) {
                $('html, body').animate({
                    scrollTop: $(this).parent().offset().top=($(this).parent().offset().top)-($(this).parent().outerHeight())
                }, 250);
                $(this).parent().parent().fadeIn(200).fadeOut(200).fadeIn(200).fadeOut(200).fadeIn(200);
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
});