$(document).ready(function() {
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