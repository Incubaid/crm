/*

How to apply:

Edit -> Current project's trigger then (setFilter, on change)
Resource -> Advanced google services -> 

*/

function setFilter() {
    
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var import = ss.getSheetByName('IMPORT')
  var list = ss.getSheetByName('List')
  
  list.clear()
  
  // Copy All data
 var data = import.getRange('A:Z').getValues()
 for (var i=0; i < data.length; i++){
   list.appendRow(data[i])
 }
   
  // Apply filter to list
  
  var request = {
    "setBasicFilter": {
      "filter": {
           "range" : {
             sheetId: list.getSheetId()
           },
        
           "criteria": {
             4 : { 'hiddenValues': ['AMBASSADOR', 'ITFT']},      
             5 : {'hiddenValues': ['NEW', 'CLOSED']}
        }
      }
    }
  };
  
  // Apply filter
  var data = Sheets.Spreadsheets.batchUpdate({'requests': [request]}, ss.getId());
  
}
