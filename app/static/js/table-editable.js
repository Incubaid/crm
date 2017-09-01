var EditableTable = function () {

    return {

        //main function to initiate the module
        init: function () {
            function restoreRow(oTable, nRow) {
                var aData = oTable.fnGetData(nRow);
                var jqTds = $('>td', nRow);

                for (var i = 0, iLen = jqTds.length; i < iLen; i++) {
                    oTable.fnUpdate(aData[i], nRow, i, false);
                }

                oTable.fnDraw();
            }

            function editRow(oTable, nRow) {
                var aData = oTable.fnGetData(nRow);
                var jqTds = $('>td', nRow);
                jqTds[0].innerHTML = '<input type="text" class="form-control small" value="' + aData[0] + '">';
                jqTds[1].innerHTML = '<input type="text" class="form-control small" value="' + aData[1] + '">';
                jqTds[2].innerHTML = '<input type="text" class="form-control small" value="' + aData[2] + '">';
                jqTds[3].innerHTML = '<input type="text" class="form-control small" value="' + aData[3] + '">';
                jqTds[4].innerHTML = '<input type="text" class="form-control small" value="' + aData[4] + '">';
                jqTds[5].innerHTML = '<input type="text" class="form-control small" value="' + aData[5] + '">';
                jqTds[6].innerHTML = '<input type="text" class="form-control small" value="' + aData[6] + '">';
                jqTds[7].innerHTML = '<a class="edit" href="">حفظ</a>';
                jqTds[8].innerHTML = '<a class="cancel" href="">إلغاء</a>';
            }

            function saveRow(oTable, nRow) {
                var jqInputs = $('input', nRow);
                oTable.fnUpdate(jqInputs[0].value, nRow, 0, false);
                oTable.fnUpdate(jqInputs[1].value, nRow, 1, false);
                oTable.fnUpdate(jqInputs[2].value, nRow, 2, false);
                oTable.fnUpdate(jqInputs[3].value, nRow, 3, false);
                oTable.fnUpdate(jqInputs[4].value, nRow, 4, false);
                oTable.fnUpdate(jqInputs[5].value, nRow, 5, false);
                oTable.fnUpdate(jqInputs[6].value, nRow, 6, false);
                oTable.fnUpdate('<a class="edit" href="">تعديل</a>', nRow, 7, false);
                oTable.fnUpdate('<a class="delete" href="">حذف</a>', nRow, 8, false);
                oTable.fnDraw();
            }

            function cancelEditRow(oTable, nRow) {
                var jqInputs = $('input', nRow);
                oTable.fnUpdate(jqInputs[0].value, nRow, 0, false);
                oTable.fnUpdate(jqInputs[1].value, nRow, 1, false);
                oTable.fnUpdate(jqInputs[2].value, nRow, 2, false);
                oTable.fnUpdate(jqInputs[3].value, nRow, 3, false);
                oTable.fnUpdate(jqInputs[4].value, nRow, 4, false);
                oTable.fnUpdate(jqInputs[5].value, nRow, 5, false);
                oTable.fnUpdate(jqInputs[6].value, nRow, 6, false);
                oTable.fnUpdate('<a class="edit" href="">تعديل</a>', nRow, 7, false);
                oTable.fnDraw();
            }

            var oTable = $('#editable-sample').dataTable({
                "aLengthMenu": [
                    [10, 15, 20, -1],
                    [10, 15, 20, "All"] // change per page values here
                ],
                // set the initial value
                "iDisplayLength": 10,
                "sDom": "<'row'<'col-lg-6'l><'col-lg-6'f>r>t<'row'<'col-lg-6'i><'col-lg-6'p>>",
                "sPaginationType": "bootstrap",
                "oLanguage": {
                    "sLengthMenu": "عدد المدخلات في الصفحة _MENU_ ",
                     "oPaginate": {
                        "sFirst": "الصفحة الأولى",
                        "sLast": "الصفحة الأخيرة",
                        "sNext": "التالي",
                        "sPrevious": "السابق"
                                        },
                        "sEmptyTable": "لا توجد بيانات للعرض",
                        "sInfoEmpty": "عرض 0 بيانات من 0 إلى 0",
                        "sInfo": "عرض _START_ إلى _END_ من _TOTAL_ مدخل",
                        "sLoadingRecords": "جاري تحميل البيانات ...",
                        "sProcessing": "جاري تحميل البيانات ...",
                        "sSearch": "البحث:",
                        "sZeroRecords": "لا توجد بيانات متطابقة"
                             },
                "aoColumnDefs": [{
                        'bSortable': false,
                        'aTargets': [0]
                    }
                ]
            });

            jQuery('#editable-sample_wrapper .dataTables_filter input').addClass("form-control medium"); // modify table search input
            jQuery('#editable-sample_wrapper .dataTables_length select').addClass("form-control xsmall"); // modify table per page dropdown

            var nEditing = null;

            $('#editable-sample_new').click(function (e) {
                e.preventDefault();
                var aiNew = oTable.fnAddData(['', '', '', '', '', '', '',
                        '<a class="edit" href="">تعديل</a>', '<a class="cancel" data-mode="new" href="">إلغاء</a>'
                ]);
                var nRow = oTable.fnGetNodes(aiNew[0]);
                editRow(oTable, nRow);
                nEditing = nRow;
            });

            $('#editable-sample a.delete').live('click', function (e) {
                e.preventDefault();

                if (confirm("هل أنت متأكد من حذف هذا الصف ؟") == false) {
                    return;
                }

                var nRow = $(this).parents('tr')[0];
                oTable.fnDeleteRow(nRow);
                alert("تم الحذف .. لا تنسى إضافة جزء الأجاكس الذي يربط بيانات الجدول بقاعدة البيانات");
            });

            $('#editable-sample a.cancel').live('click', function (e) {
                e.preventDefault();
                if ($(this).attr("data-mode") == "new") {
                    var nRow = $(this).parents('tr')[0];
                    oTable.fnDeleteRow(nRow);
                } else {
                    restoreRow(oTable, nEditing);
                    nEditing = null;
                }
            });

            $('#editable-sample a.edit').live('click', function (e) {
                e.preventDefault();

                /* Get the row as a parent of the link that was clicked on */
                var nRow = $(this).parents('tr')[0];

                if (nEditing !== null && nEditing != nRow) {
                    /* Currently editing - but not this row - restore the old before continuing to edit mode */
                    restoreRow(oTable, nEditing);
                    editRow(oTable, nRow);
                    nEditing = nRow;
                } else if (nEditing == nRow && this.innerHTML == "Save") {
                    /* Editing this row and want to save it */
                    saveRow(oTable, nEditing);
                    nEditing = null;
                    alert("تم الحفظ .. لا تنسى إضافة جزء الأجاكس الذي يربط بيانات الجدول بقاعدة البيانات");
                } else {
                    /* No edit in progress - let's start one */
                    editRow(oTable, nRow);
                    nEditing = nRow;
                }
            });
        }

    };

}();