function updateUpload(i) {
	document.getElementById("fileUpload-text").value = i.value.replace("C:\\fakepath\\", "");
};
function showUpload(){
	var div = $("#upload-section");
	var modal = $("#modal");
	if(div.is(":hidden")){
		div.fadeIn(400);
		modal.fadeIn(400);
	} else {
		div.fadeOut(400);
		modal.fadeOut(400);
	}
}
function handleSearch(event){
	if(event.keyCode === 13){
		console.log($("#search-box"));
		window.location.href = "http://pictur.ml:2086/search?tag="+$("#search-box")[0].value;
	}
	return false;
}
function showReply(i){
	if($(i).parent().has("> div.comment-reply-wrapper").length == 0){
		$('<div class="comment-reply-wrapper"><form><textarea></textarea><button class="post-button">Post</button></form></div>').insertAfter($(i).parent().children("p.comment-text"));
	}
	else{
		$(i).parent().children("div.comment-reply-wrapper").remove();
	}
}
function showMobileNav(){
	for(var i=3; i<6; i++){
		if(!$('#svg_'+i).attr('class'))
			$('#svg_'+i).attr('class', 'svg_'+i);
		else
			$('#svg_'+i).removeAttr('class');
	}
	$('#navbar').slideToggle(400);
}