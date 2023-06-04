$(document).ready(function() {
  $('#uploadForm').submit(function(event) {
    event.preventDefault();
    var textInput = $('#textInput').val();
    var fileInput = document.getElementById('fileInput');
    var file = fileInput.files[0];
    if (!file || !file.type || file.type.indexOf('image/') !== 0) {
      alert('画像ファイルを選択してください.');
      return;
    }

    var formData = new FormData();
    formData.append('image_data', file);
    // formData.append('text_data', textInput);
    onsole.log("go")
    $.ajax({
      url: 'http://127.0.0.1:8000/predict',
      type: 'POST',
      data: formData,
      processData: false,
      contentType: false,
      success: function(response) {
	  // 可能なBase64-encodedの方法
	  //var image = atob(response);
	  //var blob = new Blob([image], {type: 'image/jpeg'});

	  var url = URL.createObjectURL(file);
      var result=response.result;
	  $('#output').html('<p>アップロード完了!</p><p>結果:' +result+'</p><img src="'+url+'">');
      },
      error: function() {
        $('#output').html('<p class="error">何かが間違っています.</p><img src="' + URL.createObjectURL(file) + '">');
      }
    });
    });
});
