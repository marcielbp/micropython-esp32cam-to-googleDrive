function doPost(e) {
  dataDrive = e;
  testBlob(dataDrive);
}

function doGet(e) {
  dataDrive = e;
  testBlob(dataDrive);
}

function testBlob(dataIn) {
  var folderID = "putYourFolderIDHere"
  var strAux = "";
  strAux = dataIn.parameter.data;
  var strInput = strAux.replace(/ /g, "+");
  var decoded = Utilities.base64Decode(strInput, Utilities.Charset.UTF_8);
  var date = Utilities.formatDate(new Date(), "GMT-3", "yyyyMMdd_HHmmss");
  var blob = Utilities.newBlob(decoded, "image/jpeg", 'img_'+date+'.jpg');
  var folder = DriveApp.getFolderById(folderID);
  folder.createFile(blob);
}
