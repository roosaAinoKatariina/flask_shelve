
function flask_shelve(idx,element) {
    if ($(element).attr("fstype")=="multichoice") {
	var collection=$(element).attr("fscol");
	var fsid=$(element).attr("fsid");
	var choices=$(element).attr("fschoices").split("|");
	var choicebox=jQuery("<div/>", {"id":collection+"_"+fsid});
	for (choice of choices) {
	    var newlabel=jQuery("<label/>", {"for": collection+"_"+fsid});
	    newlabel.text(choice);
	    newlabel.appendTo(choicebox);
	    var newbutton=jQuery('<input/>', {type: "radio", fsid: fsid, fscol: collection, name: collection+"_"+fsid,"fschoice": choice});
	    newbutton.on('change', function() {
		register_value($(this));
	    });
	    newbutton.appendTo(choicebox);
	}
	choicebox.appendTo($(element));
    }    
}    

function initialize_value(element) {
}

function register_value(element) {

    var collection=element.attr("fscol");
    var id=element.attr("fsid");
    var new_val=element.attr("fschoice");
    var request_url="http://127.0.0.1:5000/set/"+collection+"/"+id;
    $.ajax({url: request_url, data:{"value":JSON.stringify(new_val)}, type: 'GET', dataType: 'json',
	    beforeSend: function() {$("#"+collection+"_"+id).css("border","1px solid orange");},
	    success: function(error) {console.log("OK",collection,id);$("#"+collection+"_"+id).css("border","1px solid green");},
	    fail: function(error) {console.log("FAIL",collection,id);$("#"+collection+"_"+id).css("border","1px solid red");},
	    error: function(request,status,error) {console.log("FAIL",collection,id,error);$("#"+collection+"_"+id).css("border","1px solid red");},
	    timeout:3000});
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


