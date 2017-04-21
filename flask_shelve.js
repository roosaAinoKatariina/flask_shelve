function flask_shelve(idx,element) {
    if ($(element).attr("fstype")=="multichoice") {
	var collection=$(element).attr("fscol");
	var fsid=$(element).attr("fsid");
	var choices=$(element).attr("fschoices").split("|");
	for (choice of choices) {
	    var newbutton=jQuery('<input/>', {type: "radio", name: collection+"_"+fsid, "fschoice": choice});
	    newbutton.on('change', function() {
		console.log($(this).attr("name")," ",$(this).attr("fschoice"));
	    });
	    newbutton.appendTo($(element));
	}
    }    
    
  //   $("#yourcontainer").append("<input type='radio' name='myRadio' />");
  // }


    
  //   $.ajax({
  //       url: $APP_ROOT+path,
  //       data: $(frm).serialize(),
  //       type: 'POST',
  //       beforeSend: function() { $(resdiv).html('');$(resdiv).hide(); $('#loading').show(); },
  //       complete: function() { $('#loading').hide(); $(resdiv).show(); },
  //       success: function(response){
  //           dsearch_ajax_response(response,resdiv);
  //       },
  //       error: function(error){
  //           $(resdiv).html('Backend server timeout.');
  //           console.log("error, maybe timeout");
  //           console.log(error);
  //       },
  //       fail: function(error){
  //           $(resdiv).html('Backend server timeout.');
  //           console.log("fail, maybe timeout");
  //           console.log(error);
  //       },
  //       timeout:600000

  //   });
}

